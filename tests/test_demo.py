import os
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from parallax.demo import load_selection
from parallax.model_api import MODEL, ModelAPIError
from parallax.real_world import build_disclosure_request, load_disclosure


APP = Path(__file__).resolve().parent.parent / "streamlit_app.py"


class DemoTests(unittest.TestCase):
    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_nvidia_saved_investor_switching_without_key_or_synthetic_calculations(self, chat):
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        with patch("parallax.demo.reference_calculations") as harbor_calculations, patch("parallax.demo.reference_values") as cedar_calculations:
            app.selectbox[0].set_value("NVIDIA PORTS").run()
            evidence = []
            for perspective in ("equity_holder", "senior_unsecured_creditor"):
                app.selectbox[1].set_value(perspective).run()
                self.assertFalse(app.exception)
                self.assertEqual(len(app.selectbox), 2)
                self.assertEqual(len(app.metric), 0)
                self.assertEqual(len(app.table), 0)
                self.assertNotIn("Verified calculations", [item.value for item in app.subheader])
                self.assertNotIn("All deterministic reference values", [item.label for item in app.expander])
                self.assertTrue(app.button[0].disabled)
                selected = load_selection("NVIDIA PORTS", perspective)
                self.assertFalse(selected["synthetic"])
                self.assertIsNone(selected["summary"])
                self.assertIsNone(selected["references"])
                self.assertEqual(selected["request"], build_disclosure_request(load_disclosure(), perspective))
                evidence.append(selected["evidence"])
                text = [item.value for item in app.markdown]
                self.assertIn(selected["historical"]["choices"][0]["message"]["content"].strip(), text)
                self.assertTrue(any("2026-08-26" in item.value for item in app.caption))
                self.assertTrue(any("neither outstanding debt nor an expected loss" in item.value for item in app.info))
                self.assertIn("Historical model output", [item.value for item in app.subheader])
                for document in selected["evidence"]["documents"]:
                    self.assertTrue(any(document["url"] in item for item in text))
            self.assertEqual(evidence[0], evidence[1])
            harbor_calculations.assert_not_called()
            cedar_calculations.assert_not_called()
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.demo.chat_completion")
    def test_nvidia_live_button_reuses_selected_investor_builder(self, chat):
        chat.return_value = {"model": MODEL, "choices": [{"message": {"content": "Fresh NVIDIA test interpretation"}, "finish_reason": "stop"}]}
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        app.selectbox[0].set_value("NVIDIA PORTS").run()
        app.selectbox[1].set_value("senior_unsecured_creditor").run()
        chat.assert_not_called()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        chat.assert_called_once_with(build_disclosure_request(load_disclosure(), "senior_unsecured_creditor"), "test-secret")
        self.assertIn("Fresh NVIDIA test interpretation", [item.value for item in app.markdown])
        app.selectbox[1].set_value("equity_holder").run()
        self.assertNotIn("Fresh NVIDIA test interpretation", [item.value for item in app.markdown])
        self.assertEqual(chat.call_count, 1)

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_saved_mode_all_eight_selections_needs_no_key_or_calls(self, chat):
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        for company, variants in (("Harbor", ("base", "stress")), ("Cedar", ("A", "B"))):
            app.selectbox[0].set_value(company).run()
            for perspective in ("equity_holder", "senior_unsecured_creditor"):
                app.selectbox[1].set_value(perspective).run()
                for variant in variants:
                    app.selectbox[2].set_value(variant).run()
                    self.assertFalse(app.exception)
                    selected = load_selection(company, perspective, variant)
                    historical_text = selected["historical"]["choices"][0]["message"]["content"]
                    self.assertIn(historical_text.strip(), [element.value for element in app.markdown])
                    self.assertTrue(app.button[0].disabled)
                    recovery = selected["summary"][2].rstrip("0").rstrip(".") + "%"
                    self.assertEqual(app.metric[2].value, recovery)
                    self.assertNotIn("deterministic_reference", selected["request"])
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.demo.chat_completion")
    def test_button_submits_only_selected_case_and_preserves_selection_binding(self, chat):
        chat.return_value = {"model": MODEL, "choices": [{"message": {"content": "Fresh unverified test output"}, "finish_reason": "stop"}]}
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        app.selectbox[0].set_value("Cedar").run()
        app.selectbox[1].set_value("senior_unsecured_creditor").run()
        app.selectbox[2].set_value("A").run()
        chat.assert_not_called()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        chat.assert_called_once_with(load_selection("Cedar", "senior_unsecured_creditor", "A")["request"], "test-secret")
        self.assertIn("Fresh unverified test output", [element.value for element in app.markdown])
        app.selectbox[2].set_value("B").run()
        self.assertNotIn("Fresh unverified test output", [element.value for element in app.markdown])
        app.selectbox[2].set_value("A").run()
        self.assertIn("Fresh unverified test output", [element.value for element in app.markdown])
        self.assertEqual(chat.call_count, 1)

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.demo.chat_completion", side_effect=ModelAPIError("Meta Model API returned HTTP 429"))
    def test_live_failure_keeps_historical_output_and_does_not_retry(self, chat):
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.error[0].value, "Meta Model API returned HTTP 429")
        self.assertIn(load_selection("Harbor", "equity_holder", "stress")["historical"]["choices"][0]["message"]["content"].strip(),
                      [element.value for element in app.markdown])
        chat.assert_called_once()
