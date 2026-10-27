from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from parallax import benchmark as b
from parallax.model_api import ModelAPIError


def response(text="An unverified interpretation", finish="stop"):
    return {"model": "muse-spark-1.3", "choices": [{"message": {"content": text}, "finish_reason": finish}]}


class BenchmarkTests(unittest.TestCase):
    def test_three_cases_isolate_references_and_hold_evidence_constant(self):
        self.assertEqual(set(b.registry()), {"nvidia-ports", "meta-capacity", "coreweave-deposit"})
        for key, entry in b.registry().items():
            normalized = []
            user_messages = []
            for perspective in entry["perspectives"]:
                request = b.request_for(key, perspective)
                user_messages.append(request["messages"][1])
                for hidden in ("HL-0001", "HL-0047", "HL-0041", "verified_facts", "wrong_way_flag", "reference_sha256", "Nebius"):
                    self.assertNotIn(hidden, json.dumps(request))
                label = (f"an equity investor in {entry['company']}" if perspective == "equity_holder" else f"a senior unsecured creditor of {entry['company']}")
                request["messages"][0]["content"] = request["messages"][0]["content"].replace(label, "<investor>")
                normalized.append(request)
            self.assertEqual(normalized[0], normalized[1])
            self.assertEqual(user_messages[0], user_messages[1])
        old = b.read_json(b.ROOT / "results/nvidia-ports-investor-pair-live.json")
        for item in old["evaluations"]:
            self.assertEqual(b.request_for("nvidia-ports", item["perspective"]), item["request"])

    def test_source_cutoff_unknown_case_and_path_escape_are_rejected(self):
        with self.assertRaises(ValueError):
            b.load_case("unknown")
        with self.assertRaises(ValueError):
            b.case_path("../../outside.json")
        entries = b.registry()
        _, case = b.load_case("meta-capacity")
        case["documents"][0]["filed_on"] = "2099-01-01"
        with patch("parallax.benchmark.read_json", side_effect=[{"schema_version": 1, "cases": entries}, case]):
            with self.assertRaisesRegex(ValueError, "cutoff"):
                b.load_case("meta-capacity")

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.benchmark.chat_completion")
    def test_run_preserves_two_provider_responses_and_versions(self, chat):
        originals = [response("Original equity, even if wrong"), response("Original creditor")]
        chat.side_effect = originals
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run.json"
            run = b.run_case("meta-capacity", path)
            self.assertEqual(chat.call_count, 2)
            self.assertEqual(b.read_json(path), run)
            self.assertNotIn("test-secret", path.read_text())
            for index, item in enumerate(run["evaluations"]):
                self.assertEqual(item["model_generated"], originals[index])
                self.assertEqual(chat.call_args_list[index].args, (item["request"], "test-secret"))
            checks = b.protocol_checks(run)
            self.assertTrue(checks["only_investor_phrase_differs"])
            self.assertTrue(checks["requests_match_case_and_builder"])
            self.assertTrue(checks["source_versions_match_current_files"])
            with self.assertRaises(FileExistsError):
                b.run_case("meta-capacity", path)
            self.assertEqual(chat.call_count, 2)

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.benchmark.chat_completion")
    def test_failure_then_incomplete_are_checkpointed_without_retry(self, chat):
        def partial(*args):
            self.assertEqual(b.read_json(path)["evaluations"][0]["status"], "error")
            return response("Partial", "length")
        chat.side_effect = [ModelAPIError("HTTP 429"), response("Partial", "length")]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run.json"
            outcomes = iter((ModelAPIError("HTTP 429"), partial))
            def dispatch(*args):
                result = next(outcomes)
                if isinstance(result, Exception):
                    raise result
                return result(*args)
            chat.side_effect = dispatch
            run = b.run_case("coreweave-deposit", path)
            self.assertEqual([item["status"] for item in run["evaluations"]], ["error", "incomplete"])
            self.assertEqual(chat.call_count, 2)
            self.assertEqual(b.protocol_checks(run)["response_text_present"]["equity_holder"], False)

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.benchmark.chat_completion", return_value=response("Semantically false claim"))
    def test_comparison_reports_missing_unscorable_and_only_recognizes_identifiers(self, chat):
        with tempfile.TemporaryDirectory() as directory:
            run_path = Path(directory) / "run.json"
            b.run_case("meta-capacity", run_path)
            assessment = b.assessment_template("meta-capacity", run_path)
            field = assessment["evaluations"][0]["objective"]["citations"]
            field.update(status="concern", notes="Known source ID does not make the false claim supported.",
                         citations=[{"document_id": "META_10Q", "location_id": "Q_NOTE9_CAPACITY"},
                                    {"document_id": "UNKNOWN", "location_id": "unknown"}])
            assessment["evaluations"][0]["objective"].pop("disclosed_amounts")
            assessment["evaluations"][1]["judgment"]["investor_implications"].update(status="unscorable", notes="Financial inputs absent")
            path = Path(directory) / "assessment.json"
            b.write_new(path, assessment)
            text = b.comparison([path])
            self.assertIn("**concern**", text)
            self.assertIn("recognized identifier = True; semantic support requires human review", text)
            self.assertIn("recognized identifier = False", text)
            self.assertIn("disclosed_amounts: **missing**", text)
            self.assertIn("**unscorable**", text)
            self.assertIn("**not_reviewed**", text)
            self.assertNotIn("accuracy:", text.lower())
            run_path.write_text(run_path.read_text() + " ")
            self.assertIn("Assessment binds recorded run bytes: False", b.comparison([path]))

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    def test_list_preview_and_overwrite_protection_without_key(self):
        def cli(*args):
            return subprocess.run([sys.executable, "-m", "parallax.benchmark", *args], cwd=b.ROOT, capture_output=True, text=True, check=True).stdout
        self.assertIn("nvidia-ports", cli("list"))
        for key in b.registry():
            self.assertEqual(json.loads(cli("preview", key, "--perspective", "equity_holder")), b.request_for(key, "equity_holder"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.md"
            b.write_new(path, "original")
            with self.assertRaises(FileExistsError):
                b.write_new(path, "replacement")
            self.assertEqual(path.read_text(), "original")
