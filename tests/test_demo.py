import os
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from parallax.demo import load_selection
from parallax.model_api import MODEL, ModelAPIError


APP = Path(__file__).resolve().parent.parent / "streamlit_app.py"


class DemoTests(unittest.TestCase):
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
