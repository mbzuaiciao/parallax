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

from parallax.model_api import ModelAPIError
from parallax.real_world import INVESTORS, SOURCE_PATH, build_disclosure_request, evaluate_investors, load_disclosure


class InvestorConditionalTests(unittest.TestCase):
    def test_only_investor_phrase_changes_and_original_evidence_is_exact(self):
        case = load_disclosure()
        original = deepcopy(case)
        baseline = json.loads((SOURCE_PATH.parents[2] / "results/nvidia-ports-live.json").read_text())
        self.assertEqual(build_disclosure_request(case), baseline["request"])
        self.assertEqual(hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(), baseline["input_sha256"])
        normalized = []
        case["wagner_annotations"] = "HIDDEN_REFERENCE_SENTINEL"
        case["combined_response"] = "HIDDEN_REFERENCE_SENTINEL"
        for perspective, label in INVESTORS.items():
            request = build_disclosure_request(case, perspective)
            self.assertEqual(request["messages"][1], baseline["request"]["messages"][1])
            for hidden in ("HIDDEN_REFERENCE_SENTINEL", "HL-0001", "ladder_rung", "wrong_way_flag"):
                self.assertNotIn(hidden, json.dumps(request))
            instruction = request["messages"][0]["content"]
            self.assertEqual(instruction.count(label), 1)
            request["messages"][0]["content"] = instruction.replace(label, "<selected investor>")
            normalized.append(request)
        self.assertEqual(normalized[0], normalized[1])
        self.assertEqual(load_disclosure(), original)
        with self.assertRaises(ValueError):
            build_disclosure_request(case, "unknown")

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.real_world.chat_completion")
    def test_two_requests_are_independent_saved_unchanged_and_not_overwritten(self, chat):
        responses = [{"choices": [{"message": {"content": text}, "finish_reason": "stop"}]}
                     for text in ("Original equity answer", "Original creditor answer")]
        chat.side_effect = responses
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pair.json"
            report = evaluate_investors(path)
            self.assertEqual(chat.call_count, 2)
            for index, perspective in enumerate(INVESTORS):
                item = report["evaluations"][index]
                request = build_disclosure_request(load_disclosure(), perspective)
                self.assertEqual(chat.call_args_list[index].args, (request, "test-secret"))
                self.assertEqual(item["request"], request)
                self.assertEqual(item["model_generated"], responses[index])
                self.assertEqual(item["status"], "completed")
                self.assertEqual(len(item["request"]["messages"]), 2)
            self.assertEqual(json.loads(path.read_text()), report)
            self.assertNotIn("test-secret", path.read_text())
            with self.assertRaises(FileExistsError):
                evaluate_investors(path)
            self.assertEqual(chat.call_count, 2)

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.real_world.chat_completion")
    def test_failure_does_not_prevent_second_request_or_retry(self, chat):
        partial = {"choices": [{"message": {"content": "Unchanged partial answer"}, "finish_reason": "length"}]}
        chat.side_effect = [ModelAPIError("HTTP 429"), partial]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pair.json"
            report = evaluate_investors(path)
            self.assertEqual(chat.call_count, 2)
            self.assertEqual([item["status"] for item in report["evaluations"]], ["error", "incomplete"])
            self.assertEqual(report["evaluations"][1]["model_generated"], partial)
            self.assertEqual(json.loads(path.read_text()), report)

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    def test_cli_preview_matches_pair_without_key(self):
        result = subprocess.run([sys.executable, "-m", "parallax.real_world", "--preview", "--investor-pair"],
                                cwd=SOURCE_PATH.parents[2], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), [build_disclosure_request(load_disclosure(), p) for p in INVESTORS])
