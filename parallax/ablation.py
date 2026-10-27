"""Preregistered guided/neutral ablation on the three existing real-world cases."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import secrets
import subprocess
import sys

from . import benchmark as b
from .evaluate import save_report
from .model_api import ENDPOINT, MODEL, ModelAPIError, chat_completion, get_api_key


CASES = ("nvidia-ports", "meta-capacity", "coreweave-deposit")
CONDITIONS = ("guided", "neutral")
NEUTRAL_TEMPLATE = (
    "Analyze the supplied financing arrangement from the perspective of {investor}. "
    "Explain its economic significance, cite supporting evidence, and identify material uncertainties."
)


def now():
    return datetime.now(timezone.utc).isoformat()


def hash_value(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def request_for(case, perspective, condition):
    request = b.request_for(case, perspective)
    if condition == "neutral":
        company = b.registry()[case]["company"]
        investor = (f"an equity investor in {company}" if perspective == "equity_holder"
                    else f"a senior unsecured creditor of {company}")
        request["messages"][0]["content"] = NEUTRAL_TEMPLATE.format(investor=investor)
    elif condition != "guided":
        raise ValueError("Unknown condition")
    return request


def matrix(samples=1, seed=20261027):
    if samples < 1:
        raise ValueError("samples must be positive")
    cells = [
        {"cell_id": f"{case}:{p}:{condition}:{sample}", "case_key": case,
         "perspective": p, "condition": condition, "sample": sample,
         "request": request_for(case, p, condition)}
        for sample in range(1, samples + 1) for case in CASES
        for p in b.INVESTORS for condition in CONDITIONS
    ]
    random.Random(seed).shuffle(cells)
    return cells


def preregistration(narrative, samples=1, seed=20261027):
    path = Path(narrative).resolve()
    return {
        "protocol_schema_version": 1, "experiment": "prompt_guidance_ablation_v1",
        "created_at": now(), "narrative_file": str(path.relative_to(b.ROOT)),
        "narrative_sha256": b.digest(path), "samples": samples, "execution_seed": seed,
        "model": MODEL, "endpoint": ENDPOINT, "neutral_template": NEUTRAL_TEMPLATE,
        "source_versions": {case: b.versions(case) for case in CASES},
        "objective_fields": list(b.OBJECTIVE_FIELDS), "judgment_fields": list(b.JUDGMENT_FIELDS),
        "cells": [{**{k: v for k, v in cell.items() if k != "request"},
                   "request_sha256": hash_value(cell["request"]),
                   "developer_instruction": cell["request"]["messages"][0]["content"],
                   "evidence_message_sha256": hash_value(cell["request"]["messages"][1])}
                  for cell in matrix(samples, seed)],
    }


def require_committed(path):
    path = Path(path).resolve()
    relative = path.relative_to(b.ROOT).as_posix()
    result = subprocess.run(["git", "show", f"HEAD:{relative}"], cwd=b.ROOT, capture_output=True, check=True)
    if result.stdout != path.read_bytes():
        raise ValueError("Preregistration must match its committed bytes before live calls")


def validate_protocol(path, samples):
    protocol = b.read_json(path)
    if protocol["protocol_schema_version"] != 1 or samples != protocol["samples"]:
        raise ValueError("Sample count must match the preregistered protocol")
    narrative = b.ROOT / protocol["narrative_file"]
    if b.digest(narrative) != protocol["narrative_sha256"]:
        raise ValueError("Narrative protocol changed")
    expected = preregistration(narrative, samples, protocol["execution_seed"])
    for field in ("model", "endpoint", "neutral_template", "source_versions", "objective_fields", "judgment_fields", "cells"):
        if protocol[field] != expected[field]:
            raise ValueError(f"Protocol drift: {field}")
    require_committed(path)
    require_committed(narrative)
    return protocol


def run(protocol_path, output, samples=1):
    protocol = validate_protocol(protocol_path, samples)
    key = get_api_key()
    cells = matrix(samples, protocol["execution_seed"])
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=b.ROOT, text=True).strip()
    report = {
        "ablation_schema_version": 1, "experiment": protocol["experiment"],
        "started_at": now(), "model": MODEL, "endpoint": ENDPOINT,
        "protocol_file": str(Path(protocol_path).resolve().relative_to(b.ROOT)),
        "protocol_sha256": b.digest(protocol_path), "protocol_snapshot": protocol,
        "code_revision": revision,
        "working_tree_dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=b.ROOT, text=True)),
        "runner_sha256": b.digest(__file__), "api_client_sha256": b.digest(b.ROOT / "parallax/model_api.py"),
        "python_version": sys.version, "samples": samples,
        "evaluations": [{**cell, "status": "pending", "model_generated": None} for cell in cells],
        "notes": "Independent conversations; no retries; no historical responses or references submitted. All prompts and provider JSON preserved. Conditions are unblinded researcher data; do not give this file to a blinded reviewer.",
    }
    b.write_new(output, report)
    for index, item in enumerate(report["evaluations"], 1):
        item.update(status="in_progress", submitted_at=now())
        save_report(Path(output), report)
        print(f"Submitting {index}/{len(cells)}: {item['case_key']} / {item['perspective']}", file=sys.stderr, flush=True)
        try:
            response = chat_completion(item["request"], key)
            item["model_generated"] = response
            item["status"] = "completed" if response["choices"][0]["finish_reason"] == "stop" else "incomplete"
        except ModelAPIError as exc:
            item.update(status="error", error=str(exc), model_generated=exc.response)
        item["finished_at"] = now()
        save_report(Path(output), report)
    report["finished_at"] = now()
    save_report(Path(output), report)
    return report


def response_text(item):
    try:
        text = item["model_generated"]["choices"][0]["message"]["content"]
        return text if isinstance(text, str) else None
    except (KeyError, TypeError, IndexError):
        return None


def blind_package(run_file, directory, mapping_file, seed=None):
    directory, mapping_file = Path(directory), Path(mapping_file)
    if mapping_file.resolve().is_relative_to(directory.resolve()):
        raise ValueError("Condition mapping must be outside the reviewer directory")
    if directory.exists() or mapping_file.exists():
        raise FileExistsError("Review directory and mapping path must both be new")
    report = b.read_json(run_file)
    if report["ablation_schema_version"] != 1:
        raise ValueError("Expected an ablation run")
    if report["protocol_snapshot"]["source_versions"] != {case: b.versions(case) for case in CASES}:
        raise ValueError("Current evidence/references differ from the run; do not silently substitute them")
    seed = secrets.randbits(64) if seed is None else seed
    rng = random.Random(seed)
    arms = ["Arm X", "Arm Y"]
    rng.shuffle(arms)
    labels = dict(zip(CONDITIONS, arms))
    order = list(range(len(report["evaluations"])))
    rng.shuffle(order)
    directory.mkdir(parents=True)
    package = {
        "review_package_schema_version": 1,
        "instructions": "Conditions are anonymized. Review only this directory. Do not consult raw runs, prompts, protocol, mapping, outcome reports or historical model answers before recording assessments. Wording/style can still suggest a condition; blinding is not guaranteed.",
        "cases": {}, "answers": [],
    }
    for case in CASES:
        entry, evidence = b.load_case(case)
        package["cases"][case] = {"company": entry["company"], "information_cutoff": entry["information_cutoff"],
                                  "evidence": evidence, "reference": b.read_json(b.case_path(entry["reference_file"]))}
    mapping = {"mapping_schema_version": 1, "run_file": str(Path(run_file).resolve()),
               "run_sha256": b.digest(run_file), "blind_seed": seed, "condition_arms": labels, "assignments": {}}
    for position, index in enumerate(order, 1):
        item = report["evaluations"][index]
        identifier = f"R{position:03d}"
        package["answers"].append({"review_id": identifier, "arm": labels[item["condition"]],
                                    "case_key": item["case_key"], "perspective": item["perspective"],
                                    "status": item["status"], "answer": response_text(item), "error": item.get("error")})
        mapping["assignments"][identifier] = {k: item[k] for k in ("cell_id", "case_key", "perspective", "condition", "sample")}
    b.write_new(directory / "review.json", package)
    mapping["package_sha256"] = b.digest(directory / "review.json")
    b.write_new(mapping_file, mapping)
    def blank():
        return {"status": "not_reviewed", "response_excerpt": "", "notes": "", "citations": []}
    assessment = {
        "assessment_schema_version": 1, "package_sha256": mapping["package_sha256"],
        "reviewer": "", "review_type": "unassigned", "reviewed_on": "",
        "answers": [{"review_id": item["review_id"], "objective": {f: blank() for f in b.OBJECTIVE_FIELDS},
                     "judgment": {f: blank() for f in b.JUDGMENT_FIELDS}} for item in package["answers"]],
        "pair_consistency": [{"case_key": case, "arm": arm, **blank()} for case in CASES for arm in arms],
    }
    b.write_new(directory / "assessment-template.json", assessment)
    lines = ["# Anonymized reviewer package", "", package["instructions"], "", "Use review.json for the unchanged evidence and reference facts. Fill a COPY of assessment-template.json. No independent reviewer has been recruited or rated these answers. Do not use verbosity to assume quality. Fields can be missing or unscorable without being false.", ""]
    for answer in package["answers"]:
        lines += [f"## {answer['review_id']} · {answer['arm']} · {answer['case_key']} · {answer['perspective']}", "",
                  f"Completion status: {answer['status']}", "", answer["answer"] or "No text response available; do not invent an answer.", ""]
    b.write_new(directory / "review.md", "\n".join(lines).rstrip() + "\n")
    return package


def reveal(directory, assessment_file, mapping_file, output):
    package = b.read_json(Path(directory) / "review.json")
    assessment, mapping = b.read_json(assessment_file), b.read_json(mapping_file)
    package_hash = b.digest(Path(directory) / "review.json")
    if assessment["package_sha256"] != package_hash or mapping["package_sha256"] != package_hash:
        raise ValueError("Review package binding differs")
    if not assessment["reviewer"] or assessment["review_type"] == "unassigned":
        raise ValueError("Record actual reviewer and review type before reveal")
    ids = [item["review_id"] for item in assessment["answers"]]
    if len(ids) != len(set(ids)) or set(ids) != {item["review_id"] for item in package["answers"]} or set(ids) != set(mapping["assignments"]):
        raise ValueError("Assessment must cover every answer ID exactly once")
    expected_pairs = {(case, answer["arm"]) for case in CASES for answer in package["answers"] if answer["case_key"] == case}
    pairs = assessment["pair_consistency"]
    if len(pairs) != len(expected_pairs) or {(item["case_key"], item["arm"]) for item in pairs} != expected_pairs:
        raise ValueError("Record every case/arm consistency assessment")
    records = list(pairs)
    for item in assessment["answers"]:
        for section, fields in (("objective", b.OBJECTIVE_FIELDS), ("judgment", b.JUDGMENT_FIELDS)):
            for field in fields:
                records.append(item[section][field])
    if any(item["status"] not in b.STATUSES or item["status"] == "not_reviewed" or not item["notes"] for item in records):
        raise ValueError("Record a status and rationale (including missing/unscorable) before reveal")
    result = {"revealed_at": now(), "assessment_sha256": b.digest(assessment_file),
              "package_sha256": package_hash, "run_sha256": mapping["run_sha256"],
              "reviewer": assessment["reviewer"], "review_type": assessment["review_type"],
              "answers": [{**item, **mapping["assignments"][item["review_id"]]} for item in assessment["answers"]],
              "pair_consistency": assessment["pair_consistency"], "condition_arms": mapping["condition_arms"],
              "notes": "Revealed only after recorded assessments. This gate does not prove that a reviewer was independently blinded; consult reviewer type and limitations."}
    b.write_new(output, result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    pre = commands.add_parser("preregister")
    pre.add_argument("--narrative", type=Path, required=True)
    pre.add_argument("--output", type=Path, required=True)
    pre.add_argument("--samples", type=int, default=1)
    pre.add_argument("--seed", type=int, default=20261027)
    plan = commands.add_parser("plan")
    plan.add_argument("--samples", type=int, default=1)
    plan.add_argument("--seed", type=int, default=20261027)
    run_parser = commands.add_parser("run")
    run_parser.add_argument("--protocol", type=Path, required=True)
    run_parser.add_argument("--output", type=Path, required=True)
    run_parser.add_argument("--samples", type=int, default=1)
    blind = commands.add_parser("blind")
    blind.add_argument("--run", type=Path, required=True)
    blind.add_argument("--directory", type=Path, required=True)
    blind.add_argument("--mapping", type=Path, required=True)
    blind.add_argument("--seed", type=int)
    unblind = commands.add_parser("reveal")
    unblind.add_argument("--directory", type=Path, required=True)
    unblind.add_argument("--assessment", type=Path, required=True)
    unblind.add_argument("--mapping", type=Path, required=True)
    unblind.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "preregister":
            b.write_new(args.output, preregistration(args.narrative, args.samples, args.seed))
        elif args.command == "plan":
            print(json.dumps(matrix(args.samples, args.seed), indent=2, sort_keys=True))
        elif args.command == "run":
            report = run(args.protocol, args.output, args.samples)
            completed = sum(item["status"] == "completed" for item in report["evaluations"])
            print(f"Saved {args.output}: {completed}/{len(report['evaluations'])} completed")
            if completed != len(report["evaluations"]):
                parser.exit(1, "Failures/incomplete outputs retained; no automatic retries.\n")
        elif args.command == "blind":
            blind_package(args.run, args.directory, args.mapping, args.seed)
        elif args.command == "reveal":
            reveal(args.directory, args.assessment, args.mapping, args.output)
    except (OSError, ValueError, KeyError, TypeError, IndexError, subprocess.CalledProcessError, ModelAPIError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
