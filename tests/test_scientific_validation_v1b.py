"""Offline v1B prompt/plan invariants; no provider calls."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("v1b_prepare", ROOT / "protocols/scientific-validation-v1b/prepare.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


class V1BTests(unittest.TestCase):
    @patch("socket.socket", side_effect=AssertionError("No network"))
    @patch("parallax.model_api.get_api_key", side_effect=AssertionError("No credential read"))
    @patch("parallax.model_api.chat_completion", side_effect=AssertionError("No paid calls"))
    def test_ten_reproducible_slots_and_frozen_sources(self, chat, key, network):
        plan = b.plan()
        self.assertEqual(plan, b.plan())
        self.assertEqual(len(plan["evaluations"]), 10)
        self.assertEqual(len({c["run_id"] for c in plan["evaluations"]}), 10)
        for case in plan["source_versions"]:
            cells = [c for c in plan["evaluations"] if c["case_key"] == case]
            self.assertEqual({c["condition"] for c in cells}, {"A", "B"})
            self.assertEqual({c["repeat"] for c in cells}, {1})
        for c in plan["evaluations"]:
            self.assertEqual(c["request"], json.loads(c["wire_request_utf8"]))
            self.assertEqual(hashlib.sha256(c["wire_request_utf8"].encode()).hexdigest(), c["wire_request_sha256"])
            self.assertIsNone(c["raw_provider_response"])
        for path, expected in plan["historical_v1_files_sha256"].items():
            self.assertEqual(b.digest(ROOT / path), expected)
        chat.assert_not_called(); key.assert_not_called(); network.assert_not_called()

    def test_exact_positive_and_negative_transformations_only(self):
        records = b.plan()["reference_snapshot"]["cases"]
        for r in records:
            a = b.request_for(r, "A"); neg = b.request_for(r, "B")
            guided = b.v1.request_for(r, "guided"); neutral = b.v1.request_for(r, "neutral")
            expected = guided["messages"][0]["content"].replace(b.NEGATIVE + " ", "").replace(b.UNAVAILABLE + " ", "").replace("Analyze only the single", "Analyze the single", 1)
            self.assertEqual(a["messages"][0]["content"], expected)
            self.assertNotIn("do not", expected.lower())
            self.assertNotIn(b.NEGATIVE, expected)
            self.assertEqual(neg["messages"][0]["content"], neutral["messages"][0]["content"] + " " + b.NEGATIVE)
            for request in (a, neg):
                self.assertEqual(request["messages"][1], guided["messages"][1])
                normalized = copy.deepcopy(request)
                normalized["messages"][0] = guided["messages"][0]
                self.assertEqual(normalized, guided)
                self.assertEqual(request["temperature"], .7)
                self.assertEqual(request["max_completion_tokens"], 8192)
            poisoned = copy.deepcopy(r)
            poisoned["source_checked_facts"] = "REFERENCE_SENTINEL"
            poisoned["financial_interpretations"] = "JUDGMENT_SENTINEL"
            self.assertEqual(b.request_for(poisoned, "A"), a)
        with self.assertRaises(ValueError):
            b.request_for(records[0], "third_condition")


if __name__ == "__main__":
    unittest.main()
