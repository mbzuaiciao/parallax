"""Offline preparation only. No API invocation, credentials, or experiment runner.

From repository root: python protocols/scientific-validation-v1/prepare.py
Prints the reproducible plan; redirect to a NEW file to preserve a review snapshot.
"""

import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from parallax.ablation import NEUTRAL_TEMPLATE, hash_value
from parallax.benchmark import digest, read_json
from parallax.cli import load_case, reference_calculations
from parallax.model_api import ENDPOINT, MODEL
from parallax.paired import load_pair, reference_values
from parallax.real_world import build_disclosure_request

HERE = Path(__file__).resolve().parent
SEED = 20261029
DIMENSIONS = ("factual_correctness", "financial_interpretation", "evidence_grounding",
              "unsupported_inference", "uncertainty_abstention")


def request_for(record, condition):
    if condition not in ("neutral", "guided"):
        raise ValueError("Unknown condition")
    evidence = read_json(ROOT / record["evidence_file"])
    request = build_disclosure_request(evidence, company=record["company"])
    request["temperature"] = 0.7
    if condition == "neutral":
        investors = (f"(1) an equity investor in {record['company']} and "
                     f"(2) a senior unsecured creditor of {record['company']}")
        request["messages"][0]["content"] = NEUTRAL_TEMPLATE.format(investor=investors)
    return request


def plan():
    records = read_json(HERE / "references.json")["cases"]
    cells = []
    sources = {}
    for record in records:
        path = ROOT / record["evidence_file"]
        evidence = read_json(path)
        sources[record["case_key"]] = {
            "evidence_file": record["evidence_file"], "sha256": digest(path),
            "documents": [{k: doc[k] for k in ("id", "accession", "url", "filed_on", "locator")}
                          for doc in evidence["documents"]],
            "ground_truth_status": record["status"],
            "legacy_reference_sha256": (digest(ROOT / record["legacy_reference_file"])
                                        if record.get("legacy_reference_file") else None),
        }
        for condition in ("neutral", "guided"):
            request = request_for(record, condition)
            for repeat in range(1, 4):
                cells.append({
                    "run_id": f"sv1:{record['case_key']}:{condition}:{repeat}",
                    "case_key": record["case_key"], "condition": condition,
                    "repeat": repeat, "request": request,
                    "request_sha256": hash_value(request),
                    "evidence_message_sha256": hash_value(request["messages"][1]),
                    "status": "planned_not_executed",
                    "provider_response_id": None, "returned_model_version": None,
                    "submitted_at_utc": None, "finished_at_utc": None,
                    "finish_reason": None, "raw_provider_response": None,
                })
    random.Random(SEED).shuffle(cells)
    # Existing arithmetic is applicable only to these synthetic assumptions.
    # These are offline scope controls, never additional experimental cells.
    harbor, cedar = load_case(), load_pair()
    baseline = {
        "five_disclosure_cases": "not_applicable: no supplied settlement pools or complete waterfall inputs",
        "existing_text_extractor": "none found in parallax; audit recommendation is not an implemented baseline",
        "harbor": {s: reference_calculations(harbor, s) for s in ("base", "stress")},
        "cedar": {s: reference_values(cedar, s) for s in ("A", "B")},
        "scope": "Exact arithmetic under explicit synthetic assumptions; not legal, accounting or economic adjudication.",
    }
    files = [HERE / "protocol.md", HERE / "references.json", Path(__file__),
             ROOT / "parallax/ablation.py", ROOT / "parallax/real_world.py",
             ROOT / "parallax/benchmark.py", ROOT / "parallax/model_api.py",
             ROOT / "parallax/cli.py", ROOT / "parallax/paired.py",
             ROOT / "cases/harbor.json", ROOT / "cases/subsidiary_pair.json"]
    return {
        "experiment": "scientific-validation-v1", "stage": "independent_review_only",
        "execution_authorized": False, "requested_model_version": MODEL, "endpoint": ENDPOINT,
        "execution_ready": False,
        "provider_readiness": {
            "checked_on": "2026-10-29", "method": "official_documentation_only_no_API_calls",
            "sources": ["https://dev.meta.ai/docs/models",
                        "https://dev.meta.ai/docs/protocols/chat-completions",
                        "https://dev.meta.ai/docs/api-reference/chat-completions"],
            "status": "model_endpoint_and_parameter_names_documented_numeric_limit_unresolved",
            "unresolved": ["model-specific acceptance of 8192 output tokens",
                           "account access and current backend version",
                           "effective model-set reasoning default"],
        },
        "temperature": 0.7, "max_completion_tokens": 8192,
        "other_sampling_parameters": "omitted; documented top_p=1, stream=false, n=1, seed=null; reasoning effort model-set; recheck before future execution",
        "schedule_seed": SEED, "model_seed": None, "planned_responses": 30,
        "files_sha256": {str(p.relative_to(ROOT)): digest(p) for p in files},
        "source_versions": sources, "evaluations": cells, "deterministic_baseline": baseline,
        "rating_template": {
            "review_id": None, "reviewer": None, "reviewed_on": None,
            "reference_version_sha256": None,
            "dimensions": {d: {"score": None, "status": "not_reviewed", "answer_excerpt": "",
                               "source_locator": "", "rationale": ""} for d in DIMENSIONS},
            "material_unsupported_assertion": None, "claim_log": [],
            "adjudicator": None, "adjudication_rationale": None,
        },
    }


if __name__ == "__main__":
    print(json.dumps(plan(), indent=2, sort_keys=True, allow_nan=False))
