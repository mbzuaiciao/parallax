"""One historical SEC-disclosure evaluation; no dataset labels enter the prompt."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from .evaluate import save_report
from .model_api import ENDPOINT, MODEL, ModelAPIError, chat_completion, get_api_key


SOURCE_PATH = Path(__file__).resolve().parent.parent / "cases" / "real_world" / "nvidia_ports.json"
INVESTORS = {
    "equity_holder": "an equity investor in NVIDIA",
    "senior_unsecured_creditor": "a senior unsecured creditor of NVIDIA",
}


def load_disclosure():
    case = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    if case["schema_version"] != 1 or case["case_id"] != "nvidia_ports_2026_disclosure":
        raise ValueError("Unsupported real-world case")
    if {doc["id"] for doc in case["documents"]} != {"SEC_8K", "SEC_10Q", "SEC_FORM"}:
        raise ValueError("The three primary disclosures are required")
    for doc in case["documents"]:
        if not doc["url"].startswith("https://www.sec.gov/Archives/edgar/"):
            raise ValueError("Case evidence must cite primary SEC disclosures")
        for field in ("accession", "filed_on", "locator", "short_quote", "factual_paraphrase"):
            if not doc[field]:
                raise ValueError(f"Missing primary evidence: {field}")
    return case


def build_disclosure_request(case, perspective=None, *, company="NVIDIA"):
    if perspective is not None and perspective not in INVESTORS:
        raise ValueError("Unknown investor perspective")
    investor_labels = {
        "equity_holder": f"an equity investor in {company}",
        "senior_unsecured_creditor": f"a senior unsecured creditor of {company}",
    }
    investor_instruction = (
        "Separately assess the implications for "
        f"(1) an equity investor in {company} and (2) a senior unsecured creditor of {company}. "
        if perspective is None else
        f"Assess the implications for {investor_labels[perspective]}. "
    )
    # The separate Wagner reference file is intentionally neither imported nor read.
    evidence = {key: deepcopy(case[key]) for key in (
        "case_id", "arrangement", "analysis_as_of", "preparation", "documents",
    )}
    return {
        "model": MODEL,
        "max_completion_tokens": 8192,
        "messages": [
            {"role": "developer", "content": (
                "Analyze only the single financing arrangement in the supplied historical "
                "SEC-disclosure source pack, as of its analysis date. Identify contractual "
                "obligors and beneficiaries, distinguishing direct from contingent obligations. "
                "Explain payment triggers, effectiveness, contractual limits, recoveries, "
                "remedies and termination terms. "
                + investor_instruction +
                "Distinguish disclosed facts from conditional economic interpretations. "
                "Cite document IDs and provision locators. Disclose material missing terms "
                "and uncertainties preventing definitive quantitative risk assessment. "
                "Use only the supplied evidence; do not infer redacted identities, invent "
                "financial inputs, assume a creditor ranking, or turn a disclosed cap into "
                "an expected loss or payable balance. No outside research or dataset "
                "classifications are available. Give a concise, structured analysis."
            )},
            {"role": "user", "content": json.dumps(evidence, sort_keys=True)},
        ],
    }


def evaluate_disclosure(output):
    case = load_disclosure()
    key = get_api_key()
    path = Path(output)
    report = {
        "evaluation_schema_version": 1,
        "case_id": case["case_id"],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
        "model": MODEL,
        "input_sha256": hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        "request": build_disclosure_request(case),
        "status": "in_progress",
        "model_generated": None,
        "notes": "One request assessing both NVIDIA investor perspectives. Model output is preserved without correction. Wagner annotations and the manual review are separate, never submitted. No numerical risk ground truth is asserted.",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    try:
        response = chat_completion(report["request"], key)
        report["model_generated"] = response
        report["status"] = "completed" if response["choices"][0]["finish_reason"] == "stop" else "incomplete"
    except ModelAPIError as exc:
        report.update(status="error", error=str(exc), model_generated=exc.response)
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    save_report(path, report)
    return report


def evaluate_investors(output):
    """Exactly two independent requests on the unchanged existing evidence."""
    case = load_disclosure()
    key = get_api_key()
    path = Path(output)
    report = {
        "evaluation_schema_version": 1,
        "experiment_id": "nvidia_ports_investor_pair_v1",
        "case_id": case["case_id"],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
        "model": MODEL,
        "input_sha256": hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        "notes": "Two independent conversations. Only the investor phrase differs between requests; evidence and other instructions are identical. No combined response, research annotations or reference conclusions are submitted. Provider responses are preserved without correction.",
        "evaluations": [
            {
                "perspective": perspective,
                "request": build_disclosure_request(case, perspective),
                "status": "pending",
                "model_generated": None,
            }
            for perspective in INVESTORS
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    for item in report["evaluations"]:
        item["status"] = "in_progress"
        save_report(path, report)
        try:
            response = chat_completion(item["request"], key)
            item["model_generated"] = response
            item["status"] = "completed" if response["choices"][0]["finish_reason"] == "stop" else "incomplete"
        except ModelAPIError as exc:
            item.update(status="error", error=str(exc), model_generated=exc.response)
        save_report(path, report)
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    save_report(path, report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preview", action="store_true")
    mode.add_argument("--evaluate", action="store_true")
    parser.add_argument("--investor-pair", action="store_true", help="Use two independent investor prompts on the same evidence")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if bool(args.output) != args.evaluate:
        parser.error("--output PATH is required only with --evaluate")
    try:
        if args.preview:
            case = load_disclosure()
            payload = ([build_disclosure_request(case, p) for p in INVESTORS]
                       if args.investor_pair else build_disclosure_request(case))
            print(json.dumps(payload, indent=2, sort_keys=True))
            return
        report = evaluate_investors(args.output) if args.investor_pair else evaluate_disclosure(args.output)
    except (OSError, ValueError, ModelAPIError) as exc:
        parser.error(str(exc))
    completed = (all(item["status"] == "completed" for item in report["evaluations"])
                 if args.investor_pair else report["status"] == "completed")
    status = "completed" if completed else "failed or incomplete"
    print(f"Saved {args.output}: {status}")
    if not completed:
        parser.exit(1, "Evaluation failed or was incomplete; inspect the saved report.\n")


if __name__ == "__main__":
    main()
