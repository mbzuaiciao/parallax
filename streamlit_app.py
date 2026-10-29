"""Parallax: Corporate Obligation Reconstruction & Analysis Workstation.

Launch with: uv run streamlit run streamlit_app.py
"""

from decimal import Decimal
from html import escape
import json
import re
from pathlib import Path

import streamlit as st

from parallax import benchmark
from parallax.demo import (
    ALL_PERSPECTIVES,
    INVESTOR_LABELS,
    ISSUER_REGISTRY,
    REAL_CASES,
    ROOT,
    capital_comparison,
    fresh_analysis,
    load_selection,
    normalize_company,
    recorded_assessment,
    search_issuer,
)
from parallax.model_api import MODEL, ModelAPIError, get_api_key


FUNCTIONS = (
    "Issuer Overview",
    "Financial Obligations",
    "Capital Structure",
    "Scenario Analysis",
    "AI Diagnostics",
)


def number(value, places=2):
    return f"{Decimal(value):,.{places}f}".rstrip("0").rstrip(".")


def money(value):
    return f"${number(value)}m"


def prose(text):
    """Escape dollar signs in financial prose so adjacent amounts are not rendered as KaTeX math."""
    st.markdown(text.replace("$", "\\$"))


def caption(text):
    st.caption(text.replace("$", "\\$"))


def benchmark_json(value):
    return json.dumps(value, indent=2, ensure_ascii=False)


def render_sources_section(evidence):
    st.caption(f"Historical information cutoff: {evidence['analysis_as_of']} · Historical snapshot, not current status.")
    for doc in evidence["documents"]:
        st.markdown(f"[{doc['id']} · {doc['title']}]({doc['url']})")
        st.caption(f"Locator: {doc['locator']} · Filed: {doc.get('filed_on', 'N/A')}")
    with st.expander("Primary contractual disclosure & preparation"):
        prose(evidence.get("preparation", ""))
        for doc in evidence["documents"]:
            st.markdown(f"**{doc['id']} · {doc.get('accession', '')}**")
            prose(doc.get("factual_paraphrase", ""))


def render_allocation_bars(rows):
    """Actual allocation of one fixed cash pool; strictly conserves cash."""
    segments = (
        ("Bond payment", "#176b78"),
        ("Guarantee payment", "#c67736"),
        ("Equity distribution", "#8ba5ba"),
    )
    st.caption("Terminal settlement cash distribution · USD millions")
    for row in rows:
        pool = Decimal(row["Cash pool"])
        label = " · ".join(f"{name}: {money(row[name])}" for name, _ in segments)
        bars = "".join(
            f'<span style="width:{Decimal(row[name]) / pool * 100 if pool else 0}%;background:{color}"></span>'
            for name, color in segments
            if Decimal(row[name]) > 0
        )
        st.markdown(
            f'<div class="allocation-label">{escape(row["Structure"])}</div>'
            f'<div class="allocation" role="img" aria-label="{escape(label)}">{bars}</div>'
            f'<div class="allocation-detail">{escape(label)}</div>',
            unsafe_allow_html=True,
        )
    st.caption("Teal: bondholder payment · Amber: guarantee payment · Slate: equity residual")


def render_saved_and_live(selection):
    with st.expander("Original saved response & exact request"):
        st.caption(
            f"Historical model output · {MODEL} · {selection['historical_run_at']} · "
            f"Source: {selection['historical_source']} · Status: {selection['status']}"
        )
        st.caption("Model-generated interpretation, preserved unchanged. Completion indicates delivery, not factual correctness.")
        if st.toggle("Show original saved response", key="show_saved"):
            response = selection["historical"]
            if response:
                choice = response["choices"][0]
                if choice.get("finish_reason") != "stop":
                    st.warning("The provider marked this answer incomplete.")
                with st.container(height=450, border=True):
                    prose(choice["message"]["content"])
            else:
                st.warning("No model text was returned. Inspect recorded status and source file.")
        st.download_button(
            "Download exact request (JSON)",
            benchmark_json(selection["request"]),
            "selected-request.json",
            "application/json",
            key=f"dl_req_{selection['task_id']}",
        )
        st.download_button(
            "Download original provider response (JSON)",
            benchmark_json(selection["historical"]),
            "provider-response.json",
            "application/json",
            key=f"dl_resp_{selection['task_id']}",
        )

    with st.expander("Optional live analysis · one selected request"):
        st.caption("One independent request for the selected case, investor and prompt. No retries. Fresh responses remain in session.")
        try:
            get_api_key()
            configured = True
        except ModelAPIError:
            configured = False
        if not configured:
            st.caption("Saved mode works keyless. Enable live inference with MODEL_API_KEY loaded locally via uv --env-file .env.")
        if st.button("Run fresh analysis", disabled=not configured, key="run_fresh"):
            st.session_state.setdefault("fresh_responses", {}).pop(selection["task_id"], None)
            try:
                with st.spinner("Submitting single request to Meta Model API…"):
                    st.session_state["fresh_responses"][selection["task_id"]] = fresh_analysis(selection["request"])
            except ModelAPIError as exc:
                st.error(str(exc))
        response = st.session_state.get("fresh_responses", {}).get(selection["task_id"])
        if response:
            st.markdown("**Fresh model output · unverified interpretation**")
            prose(response["choices"][0]["message"]["content"])


def render_unsupported_panel(query):
    with st.container(border=True):
        st.markdown(
            f'<div class="unsupported-banner">'
            f'<span class="badge-tag">COVERAGE STATUS: NOT COVERED</span>'
            f'<h3>Issuer query "{escape(query)}" is not in Parallax verified coverage</h3>'
            f'<p>Parallax reconstructs corporate obligations from verified primary contractual disclosure packs '
            f'(CC BY 4.0 Wagner AI build-out dataset and SEC EDGAR filings) and deterministic benchmark sandboxes. '
            f'Parallax does not fabricate issuer financials, balance sheets, synthetic ratings, or live pricing feeds.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Select from currently verified issuers or sandbox cases:**")
        cols = st.columns(len(ISSUER_REGISTRY))
        for col, (key, info) in zip(cols, ISSUER_REGISTRY.items()):
            if col.button(f"{info['ticker']} · {info['name']}", key=f"switch_to_{key}"):
                st.session_state["active_issuer"] = key
                st.session_state["issuer_search_input"] = ""
                st.rerun()


# ==============================================================================
# FUNCTION 1: ISSUER OVERVIEW
# ==============================================================================
def page_issuer_overview(issuer_data, active_perspective):
    st.markdown(
        f'<div class="issuer-header">'
        f'<div class="issuer-title-row">'
        f'<span class="ticker-badge">{escape(issuer_data["ticker"])}</span>'
        f'<h2>{escape(issuer_data["name"])}</h2>'
        f'</div>'
        f'<div class="issuer-meta-row">'
        f'<span><strong>Arrangement:</strong> {escape(issuer_data["arrangement"])}</span> · '
        f'<span><strong>Cutoff:</strong> {escape(issuer_data["as_of"])}</span> · '
        f'<span><strong>Classification:</strong> {escape(issuer_data["obligation_type"])}</span> · '
        f'<span><strong>Active Perspective:</strong> {escape(ALL_PERSPECTIVES[active_perspective]["label"])}</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if issuer_data["is_synthetic"]:
        st.info("◈ SCENARIO SANDBOX · Synthetic benchmark with stipulated contractual parameters. Settlement occurs at a fixed terminal cash pool; cash is strictly conserved.")

    # 4-Column Metric Summary
    cols = st.columns(4)
    if issuer_data["is_synthetic"]:
        if issuer_data["id"] == "cedar":
            cols[0].metric("Parent Standalone Cash", "$110m")
            cols[1].metric("Parent Bond Principal", "$100m")
            cols[2].metric("Sub External Debt", "$80m")
            cols[3].metric("Parent Guarantee Cap", "$80m (Struct B)")
        else:
            cols[0].metric("Terminal Cash Pool", "$150m (Base) / $110m (Stress)")
            cols[1].metric("Reported Principal", "$100m")
            cols[2].metric("Direct Bond Claim", "$105m (incl. coupon)")
            cols[3].metric("Guarantee Cap", "$40m")
    else:
        cols[0].metric(issuer_data.get("amount_label", "Disclosed Contractual Cap"), issuer_data["disclosed_amount"])
        cols[1].metric("Reported Carrying Debt", issuer_data["reported_principal"])
        cols[2].metric("Direct Commitment", "$189m recognized debt" if issuer_data["id"] == "coreweave-deposit" else "Contingent obligation")
        cols[3].metric("Reimbursement / Offset", "Contractual" if issuer_data["reimbursement"] else "None")

    st.markdown("### Reconstruction of Corporate Obligations & Economic Exposure")
    st.caption("NOMINAL DISCLOSURES VERSUS ECONOMIC CLAIMS · USD · CONTRACTUAL EVIDENCE CUTOFF")

    # Consistent Exposure Presentation Table
    exposure_rows = [
        {
            "Analytical Layer": "1. Reported Borrowing Principal / Carrying Value",
            "Disclosed Status": issuer_data["reported_principal"],
            "Economic Significance": "Disclosed borrowing status; a guarantee liability carrying amount is distinct from borrowing principal.",
        },
        {
            "Analytical Layer": issuer_data.get("amount_label", "2. Disclosed Contingent Obligations & Contractual Caps"),
            "Disclosed Status": issuer_data["disclosed_amount"],
            "Economic Significance": ("Original financing received, not a contractual cap or additional debt layer."
                                      if issuer_data["id"] == "coreweave-deposit" else
                                      "Maximum contractual ceiling. Never present a cap as current outstanding debt or expected loss."),
        },
        {
            "Analytical Layer": "3. Direct vs Optional Contractual Commitments",
            "Disclosed Status": issuer_data["commitment_nature"],
            "Economic Significance": "Distinguishes enforceable guarantees and in-substance debt from commercial capacity reservations.",
        },
        {
            "Analytical Layer": "4. Scenario Activated Claims",
            "Disclosed Status": (
                "Stress: $60m triggered claim against $80m cap"
                if issuer_data["id"] == "cedar"
                else "Stress: $40m triggered claim against $40m cap"
                if issuer_data["id"] == "harbor"
                else "Unactivated at cutoff (conditional upon counterparty default and termination)"
                if issuer_data["id"] == "nvidia-ports"
                else "Commercial utilization schedule (not an activated debt claim)"
                if issuer_data["id"] == "meta-capacity"
                else "$189m carrying balance (with 12% effective rate)"
            ),
            "Economic Significance": ("Recognized financing balance; no additional guarantee activation is required."
                                      if issuer_data["id"] == "coreweave-deposit" else
                                      "Contractual claim amount competing at settlement only if specific trigger events occur."),
        },
        {
            "Analytical Layer": "5. Actual Scenario Cash Payments",
            "Disclosed Status": (
                "Structure A: $0 | Structure B: $41.25m guarantee payment"
                if issuer_data["id"] == "cedar"
                else "Base: $0 | Stress: $30.34m guarantee payment"
                if issuer_data["id"] == "harbor"
                else "Unscorable without closed enterprise cash distribution and claim resolution"
            ),
            "Economic Significance": "Actual settlement dollars disbursed from available cash; depends on claim priority and liquidity.",
        },
        {
            "Analytical Layer": "6. Recovery & Loss Measures",
            "Disclosed Status": (
                "Bond recovery: Struct A 100% → Struct B 68.75% | Equity: $10m → $0m"
                if issuer_data["id"] == "cedar"
                else "Bond recovery: Base 100% → Stress 75.86% | Equity: $45m → $0m"
                if issuer_data["id"] == "harbor"
                else "Unscorable (Cannot calculate loss rates from isolated contractual disclosures)"
            ),
            "Economic Significance": "Creditor recovery and equity dilution require full claim stack and asset valuation data.",
        },
    ]
    st.table(exposure_rows)

    with st.container(border=True):
        st.markdown("**Analytical Principle: Never fabricate adjusted-debt totals**")
        prose(
            "Contractual caps are contingent ceilings, not current outstanding debt. Adding contingent caps "
            "to reported debt principal, or adding an original deposit again to its recognized carrying balance, distorts "
            "legal priority and economic exposure. Claims must be evaluated in their distinct contractual mechanisms."
        )

    # Missing / Unscorable Metrics Table
    if not issuer_data["is_synthetic"]:
        st.markdown("### Disclosed Limitations & Unscorable Metrics")
        st.caption("EXPLICIT BOUNDARIES · METRICS WITHHELD TO PREVENT FABRICATION")
        unscorable_data = [
            {"Metric": k, "Status": "Unscorable", "Explanation": v}
            for k, v in issuer_data["unscorable_metrics"].items()
        ]
        st.table(unscorable_data)

    st.markdown("### Contract Summary & Caveats")
    prose(issuer_data["summary"] + " " + issuer_data["caveat"])

    if not issuer_data["is_synthetic"]:
        _, evidence = benchmark.load_case(issuer_data["case_key"])
        render_sources_section(evidence)


# ==============================================================================
# FUNCTION 2: FINANCIAL OBLIGATIONS
# ==============================================================================
def page_financial_obligations(issuer_data, active_perspective):
    st.markdown(
        f'<div class="issuer-header">'
        f'<h3>Financial Obligations · {escape(issuer_data["name"])}</h3>'
        f'<div class="issuer-meta-row">As of {escape(issuer_data["as_of"])} · Provenance: {escape(issuer_data["provenance"])}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if issuer_data["is_synthetic"]:
        st.info("Synthetic Scenario Sandbox obligations are defined by stipulated contract parameters.")
        if issuer_data["id"] == "cedar":
            st.markdown("#### Stipulated Instruments")
            st.write("- **Parent Bond:** Senior unsecured bullet bond, $100m principal, zero coupon, all due at settlement. Legally separate from subsidiary debt.")
            st.write("- **Subsidiary External Debt:** $80m principal, zero coupon. Non-recourse to parent unless separate guarantee explicitly present.")
            st.write("- **Parent Guarantee (Structure B only):** Enforceable irrevocable guarantee capped at $80m, covering subsidiary shortfall after liquidation.")
        else:
            st.markdown("#### Stipulated Instruments")
            st.write("- **Senior Unsecured Bond:** $100m principal with 5% annual coupon ($5m interest due at settlement), total claim $105m.")
            st.write("- **Contingent Guarantee:** Irrevocable guarantee capped at $40m issued to lender of unrelated distributor.")
        return

    key = issuer_data["case_key"]
    entry, evidence = benchmark.load_case(key)
    ref_file = benchmark.CASE_ROOT / entry["reference_file"]
    ref_data = benchmark.read_json(ref_file) if ref_file.exists() else {}

    st.markdown("#### Primary Reconstructed Contracts & Disclosed Terms")
    col1, col2 = st.columns((1.5, 1), gap="medium")
    with col1, st.container(border=True):
        st.markdown("**Contractual Provisions & Mechanics**")
        st.write(f"- **Arrangement:** {issuer_data['arrangement']}")
        st.write(f"- **Obligor:** {issuer_data['obligor']}")
        st.write(f"- **Beneficiary / Counterparty:** {issuer_data['beneficiary']}")
        st.write(f"- **Trigger Conditions:** {issuer_data['triggers']}")
        st.write(f"- **Reimbursement / Mitigant:** {issuer_data['reimbursement']}")
        st.write(f"- **Stated Seniority / Rank:** {issuer_data['ranking']}")
        prose(issuer_data["caveat"])

    with col2, st.container(border=True):
        st.markdown("**Disclosed Amounts & Caps**")
        st.metric(issuer_data.get("amount_label", "Disclosed Cap / Value"), issuer_data["disclosed_amount"])
        st.metric("Balance Sheet Carrying Debt", issuer_data["reported_principal"])
        st.caption(f"Historical cutoff: {evidence['analysis_as_of']}")

    # Verified Reference Facts Table
    st.markdown("#### Verified Disclosed Facts (Reference Dataset)")
    st.caption("SOURCE CHECKED FACTS FROM PRIMARY SEC DISCLOSURES · INDEPENDENTLY AUDITABLE")
    facts = ref_data.get("verified_facts", [])
    if facts:
        fact_rows = [
            {
                "ID": f["id"],
                "Category": f["category"].replace("_", " ").title(),
                "Verified Assertion": f["assertion"],
                "Document Locator": ref_data.get("locations", {}).get(f.get("location_id"), {}).get("locator", f.get("document_id", "")),
            }
            for f in facts
        ]
        st.table(fact_rows)

    # Material Unknowns
    st.markdown("#### Material Disclosed Unknowns & Indenture Gaps")
    unknowns = ref_data.get("material_unknowns", [])
    for unk in unknowns:
        st.write(f"• {unk}")

    # Primary Documents
    st.markdown("#### Primary SEC Source Documents")
    for doc in evidence["documents"]:
        with st.container(border=True):
            st.markdown(f"**[{doc['id']} · {doc['title']}]({doc['url']})**")
            st.caption(f"Accession: {doc.get('accession', '')} · Filed on: {doc.get('filed_on', '')} · Locator: {doc.get('locator', '')}")
            prose(doc.get("factual_paraphrase", ""))

    with st.expander("Download raw evidence & reference files"):
        st.download_button(
            "Download primary source pack (JSON)",
            (benchmark.CASE_ROOT / entry["evidence_file"]).read_text(encoding="utf-8"),
            entry["evidence_file"],
            "application/json",
            key="dl_ev_raw",
        )
        st.download_button(
            "Download reference annotations (JSON)",
            (benchmark.CASE_ROOT / entry["reference_file"]).read_text(encoding="utf-8"),
            entry["reference_file"],
            "application/json",
            key="dl_ref_raw",
        )


# ==============================================================================
# FUNCTION 3: CAPITAL STRUCTURE
# ==============================================================================
def page_capital_structure(issuer_data, active_perspective):
    st.markdown(
        f'<div class="issuer-header">'
        f'<h3>Capital Structure & Claims Hierarchy · {escape(issuer_data["name"])}</h3>'
        f'<div class="issuer-meta-row">Active Perspective: {escape(ALL_PERSPECTIVES[active_perspective]["label"])}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Perspective Alert / Notice
    persp_info = ALL_PERSPECTIVES[active_perspective]
    if persp_info["status"] == "planned":
        st.warning(
            f"**Perspective Data Pending: {persp_info['label']}**\n\n"
            f"{persp_info['focus']}\n\n"
            "Analytical workflows for Secured Creditors, Subordinated Creditors, and CDS Participants require "
            "independently verified indenture covenants, lien priority schedules, and ISDA documentation. "
            "Parallax does not display fabricated analytical results for unmodeled perspectives."
        )
        return

    st.markdown(
        f'<div class="investor-lens-card">'
        f'<span class="eyebrow">INVESTOR LENS · {persp_info["label"].upper()}</span>'
        f'<p>{escape(persp_info["focus"])}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if issuer_data["is_synthetic"]:
        company = issuer_data["demo_company"]
        ctrl_cols = st.columns(2)
        if company == "Harbor":
            scenario = ctrl_cols[0].selectbox("Economic Scenario", ("stress", "base"), format_func=str.title, key="harbor_scenario")
            variant = scenario
        else:
            variant = ctrl_cols[0].selectbox(
                "Structure Comparison",
                ("B", "A"),
                format_func=lambda s: "Structure B: Parent guarantee" if s == "B" else "Structure A: Non-recourse",
                key="cedar_structure",
            )
            scenario = "stress"

        rows = capital_comparison(company, scenario)
        selected = load_selection(company, active_perspective, variant)

        a, b = rows
        inspected = a if company == "Cedar" and variant == "A" else b

        st.caption("SYNTHETIC LEDGER · USD MILLIONS · SETTLEMENT WATERFALL · Existing tested calculations")
        m_cols = st.columns(4)
        m_cols[0].metric("Reported Principal", money(inspected["Reported principal"]))
        m_cols[1].metric("Direct Bond Claim", money(inspected["Direct bond claim"]))
        m_cols[2].metric("Guarantee Cap", money(inspected["Guarantee cap"]))
        m_cols[3].metric("Triggered Claim", money(inspected["Triggered claim"]))

        st.markdown("#### Comparative Claim Settlement")
        for col, row in zip(st.columns(2), rows):
            with col, st.container(border=True):
                st.subheader(row["Structure"])
                if active_perspective == "senior_unsecured_creditor":
                    st.metric("Bond Recovery", f"{number(row['Bond recovery %'])}%")
                    prose(f"Claim: {money(row['Direct bond claim'])} · Paid: {money(row['Bond payment'])} · Unpaid: {money(row['Bond shortfall'])}")
                else:
                    st.metric("Equity Distribution", money(row["Equity distribution"]))
                    prose(f"Cash pool: {money(row['Cash pool'])} · Prior claims: {money(row['Total claims'])}")

        if company == "Cedar" and active_perspective == "equity_holder":
            v = selected["references"]
            st.info(
                f"No parent liability does not mean no shareholder exposure. Without a guarantee, parent equity distributions "
                f"fall from {money(v['no_default_parent_equity_distribution'])} (without subsidiary default) to "
                f"{money(rows[0]['Equity distribution'])} (with default): the parent loses the subsidiary's residual distribution."
            )

        render_allocation_bars(rows)

        with st.expander("Settlement ledger & contractual assumptions"):
            st.table([
                {
                    **{"Structure": r["Structure"]},
                    **{k: f"{number(v)}%" if k.endswith("%") else money(v) for k, v in r.items() if k != "Structure"},
                }
                for r in rows
            ])
            for asm in selected["evidence"]["assumptions"]:
                st.write(f"• {asm}")

        render_saved_and_live(selected)
        return

    # Real-world Capital Structure View
    st.markdown("#### Contractual Claims & Obligor Hierarchy")
    st.caption("RECONSTRUCTED OBLIGATION HIERARCHY · UNMODELED PERSPECTIVES REMAIN UNMODELED")

    claims_stack = [
        {
            "Legal Entity": issuer_data["obligor"],
            "Contract / Obligation": issuer_data["arrangement"],
            "Contractual Nature": issuer_data["obligation_type"],
            "Disclosed Amount / Basis": (issuer_data["reported_principal"] if issuer_data["id"] == "coreweave-deposit"
                                         else issuer_data["disclosed_amount"]),
            "Seniority Status": issuer_data["ranking"],
            "Investor Exposure": (
                "Subordinate claim on cash; value offset by commercial capacity and reimbursement rights"
                if active_perspective == "equity_holder"
                else "Potential competing claim on cash; priority relative to senior notes is unestablished in filing"
            ),
        }
    ]
    st.table(claims_stack)

    with st.container(border=True):
        st.markdown("**Creditor Recovery and Equity Valuation Boundaries**")
        prose(
            "Isolated SEC disclosure notes do not establish relative creditor priority, collateral pools, or total "
            "liquidation asset values. Numerical leverage ratios, expected losses, and creditor recovery rates "
            "cannot be determined from these packs without fabricating missing financial inputs."
        )

    # Saved and live inference integration
    selected = load_selection(issuer_data["demo_company"], active_perspective)
    render_saved_and_live(selected)


# ==============================================================================
# FUNCTION 4: SCENARIO ANALYSIS
# ==============================================================================
def page_scenario_analysis(issuer_data, active_perspective):
    st.markdown(
        f'<div class="issuer-header">'
        f'<h3>Scenario Analysis & Activation Pathways · {escape(issuer_data["name"])}</h3>'
        f'<div class="issuer-meta-row">Issuer: {escape(issuer_data["display_name"])}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if issuer_data["is_synthetic"]:
        st.markdown("#### Scenario Sandbox · Deterministic Settlement Waterfalls")
        company = issuer_data["demo_company"]
        if company == "Cedar":
            st.write(
                "Compare Structure A (Non-recourse) against Structure B (Parent guarantee). "
                "Holding parent cash fixed at $110m and subsidiary default proceeds fixed at $20m ($60m shortfall against $80m debt)."
            )
            rows = capital_comparison("Cedar", "stress")
            a, b = rows

            col1, col2 = st.columns(2)
            with col1, st.container(border=True):
                st.markdown("**Structure A: Non-recourse Subsidiary Debt**")
                st.metric("Bond Recovery", f"{number(a['Bond recovery %'])}%")
                st.metric("Equity Distribution", money(a["Equity distribution"]))
                st.caption("Parent claims: $100m bond. Guarantee claim: $0. Bond paid in full; equity receives $10m residual.")

            with col2, st.container(border=True):
                st.markdown("**Structure B: Enforceable Parent Guarantee**")
                st.metric("Bond Recovery", f"{number(b['Bond recovery %'])}%")
                st.metric("Equity Distribution", money(b["Equity distribution"]))
                st.caption("Parent claims: $100m bond + $60m guarantee = $160m claims against $110m cash. Both claims recover 68.75%.")

            render_allocation_bars(rows)

            with st.expander("Arithmetic verification & cash conservation"):
                st.code(
                    "Subsidiary shortfall: 80 − 20 = 60\n"
                    "Structure B Parent claims: 100 + 60 = 160\n"
                    "Bond pro-rata payment: 100 × (110 / 160) = 68.75\n"
                    "Guarantee payment: 60 × (110 / 160) = 41.25\n"
                    "Total cash paid: 68.75 + 41.25 = 110.00 (Cash strictly conserved)"
                )
        else:
            st.write(
                "Harbor Components: Senior bullet bond ($100m principal + $5m coupon = $105m claim) "
                "with an irrevocable guarantee capped at $40m covering distributor debt shortfall."
            )
            rows_base = capital_comparison("Harbor", "base")
            rows_stress = capital_comparison("Harbor", "stress")

            col1, col2 = st.columns(2)
            with col1, st.container(border=True):
                st.markdown("**Base Scenario ($150m Distributable Cash)**")
                st.caption("Distributor pays own debt; guarantee is not triggered.")
                st.metric("Bond Recovery", f"{number(rows_base[1]['Bond recovery %'])}%")
                st.metric("Equity Distribution", money(rows_base[1]["Equity distribution"]))

            with col2, st.container(border=True):
                st.markdown("**Stress Scenario ($110m Distributable Cash)**")
                st.caption("Distributor defaults with $10m recovery against $50m debt -> $40m guarantee claim.")
                st.metric("Bond Recovery", f"{number(rows_stress[1]['Bond recovery %'])}%")
                st.metric("Equity Distribution", money(rows_stress[1]["Equity distribution"]))

            render_allocation_bars(rows_stress)

            with st.expander("Arithmetic verification"):
                st.code(
                    "Covered debt shortfall: 50 − 10 = 40 (At $40m cap)\n"
                    "Total stress claims: 105 (bond) + 40 (guarantee) = 145\n"
                    "Bond payment: 105 × (110 / 145) = 79.66\n"
                    "Guarantee payment: 40 × (110 / 145) = 30.34\n"
                    "Total cash paid: 79.66 + 30.34 = 110.00 (Cash strictly conserved)"
                )
        return

    # Real-World Activation Sensitivity Matrix
    st.markdown("#### Contractual Activation Sensitivity Matrix")
    st.caption("CONDITIONS PRECEDENT TO CLAIM ENFORCEMENT · BASED ON PRIMARY FILING PROVISIONS")

    matrix_rows = [
        {
            "Scenario / Stage": "Baseline / Non-Trigger",
            "Contract Status": "Contingent or performing",
            "Cash Demand on Issuer": "$0 cash outflow under guarantee / commitment",
            "Investor Consequence": "Operating expense / regular capacity usage; no claim dilution.",
        },
        {
            "Scenario / Stage": "Counterparty Default / Notice",
            "Contract Status": "Effectiveness condition met; cure period begins",
            "Cash Demand on Issuer": "Subject to formal demand and remedy election",
            "Investor Consequence": "Potential liquidity call; reimbursement right becomes active.",
        },
        {
            "Scenario / Stage": "Max Contractual Enforcement",
            "Contract Status": f"Liability capped at {issuer_data['disclosed_amount']}",
            "Cash Demand on Issuer": f"Up to contractual cap ({issuer_data['disclosed_amount']})",
            "Investor Consequence": "Competes with other unsecured creditors if default occurs; mitigants apply.",
        },
    ]
    if issuer_data["id"] == "coreweave-deposit":
        matrix_rows = [
            {
                "Scenario / Stage": "Recognized financing at cutoff",
                "Contract Status": "On-balance-sheet recourse debt",
                "Cash Demand on Issuer": "$189m carrying value at 30 Jun 2026; future payoff not established",
                "Investor Consequence": "Already included in reported debt; $230m original deposit is not a cap.",
            },
            {
                "Scenario / Stage": "Termination / Maturity",
                "Contract Status": "Termination rights; January 2029 table maturity; 12% effective return",
                "Cash Demand on Issuer": "Unused deposit plus applicable redemption premiums; payment schedule not supplied",
                "Investor Consequence": "Liquidity and competing claims matter; relative priority is unestablished.",
            },
        ]
    st.table(matrix_rows)

    with st.container(border=True):
        st.markdown("**Why Deterministic Scenario Recovery Is Withheld for Real Issuers**")
        prose(
            "Deterministic settlement waterfalls require a closed asset pool, verified creditor hierarchy, and "
            "comprehensive claim amounts. These disclosures provide selected contractual amounts, not total enterprise "
            "liquidation values. Parallax traces the contractual activation pathway without fabricating recovery percentages."
        )

    st.markdown("#### Test Synthetic Settlement Waterfalls in Scenario Sandbox")
    sc1, sc2 = st.columns(2)
    if sc1.button("Open Cedar Holdings Waterfall (Subsidiary Recourse)", key="goto_cedar_sandbox"):
        st.session_state["active_issuer"] = "cedar"
        st.rerun()
    if sc2.button("Open Harbor Components Waterfall (Contingent Guarantee)", key="goto_harbor_sandbox"):
        st.session_state["active_issuer"] = "harbor"
        st.rerun()


# ==============================================================================
# FUNCTION 5: AI DIAGNOSTICS
# ==============================================================================
def page_ai_diagnostics(issuer_data, active_perspective):
    st.markdown(
        f'<div class="issuer-header">'
        f'<h3>AI Reliability & Diagnostics · {escape(issuer_data["name"])}</h3>'
        f'<div class="issuer-meta-row">Model: {MODEL} · Preregistered Guidance Ablation Study</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.warning(
        "Research Status: Preliminary assistant-authored assessments. No independent blinded human ratings, "
        "manufactured accuracy scores, or statistical significance. A completed API call is not successful financial reasoning."
    )

    if issuer_data["is_synthetic"]:
        st.info("AI Diagnostics focuses on the preregistered real-world disclosure experiments. Select NVIDIA, Meta, or CoreWeave to inspect model assessments.")
        cols = st.columns(3)
        for col, key in zip(cols, ("nvidia-ports", "meta-capacity", "coreweave-deposit")):
            if col.button(f"Inspect {ISSUER_REGISTRY[key]['ticker']} Diagnostics", key=f"diag_switch_{key}"):
                st.session_state["active_issuer"] = key
                st.rerun()
        return

    company = issuer_data["demo_company"]
    key = issuer_data["case_key"]
    entry, evidence = benchmark.load_case(key)

    st.markdown("#### Prompt-Guidance Controlled Comparison")
    st.caption("12 INDEPENDENT RUNS · 3 CASES × 2 INVESTORS × 2 CONDITIONS · ONE SAMPLE PER CELL")

    cond_cols = st.columns(2)
    for col, condition in zip(cond_cols, ("guided", "neutral")):
        assessment = recorded_assessment(company, active_perspective, condition)
        with col, st.container(border=True):
            st.subheader(condition.title())
            st.caption(f"Recorded review · {assessment['review_id']} · not an automated verdict")

            st.markdown("**Contractual Identification**")
            prose(re.split(r"(?<=[.!?])\s+", assessment["objective"]["obligation_classification"]["notes"])[0])

            st.markdown("**Investor Implications & Omissions**")
            prose(re.split(r"(?<=[.!?])\s+", assessment["judgment"]["investor_implications"]["notes"])[0])

            st.markdown("**Unsupported Conclusions**")
            prose(re.split(r"(?<=[.!?])\s+", assessment["judgment"]["unsupported_assumptions"]["notes"])[0])

            with st.expander("Claim excerpt & complete category review"):
                st.caption("Excerpt from the original answer · model-generated, not an endorsed conclusion")
                prose(assessment["judgment"]["unsupported_assumptions"]["response_excerpt"])
                prose(assessment["judgment"]["unsupported_assumptions"]["notes"])
                st.json(assessment)

    with st.expander("Findings, limitations & research comparison"):
        st.write("Basic extraction remained stable in both arms. Neutral answers added more unsupported priority, funding and loss interpretations in this sample. Guidance did not eliminate mistakes: zero-cash assertions, accounting/contract taxonomy and profit-share offsets remain concerns.")
        st.write("Curated evidence already names mechanisms and contains caveats. This is not unaided full-filing extraction. Nonrandom cases, one sampled answer per cell, possible familiarity, imperfect masking and assistant judgment prevent broad causal conclusions.")
        st.download_button(
            "Read full preliminary comparison (Markdown)",
            (ROOT / "results/guidance-ablation-v1-preliminary-review.md").read_text(encoding="utf-8"),
            "preliminary-comparison.md",
            "text/markdown",
            key="dl_prelim_comp",
        )

    # Response Inspector
    study = st.radio("Response collection", ("Prompt-guidance ablation", "Earlier guided evaluation"), horizontal=True, key="lab_study")
    condition = (
        st.radio("Prompt to inspect", ("guided", "neutral"), format_func=str.title, horizontal=True, key="lab_condition")
        if study == "Prompt-guidance ablation"
        else None
    )
    selected = load_selection(company, active_perspective, condition=condition)
    render_saved_and_live(selected)


# ==============================================================================
# MAIN APPLICATION WORKSPACE
# ==============================================================================
def main():
    st.set_page_config(
        page_title="Parallax · Financial Obligation Workstation",
        page_icon="◈",
        layout="wide",
    )

    # Professional Financial-Workstation Aesthetic Styling
    st.markdown(
        """<style>
    .block-container {max-width:1280px;padding-top:2.5rem;padding-bottom:3rem}
    h1, h2, h3, h4 {letter-spacing:-.03em;font-weight:600}
    [data-testid="stMetricValue"] {font-variant-numeric:tabular-nums;font-weight:700}
    .workstation-bar {display:flex;justify-content:space-between;align-items:center;padding:8px 16px;background:#131c26;color:#e5ebef;border-radius:6px;margin-bottom:16px;font-size:.82rem}
    .workstation-bar strong {color:#48cae4;letter-spacing:.05em}
    .workstation-bar span {color:#8ba5ba}
    .issuer-header {background:#f4f7f9;border:1px solid #dce4ec;border-radius:8px;padding:16px 20px;margin-bottom:20px}
    .issuer-title-row {display:flex;align-items:center;gap:12px}
    .issuer-title-row h2 {margin:0;font-size:1.6rem}
    .ticker-badge {background:#176b78;color:#fff;font-weight:700;padding:3px 8px;border-radius:4px;font-size:.85rem;letter-spacing:.05em}
    .badge-tag {background:#c67736;color:#fff;font-weight:600;padding:2px 8px;border-radius:4px;font-size:.75rem}
    .issuer-meta-row {font-size:.85rem;color:#495d70;margin-top:8px}
    .investor-lens-card {background:#eaf2f5;border-left:4px solid #176b78;padding:12px 18px;border-radius:6px;margin-bottom:16px}
    .investor-lens-card .eyebrow {font-size:.72rem;letter-spacing:.07em;color:#176b78;font-weight:700;display:block;margin-bottom:4px}
    .investor-lens-card p {margin:0;font-size:.88rem;color:#1a3038}
    .unsupported-banner {background:#fff4eb;border:1px solid #f2cfb3;padding:18px 24px;border-radius:8px;margin-bottom:18px}
    .unsupported-banner h3 {color:#964b15;margin-top:8px}
    .unsupported-banner p {color:#6b350e;font-size:.9rem;line-height:1.6}
    .allocation {height:24px;display:flex;border-radius:4px;overflow:hidden;background:#e5ebef;margin:6px 0}
    .allocation-label {font-size:.88rem;font-weight:600;margin-top:12px}
    .allocation-detail {font-size:.8rem;color:#516273;line-height:1.6;margin-bottom:8px}
    </style>""",
        unsafe_allow_html=True,
    )

    # Initialize Session State
    if "active_issuer" not in st.session_state:
        st.session_state["active_issuer"] = "nvidia-ports"
    if "active_investor" not in st.session_state:
        st.session_state["active_investor"] = "equity_holder"
    if "page" not in st.session_state:
        st.session_state["page"] = "Issuer Overview"

    # Top Status Bar
    try:
        get_api_key()
        mode_label = "LIVE API ENABLED"
    except ModelAPIError:
        mode_label = "SAVED RECORDS (KEYLESS)"

    st.markdown(
        f'<div class="workstation-bar">'
        f'<div><strong>◈ PARALLAX</strong> | FINANCIAL OBLIGATION WORKSTATION</div>'
        f'<div>MODE: <span>{mode_label}</span> · UNIVERSE: <span>3 REAL ISSUERS · 2 SANDBOX BENCHMARKS</span></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Issuer Search / Selector Bar
    search_col, select_col, persp_col = st.columns((1.5, 1.5, 1.2), gap="medium")
    with search_col:
        search_query = st.text_input(
            "Issuer Search / Command",
            placeholder="Search ticker or issuer (NVDA, META, CRWV, AAPL, CEDAR)...",
            key="issuer_search_input",
        )

    # Handle Search Resolution
    unsupported_query = None
    if search_query.strip():
        matched = search_issuer(search_query)
        if matched:
            st.session_state["active_issuer"] = matched
        else:
            unsupported_query = search_query.strip()

    with select_col:
        selected_issuer_id = st.selectbox(
            "Active Issuer Coverage",
            options=list(ISSUER_REGISTRY.keys()),
            format_func=lambda k: ISSUER_REGISTRY[k]["display_name"],
            key="active_issuer_select",
            index=list(ISSUER_REGISTRY.keys()).index(st.session_state["active_issuer"]),
        )
        if selected_issuer_id != st.session_state["active_issuer"] and not search_query.strip():
            st.session_state["active_issuer"] = selected_issuer_id

    with persp_col:
        st.selectbox(
            "Investor Perspective",
            options=list(ALL_PERSPECTIVES.keys()),
            format_func=lambda k: ALL_PERSPECTIVES[k]["label"],
            key="active_investor",
        )

    # Function Navigation
    page = st.radio(
        "Analytical Function",
        FUNCTIONS,
        key="page",
        horizontal=True,
        label_visibility="collapsed",
    )

    # Handle Unsupported Search Query
    if unsupported_query:
        render_unsupported_panel(unsupported_query)
        return

    # Active Issuer Data
    issuer_data = ISSUER_REGISTRY[st.session_state["active_issuer"]]
    active_perspective = st.session_state["active_investor"]

    # Dispatch to Active Analytical Function
    dispatch = {
        "Issuer Overview": page_issuer_overview,
        "Financial Obligations": page_financial_obligations,
        "Capital Structure": page_capital_structure,
        "Scenario Analysis": page_scenario_analysis,
        "AI Diagnostics": page_ai_diagnostics,
    }
    dispatch[page](issuer_data, active_perspective)


if __name__ == "__main__":
    main()
