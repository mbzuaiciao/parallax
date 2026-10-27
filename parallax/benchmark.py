"""Small, versioned disclosure registry and human-assessment workflow."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from .evaluate import save_report
from .model_api import ENDPOINT, MODEL, ModelAPIError, chat_completion, get_api_key
from .real_world import INVESTORS, build_disclosure_request


ROOT = Path(__file__).resolve().parent.parent
CASE_ROOT = ROOT / "cases" / "real_world"
REGISTRY = CASE_ROOT / "registry.json"
OBJECTIVE_FIELDS = ("obligors_beneficiaries", "obligation_classification", "limits_triggers", "disclosed_amounts", "citations")
JUDGMENT_FIELDS = ("investor_implications", "missing_information", "unsupported_assumptions")
STATUSES = ("not_reviewed", "supported", "concern", "missing", "unscorable")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def case_path(relative):
    path = (CASE_ROOT / relative).resolve()
    if not path.is_relative_to(CASE_ROOT.resolve()):
        raise ValueError("Case files must remain inside cases/real_world")
    return path


def registry():
    data = read_json(REGISTRY)
    if data["schema_version"] != 1:
        raise ValueError("Unsupported registry version")
    return data["cases"]


def load_case(case_key):
    entries = registry()
    if case_key not in entries:
        raise ValueError(f"Unknown case: {case_key}")
    entry = entries[case_key]
    case = read_json(case_path(entry["evidence_file"]))
    if case["schema_version"] != 1 or case["analysis_as_of"] != entry["information_cutoff"] or case["arrangement"] != entry["arrangement"]:
        raise ValueError("Registry and evidence metadata disagree")
    if entry["perspectives"] != list(INVESTORS):
        raise ValueError("Expected the two supported investor perspectives")
    ids = [doc["id"] for doc in case["documents"]]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Source IDs must be nonempty and unique")
    for doc in case["documents"]:
        if not doc["url"].startswith("https://www.sec.gov/Archives/edgar/") or doc["filed_on"] > case["analysis_as_of"]:
            raise ValueError("Source must be a primary SEC document available by cutoff")
        for field in ("accession", "locator", "factual_paraphrase"):
            if not doc[field]:
                raise ValueError(f"Missing source field: {field}")
    return entry, case


def request_for(case_key, perspective):
    entry, case = load_case(case_key)
    return build_disclosure_request(case, perspective, company=entry["company"])


def versions(case_key):
    entry, case = load_case(case_key)
    return {
        "registry_sha256": digest(REGISTRY),
        "evidence_sha256": digest(case_path(entry["evidence_file"])),
        "reference_sha256": digest(case_path(entry["reference_file"])),
        "annotations_sha256": digest(case_path(entry["annotations_file"])),
        "dataset": entry["dataset"],
        "primary_sources": [{k: doc[k] for k in ("id", "accession", "url", "filed_on")} for doc in case["documents"]],
    }


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(value if isinstance(value, str) else json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def run_case(case_key, output):
    entry, case = load_case(case_key)
    key = get_api_key()
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True).stdout)
    report = {
        "run_schema_version": 1, "case_key": case_key, "case_id": case["case_id"],
        "company": entry["company"], "information_cutoff": case["analysis_as_of"],
        "started_at": datetime.now(timezone.utc).isoformat(), "endpoint": ENDPOINT,
        "model": MODEL, "source_versions": versions(case_key),
        "code_revision": revision, "working_tree_dirty": dirty, "python_version": sys.version,
        "runner_sha256": digest(__file__),
        "request_builder_sha256": digest(ROOT / "parallax/real_world.py"),
        "api_client_sha256": digest(ROOT / "parallax/model_api.py"),
        "notes": "Independent calls, no retries. Evidence is identical; only investor instruction changes. Local reference/annotation files are hashed for traceability but never supplied to the model. Unchanged provider JSON is saved; no automated financial accuracy score.",
        "evaluations": [{"perspective": p, "request": request_for(case_key, p), "status": "pending", "model_generated": None} for p in entry["perspectives"]],
    }
    write_new(output, report)
    for item in report["evaluations"]:
        item["status"] = "in_progress"
        item["submitted_at"] = datetime.now(timezone.utc).isoformat()
        save_report(Path(output), report)
        print(f"Submitting {case_key} / {item['perspective']}", file=sys.stderr, flush=True)
        try:
            response = chat_completion(item["request"], key)
            item["model_generated"] = response
            item["status"] = "completed" if response["choices"][0]["finish_reason"] == "stop" else "incomplete"
        except ModelAPIError as exc:
            item.update(status="error", error=str(exc), model_generated=exc.response)
        item["finished_at"] = datetime.now(timezone.utc).isoformat()
        save_report(Path(output), report)
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    save_report(Path(output), report)
    return report


def protocol_checks(run):
    """Check bytes/structure only. These checks do not assess financial correctness."""
    case_key = run["case_key"]
    entry, _ = load_case(case_key)
    items = run["evaluations"]
    expected = entry["perspectives"]
    matching = [item["perspective"] for item in items] == expected
    normalized = []
    for item in items:
        request = json.loads(json.dumps(item["request"]))
        label = (f"an equity investor in {entry['company']}" if item["perspective"] == "equity_holder"
                 else f"a senior unsecured creditor of {entry['company']}")
        request["messages"][0]["content"] = request["messages"][0]["content"].replace(label, "<investor>")
        normalized.append(request)
    def text_present(item):
        try:
            text = item["model_generated"]["choices"][0]["message"]["content"]
            return isinstance(text, str) and bool(text.strip())
        except (KeyError, IndexError, TypeError):
            return False
    return {
        "two_expected_perspectives": matching,
        "requests_match_case_and_builder": matching and all(item["request"] == request_for(case_key, item["perspective"]) for item in items),
        "only_investor_phrase_differs": matching and normalized[0] == normalized[1],
        "source_versions_match_current_files": run["source_versions"] == versions(case_key),
        "statuses": {item["perspective"]: item["status"] for item in items},
        "response_text_present": {item["perspective"]: text_present(item) for item in items},
    }


def assessment_template(case_key, run_file):
    run = read_json(run_file)
    if run["case_key"] != case_key:
        raise ValueError("Assessment case differs from run")
    def blank():
        return {"status": "not_reviewed", "response_excerpt": "", "notes": "", "citations": []}
    return {
        "assessment_schema_version": 1, "case_key": case_key,
        "run_file": str(Path(run_file).resolve().relative_to(ROOT)) if Path(run_file).resolve().is_relative_to(ROOT) else str(Path(run_file).resolve()),
        "run_sha256": digest(run_file), "reference_sha256": versions(case_key)["reference_sha256"],
        "reviewer": "", "review_type": "unassigned", "reviewed_on": "", "summary": "", "unscorable_fields": {},
        "evaluations": [{"perspective": p, "objective": {key: blank() for key in OBJECTIVE_FIELDS},
                         "judgment": {key: blank() for key in JUDGMENT_FIELDS}} for p in INVESTORS],
        "pair_consistency": blank(),
    }


def comparison(assessment_files):
    lines = ["# Recorded reviewer assessments", "", "Recorded verdicts are not automated accuracy scores. Consult reviewer/type metadata: assistant drafts are not independent human ratings. Identifier recognition checks catalog membership only; they do not verify the cited passage or whether it supports a claim.", ""]
    for assessment_file in assessment_files:
        assessment = read_json(assessment_file)
        if assessment["assessment_schema_version"] != 1:
            raise ValueError("Unsupported assessment schema")
        key = assessment["case_key"]
        entry, _ = load_case(key)
        run_path = ROOT / assessment["run_file"]
        run = read_json(run_path)
        if run["case_key"] != key or [item["perspective"] for item in assessment["evaluations"]] != entry["perspectives"]:
            raise ValueError("Assessment case or perspectives disagree with run/registry")
        reference = read_json(case_path(entry["reference_file"]))
        known = reference["locations"]
        lines += [f"## {key}", "", f"Reviewer: {assessment['reviewer'] or 'NOT RECORDED'}; type: {assessment.get('review_type', 'NOT RECORDED')}; date: {assessment['reviewed_on'] or 'NOT RECORDED'}.", "", assessment["summary"] or "Summary: NOT RECORDED.", "", "### Deterministic provenance/protocol checks", "", f"- Assessment binds recorded run bytes: {digest(run_path) == assessment['run_sha256']}", f"- Assessment binds current reference bytes: {digest(case_path(entry['reference_file'])) == assessment['reference_sha256']}"]
        for name, result in protocol_checks(run).items():
            lines.append(f"- {name}: {json.dumps(result, sort_keys=True)}")
        lines += ["", "### Explicitly unscorable fields", ""]
        for field, reason in assessment.get("unscorable_fields", {}).items():
            lines.append(f"- {field}: **unscorable** — {reason}")
        if not assessment.get("unscorable_fields"):
            lines.append("No unscorable fields recorded; this is not a claim that every financial quantity is estimable.")
        lines += ["", "### Recorded review (semantic judgments require human validation)", ""]
        for item in assessment["evaluations"]:
            lines += [f"#### {item['perspective']}", ""]
            for section, fields in (("objective", OBJECTIVE_FIELDS), ("judgment", JUDGMENT_FIELDS)):
                for field in fields:
                    record = item[section].get(field, {"status": "missing", "notes": "Assessment field absent", "citations": []})
                    if record["status"] not in STATUSES:
                        raise ValueError(f"Unknown human review status: {record['status']}")
                    lines.append(f"- {section}/{field}: **{record['status']}** — {record.get('notes') or 'No rationale recorded.'}")
                    for citation in record.get("citations", []):
                        source = citation["document_id"]
                        location = citation["location_id"]
                        recognized = location in known and known[location]["document_id"] == source
                        lines.append(f"  - Reviewer-entered citation {source}/{location}: recognized identifier = {recognized}; semantic support requires human review.")
        pair = assessment["pair_consistency"]
        if pair["status"] not in STATUSES:
            raise ValueError("Unknown pair consistency status")
        lines += ["", f"Pair consistency (recorded judgment): **{pair['status']}** — {pair['notes'] or 'No rationale recorded.'}", ""]
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    preview = commands.add_parser("preview")
    preview.add_argument("case")
    preview.add_argument("--perspective", choices=(*INVESTORS, "both"), default="both")
    run = commands.add_parser("run")
    run.add_argument("case")
    run.add_argument("--output", type=Path, required=True)
    template = commands.add_parser("assess-template")
    template.add_argument("case")
    template.add_argument("--run", type=Path, required=True)
    template.add_argument("--output", type=Path, required=True)
    summary = commands.add_parser("summary")
    summary.add_argument("assessments", nargs="+", type=Path)
    summary.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            for key, entry in registry().items():
                print(f"{key}\t{entry['company']}\t{entry['information_cutoff']}\t{entry['arrangement']}")
        elif args.command == "preview":
            payload = ([request_for(args.case, p) for p in INVESTORS] if args.perspective == "both" else request_for(args.case, args.perspective))
            print(json.dumps(payload, indent=2, sort_keys=True))
        elif args.command == "run":
            report = run_case(args.case, args.output)
            completed = sum(item["status"] == "completed" for item in report["evaluations"])
            print(f"Saved {args.output}: {completed}/2 completed")
            if completed != 2:
                parser.exit(1, "Failures/incomplete outputs preserved; inspect report.\n")
        elif args.command == "assess-template":
            write_new(args.output, assessment_template(args.case, args.run))
        elif args.command == "summary":
            text = comparison(args.assessments)
            write_new(args.output, text) if args.output else print(text, end="")
    except (OSError, ValueError, KeyError, TypeError, IndexError, ModelAPIError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
