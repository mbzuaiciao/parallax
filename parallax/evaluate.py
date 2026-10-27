"""Run exactly the four case combinations and checkpoint inspectable JSON."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile

from .cli import PERSPECTIVES, SCENARIOS, reference_calculations
from .model_api import ENDPOINT, MODEL, ModelAPIError, build_request, chat_completion, get_api_key


def save_report(path, report):
    """Replace a checkpoint atomically so completed responses survive later errors."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(report, handle, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def run_evaluations(case, output):
    api_key = get_api_key()
    path = Path(output)
    report = {
        "evaluation_schema_version": 1,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
        "model": MODEL,
        "case_id": case["case_id"],
        "notes": "Model responses are unverified model-generated claims, preserved without correction. Deterministic references are local calculations never sent to the model.",
        "evaluations": [],
    }
    for perspective in PERSPECTIVES:
        for scenario in SCENARIOS:
            report["evaluations"].append({
                "task_id": f"{case['case_id']}:{perspective}:{scenario}",
                "perspective": perspective,
                "scenario": scenario,
                "request": build_request(case, perspective, scenario),
                "status": "pending",
                "model_generated": None,
                "deterministic_reference": {
                    "sent_to_model": False,
                    "amount_unit": case["amount_unit"],
                    "currency": case["currency"],
                    "rounding": "Six decimal places, half-even; recovery expressed as percent.",
                    "values": reference_calculations(case, scenario),
                },
            })
    # Fail before paid calls if the destination is unavailable or already exists.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    for evaluation in report["evaluations"]:
        print(f"Submitting {evaluation['task_id']}", file=sys.stderr, flush=True)
        evaluation["status"] = "in_progress"
        save_report(path, report)
        try:
            response = chat_completion(evaluation["request"], api_key)
            evaluation["model_generated"] = response
            evaluation["status"] = ("completed" if response["choices"][0]["finish_reason"] == "stop" else "incomplete")
        except ModelAPIError as exc:
            evaluation["status"] = "error"
            evaluation["error"] = str(exc)
            evaluation["model_generated"] = exc.response
        save_report(path, report)
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    save_report(path, report)
    return report
