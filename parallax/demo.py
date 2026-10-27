"""Small adapter for the existing cases and their saved model responses."""

import json
from pathlib import Path
from decimal import Decimal

from . import benchmark
from .ablation import request_for as ablation_request
from .cli import load_case, reference_calculations
from .model_api import build_request, chat_completion, get_api_key
from .paired import build_paired_request, load_pair, reference_values


ROOT = Path(__file__).resolve().parent.parent
REAL_CASES = {"NVIDIA PORTS": "nvidia-ports", "Meta capacity purchases": "meta-capacity",
              "CoreWeave deposit financing": "coreweave-deposit"}
INVESTOR_LABELS = {"equity_holder": "Common equity holder", "senior_unsecured_creditor": "Senior unsecured creditor"}


def load_selection(company, perspective, variant=None, condition=None):
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
    elif company in REAL_CASES:
        key = REAL_CASES[company]
        _, case = benchmark.load_case(key)
        request = benchmark.request_for(key, perspective) if condition is None else ablation_request(key, perspective, condition)
        values = None
        task_id = f"{case['case_id']}:{perspective}" + (f":{condition}" if condition else "")
        saved_path = ROOT / "results" / ("guidance-ablation-v1-live.json" if condition else
                     "nvidia-ports-investor-pair-live.json" if key == "nvidia-ports" else f"benchmark-{key}-live.json")
    else:
        raise ValueError("Unknown company")
    synthetic = company not in REAL_CASES
    report = json.loads(saved_path.read_text(encoding="utf-8"))
    historical = next(item for item in report["evaluations"]
                      if (item["task_id"] == task_id if synthetic else
                          item["perspective"] == perspective and (condition is None or
                          (item["case_key"] == key and item["condition"] == condition))))
    if historical["request"] != request:
        raise ValueError("Saved response inputs differ from current case inputs")
    evidence = json.loads(request["messages"][1]["content"])
    return {
        "task_id": task_id,
        "synthetic": synthetic,
        "request": request,
        "evidence": evidence["evidence"] if synthetic else evidence,
        "references": values,
        "summary": [values[key] for key in summary_keys] if synthetic else None,
        "historical": historical["model_generated"],
        "historical_run_at": report["started_at"],
        "historical_source": saved_path.name,
        "status": historical["status"],
    }


def capital_comparison(company, scenario="stress"):
    """Display adapter only: all settlement values come from existing calculators.

    Harbor's absent-guarantee counterfactual holds cash/default fixed. Cedar's
    structures hold all inputs fixed except the parent's separate guarantee.
    """
    if company == "Cedar":
        case = load_pair()
        a, b = (reference_values(case, s) for s in ("A", "B"))
        rows = []
        for label, values in (("No parent guarantee", a), ("Parent guarantee", b)):
            rows.append({"Structure": label, "Cash pool": values["parent_cash_pool"],
                         "Reported principal": case["common"]["parent"]["bond_principal_due"],
                         "Direct bond claim": case["common"]["parent"]["bond_principal_due"],
                         "Guarantee cap": "0" if label == "No parent guarantee" else case["structures"]["B"]["parent_guarantee"]["cap"],
                         "Triggered claim": values["parent_guarantee_claim"],
                         "Total claims": values["parent_total_contractual_claims"],
                         "Bond payment": values["parent_bond_payment"],
                         "Guarantee payment": values["parent_guarantee_payment"],
                         "Bond recovery %": values["parent_bond_recovery_percent"],
                         "Bond shortfall": str(Decimal(case["common"]["parent"]["bond_principal_due"])-Decimal(values["parent_bond_payment"])),
                         "Equity distribution": values["parent_equity_distribution"]})
        return rows
    if company != "Harbor":
        raise ValueError("Only synthetic cases have deterministic settlement comparisons")
    case = load_case()
    v = reference_calculations(case, scenario)
    rows = []
    for present in (False, True):
        paid = v["bond_payment"] if present else v["no_guarantee_bond_payment"]
        rows.append({"Structure": "Guarantee contract" if present else "Absent guarantee",
                     "Cash pool": v["distributable_cash"], "Reported principal": v["reported_debt_principal"],
                     "Direct bond claim": v["bond_contractual_claim"],
                     "Guarantee cap": case["contingent_guarantee"]["cap"] if present else "0",
                     "Triggered claim": v["guarantee_contractual_claim"] if present else "0",
                     "Total claims": v["total_contractual_claims"] if present else v["bond_contractual_claim"],
                     "Bond payment": paid, "Guarantee payment": v["guarantee_payment"] if present else "0",
                     "Bond recovery %": v["bond_recovery_percent"] if present else str(Decimal(paid)/Decimal(v["bond_contractual_claim"])*100),
                     "Bond shortfall": str(Decimal(v["bond_contractual_claim"])-Decimal(paid)),
                     "Equity distribution": v["equity_residual"] if present else v["no_guarantee_equity_residual"]})
    return rows


def recorded_assessment(company, perspective, condition):
    """Read the recorded review rather than recomputing semantic verdicts."""
    report = benchmark.read_json(ROOT / "results/guidance-ablation-v1-revealed.json")
    return next(item for item in report["answers"] if item["case_key"] == REAL_CASES[company]
                and item["perspective"] == perspective and item["condition"] == condition)


def fresh_analysis(request):
    """Exactly one selected completion; no batch runner, writes, or retries."""
    return chat_completion(request, get_api_key())
