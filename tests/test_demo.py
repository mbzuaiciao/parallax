import os
from decimal import Decimal
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from parallax import benchmark
from parallax.ablation import request_for
from parallax.demo import (
    ALL_PERSPECTIVES,
    INVESTOR_LABELS,
    ISSUER_REGISTRY,
    REAL_CASES,
    capital_comparison,
    load_selection,
    recorded_assessment,
    search_issuer,
)
from parallax.model_api import MODEL, ModelAPIError
from parallax.real_world import build_disclosure_request, load_disclosure

APP = Path(__file__).resolve().parent.parent / "streamlit_app.py"


def text(app):
    parts = []
    for group in (
        app.markdown,
        app.caption,
        app.info,
        app.warning,
        app.error,
        app.code,
    ):
        for x in group:
            parts.append(str(x.value))
    for t in app.table:
        val = t.value
        if hasattr(val, "to_string"):
            parts.append(val.to_string(max_colwidth=None))
        else:
            parts.append(str(val))
    return "\n".join(parts)


def open_app(page=None, issuer=None, perspective=None):
    app = AppTest.from_file(str(APP), default_timeout=15).run()
    if issuer and issuer in list(ISSUER_REGISTRY.keys()):
        app.selectbox(key="active_issuer_select").set_value(issuer).run()
    if perspective and perspective in list(ALL_PERSPECTIVES.keys()):
        app.selectbox(key="active_investor").set_value(perspective).run()
    if page:
        app.radio(key="page").set_value(page).run()
    return app


class DemoTests(unittest.TestCase):
    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_issuer_workspace_and_navigation(self, chat):
        app = open_app()
        self.assertFalse(app.exception)
        # Verify 5 analytical functions
        self.assertEqual(
            app.radio(key="page").options,
            [
                "Issuer Overview",
                "Financial Obligations",
                "Capital Structure",
                "Scenario Analysis",
                "AI Diagnostics",
            ],
        )
        # Default issuer is NVIDIA
        self.assertIn("NVIDIA Corporation", text(app))
        self.assertIn("$105bn", text(app))
        self.assertIn("neither outstanding debt nor an expected loss", text(app))
        # Verify unscorable metrics are explicitly stated
        self.assertIn("Debt / EBITDA Leverage", text(app))
        self.assertIn("Market Probability of Default", text(app))
        self.assertIn("Expected Loss", text(app))
        self.assertIn("Creditor Recovery Rate", text(app))
        # Verify primary SEC link
        _, evidence = benchmark.load_case("nvidia-ports")
        for doc in evidence["documents"]:
            self.assertIn(doc["url"], text(app))
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_unsupported_issuer_search_displays_status_and_does_not_fabricate(self, chat):
        app = open_app()
        # Search an unsupported issuer
        app.text_input(key="issuer_search_input").set_value("AAPL").run()
        self.assertFalse(app.exception)
        self.assertIn("COVERAGE STATUS: NOT COVERED", text(app))
        self.assertIn('query "AAPL"', text(app))
        self.assertIn("Parallax does not fabricate", text(app))
        # Ensure no fabricated financials or ratings
        self.assertNotIn("AAA", text(app))
        self.assertNotIn("BBB", text(app))
        # Switch to supported search
        app.text_input(key="issuer_search_input").set_value("NVDA").run()
        self.assertFalse(app.exception)
        self.assertIn("NVIDIA Corporation", text(app))
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_persistent_context_across_functions(self, chat):
        app = open_app(issuer="meta-capacity", perspective="senior_unsecured_creditor")
        self.assertFalse(app.exception)
        self.assertIn("Meta Platforms, Inc.", text(app))
        self.assertIn("Senior unsecured creditor", text(app))

        # Navigate through all functions and verify context persists
        for page_name in (
            "Financial Obligations",
            "Capital Structure",
            "Scenario Analysis",
            "AI Diagnostics",
            "Issuer Overview",
        ):
            app.radio(key="page").set_value(page_name).run()
            self.assertFalse(app.exception)
            self.assertEqual(app.selectbox(key="active_issuer_select").value, "meta-capacity")
            self.assertEqual(app.selectbox(key="active_investor").value, "senior_unsecured_creditor")
            self.assertIn("Meta Platforms", text(app))
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_planned_investor_perspectives_disclose_data_pending(self, chat):
        app = open_app(page="Capital Structure", perspective="senior_secured_creditor")
        self.assertFalse(app.exception)
        self.assertIn("Perspective Data Pending", text(app))
        self.assertIn("Senior secured creditor", text(app))
        self.assertIn("does not display fabricated analytical results", text(app))
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_financial_obligations_shows_sources_and_verified_facts(self, chat):
        app = open_app(page="Financial Obligations", issuer="nvidia-ports")
        self.assertFalse(app.exception)
        self.assertIn("NVIDIA PORTS Technology Campus residual value guaranties", text(app))
        self.assertIn("0001045810-26-000069", text(app))
        self.assertIn("0001045810-26-000075", text(app))
        # Verified fact N1-N4 assertions
        self.assertIn("OpenAI reimbursement undertaking", text(app))
        self.assertIn("Residual-value guaranties have commencement", text(app))
        self.assertIn("Initial shared aggregate cap is USD 105 billion", text(app))
        chat.assert_not_called()

    def test_registry_provenance_matches_primary_document_accessions(self):
        for key in REAL_CASES.values():
            with self.subTest(case=key):
                _, evidence = benchmark.load_case(key)
                for doc in evidence["documents"]:
                    self.assertIn(doc["accession"], ISSUER_REGISTRY[key]["provenance"])
                    self.assertIn(doc["accession"].replace("-", ""), doc["url"])

    def test_meta_overview_preserves_complete_contractual_cap(self):
        app = open_app(issuer="meta-capacity")
        self.assertFalse(app.exception)
        cap = next(m for m in app.metric if m.label == "Disclosed Contractual Cap")
        self.assertEqual(cap.value, "Up to $14.72bn over five years")

    def test_accounting_amounts_and_deposit_are_not_zero_liability_or_cap(self):
        app = open_app(issuer="nvidia-ports")
        self.assertFalse(app.exception)
        self.assertIn("PORTS guarantee liability carrying amount not separately established", text(app))
        self.assertNotIn("$0 recognized on balance sheet", text(app))
        app.selectbox(key="active_issuer_select").set_value("coreweave-deposit").run()
        deposit = next(m for m in app.metric if m.label == "Original Deposit Received")
        self.assertEqual(deposit.value, "$230m original refundable deposit ($100m settled Jun 2026)")
        self.assertIn("On-balance-sheet comparison case", text(app))
        self.assertNotIn("includes $43m accrued premiums", text(app))
        for page in ("Financial Obligations", "Capital Structure", "Scenario Analysis"):
            app.radio(key="page").set_value(page).run()
            self.assertFalse(app.exception)
            self.assertNotIn("Liability capped at", text(app))
            self.assertNotIn("Up to contractual cap", text(app))
            self.assertIn("$189m", text(app) + "\n" + "\n".join(m.value for m in app.metric))

    def test_cash_conservation_and_controlled_calculation_comparisons(self):
        a, b = capital_comparison("Cedar")
        self.assertEqual(
            (Decimal(a["Bond recovery %"]), Decimal(b["Bond recovery %"])),
            (Decimal(100), Decimal("68.75")),
        )
        self.assertEqual(Decimal(b["Triggered claim"]), Decimal(60))
        self.assertEqual(Decimal(b["Guarantee cap"]), Decimal(80))
        self.assertEqual(Decimal(b["Guarantee payment"]), Decimal("41.25"))
        for company, scenario in (("Cedar", "stress"), ("Harbor", "base"), ("Harbor", "stress")):
            rows = capital_comparison(company, scenario)
            self.assertEqual(rows[0]["Cash pool"], rows[1]["Cash pool"])
            self.assertEqual(rows[0]["Reported principal"], rows[1]["Reported principal"])
            for row in rows:
                allocated = sum(
                    Decimal(row[k]) for k in ("Bond payment", "Guarantee payment", "Equity distribution")
                )
                self.assertLessEqual(abs(allocated - Decimal(row["Cash pool"])), Decimal(".000001"))
        with self.assertRaises(ValueError):
            capital_comparison("NVIDIA PORTS")

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_capital_navigation_investor_switch_and_synthetic_sandbox(self, chat):
        app = open_app(page="Capital Structure", issuer="cedar", perspective="equity_holder")
        self.assertFalse(app.exception)
        self.assertIn("No parent liability does not mean no shareholder exposure", text(app))
        self.assertEqual([x.value for x in app.metric][-2:], ["$10m", "$0m"])

        # Switch to senior unsecured creditor
        app.selectbox(key="active_investor").set_value("senior_unsecured_creditor").run()
        self.assertEqual([x.value for x in app.metric][-2:], ["100%", "68.75%"])

        # Switch structure to Structure A
        app.selectbox(key="cedar_structure").set_value("A").run()
        self.assertEqual([x.value for x in app.metric][:4], ["$100m", "$100m", "$0m", "$0m"])

        # Switch to Harbor sandbox
        app.selectbox(key="active_issuer_select").set_value("harbor").run()
        self.assertEqual(app.metric[1].value, "$105m")  # principal plus coupon, not $100m
        self.assertEqual([x.value for x in app.metric][-2:], ["100%", "75.86%"])

        # Switch Harbor scenario to base
        app.selectbox(key="harbor_scenario").set_value("base").run()
        self.assertEqual([x.value for x in app.metric][-2:], ["100%", "100%"])
        self.assertEqual(app.metric[3].value, "$0m")  # untriggered cap is not a claim
        self.assertTrue(app.button(key="run_fresh").disabled)
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_scenario_analysis_sandbox_and_real_issuer_pathways(self, chat):
        # Synthetic Cedar scenario analysis
        app = open_app(page="Scenario Analysis", issuer="cedar")
        self.assertFalse(app.exception)
        self.assertIn("Structure A: Non-recourse Subsidiary Debt", text(app))
        self.assertIn("Structure B: Enforceable Parent Guarantee", text(app))
        self.assertIn("Subsidiary shortfall: 80 − 20 = 60", text(app))

        # Real issuer scenario activation pathways
        app = open_app(page="Scenario Analysis", issuer="nvidia-ports")
        self.assertFalse(app.exception)
        self.assertIn("Contractual Activation Sensitivity Matrix", text(app))
        self.assertIn("Why Deterministic Scenario Recovery Is Withheld", text(app))
        chat.assert_not_called()

    def test_legacy_saved_selections_and_exact_request_backwards_compatibility(self):
        for company, variants in (("Harbor", ("base", "stress")), ("Cedar", ("A", "B"))):
            for p in INVESTOR_LABELS:
                for variant in variants:
                    selection = load_selection(company, p, variant)
                    self.assertTrue(selection["synthetic"])
                    self.assertNotIn("deterministic_reference", selection["request"])
                    self.assertTrue(selection["historical"]["choices"][0]["message"]["content"])
        for p in INVESTOR_LABELS:
            self.assertEqual(
                load_selection("NVIDIA PORTS", p)["request"],
                build_disclosure_request(load_disclosure(), p),
            )
            for company, key in REAL_CASES.items():
                original = load_selection(company, p)
                self.assertEqual(original["request"], benchmark.request_for(key, p))
                self.assertIsNone(original["references"])
                self.assertEqual(original["status"], "completed")

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_ai_diagnostics_shows_recorded_assessments_and_ablation(self, chat):
        app = open_app(page="AI Diagnostics", issuer="nvidia-ports")
        with patch("parallax.demo.reference_calculations") as harbor, patch(
            "parallax.demo.reference_values"
        ) as cedar:
            for company, key in REAL_CASES.items():
                app.selectbox(key="active_issuer_select").set_value(key).run()
                for p in INVESTOR_LABELS:
                    app.selectbox(key="active_investor").set_value(p).run()
                    for condition in ("guided", "neutral"):
                        app.radio(key="lab_condition").set_value(condition).run()
                        self.assertFalse(app.exception)
                        selection = load_selection(key, p, condition=condition)
                        self.assertEqual(selection["request"], request_for(key, p, condition))
                        self.assertIsNone(selection["references"])
                        self.assertIn(
                            recorded_assessment(key, p, condition)["judgment"][
                                "unsupported_assumptions"
                            ]["notes"].replace("$", "\\$"),
                            text(app),
                        )
                        self.assertTrue(app.button(key="run_fresh").disabled)
                harbor.assert_not_called()
                cedar.assert_not_called()
        self.assertIn("preliminary assistant-authored", text(app).lower())
        self.assertIn("one sample per cell", text(app).lower())
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_original_response_toggle_and_inspection(self, chat):
        app = open_app(page="AI Diagnostics", issuer="nvidia-ports", perspective="equity_holder")
        guided = load_selection("NVIDIA PORTS", "equity_holder", condition="guided")["historical"][
            "choices"
        ][0]["message"]["content"]
        self.assertNotIn(guided.strip(), text(app))
        app.toggle(key="show_saved").set_value(True).run()
        self.assertIn(guided.strip().replace("$", "\\$"), text(app))
        app.radio(key="lab_condition").set_value("neutral").run()
        neutral = load_selection("NVIDIA PORTS", "equity_holder", condition="neutral")[
            "historical"
        ]["choices"][0]["message"]["content"]
        self.assertIn(neutral.strip().replace("$", "\\$"), text(app))
        self.assertNotIn(guided.strip().replace("$", "\\$"), text(app))
        app.radio(key="lab_study").set_value("Earlier guided evaluation").run()
        historical = load_selection("NVIDIA PORTS", "equity_holder")["historical"]["choices"][0][
            "message"
        ]["content"]
        self.assertIn(historical.strip().replace("$", "\\$"), text(app))
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.demo.chat_completion")
    def test_optional_live_submits_only_selected_neutral_investor_and_keeps_binding(self, chat):
        chat.return_value = {
            "model": MODEL,
            "choices": [
                {
                    "message": {"content": "Fresh unverified live test output"},
                    "finish_reason": "stop",
                }
            ],
        }
        app = open_app(
            page="AI Diagnostics", issuer="meta-capacity", perspective="senior_unsecured_creditor"
        )
        app.radio(key="lab_condition").set_value("neutral").run()
        chat.assert_not_called()
        app.button(key="run_fresh").click().run()
        self.assertFalse(app.exception)
        chat.assert_called_once_with(
            request_for("meta-capacity", "senior_unsecured_creditor", "neutral"), "test-secret"
        )
        self.assertIn("Fresh unverified live test output", text(app))
        app.radio(key="lab_condition").set_value("guided").run()
        self.assertNotIn("Fresh unverified live test output", text(app))
        self.assertEqual(chat.call_count, 1)

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch(
        "parallax.demo.chat_completion",
        side_effect=ModelAPIError("Meta Model API returned HTTP 429"),
    )
    def test_live_failure_preserves_saved_response_and_does_not_retry(self, chat):
        app = open_app(page="Capital Structure", issuer="cedar", perspective="equity_holder")
        app.toggle(key="show_saved").set_value(True).run()
        app.button(key="run_fresh").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.error[0].value, "Meta Model API returned HTTP 429")
        self.assertIn(
            load_selection("Cedar", "equity_holder", "B")["historical"]["choices"][0]["message"][
                "content"
            ]
            .strip()
            .replace("$", "\\$"),
            text(app),
        )
        chat.assert_called_once_with(
            load_selection("Cedar", "equity_holder", "B")["request"], "test-secret"
        )
