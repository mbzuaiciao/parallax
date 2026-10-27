"""Load the bundled case and prepare reproducible, model-neutral JSON tasks."""

import argparse
from copy import deepcopy
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext
import json
from pathlib import Path


DEFAULT_CASE = Path(__file__).resolve().parent.parent / "cases" / "harbor.json"
PERSPECTIVES = ("equity_holder", "senior_unsecured_creditor")
SCENARIOS = ("base", "stress")


def amount(value):
    """Require explicit finite nonnegative decimal strings (no float coercion)."""
    if not isinstance(value, str):
        raise ValueError("Amounts and rates must be decimal strings")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("Invalid decimal amount") from exc
    if not result.is_finite() or result < 0:
        raise ValueError("Amounts and rates must be finite and nonnegative")
    return result


def load_case(path=DEFAULT_CASE):
    """Load and validate the single supported case schema without network access."""
    with Path(path).open(encoding="utf-8") as handle:
        case = json.load(handle)
    try:
        if case["schema_version"] != 1:
            raise ValueError("Unsupported case schema version")
        if set(case["perspectives"]) != set(PERSPECTIVES):
            raise ValueError("Case must define the two supported perspectives")
        if set(case["scenarios"]) != set(SCENARIOS):
            raise ValueError("Case must define base and stress scenarios")
        for key in ("case_id", "company", "provenance", "currency", "amount_unit",
                    "valuation_date", "settlement_date", "assumptions", "reference_facts"):
            if not case[key]:
                raise ValueError(f"Missing case content: {key}")
        for key in ("principal", "annual_coupon_rate"):
            amount(case["reported_debt"][key])
        amount(case["contingent_guarantee"]["cap"])
        for scenario in case["scenarios"].values():
            for key in ("distributable_cash", "covered_debt_due", "lender_recoveries"):
                amount(scenario[key])
            if type(scenario["distributor_default"]) is not bool:
                raise ValueError("distributor_default must be a boolean")
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError(f"Malformed case: {exc}") from exc
    return case


def reference_calculations(case, scenario):
    """One-year simple interest and simultaneous pari passu distribution."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    with localcontext() as context:
        context.prec = 40
        context.rounding = ROUND_HALF_EVEN
        inputs = case["scenarios"][scenario]
        debt = case["reported_debt"]
        principal = amount(debt["principal"])
        coupon = principal * amount(debt["annual_coupon_rate"])
        bond_claim = principal + coupon
        shortfall = max(amount(inputs["covered_debt_due"]) - amount(inputs["lender_recoveries"]), Decimal(0))
        guarantee = min(amount(case["contingent_guarantee"]["cap"]), shortfall) if inputs["distributor_default"] else Decimal(0)
        cash = amount(inputs["distributable_cash"])
        total = bond_claim + guarantee
        recovery = min(cash / total, Decimal(1)) if total else Decimal(1)
        bond_paid = bond_claim * recovery
        guarantee_paid = guarantee * recovery
        equity = max(cash - total, Decimal(0))
        values = {
            "reported_debt_principal": principal,
            "bond_coupon_due": coupon,
            "bond_contractual_claim": bond_claim,
            "guarantee_contractual_claim": guarantee,
            "total_contractual_claims": total,
            "distributable_cash": cash,
            "bond_payment": bond_paid,
            "guarantee_payment": guarantee_paid,
            "bond_shortfall": bond_claim - bond_paid,
            "bond_recovery_percent": recovery * 100,
            "equity_residual": equity,
            "no_guarantee_bond_payment": min(cash, bond_claim),
            "no_guarantee_equity_residual": max(cash - bond_claim, Decimal(0)),
        }
        return {key: format(value.quantize(Decimal("0.000001")), "f") for key, value in values.items()}


def prepare_task(case, perspective, scenario):
    if perspective not in PERSPECTIVES:
        raise ValueError(f"Unknown perspective: {perspective}")
    calculations = reference_calculations(case, scenario)
    evidence = deepcopy(case)
    evidence["scenarios"] = {scenario: evidence["scenarios"][scenario]}
    return {
        "task_schema_version": 1,
        "task_id": f"{case['case_id']}:{perspective}:{scenario}",
        "perspective": perspective,
        "scenario": scenario,
        "instructions": (
            "Evaluate the obligations from the selected investor perspective at settlement. "
            "Separate reported debt principal, contractual claims, and actual payments. "
            "Explain the guarantee trigger, ranking, recovery dilution and equity residual. "
            "Compare with the same cash pool absent the guarantee. Use only the supplied "
            "evidence; distinguish synthetic assumptions from cited reference facts. "
            "Do not infer probabilities, prices, accounting recognition or investment returns. "
            "Cite case field paths and reference fact IDs for material claims."
        ),
        "case_evidence": evidence,
        "deterministic_reference": {
            "purpose": "Visible arithmetic checks for reasoning; not a hidden evaluation benchmark.",
            "rounding": "Amounts in case units and recovery percent rounded to six decimals, half-even. Calculate before rounding.",
            "values": calculations,
        },
        "requested_response": {
            "perspective_summary": "string",
            "obligation_analysis": "array of claims with case field paths or reference fact IDs",
            "scenario_cash_flows": "object with bond payment, guarantee payment, equity residual and bond recovery percent",
            "guarantee_counterfactual": "string explaining the same cash pool without the guarantee",
            "limitations": "array of missing information and simplifying assumptions",
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=DEFAULT_CASE)
    parser.add_argument("--perspective", choices=PERSPECTIVES)
    parser.add_argument("--scenario", choices=SCENARIOS)
    parser.add_argument("--all", action="store_true", help="Emit all four tasks as a JSON array")
    parser.add_argument("--evaluate", action="store_true", help="Submit all four answer-free tasks to Meta Model API")
    parser.add_argument("--output", type=Path, help="New JSON report path, required with --evaluate")
    args = parser.parse_args(argv)
    if args.evaluate:
        if args.all or args.perspective or args.scenario or not args.output:
            parser.error("Use --evaluate --output PATH without task-selection flags")
        from .evaluate import run_evaluations
        from .model_api import ModelAPIError
        try:
            report = run_evaluations(load_case(args.case), args.output)
        except (OSError, ValueError, ModelAPIError) as exc:
            parser.error(str(exc))
        completed = sum(item["status"] == "completed" for item in report["evaluations"])
        print(f"Saved {args.output}: {completed}/4 completed responses")
        if completed != 4:
            parser.exit(1, "Some evaluations failed or ended incompletely; inspect the saved report.\n")
        return
    if args.output:
        parser.error("--output requires --evaluate")
    if args.all and (args.perspective or args.scenario):
        parser.error("Use --all alone or select one perspective and scenario")
    if not args.all and not (args.perspective and args.scenario):
        parser.error("Provide --all or both --perspective and --scenario")
    try:
        case = load_case(args.case)
        output = ([prepare_task(case, p, s) for p in PERSPECTIVES for s in SCENARIOS]
                  if args.all else prepare_task(case, args.perspective, args.scenario))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
