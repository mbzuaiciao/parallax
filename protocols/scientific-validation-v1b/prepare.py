"""Offline v1B plan; exactly two prompt transformations of frozen v1 requests."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from parallax.ablation import hash_value
from parallax.benchmark import digest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("v1_preparation", ROOT / "protocols/scientific-validation-v1/prepare.py")
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)
NEGATIVE = ("Use only the supplied evidence; do not infer redacted identities, invent "
            "financial inputs, assume a creditor ranking, or turn a disclosed cap into "
            "an expected loss or payable balance.")
UNAVAILABLE = "No outside research or dataset classifications are available."


def request_for(record, condition):
    if condition == "A":
        request = v1.request_for(record, "guided")
        text = request["messages"][0]["content"]
        assert text.count(NEGATIVE) == text.count(UNAVAILABLE) == 1
        text = text.replace(NEGATIVE + " ", "").replace(UNAVAILABLE + " ", "")
        request["messages"][0]["content"] = text.replace("Analyze only the single", "Analyze the single", 1)
    elif condition == "B":
        request = v1.request_for(record, "neutral")
        request["messages"][0]["content"] += " " + NEGATIVE
    else:
        raise ValueError("Exactly conditions A and B are supported")
    return request


def plan():
    base = v1.plan()
    refs = json.loads((ROOT / "protocols/scientific-validation-v1/references.json").read_text())
    cells = []
    for record in refs["cases"]:
        for condition in ("A", "B"):
            request = request_for(record, condition)
            wire = json.dumps(request, allow_nan=False)
            cells.append({"run_id": f"sv1b:{record['case_key']}:{condition}:1",
                          "case_key": record["case_key"], "condition": condition, "repeat": 1,
                          "request": request, "request_sha256": hash_value(request),
                          "wire_request_utf8": wire,
                          "wire_request_sha256": hashlib.sha256(wire.encode()).hexdigest(),
                          "evidence_message_sha256": hash_value(request["messages"][1]),
                          "status": "planned_not_executed", "raw_provider_response": None})
    random.Random(20261029).shuffle(cells)
    hashes = deepcopy(base["files_sha256"])
    for path in [HERE / "protocol.md", Path(__file__),
                 ROOT / "research/scientific-validation-v1-pilot-results.md",
                 ROOT / "research/scientific-validation-v1-independent-results-audit.md"]:
        hashes[str(path.relative_to(ROOT))] = digest(path)
    # Preserve every historical v1 file, including untracked raw outputs/ratings.
    history = ROOT / "research/scientific-validation-v1-pilot-20261029"
    historical = {str(p.relative_to(ROOT)): digest(p) for p in history.iterdir() if p.is_file()}
    return {"experiment": "scientific-validation-v1B", "stage": "frozen_before_inference",
            "scope": "user-authorized exploratory, provisional AI-assisted references",
            "requested_model": base["requested_model_version"], "endpoint": base["endpoint"],
            "temperature": 0.7, "max_completion_tokens": 8192,
            "schedule_seed": 20261029, "planned_slots": 10, "samples_per_cell": 1,
            "condition_labels": {"A": "positive analytical structure only", "B": "neutral plus negative constraints only"},
            "files_sha256": hashes, "historical_v1_files_sha256": historical,
            "source_versions": base["source_versions"], "reference_snapshot": refs,
            "evaluations": cells}


if __name__ == "__main__":
    print(json.dumps(plan(), indent=2, sort_keys=True, allow_nan=False))
