"""One subsidiary-recourse paired experiment; reuse the existing Meta client."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN, localcontext
import json
from pathlib import Path
import sys

from .cli import PERSPECTIVES, amount
from .evaluate import save_report
from .model_api import ENDPOINT, MODEL, ModelAPIError, chat_completion, get_api_key


DEFAULT_PAIR = Path(__file__).resolve().parent.parent / "cases" / "subsidiary_pair.json"
STRUCTURES = ("A", "B")


def load_pair(path=DEFAULT_PAIR):
    with Path(path).open(encoding="utf-8") as handle:
        pair = json.load(handle)
    try:
        if pair["schema_version"] != 1 or set(pair["structures"]) != set(STRUCTURES):
            raise ValueError("Unsupported paired case schema")
        common = pair["common"]
        for group, fields in (
            ("parent", ("standalone_cash_at_settlement", "bond_principal_due")),
            ("subsidiary", ("external_debt_principal_due", "parent_ownership_percent")),
            ("default_scenario", ("subsidiary_net_liquidation_proceeds",)),
            ("no_default_comparison", ("subsidiary_net_liquidation_proceeds",)),
        ):
            for field in fields:
                amount(common[group][field])
        if common["subsidiary"]["parent_ownership_percent"] != "100":
            raise ValueError("This experiment requires full parent ownership")
        if common["default_scenario"]["subsidiary_default"] is not True:
            raise ValueError("This experiment requires subsidiary default")
        debt = amount(common["subsidiary"]["external_debt_principal_due"])
        if not (amount(common["default_scenario"]["subsidiary_net_liquidation_proceeds"]) < debt
                <= amount(common["no_default_comparison"]["subsidiary_net_liquidation_proceeds"])):
            raise ValueError("Proceeds must establish default and a solvent comparison")
        if pair["structures"]["A"] != {"parent_guarantee": None}:
            raise ValueError("A must have no parent guarantee or other changed facts")
        if set(pair["structures"]["B"]) != {"parent_guarantee"}:
            raise ValueError("Only parent guarantee may change between structures")
        amount(pair["structures"]["B"]["parent_guarantee"]["cap"])
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Malformed paired case: {exc}") from exc
    return pair


def reference_values(pair, structure):
    if structure not in STRUCTURES:
        raise ValueError("Unknown structure")
    with localcontext() as context:
        context.prec = 40
        context.rounding = ROUND_HALF_EVEN
        common = pair["common"]
        parent_cash = amount(common["parent"]["standalone_cash_at_settlement"])
        bond = amount(common["parent"]["bond_principal_due"])
        sub_debt = amount(common["subsidiary"]["external_debt_principal_due"])
        sub_cash = amount(common["default_scenario"]["subsidiary_net_liquidation_proceeds"])
        sub_paid = min(sub_debt, sub_cash)
        sub_residual = max(sub_cash - sub_debt, Decimal(0))
        unpaid = sub_debt - sub_paid
        guarantee = pair["structures"][structure]["parent_guarantee"]
        guarantee_claim = min(amount(guarantee["cap"]), unpaid) if guarantee else Decimal(0)
        parent_pool = parent_cash + sub_residual
        claims = bond + guarantee_claim
        ratio = min(Decimal(1), parent_pool / claims) if claims else Decimal(1)
        parent_equity = max(parent_pool - claims, Decimal(0))
        comparison_sub_equity = max(amount(common["no_default_comparison"]["subsidiary_net_liquidation_proceeds"]) - sub_debt, Decimal(0))
        comparison_equity = max(parent_cash + comparison_sub_equity - bond, Decimal(0))
        values = {
            "group_gross_borrowing_principal": bond + sub_debt,
            "subsidiary_debt_claim": sub_debt,
            "subsidiary_lender_payment_from_subsidiary": sub_paid,
            "subsidiary_unpaid_debt_after_liquidation": unpaid,
            "subsidiary_equity_distribution": sub_residual,
            "parent_guarantee_claim": guarantee_claim,
            "parent_total_contractual_claims": claims,
            "parent_cash_pool": parent_pool,
            "parent_bond_payment": bond * ratio,
            "parent_bond_recovery_percent": ratio * 100,
            "parent_guarantee_payment": guarantee_claim * ratio,
            "subsidiary_lender_total_recovery": sub_paid + guarantee_claim * ratio,
            "parent_equity_distribution": parent_equity,
            "no_default_subsidiary_equity_distribution": comparison_sub_equity,
            "no_default_parent_equity_distribution": comparison_equity,
            "lost_subsidiary_equity_distribution": comparison_sub_equity - sub_residual,
            "parent_equity_decline_vs_no_default": comparison_equity - parent_equity,
        }
        return {key: format(value.quantize(Decimal("0.000001")), "f") for key, value in values.items()}


def build_paired_request(pair, structure, perspective):
    if structure not in STRUCTURES or perspective not in PERSPECTIVES:
        raise ValueError("Unknown structure or perspective")
    evidence = deepcopy(pair["common"])
    evidence["parent_guarantee"] = deepcopy(pair["structures"][structure]["parent_guarantee"])
    return {
        "model": MODEL,
        "max_completion_tokens": 8192,
        "messages": [
            {"role": "developer", "content": (
                "Analyze this synthetic corporate structure from the selected parent-company "
                "investor perspective under the supplied subsidiary-default scenario. "
                "Identify the borrower and any obligors, distinguish entity-level contractual "
                "claims from group borrowing figures, and explain economic exposure. "
                "Show the necessary calculations and trace settlement cash flows at both "
                "entities, including any parent payment claims, creditor recoveries and "
                "shareholder distributions. Compare the supplied no-default counterfactual. "
                "Explain implications for the selected investor and for the other parent "
                "investor class. Preserve all supplied facts and do not introduce extra "
                "support payments or change cash, terms, ownership or priorities. "
                "Cite input field paths. Disclose uncertainties; use only the stipulated "
                "facts. Provide a concise analysis."
            )},
            {"role": "user", "content": json.dumps({
                "experiment_id": pair["experiment_id"],
                "structure": structure,
                "provenance": pair["provenance"],
                "perspective": perspective,
                "investor": ("Holder of parent common equity" if perspective == "equity_holder"
                             else "Holder of the entire parent senior unsecured bond"),
                "evidence": evidence,
            }, sort_keys=True)},
        ],
    }


def run_pair(pair, output):
    key = get_api_key()
    path = Path(output)
    report = {
        "evaluation_schema_version": 1,
        "experiment_id": pair["experiment_id"],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
        "model": MODEL,
        "notes": "Four independent requests. Model-generated claims are preserved without correction. Local deterministic references are never sent to the model. Common evidence is identical across A and B; only parent_guarantee changes.",
        "evaluations": [
            {
                "task_id": f"{pair['experiment_id']}:{structure}:{perspective}",
                "structure": structure,
                "perspective": perspective,
                "request": build_paired_request(pair, structure, perspective),
                "deterministic_reference": {"sent_to_model": False, "values": reference_values(pair, structure)},
                "status": "pending",
                "model_generated": None,
            }
            for structure in STRUCTURES for perspective in PERSPECTIVES
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    for item in report["evaluations"]:
        print(f"Submitting {item['task_id']}", file=sys.stderr, flush=True)
        item["status"] = "in_progress"
        save_report(path, report)
        try:
            item["model_generated"] = chat_completion(item["request"], key)
            item["status"] = ("completed" if item["model_generated"]["choices"][0]["finish_reason"] == "stop"
                              else "incomplete")
        except ModelAPIError as exc:
            item.update(status="error", error=str(exc), model_generated=exc.response)
        save_report(path, report)
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    save_report(path, report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=DEFAULT_PAIR)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--all", action="store_true", help="Preview four answer-free API payloads, without network access")
    mode.add_argument("--evaluate", action="store_true", help="Run the four live requests")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if bool(args.output) != args.evaluate:
        parser.error("--output PATH is required only with --evaluate")
    try:
        pair = load_pair(args.case)
        if args.all:
            print(json.dumps([build_paired_request(pair, s, p) for s in STRUCTURES for p in PERSPECTIVES], indent=2, sort_keys=True))
            return
        report = run_pair(pair, args.output)
    except (OSError, ValueError, ModelAPIError) as exc:
        parser.error(str(exc))
    completed = sum(item["status"] == "completed" for item in report["evaluations"])
    print(f"Saved {args.output}: {completed}/4 completed responses")
    if completed != 4:
        parser.exit(1, "Some evaluations failed or ended incompletely; inspect the saved report.\n")


if __name__ == "__main__":
    main()
