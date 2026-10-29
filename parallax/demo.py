"""Small adapter for the existing cases and their saved model responses."""

from decimal import Decimal
import json
from pathlib import Path

from . import benchmark
from .ablation import request_for as ablation_request
from .cli import load_case, reference_calculations
from .model_api import build_request, chat_completion, get_api_key
from .paired import build_paired_request, load_pair, reference_values


ROOT = Path(__file__).resolve().parent.parent
REAL_CASES = {
    "NVIDIA PORTS": "nvidia-ports",
    "Meta capacity purchases": "meta-capacity",
    "CoreWeave deposit financing": "coreweave-deposit",
}
INVESTOR_LABELS = {
    "equity_holder": "Common equity holder",
    "senior_unsecured_creditor": "Senior unsecured creditor",
}

ALL_PERSPECTIVES = {
    "equity_holder": {
        "label": "Common equity holder",
        "status": "supported",
        "focus": "Residual cash flows, equity dilution, commercial capacity value, and downside exposure.",
    },
    "senior_unsecured_creditor": {
        "label": "Senior unsecured creditor",
        "status": "supported",
        "focus": "Contractual claim coverage, pari passu dilution by competing guarantees, and liquidity demands.",
    },
    "senior_secured_creditor": {
        "label": "Senior secured creditor [Data Pending]",
        "status": "planned",
        "focus": "Lien perfection, collateral coverage, and priority waterfalls. Independent experimental data pending.",
    },
    "subordinated_creditor": {
        "label": "Subordinated creditor [Data Pending]",
        "status": "planned",
        "focus": "Contractual subordination, payment stop provisions, and turnover rules. Independent experimental data pending.",
    },
    "cds_participant": {
        "label": "CDS participant [Data Pending]",
        "status": "planned",
        "focus": "Credit event determinations, deliverable obligations, and basis risk. Independent experimental data pending.",
    },
}

COMPANY_ALIASES = {
    "nvidia-ports": "NVIDIA PORTS",
    "nvidia": "NVIDIA PORTS",
    "nvidia corporation": "NVIDIA PORTS",
    "nvda": "NVIDIA PORTS",
    "nvidia ports": "NVIDIA PORTS",
    "meta-capacity": "Meta capacity purchases",
    "meta": "Meta capacity purchases",
    "meta platforms": "Meta capacity purchases",
    "meta platforms, inc.": "Meta capacity purchases",
    "meta platforms inc": "Meta capacity purchases",
    "meta capacity": "Meta capacity purchases",
    "meta capacity purchases": "Meta capacity purchases",
    "coreweave-deposit": "CoreWeave deposit financing",
    "coreweave": "CoreWeave deposit financing",
    "coreweave, inc.": "CoreWeave deposit financing",
    "coreweave inc": "CoreWeave deposit financing",
    "crwv": "CoreWeave deposit financing",
    "coreweave deposit": "CoreWeave deposit financing",
    "coreweave deposit financing": "CoreWeave deposit financing",
    "cedar": "Cedar",
    "cedar holdings": "Cedar",
    "harbor": "Harbor",
    "harbor components": "Harbor",
}

UNSCORABLE_EXPLANATIONS = {
    "Debt / EBITDA Leverage": "Issuer-wide balance sheet and EBITDA figures are not part of the isolated contractual disclosure pack.",
    "Market Probability of Default": "Market CDS spreads, market pricing, and credit rating agency models are not modeled in Parallax.",
    "Expected Loss": "Loss distributions require default probability and recovery distribution inputs not present in disclosure notes.",
    "Creditor Recovery Rate": "Total enterprise liquidation assets and complete creditor claim registry are not disclosed in isolated SEC filing notes.",
}

ISSUER_REGISTRY = {
    "nvidia-ports": {
        "id": "nvidia-ports",
        "ticker": "NVDA",
        "name": "NVIDIA Corporation",
        "display_name": "NVIDIA Corporation (NVDA)",
        "case_key": "nvidia-ports",
        "demo_company": "NVIDIA PORTS",
        "is_synthetic": False,
        "as_of": "2026-08-26",
        "provenance": "SEC Form 8-K (0001045810-26-000069) / 10-Q (0001045810-26-000075)",
        "arrangement": "NVIDIA PORTS Technology Campus residual value guaranties",
        "obligation_type": "Contingent guarantee (residual-value guaranties)",
        "reported_principal": "Not borrowing principal; PORTS guarantee liability carrying amount not separately established",
        "disclosed_amount": "$105bn initial shared aggregate cap",
        "commitment_nature": "Contingent guarantee with OpenAI reimbursement undertaking",
        "triggers": "OpenAI affiliate payment default + landlord termination/remedy election",
        "ranking": "Not disclosed in filing; relative creditor ranking unestablished",
        "summary": "Residual-value support for an OpenAI affiliate's leases, with reimbursement rights.",
        "caveat": "The cap is neither outstanding debt nor an expected loss. Payment depends on contractual conditions; some cap qualifications and costs are redacted.",
        "obligor": "NVIDIA Corporation",
        "beneficiary": "SB Energy-associated lessors & OpenAI affiliate tenant",
        "reimbursement": "OpenAI reimbursement undertaking",
        "unscorable_metrics": UNSCORABLE_EXPLANATIONS,
    },
    "meta-capacity": {
        "id": "meta-capacity",
        "ticker": "META",
        "name": "Meta Platforms, Inc.",
        "display_name": "Meta Platforms, Inc. (META)",
        "case_key": "meta-capacity",
        "demo_company": "Meta capacity purchases",
        "is_synthetic": False,
        "as_of": "2026-07-30",
        "provenance": "SEC Form 10-Q (Note 9, accession 0001628280-26-050705)",
        "arrangement": "Meta contingent purchase of cloud capacity",
        "obligation_type": "Contingent commercial commitment",
        "reported_principal": "None ($0 debt recognized from this contract)",
        "disclosed_amount": "Up to $14.72bn over five years",
        "commitment_nature": "Contingent commercial purchase of capacity, reduced by third-party sales",
        "triggers": "Capacity delivery; obligation reduced if provider sells capacity to third parties",
        "ranking": "Not disclosed in filing; relative creditor ranking unestablished",
        "summary": "A cloud-capacity purchase commitment that may shrink if the provider sells capacity to others.",
        "caveat": "The provider is unnamed. Trigger details, payment timing and claim ranking are not established by the selected disclosure. Capacity has commercial value; purchase payments are not necessarily losses.",
        "obligor": "Meta Platforms, Inc.",
        "beneficiary": "Unnamed cloud capacity provider",
        "reimbursement": "Commercial capacity utilization / third-party capacity resale offset",
        "unscorable_metrics": UNSCORABLE_EXPLANATIONS,
    },
    "coreweave-deposit": {
        "id": "coreweave-deposit",
        "ticker": "CRWV",
        "name": "CoreWeave, Inc.",
        "display_name": "CoreWeave, Inc. (CRWV)",
        "case_key": "coreweave-deposit",
        "demo_company": "CoreWeave deposit financing",
        "is_synthetic": False,
        "as_of": "2026-08-12",
        "provenance": "SEC Form 10-K (0001769628-26-000104) / 10-Q (0001769628-26-000366), Note 10",
        "arrangement": "CoreWeave MagAI refundable capacity deposit and in-substance debt",
        "obligation_type": "Recognized in-substance debt financing",
        "reported_principal": "$189m carrying value as of 30 Jun 2026 (unused deposit plus accrued redemption premiums)",
        "disclosed_amount": "$230m original refundable deposit ($100m settled Jun 2026)",
        "amount_label": "Original Deposit Received",
        "commitment_nature": "Recognized debt resulting from contract amendment; 12% effective annual return",
        "triggers": "Maturity January 2029 or termination by either party; unused capacity refundable",
        "ranking": "Classified as recourse in debt table; relative seniority among creditors unestablished",
        "summary": "On-balance-sheet comparison case: a refundable capacity deposit accounted for as in-substance debt.",
        "caveat": "The $273m December 2025 balance included $43m premiums; that premium figure is not the June 2026 amount. The original deposit is not a cap. The 12% effective return is not a disclosed cash-coupon schedule; future payoff and relative creditor priority are unknown.",
        "obligor": "CoreWeave, Inc.",
        "beneficiary": "MagAI Ventures LLC (portfolio-company capacity depositor)",
        "reimbursement": "Unused capacity refund offset; termination return multiplier",
        "unscorable_metrics": UNSCORABLE_EXPLANATIONS,
    },
    "cedar": {
        "id": "cedar",
        "ticker": "CEDAR",
        "name": "Cedar Holdings (Synthetic Sandbox)",
        "display_name": "Cedar Holdings [Synthetic Sandbox]",
        "case_key": "cedar",
        "demo_company": "Cedar",
        "is_synthetic": True,
        "as_of": "2027-12-31",
        "provenance": "Synthetic benchmark stipulated facts (subsidiary_recourse_pair_v1)",
        "arrangement": "Subsidiary recourse pair: Structure A (Non-recourse) vs Structure B (Parent guarantee)",
        "obligation_type": "Senior unsecured bond + contingent parent guarantee",
        "reported_principal": "$100m parent bullet bond principal due",
        "disclosed_amount": "$80m parent guarantee cap (Structure B; $0 in Structure A)",
        "commitment_nature": "Binding senior unsecured parent bond + separate contingent guarantee",
        "triggers": "Subsidiary payment default and liquidation shortfall after lender recovery",
        "ranking": "Parent bond and triggered parent guarantee rank pari passu at settlement",
        "summary": "Parent bond ($100m) with parent standalone cash ($110m). Subsidiary debt ($80m) defaults with $20m liquidation recovery, leaving $60m shortfall.",
        "caveat": "Fictional company and stipulated terms. Settlement occurs at terminal cash pool. Cash is strictly conserved across claims.",
        "obligor": "Cedar Holdings (Parent) & Cedar Operations (Subsidiary)",
        "beneficiary": "Subsidiary external lender & Parent bondholders",
        "reimbursement": "None; subsidiary assets exhausted prior to parent settlement",
        "unscorable_metrics": {},
    },
    "harbor": {
        "id": "harbor",
        "ticker": "HARBOR",
        "name": "Harbor Components (Synthetic Sandbox)",
        "display_name": "Harbor Components [Synthetic Sandbox]",
        "case_key": "harbor",
        "demo_company": "Harbor",
        "is_synthetic": True,
        "as_of": "2027-12-31",
        "provenance": "Synthetic benchmark stipulated facts (harbor_guarantee_v1)",
        "arrangement": "Contingent distributor guarantee waterfall: Base scenario vs Stress scenario",
        "obligation_type": "Senior unsecured bond with coupon + contingent guarantee",
        "reported_principal": "$100m principal ($105m contractual claim incl. 5% coupon)",
        "disclosed_amount": "$40m contingent guarantee cap",
        "commitment_nature": "Binding senior bullet bond with 5% coupon + irrevocable guarantee",
        "triggers": "Distributor payment default at settlement",
        "ranking": "Pari passu with bond principal and coupon",
        "summary": "Senior bullet bond ($100m + $5m coupon). Irrevocable guarantee capped at $40m covering distributor debt shortfall.",
        "caveat": "Fictional company and stipulated terms. Distributable cash pool is $150m in Base, $110m in Stress.",
        "obligor": "Harbor Components (fictional)",
        "beneficiary": "Lender to unrelated distributor",
        "reimbursement": "None in this model",
        "unscorable_metrics": {},
    },
}


def normalize_company(company):
    if not company:
        return company
    cleaned = company.lower().strip()
    return COMPANY_ALIASES.get(cleaned, company)


def search_issuer(query):
    """Resolve an issuer search query to a canonical issuer_id or None."""
    if not query:
        return None
    cleaned = query.strip().lower()
    # Check exact keys and tickers first
    for issuer_id, data in ISSUER_REGISTRY.items():
        if cleaned in (issuer_id.lower(), data["ticker"].lower(), data["name"].lower()):
            return issuer_id
    # Check aliases
    if cleaned in COMPANY_ALIASES:
        target = COMPANY_ALIASES[cleaned]
        for issuer_id, data in ISSUER_REGISTRY.items():
            if data["demo_company"] == target or data["name"] == target:
                return issuer_id
    # Check partial match on ticker or name
    for issuer_id, data in ISSUER_REGISTRY.items():
        if cleaned == data["ticker"].lower():
            return issuer_id
        if cleaned in data["name"].lower() or cleaned in data["display_name"].lower():
            return issuer_id
    return None


def load_selection(company, perspective, variant=None, condition=None):
    """Use existing loaders/builders; references never become part of the request."""
    normalized = normalize_company(company)
    if normalized == "Harbor":
        case = load_case()
        request = build_request(case, perspective, variant)
        values = reference_calculations(case, variant)
        task_id = f"{case['case_id']}:{perspective}:{variant}"
        saved_path = ROOT / "results" / "first-live.json"
        summary_keys = ("distributable_cash", "total_contractual_claims", "bond_recovery_percent", "equity_residual")
    elif normalized == "Cedar":
        case = load_pair()
        request = build_paired_request(case, variant, perspective)
        values = reference_values(case, variant)
        task_id = f"{case['experiment_id']}:{variant}:{perspective}"
        saved_path = ROOT / "results" / "subsidiary-pair-live.json"
        summary_keys = ("parent_cash_pool", "parent_total_contractual_claims", "parent_bond_recovery_percent", "parent_equity_distribution")
    elif normalized in REAL_CASES:
        key = REAL_CASES[normalized]
        _, case = benchmark.load_case(key)
        request = benchmark.request_for(key, perspective) if condition is None else ablation_request(key, perspective, condition)
        values = None
        task_id = f"{case['case_id']}:{perspective}" + (f":{condition}" if condition else "")
        saved_path = ROOT / "results" / ("guidance-ablation-v1-live.json" if condition else
                     "nvidia-ports-investor-pair-live.json" if key == "nvidia-ports" else f"benchmark-{key}-live.json")
    else:
        raise ValueError("Unknown company")
    synthetic = normalized not in REAL_CASES
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
        "summary": [values[k] for k in summary_keys] if synthetic else None,
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
    normalized = normalize_company(company)
    if normalized == "Cedar":
        case = load_pair()
        a, b = (reference_values(case, s) for s in ("A", "B"))
        rows = []
        for label, values in (("No parent guarantee", a), ("Parent guarantee", b)):
            rows.append({
                "Structure": label,
                "Cash pool": values["parent_cash_pool"],
                "Reported principal": case["common"]["parent"]["bond_principal_due"],
                "Direct bond claim": case["common"]["parent"]["bond_principal_due"],
                "Guarantee cap": "0" if label == "No parent guarantee" else case["structures"]["B"]["parent_guarantee"]["cap"],
                "Triggered claim": values["parent_guarantee_claim"],
                "Total claims": values["parent_total_contractual_claims"],
                "Bond payment": values["parent_bond_payment"],
                "Guarantee payment": values["parent_guarantee_payment"],
                "Bond recovery %": values["parent_bond_recovery_percent"],
                "Bond shortfall": str(Decimal(case["common"]["parent"]["bond_principal_due"]) - Decimal(values["parent_bond_payment"])),
                "Equity distribution": values["parent_equity_distribution"]
            })
        return rows
    if normalized != "Harbor":
        raise ValueError("Only synthetic cases have deterministic settlement comparisons")
    case = load_case()
    v = reference_calculations(case, scenario)
    rows = []
    for present in (False, True):
        paid = v["bond_payment"] if present else v["no_guarantee_bond_payment"]
        rows.append({
            "Structure": "Guarantee contract" if present else "Absent guarantee",
            "Cash pool": v["distributable_cash"],
            "Reported principal": v["reported_debt_principal"],
            "Direct bond claim": v["bond_contractual_claim"],
            "Guarantee cap": case["contingent_guarantee"]["cap"] if present else "0",
            "Triggered claim": v["guarantee_contractual_claim"] if present else "0",
            "Total claims": v["total_contractual_claims"] if present else v["bond_contractual_claim"],
            "Bond payment": paid,
            "Guarantee payment": v["guarantee_payment"] if present else "0",
            "Bond recovery %": v["bond_recovery_percent"] if present else str(Decimal(paid) / Decimal(v["bond_contractual_claim"]) * 100),
            "Bond shortfall": str(Decimal(v["bond_contractual_claim"]) - Decimal(paid)),
            "Equity distribution": v["equity_residual"] if present else v["no_guarantee_equity_residual"]
        })
    return rows


def recorded_assessment(company, perspective, condition):
    """Read the recorded review rather than recomputing semantic verdicts."""
    normalized = normalize_company(company)
    case_key = REAL_CASES.get(normalized, normalized)
    report = benchmark.read_json(ROOT / "results/guidance-ablation-v1-revealed.json")
    return next(item for item in report["answers"] if item["case_key"] == case_key
                and item["perspective"] == perspective and item["condition"] == condition)


def fresh_analysis(request):
    """Exactly one selected completion; no batch runner, writes, or retries."""
    return chat_completion(request, get_api_key())
