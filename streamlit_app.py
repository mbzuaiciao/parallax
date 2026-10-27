"""Launch with: uv run streamlit run streamlit_app.py"""

from datetime import datetime
from decimal import Decimal

import streamlit as st

from parallax.demo import fresh_analysis, load_selection
from parallax.model_api import MODEL, ModelAPIError, get_api_key


def number(value):
    return f"{Decimal(value):,.6f}".rstrip("0").rstrip(".")


def money(value):
    return f"${number(value)}m"


def render_obligations(company, evidence):
    if company == "Harbor":
        bond = evidence["reported_debt"]
        guarantee = evidence["contingent_guarantee"]
        scenario = evidence["scenario"]
        st.markdown(f"**Reported bond principal: {money(bond['principal'])}**")
        st.write(f"Annual coupon: {number(str(Decimal(bond['annual_coupon_rate']) * 100))}%.")
        st.write(bond["terms"])
        st.markdown(f"**Contingent guarantee · cap {money(guarantee['cap'])}**")
        st.write(guarantee["terms"])
        st.markdown("**Selected economic scenario**")
        st.write(
            f"Available cash: {money(scenario['distributable_cash'])}. "
            f"Distributor default: {'yes' if scenario['distributor_default'] else 'no'}. "
            f"Covered debt due: {money(scenario['covered_debt_due'])}; "
            f"lender recoveries on default: {money(scenario['lender_recoveries'])}."
            .replace("$", "\\$")
        )
    else:
        parent = evidence["parent"]
        subsidiary = evidence["subsidiary"]
        guarantee = evidence["parent_guarantee"]
        st.markdown(f"**Parent bond principal: {money(parent['bond_principal_due'])}**")
        st.write(parent["bond_terms"])
        st.markdown(f"**Wholly owned subsidiary debt: {money(subsidiary['external_debt_principal_due'])}**")
        st.write(subsidiary["debt_terms"])
        st.markdown("**Parent guarantee**")
        st.write(guarantee["terms"] if guarantee else "None. Subsidiary debt is legally non-recourse to the parent.")
        st.markdown("**Subsidiary default scenario**")
        st.write(
            f"Parent standalone cash: {money(parent['standalone_cash_at_settlement'])}. "
            f"Subsidiary liquidation proceeds: {money(evidence['default_scenario']['subsidiary_net_liquidation_proceeds'])}."
            .replace("$", "\\$")
        )
        st.write(evidence["default_scenario"]["settlement_sequence"])
        with st.expander("No-default comparison"):
            st.write(f"Subsidiary proceeds: {money(evidence['no_default_comparison']['subsidiary_net_liquidation_proceeds'])}.")
            st.write(evidence["no_default_comparison"]["terms"])
    with st.expander("Contractual assumptions and scope"):
        for assumption in evidence["assumptions"]:
            st.write(f"• {assumption}")
        if company == "Harbor":
            st.write(evidence["contingent_guarantee"]["reporting_treatment"])
    if company == "Harbor":
        with st.expander("Independently verifiable background facts"):
            for fact in evidence["reference_facts"]:
                st.write(fact["fact"])
                st.markdown(f"[{fact['source_title']}]({fact['url']})")
                st.caption(fact["scope"])


def render_response(response):
    choice = response["choices"][0]
    if choice["finish_reason"] != "stop":
        st.warning(f"This response may be incomplete (finish reason: {choice['finish_reason']}).")
    # Preserve the text exactly; Streamlit's default Markdown renderer disables raw HTML.
    st.markdown(choice["message"]["content"])


def main():
    st.set_page_config(page_title="Parallax · Investor perspectives", page_icon="◈", layout="wide")
    st.caption("META AI HACKATHON · FINANCIAL REASONING DEMO")
    st.title("Parallax")
    st.write("Explore how corporate obligations affect equity holders and unsecured creditors.")
    st.info("All companies, amounts, scenarios and contract terms are synthetic. Model interpretations can contain errors. Local calculations are verified by deterministic tests under the stated assumptions.")

    controls = st.columns(3)
    company = controls[0].selectbox("Synthetic company", ("Harbor", "Cedar"), key="company")
    perspective = controls[1].selectbox(
        "Investor perspective", ("equity_holder", "senior_unsecured_creditor"),
        format_func=lambda p: "Common equity holder" if p == "equity_holder" else "Senior unsecured creditor",
        key="perspective",
    )
    if company == "Harbor":
        variant = controls[2].selectbox("Economic scenario", ("base", "stress"), index=1,
                                        format_func=str.title, key="harbor_scenario")
    else:
        variant = controls[2].selectbox("Guarantee structure", ("A", "B"), index=1,
                                        format_func=lambda s: "A · Non-recourse" if s == "A" else "B · Parent guarantee",
                                        key="cedar_structure")
    selection = load_selection(company, perspective, variant)
    st.caption(
        f"Settlement: {selection['evidence']['settlement_date']} · All monetary amounts in USD millions. "
        + ("Cedar summary figures refer to the parent company." if company == "Cedar" else "Harbor is the bond issuer and guarantor.")
    )
    st.subheader("Verified calculations")
    labels = ("Available cash", "Contractual claims", "Bond recovery", "Equity distribution")
    for column, label, value in zip(st.columns(4), labels, selection["summary"]):
        column.metric(label, f"{number(value)}%" if label == "Bond recovery" else money(value))
    st.caption("Computed locally from the synthetic inputs. These reference answers are never sent to the model. Cash payments can differ from contractual claims.")

    facts, reasoning = st.columns((1, 1.3), gap="large")
    with facts:
        st.subheader("Financial obligations")
        render_obligations(company, selection["evidence"])
        with st.expander("All deterministic reference values"):
            st.table([
                {"Calculation": key.replace("_", " ").capitalize(),
                 "Value": f"{number(value)}%" if key.endswith("percent") else money(value)}
                for key, value in selection["references"].items()
            ])
            st.caption("Calculated before rounding; six decimal places, half-even.")
    with reasoning:
        st.subheader("Historical model output")
        run_time = datetime.fromisoformat(selection["historical_run_at"]).strftime("%Y-%m-%d %H:%M:%S UTC")
        st.caption(f"Muse Spark · {selection['historical'].get('model', MODEL)} · Saved run: `{run_time}` · Source: {selection['historical_source']}")
        st.caption("Model-generated interpretation, preserved unchanged. This is a saved response, not a fresh API call or a verified financial conclusion.")
        with st.container(height=580, border=True):
            render_response(selection["historical"])

        st.subheader("Optional fresh analysis")
        try:
            get_api_key()
            configured = True
        except ModelAPIError:
            configured = False
        st.caption(f"One request to {MODEL} for the current selection. No automatic retries. Responses stay in this browser session; historical files are preserved.")
        if not configured:
            st.caption("Saved mode needs no key. To enable live analysis, configure MODEL_API_KEY locally and restart with uv loading .env.")
        if st.button("Run fresh analysis", disabled=not configured, type="primary"):
            st.session_state.setdefault("fresh_responses", {}).pop(selection["task_id"], None)
            try:
                with st.spinner("Muse Spark is analyzing the selected case…"):
                    response = fresh_analysis(selection["request"])
                st.session_state["fresh_responses"][selection["task_id"]] = response
            except ModelAPIError as exc:
                st.error(str(exc))
        response = st.session_state.get("fresh_responses", {}).get(selection["task_id"])
        if response:
            st.markdown("**Fresh model output · unverified interpretation**")
            with st.container(height=480, border=True):
                render_response(response)


if __name__ == "__main__":
    main()
