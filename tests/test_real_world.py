from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from parallax.model_api import MODEL, ModelAPIError
from parallax.real_world import SOURCE_PATH, build_disclosure_request, evaluate_disclosure, load_disclosure


class DisclosureTests(unittest.TestCase):
    def test_prompt_excludes_separate_research_labels(self):
        case = load_disclosure()
        original = deepcopy(case)
        case["wagner_annotations"] = {"answer": "HIDDEN_ANNOTATION_SENTINEL"}
        request = build_disclosure_request(case)
        content = json.dumps(request)
        for hidden in ("HIDDEN_ANNOTATION_SENTINEL", "HL-0001", "ladder_rung", "wrong_way_flag", "C2", "105.0"):
            self.assertNotIn(hidden, content)
        self.assertEqual(json.loads(request["messages"][1]["content"])["documents"], original["documents"])
        self.assertEqual(build_disclosure_request(original), request)

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.real_world.chat_completion")
    def test_one_live_request_preserves_response_and_input_hash(self, chat):
        response = {"model": MODEL, "choices": [{"message": {"content": "Original model claim, even if incorrect."}, "finish_reason": "stop"}]}
        chat.return_value = response
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "response.json"
            report = evaluate_disclosure(path)
            chat.assert_called_once_with(build_disclosure_request(load_disclosure()), "test-secret")
            self.assertEqual(json.loads(path.read_text()), report)
            self.assertEqual(report["model_generated"], response)
            self.assertEqual(report["status"], "completed")
            self.assertEqual(report["input_sha256"], hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest())
            self.assertNotIn("test-secret", path.read_text())
            with self.assertRaises(FileExistsError):
                evaluate_disclosure(path)
            self.assertEqual(chat.call_count, 1)

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.real_world.chat_completion")
    def test_failed_or_incomplete_response_is_recorded_without_retry(self, chat):
        partial = {"choices": [{"message": {"content": "Incomplete original"}, "finish_reason": "length"}]}
        with tempfile.TemporaryDirectory() as directory:
            chat.return_value = partial
            report = evaluate_disclosure(Path(directory) / "partial.json")
            self.assertEqual(report["status"], "incomplete")
            self.assertEqual(report["model_generated"], partial)
            chat.side_effect = ModelAPIError("Meta Model API returned HTTP 429")
            path = Path(directory) / "error.json"
            report = evaluate_disclosure(path)
            self.assertEqual(report["status"], "error")
            self.assertEqual(json.loads(path.read_text()), report)
            self.assertEqual(chat.call_count, 2)

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    def test_preview_is_reproducible_without_key_or_research_snapshot(self):
        result = subprocess.run([sys.executable, "-m", "parallax.real_world", "--preview"],
                                cwd=SOURCE_PATH.parents[2], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), build_disclosure_request(load_disclosure()))
