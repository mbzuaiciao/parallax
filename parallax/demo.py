"""Small adapter for the two existing cases and their saved model responses."""

import json
from pathlib import Path

from .cli import load_case, reference_calculations
from .model_api import build_request, chat_completion, get_api_key
from .paired import build_paired_request, load_pair, reference_values


ROOT = Path(__file__).resolve().parent.parent


def load_selection(company, perspective, variant):
    """Use existing loaders/builders; references never become part of the request."""
    if company == "Harbor":
        case = load_case()
        request = build_request(case, perspective, variant)
        values = reference_calculations(case, variant)
        task_id = f"{case['case_id']}:{perspective}:{variant}"
        saved_path = ROOT / "results" / "first-live.json"
        summary_keys = ("distributable_cash", "total_contractual_claims", "bond_recovery_percent", "equity_residual")
    elif company == "Cedar":
        case = load_pair()
        request = build_paired_request(case, variant, perspective)
        values = reference_values(case, variant)
        task_id = f"{case['experiment_id']}:{variant}:{perspective}"
        saved_path = ROOT / "results" / "subsidiary-pair-live.json"
        summary_keys = ("parent_cash_pool", "parent_total_contractual_claims", "parent_bond_recovery_percent", "parent_equity_distribution")
    else:
        raise ValueError("Unknown company")
    report = json.loads(saved_path.read_text(encoding="utf-8"))
    historical = next(item for item in report["evaluations"] if item["task_id"] == task_id)
    if historical["request"] != request:
        raise ValueError("Saved response inputs differ from current case inputs")
    return {
        "task_id": task_id,
        "request": request,
        "evidence": json.loads(request["messages"][1]["content"])["evidence"],
        "references": values,
        "summary": [values[key] for key in summary_keys],
        "historical": historical["model_generated"],
        "historical_run_at": report["started_at"],
        "historical_source": saved_path.name,
    }


def fresh_analysis(request):
    """Exactly one selected completion; no batch runner, writes, or retries."""
    return chat_completion(request, get_api_key())
