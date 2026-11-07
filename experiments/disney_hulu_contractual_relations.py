"""Two offline Hulu payment relationships; None explicitly means unknown.

Amounts are in USD; ownership is a fraction. Synthetic substitutions must use
consistent, nonnegative Decimal inputs and the same operative ownership basis.
No calculation establishes that payment or final appraisal actually occurred.
"""

import json
from decimal import Decimal
from pathlib import Path


EVIDENCE_PATH = Path(__file__).resolve().parents[1] / "research/disney-hulu-baseten-evidence.json"
# E1–E7 follow the completed audits: paragraph/sentence suffixes are local
# excerpt locations, while these records retain the original SEC locators.
SOURCES = {
    f"E{index}": excerpt
    for index, excerpt in enumerate(json.loads(EVIDENCE_PATH.read_text())["excerpts"], 1)
}

INITIAL_PAYMENT = {
    "source_ids": ("E4.p1–2", "E6.p4"),
    "condition": "November 1, 2023 put exercise disclosed in E3.p1; no appraisal prerequisite",
    "formula": "guaranteed_purchase_price - unpaid_contributions_at_payment",
    "operands": {
        "guaranteed_purchase_price": None,
        "unpaid_contributions_at_payment": None,
    },
    "qualifications": (
        "Only outstanding NBCU capital call contributions payable to Disney remaining unpaid on payment date are offset.",
        "Due on or before December 1, 2023 (E4.p1); within 30 days of exercise (E6.p4).",
        "E4.p2's approximate payment estimate assumes the full currently outstanding contributions remain unpaid.",
        "Rounded reported amounts do not supply exact operands; no exact settlement ownership percentage is inferred.",
    ),
}

APPRAISAL_TOP_UP = {
    "source_ids": ("E2.p1–3", "E3.p1", "E5.s1–2", "E6.p2–5"),
    "condition": "Equity fair value finally determined under agreed appraisal process exceeds guaranteed floor",
    "formula": "ownership_fraction * (equity_fair_value - guaranteed_floor) if above floor, else 0",
    "operands": {
        "ownership_fraction": None,
        "equity_fair_value": None,
        "guaranteed_floor": Decimal("27500000000"),
        "finally_determined": None,
    },
    "qualifications": (
        "Incremental appraisal payment only; initial payment is separate and its capital-call offset is not deducted again.",
        "For November 2023 exercise, equity fair value is assessed as of September 30, 2023.",
        "Payable within 45 days of final determination if above floor (E5.s2).",
        "E6.p4 expects determination sometime in calendar 2024; this is not a guaranteed completion date.",
        "E1.p1/E3.p1 report 33% subject to dilution; the exact operative ownership fraction remains unknown.",
        "E2.p2: if parties disagree, each appoints a bank; if determinations are not within 10%, a third bank determines value and the closest two are averaged.",
        "E2.p3: appraisers consider relevant factors including audited historical results, going concern, future prospects and continued Disney assets/contract rights/IP on terms consistent with past practice.",
        "Zero at/below floor is an implication for this top-up only; acquisition tax sharing (E5.s3/E7.p1) is outside these two relationships.",
    ),
}


def initial_payment(relationship=INITIAL_PAYMENT):
    """Evaluate the disclosed post-exercise initial payment, or return unknown."""
    operands = relationship["operands"]
    gross = operands["guaranteed_purchase_price"]
    offset = operands["unpaid_contributions_at_payment"]
    if gross is None or offset is None:
        return None
    return gross - offset


def appraisal_top_up(relationship=APPRAISAL_TOP_UP):
    """Evaluate only a final appraisal scenario; pending is unknown, not zero."""
    operands = relationship["operands"]
    share = operands["ownership_fraction"]
    value = operands["equity_fair_value"]
    floor = operands["guaranteed_floor"]
    if operands["finally_determined"] is not True or any(
        operand is None for operand in (share, value, floor)
    ):
        return None
    if value <= floor:
        return Decimal(0)
    return share * (value - floor)
