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


def build_disclosure_request(case):
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
                "remedies and termination terms. Separately assess the implications for "
                "(1) an equity investor in NVIDIA and (2) a senior unsecured creditor of NVIDIA. "
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preview", action="store_true")
    mode.add_argument("--evaluate", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if bool(args.output) != args.evaluate:
        parser.error("--output PATH is required only with --evaluate")
    try:
        if args.preview:
            print(json.dumps(build_disclosure_request(load_disclosure()), indent=2, sort_keys=True))
            return
        report = evaluate_disclosure(args.output)
    except (OSError, ValueError, ModelAPIError) as exc:
        parser.error(str(exc))
    print(f"Saved {args.output}: {report['status']}")
    if report["status"] != "completed":
        parser.exit(1, "Evaluation failed or was incomplete; inspect the saved report.\n")


if __name__ == "__main__":
    main()
