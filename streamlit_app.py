"""Launch with: uv run streamlit run streamlit_app.py"""

from decimal import Decimal
from html import escape
import re

import streamlit as st

from parallax import benchmark
from parallax.demo import (ROOT, REAL_CASES, INVESTOR_LABELS, capital_comparison,
                           fresh_analysis, load_selection, recorded_assessment)
from parallax.model_api import MODEL, ModelAPIError, get_api_key


PAGES = ("Overview", "Capital Structure", "AI Reasoning Lab")
# Editorial summaries of the existing source packs, not new risk estimates.
CASE_BRIEFS = {
    "NVIDIA PORTS": ("Contingent guarantee", "$105bn", "Initial shared cap",
        "Residual-value support for an OpenAI affiliate's leases, with reimbursement rights.",
        "The cap is neither outstanding debt nor an expected loss. Payment depends on contractual conditions; some cap qualifications and costs are redacted."),
    "Meta capacity purchases": ("Contingent purchase", "$14.72bn", "Up to, over five years",
        "A cloud-capacity purchase commitment that may shrink if the provider sells capacity to others.",
        "The provider is unnamed. Trigger details, payment timing and claim ranking are not established by the selected disclosure. Capacity has commercial value; purchase payments are not necessarily losses."),
    "CoreWeave deposit financing": ("Recognized financing", "$189m", "Debt carrying value · 30 Jun 2026",
        "A refundable capacity deposit, amended with termination rights and accounted for as in-substance debt.",
        "The dated balance includes accrued premiums. The 12% effective return is not a disclosed cash-coupon schedule; future payoff and relative creditor priority are unknown."),
}


def number(value, places=2):
    return f"{Decimal(value):,.{places}f}".rstrip("0").rstrip(".")


def money(value):
    return f"${number(value)}m"


def prose(text):
    # Escape dollar signs in financial prose so adjacent amounts are not rendered as math.
    st.markdown(text.replace("$", "\\$"))


def caption(text):
    st.caption(text.replace("$", "\\$"))


def sources(evidence):
    st.caption(f"Historical information cutoff: {evidence['analysis_as_of']} · Not current status.")
    for doc in evidence["documents"]:
        st.markdown(f"[{doc['id']} · {doc['title']}]({doc['url']})")
        st.caption(doc["locator"])
    with st.expander("Read the selected contractual evidence"):
        prose(evidence["preparation"])
        for doc in evidence["documents"]:
            st.markdown(f"**{doc['id']}**")
            prose(doc["factual_paraphrase"])


def allocation(rows):
    """Actual allocation of one fixed cash pool; never chart caps as debt."""
    segments = (("Bond payment", "#176b78"), ("Guarantee payment", "#c67736"),
                ("Equity distribution", "#8ba5ba"))
    st.caption("Where the settlement cash goes · USD millions")
    for row in rows:
        pool = Decimal(row["Cash pool"])
        label = " · ".join(f"{name}: {money(row[name])}" for name, _ in segments)
        bars = "".join(
            f'<span style="width:{Decimal(row[name])/pool*100 if pool else 0}%;background:{color}"></span>'
            for name, color in segments if Decimal(row[name]) > 0)
        st.markdown(f'<div class="allocation-label">{escape(row["Structure"])}</div>'
                    f'<div class="allocation" role="img" aria-label="{escape(label)}">{bars}</div>'
                    f'<div class="allocation-detail">{escape(label)}</div>', unsafe_allow_html=True)
    st.caption("Teal: bondholder · Amber: guarantee beneficiary · Slate: common equity")


def case_cards():
    for col, (company, brief) in zip(st.columns(3), CASE_BRIEFS.items()):
        with col, st.container(border=True):
            kind, amount, label, summary, caveat = brief
            st.caption(kind.upper())
            st.subheader(company)
            st.metric(label, amount)
            prose(summary)
            with st.expander("Terms, sources & limitations"):
                prose(caveat)
                _, evidence = benchmark.load_case(REAL_CASES[company])
                sources(evidence)


def overview():
    st.title("Same debt. Different claims.")
    st.write("Reported financial debt is only part of the picture. Guarantees, purchase commitments and refundable deposits can change who bears risk. Parallax tests whether AI understands those contracts from an investor's perspective.")
    st.caption("THE ECONOMIC INSIGHT · SYNTHETIC CEDAR EXAMPLE · USD MILLIONS")
    rows = capital_comparison("Cedar")
    a, b = rows
    st.markdown(f'<div class="recovery-story"><div><span class="eyebrow">PARENT BOND RECOVERY</span>'
                f'<div class="recovery-values">{number(a["Bond recovery %"])}% <span>→</span> {number(b["Bond recovery %"])}%</div>'
                '<div>No parent guarantee → Enforceable parent guarantee</div></div>'
                '<div class="recovery-note">Same cash.<br>Same reported principal.<br>Different contractual claims.</div></div>', unsafe_allow_html=True)
    stats = zip(("Parent reported principal", "Direct bond claim", "Triggered guarantee claim", "Parent settlement cash"),
                (b["Reported principal"], b["Direct bond claim"], b["Triggered claim"], b["Cash pool"]))
    st.markdown('<div class="stat-grid">' + ''.join(f'<div><span>{label}</span><strong>{money(value)}</strong></div>' for label,value in stats) + '</div>', unsafe_allow_html=True)
    left, right = st.columns((1.25, 1), gap="large")
    with left:
        allocation(rows)
    with right, st.container(border=True):
        st.markdown("**A promise changes the cash split.**")
        prose(f"Same {money(b['Cash pool'])} cash. A {money(b['Triggered claim'])} guarantee claim shares it with the bond. Total parent claims rise to {money(b['Total claims'])}; reported principal stays unchanged.")
    caption("Fictional companies and stipulated terms. Subsidiary debt is $80m; liquidation pays $20m, triggering a $60m claim only when the parent guarantee exists. Parent bond and guarantee rank equally by assumption. Calculations use the existing tested settlement engine.")
    with st.expander("Verify the example and its scope"):
        st.code("Subsidiary shortfall: 80 − 20 = 60\nParent claims with guarantee: 100 + 60 = 160\nBond payment: 100 × (110 / 160) = 68.75\nGuarantee payment: 60 × (110 / 160) = 41.25")
        st.write("No probabilities, market prices or issuer valuation are supplied. These are conditional settlement recoveries, not expected losses or investment returns.")
        st.download_button("Download Cedar's stipulated case", (ROOT / "cases/subsidiary_pair.json").read_text(), "cedar-case.json", "application/json")
    st.divider()
    st.subheader("Three real arrangements. Three different mechanisms.")
    st.caption("Historical SEC disclosures · USD · bn = billion; m = million. These figures measure different things and must not be added together.")
    case_cards()
    st.info("The AI question: can a model preserve the same contractual facts while changing what matters to equity holders and creditors? Explore the AI Reasoning Lab for findings, counterexamples and original records.")


def saved_and_live(selection):
    with st.expander("Original saved response & request"):
        st.caption(f"Historical model output · {MODEL} · {selection['historical_run_at']} · {selection['historical_source']} · Status: {selection['status']}")
        st.caption("Model-generated interpretation, preserved unchanged. Completion means a response was returned, not that its reasoning is correct.")
        if st.toggle("Show original saved response", key="show_saved"):
            response = selection["historical"]
            if response:
                choice = response["choices"][0]
                if choice["finish_reason"] != "stop":
                    st.warning("The provider marked this answer incomplete.")
                with st.container(height=450, border=True):
                    prose(choice["message"]["content"])
            else:
                st.warning("No model text was returned. Inspect the recorded status and source file.")
        st.download_button("Download exact request", benchmark_json(selection["request"]), "selected-request.json", "application/json")
        st.download_button("Download original provider response", benchmark_json(selection["historical"]), "provider-response.json", "application/json")
    with st.expander("Optional live analysis · one selected request"):
        st.caption("One independent request for the selected case, investor and prompt. No retries. Fresh responses remain in this session; research files are preserved.")
        try:
            get_api_key()
            configured = True
        except ModelAPIError:
            configured = False
        if not configured:
            st.caption("Saved mode works without a key. Enable live inference with MODEL_API_KEY loaded locally using uv --env-file .env; never paste the key here.")
        if st.button("Run fresh analysis", disabled=not configured, key="run_fresh"):
            st.session_state.setdefault("fresh_responses", {}).pop(selection["task_id"], None)
            try:
                with st.spinner("Muse Spark is analyzing this selection…"):
                    st.session_state["fresh_responses"][selection["task_id"]] = fresh_analysis(selection["request"])
            except ModelAPIError as exc:
                st.error(str(exc))
        response = st.session_state.get("fresh_responses", {}).get(selection["task_id"])
        if response:
            st.markdown("**Fresh model output · unverified interpretation**")
            prose(response["choices"][0]["message"]["content"])


def benchmark_json(value):
    import json
    return json.dumps(value, indent=2, ensure_ascii=False)


def capital_structure():
    st.title("Contracts decide who gets paid.")
    st.write("Separate legal claims from reported principal, and claims from actual cash payments.")
    controls = st.columns(3)
    company = controls[0].selectbox("Synthetic company", ("Cedar", "Harbor"), key="capital_company")
    investor = controls[1].selectbox("Investor perspective", tuple(INVESTOR_LABELS), format_func=INVESTOR_LABELS.get, key="capital_investor")
    if company == "Harbor":
        scenario = controls[2].selectbox("Economic scenario", ("stress", "base"), format_func=str.title, key="harbor_scenario")
        variant = scenario
    else:
        variant = controls[2].selectbox("Structure to inspect", ("B", "A"),
                    format_func=lambda s: "Parent guarantee" if s == "B" else "Non-recourse", key="cedar_structure")
        scenario = "stress"
    rows = capital_comparison(company, scenario)
    selected = load_selection(company, investor, variant)
    st.caption("SYNTHETIC · USD MILLIONS · SETTLEMENT 31 DEC 2027 · Reference calculations, not model answers")
    if company == "Cedar":
        prose("Subsidiary default in both structures: an $80m debt claim receives $20m locally. Only the parent guarantee changes; parent standalone cash remains $110m.")
    else:
        st.write("Compare the guarantee contract with its absence at the same cash pool and distributor outcome. Switching base/stress also changes cash and default, so that switch alone does not isolate the guarantee's effect.")
    a, b = rows
    inspected = a if company == "Cedar" and variant == "A" else b
    for col, label, value in zip(st.columns(4), ("Reported principal", "Direct bond claim", "Guarantee cap", "Triggered guarantee claim"),
                                 (inspected["Reported principal"], inspected["Direct bond claim"], inspected["Guarantee cap"], inspected["Triggered claim"])):
        col.metric(label + " · selected structure", money(value))
    st.caption(f"Detail selection: {inspected['Structure']}. Both structures are compared below.")
    st.caption("A cap limits the contractual promise; a triggered claim competes at settlement. Neither is automatically an actual payment. Harbor's direct bond claim includes its coupon; Cedar figures refer to the parent, not group debt.")
    for col, row in zip(st.columns(2), rows):
        with col, st.container(border=True):
            st.subheader(row["Structure"])
            if investor == "senior_unsecured_creditor":
                st.metric("Bond recovery", f"{number(row['Bond recovery %'])}%")
                prose(f"Contractual bond claim: {money(row['Direct bond claim'])} · Paid: {money(row['Bond payment'])} · Unpaid: {money(row['Bond shortfall'])}")
            else:
                st.metric("Common equity distribution", money(row["Equity distribution"]))
                prose(f"Cash pool: {money(row['Cash pool'])} · Prior contractual claims: {money(row['Total claims'])}")
    if company == "Cedar" and investor == "equity_holder":
        v = selected["references"]
        st.info((f"No parent liability does not mean no shareholder exposure. Without a guarantee, parent equity distributions fall from {money(v['no_default_parent_equity_distribution'])} without subsidiary default to {money(rows[0]['Equity distribution'])} with default: the parent loses the subsidiary's residual distribution. These are settlement distributions, not market-value losses.").replace("$", "\\$"))
    allocation(rows)
    with st.expander("Settlement ledger & contractual assumptions"):
        st.table([{**{"Structure": row["Structure"]}, **{k: f"{number(v)}%" if k.endswith("%") else money(v) for k, v in row.items() if k != "Structure"}} for row in rows])
        for assumption in selected["evidence"]["assumptions"]:
            st.write(assumption)
        st.json(selected["evidence"])
        st.caption("Existing Decimal calculations; displayed amounts rounded to two decimals. The JSON below retains the original six-decimal references.")
        st.json(selected["references"])
    st.caption("Debt-to-EBITDA leverage, market investment returns and expected loss cannot be determined: required inputs are absent. Secured, subordinated and CDS perspectives require additional contract data and are not modeled.")
    saved_and_live(selected)


def reasoning_lab():
    st.title("Can AI keep the contract straight?")
    st.write("Muse Spark generally identifies the three mechanisms. The harder test is explaining investor consequences without inventing priority, payment timing or losses.")
    st.warning("Research status: preliminary assistant-authored assessments. No independent blinded human ratings, correctness score or statistical significance. A completed API call is not successful financial reasoning.")
    controls = st.columns(2)
    company = controls[0].selectbox("Real-world case", tuple(REAL_CASES), key="lab_company")
    investor = controls[1].selectbox("Investor perspective", tuple(INVESTOR_LABELS), format_func=INVESTOR_LABELS.get, key="lab_investor")
    key = REAL_CASES[company]
    _, evidence = benchmark.load_case(key)
    kind, amount, label, summary, caveat = CASE_BRIEFS[company]
    caption(f"{kind.upper()} · {label}: {amount} · Historical cutoff {evidence['analysis_as_of']}")
    prose(summary + " " + caveat)
    st.caption("Same contractual evidence and amounts for both investors. Only the investor's economic focus changes. Numerical leverage, equity valuation and creditor recovery cannot be determined from these packs.")
    st.markdown("**Investor lens**")
    st.write("Equity: consider commercial value received, financing costs and cash available for investment or distributions. No market-value loss is established." if investor == "equity_holder" else "Senior unsecured credit: consider liquidity demands, competing claims and collectability. Unknown ranking must stay unknown; no recovery estimate is established.")
    st.subheader("Prompt guidance: a controlled comparison")
    st.caption("12 new independent calls · 3 cases × 2 investors × 2 conditions · one sample per cell · muse-spark-1.3")
    st.write("Guided preserves the detailed investor instructions. Neutral asks for economic significance, supporting evidence and material uncertainties. Evidence, historical cutoff, investor identity and API parameters are unchanged.")
    for col, condition in zip(st.columns(2), ("guided", "neutral")):
        assessment = recorded_assessment(company, investor, condition)
        with col, st.container(border=True):
            st.subheader(condition.title())
            st.caption(f"Recorded assistant review · {assessment['review_id']} · not an automated verdict")
            st.markdown("**Contractual identification**")
            prose(re.split(r"(?<=[.!?])\s+", assessment["objective"]["obligation_classification"]["notes"])[0])
            st.markdown("**Investor implications & omissions**")
            prose(re.split(r"(?<=[.!?])\s+", assessment["judgment"]["investor_implications"]["notes"])[0])
            st.markdown("**Unsupported conclusions**")
            prose(re.split(r"(?<=[.!?])\s+", assessment["judgment"]["unsupported_assumptions"]["notes"])[0])
            st.caption("First-sentence excerpts from recorded review; full context below.")
            with st.expander("Claim excerpt & complete category review"):
                st.caption("Excerpt from the original answer · model-generated, not an endorsed conclusion")
                prose(assessment["judgment"]["unsupported_assumptions"]["response_excerpt"])
                prose(assessment["judgment"]["unsupported_assumptions"]["notes"])
                st.json(assessment)
    with st.expander("Findings, limitations & full preliminary comparison"):
        st.write("Basic extraction remained stable in both arms. Neutral answers added more unsupported priority, funding and loss interpretations in this sample. Guidance did not eliminate mistakes: zero-cash assertions, accounting/contract taxonomy and profit-share offsets remain concerns.")
        st.write("Curated evidence already names mechanisms and contains caveats. This is not unaided full-filing extraction. Nonrandom cases, one sampled answer per cell, possible familiarity, imperfect masking and assistant judgment prevent broad causal conclusions.")
        st.download_button("Read full preliminary comparison (Markdown)", (ROOT / "results/guidance-ablation-v1-preliminary-review.md").read_text(), "preliminary-comparison.md", "text/markdown")
    study = st.radio("Response collection", ("Prompt-guidance ablation", "Earlier guided evaluation"), horizontal=True, key="lab_study")
    condition = st.radio("Prompt to inspect", ("guided", "neutral"), format_func=str.title, horizontal=True, key="lab_condition") if study == "Prompt-guidance ablation" else None
    selected = load_selection(company, investor, condition=condition)
    saved_and_live(selected)
    with st.expander("Primary SEC sources, reference facts & research records"):
        sources(evidence)
        entry = benchmark.registry()[key]
        st.download_button("Download original source pack", (benchmark.CASE_ROOT / entry["evidence_file"]).read_text(), entry["evidence_file"], "application/json")
        st.download_button("Download separate reference annotations", (benchmark.CASE_ROOT / entry["reference_file"]).read_text(), entry["reference_file"], "application/json")
        st.download_button("Download full preliminary comparison", (ROOT / "results/guidance-ablation-v1-preliminary-review.md").read_text(), "preliminary-comparison.md", "text/markdown")
        st.caption("Reference annotations are for review; they are not sent to the model. Original on-disk records and previous results are preserved.")
        prose(f"Dataset: Alexander F. Wagner, *Leverage Beyond Debt*, v{entry['dataset']['version']}, [CC BY 4.0]({entry['dataset']['license_url']}). Parallax's selected/paraphrased SEC evidence and assistant reviews are adaptations. See the reference file for provenance and annotation relationships.")


def main():
    st.set_page_config(page_title="Parallax · Obligations in perspective", page_icon="◈", layout="wide")
    st.markdown('''<style>
    .block-container {max-width:1200px;padding-top:4rem;padding-bottom:3rem}
    h1 {letter-spacing:-.04em;font-weight:700} h2,h3 {letter-spacing:-.02em}
    [data-testid="stMetricValue"] {font-variant-numeric:tabular-nums}
    .allocation {height:27px;display:flex;border-radius:5px;overflow:hidden;background:#e5ebef;margin:7px 0}
    .allocation-label {font-size:.9rem;font-weight:600;margin-top:13px}
    .allocation-detail {font-size:.8rem;color:#516273;line-height:1.7;margin-bottom:10px}
    .recovery-story {display:flex;justify-content:space-between;align-items:center;gap:20px;background:#edf5f5;border-left:4px solid #176b78;border-radius:8px;padding:18px 24px;margin:4px 0 18px;font-size:.85rem}
    .eyebrow {font-size:.72rem;letter-spacing:.07em;color:#335865;font-weight:600}
    .recovery-values {font-size:2.6rem;line-height:1.4;font-weight:700;color:#125965;font-variant-numeric:tabular-nums}
    .recovery-values span {color:#8ba5ba;font-weight:400}
    .recovery-note {color:#335865;line-height:1.8}
    .stat-grid {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-bottom:20px}
    .stat-grid span {font-size:.8rem;color:#516273;display:block}
    .stat-grid strong {display:block;font-size:1.7rem;font-weight:600}
    @media(max-width:800px) {.stat-grid {grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.recovery-note {display:none}.recovery-story {padding:12px 16px}.recovery-values {font-size:2.2rem}}
    </style>''', unsafe_allow_html=True)
    st.caption("◈ PARALLAX · OBLIGATIONS IN PERSPECTIVE")
    page = st.radio("Explore", PAGES, key="page", horizontal=True, label_visibility="collapsed")
    {"Overview": overview, "Capital Structure": capital_structure, "AI Reasoning Lab": reasoning_lab}[page]()


if __name__ == "__main__":
    main()
