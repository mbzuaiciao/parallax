"""Offline checks of the review design, not financial correctness ratings."""

import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from parallax.ablation import hash_value
from parallax.benchmark import digest, read_json
from parallax.real_world import build_disclosure_request


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "protocols/scientific-validation-v1"
spec = importlib.util.spec_from_file_location("scientific_validation_prepare", HERE / "prepare.py")
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class ScientificValidationTests(unittest.TestCase):
    @patch("socket.socket", side_effect=AssertionError("Network forbidden"))
    @patch("parallax.model_api.get_api_key", side_effect=AssertionError("Credentials forbidden"))
    @patch("parallax.model_api.chat_completion", side_effect=AssertionError("Live calls forbidden"))
    def test_offline_plan_replays_exactly_thirty_unexecuted_slots(self, chat, key, network):
        plan = prepare.plan()
        self.assertEqual(plan, prepare.plan())
        self.assertFalse(plan["execution_authorized"])
        self.assertFalse(plan["execution_ready"])
        self.assertEqual(plan["provider_readiness"]["method"], "official_documentation_only_no_API_calls")
        self.assertTrue(plan["provider_readiness"]["unresolved"])
        cells = plan["evaluations"]
        self.assertEqual(len(cells), 30)
        self.assertEqual(len({c["run_id"] for c in cells}), 30)
        self.assertEqual(len(plan["source_versions"]), 5)
        for case in plan["source_versions"]:
            for condition in ("neutral", "guided"):
                group = [c for c in cells if c["case_key"] == case and c["condition"] == condition]
                self.assertEqual({c["repeat"] for c in group}, {1, 2, 3})
                self.assertEqual(len({c["request_sha256"] for c in group}), 1)
        for cell in cells:
            self.assertEqual(cell["status"], "planned_not_executed")
            self.assertIsNone(cell["raw_provider_response"])
            self.assertIsNone(cell["returned_model_version"])
            self.assertEqual(cell["request_sha256"], hash_value(cell["request"]))
        chat.assert_not_called()
        key.assert_not_called()
        network.assert_not_called()

    def test_only_guidance_changes_and_reference_sentinels_never_enter_requests(self):
        records = read_json(HERE / "references.json")["cases"]
        for record in records:
            guided = prepare.request_for(record, "guided")
            neutral = prepare.request_for(record, "neutral")
            original = build_disclosure_request(read_json(ROOT / record["evidence_file"]),
                                                company=record["company"])
            self.assertEqual(guided["messages"], original["messages"])
            self.assertEqual(guided["temperature"], 0.7)
            self.assertEqual(guided["max_completion_tokens"], 8192)
            self.assertEqual(guided["messages"][1], neutral["messages"][1])
            neutral["messages"][0] = guided["messages"][0]
            self.assertEqual(neutral, guided)
            poisoned = copy.deepcopy(record)
            poisoned["source_checked_facts"] = "DO_NOT_SEND_REFERENCE_SENTINEL"
            poisoned["financial_interpretations"] = "DO_NOT_SEND_JUDGMENT_SENTINEL"
            poisoned["evaluation_guidance"] = "DO_NOT_SEND_EVALUATION_GUIDANCE_SENTINEL"
            poisoned["legacy_reference_file"] = "nonexistent-secret-reference.json"
            self.assertEqual(prepare.request_for(poisoned, "guided"), guided)
            sent = json.loads(guided["messages"][1]["content"])
            self.assertEqual(set(sent), {"case_id", "arrangement", "analysis_as_of", "preparation", "documents"})
        with self.assertRaises(ValueError):
            prepare.request_for(records[0], "extra_condition")

    def test_meta_inference_constraint_is_not_a_core_fact_and_is_preserved(self):
        records = read_json(HERE / "references.json")["cases"]
        meta = next(r for r in records if r["case_key"] == "meta-capacity")
        self.assertEqual(meta["core_factual_targets"], ["M1", "M2"])
        self.assertNotIn("M3", [f["id"] for f in meta["source_checked_facts"]])
        guidance = meta["evaluation_guidance"][0]
        self.assertEqual(guidance["id"], "M3")
        self.assertEqual(guidance["type"], "inference_constraint")
        self.assertEqual(guidance["assertion"], "The neighboring $349.31 billion aggregate commitments and 2026/2027 amounts are separate context, not the capacity arrangement payment schedule.")
        self.assertIn(guidance["document_id"], {d["id"] for d in meta["primary_sources"]})

    def test_new_quotes_have_primary_source_check_records_and_identical_condition_bytes(self):
        records = read_json(HERE / "references.json")["cases"]
        expected_quotes = {
            "apple-manufacturing": "manufacturing purchase obligations of $56.2 billion, with $55.4 billion payable within 12 months.",
            "microsoft-leases": "Operating lease ROU assets and liabilities are recognized at commencement date based on the present value of lease payments over the lease term.",
        }
        for record in records:
            if record["case_key"] not in expected_quotes:
                continue
            doc = read_json(ROOT / record["evidence_file"])["documents"][0]
            self.assertEqual(doc["short_quote"], expected_quotes[record["case_key"]])
            check = record["short_quote_verification"]
            self.assertEqual(check["url"], doc["url"])
            self.assertEqual(check["status"], "verbatim_excerpt_checked_by_assistant")
            self.assertTrue(check["locator"])
            for condition in ("neutral", "guided"):
                evidence = json.loads(prepare.request_for(record, condition)["messages"][1]["content"])
                self.assertEqual(evidence["documents"][0]["short_quote"], doc["short_quote"])

    def test_provisional_records_have_resolvable_source_metadata_and_no_invented_reviewers(self):
        records = read_json(HERE / "references.json")["cases"]
        self.assertEqual(len({r["case_key"] for r in records}), 5)
        for record in records:
            self.assertEqual(record["status"], "provisional")
            self.assertIsNone(record["independent_verification"]["reviewer"])
            self.assertEqual(record["independent_verification"]["decision"], "pending")
            evidence = read_json(ROOT / record["evidence_file"])
            docs = {d["id"]: d for d in evidence["documents"]}
            for source in record["primary_sources"]:
                self.assertEqual(source, {k: docs[source["id"]][k] for k in source})
                self.assertRegex(source["accession"], r"^\d{10}-\d{2}-\d{6}$")
                self.assertTrue(source["url"].startswith("https://www.sec.gov/Archives/edgar/"))
                self.assertLessEqual(source["filed_on"], evidence["analysis_as_of"])
            self.assertEqual(record["core_factual_targets"], [f["id"] for f in record["source_checked_facts"]])
            for fact in record["source_checked_facts"]:
                self.assertIn(fact["document_id"], docs)
                self.assertTrue(fact["locator"])
            for field in ("contractual_obligations", "recognized_accounting_liabilities",
                          "financial_interpretations", "material_uncertainties_and_unsupported_conclusions"):
                self.assertTrue(record[field])

    def test_hashes_bind_materials_and_ratings_remain_blank(self):
        plan = prepare.plan()
        for path, expected in plan["files_sha256"].items():
            self.assertEqual(digest(ROOT / path), expected)
        for source in plan["source_versions"].values():
            self.assertEqual(digest(ROOT / source["evidence_file"]), source["sha256"])
        ratings = plan["rating_template"]
        self.assertEqual(set(ratings["dimensions"]), set(prepare.DIMENSIONS))
        self.assertIsNone(ratings["reviewer"])
        self.assertIsNone(ratings["material_unsupported_assertion"])
        for dimension in ratings["dimensions"].values():
            self.assertIsNone(dimension["score"])
            self.assertEqual(dimension["status"], "not_reviewed")

    def test_arithmetic_baseline_is_scoped_outside_the_thirty_disclosures(self):
        plan = prepare.plan()
        baseline = plan["deterministic_baseline"]
        self.assertTrue(baseline["five_disclosure_cases"].startswith("not_applicable:"))
        self.assertEqual(set(baseline["harbor"]), {"base", "stress"})
        self.assertEqual(set(baseline["cedar"]), {"A", "B"})
        self.assertGreater(float(baseline["cedar"]["B"]["parent_guarantee_claim"]), 0)
        self.assertEqual(float(baseline["cedar"]["A"]["parent_guarantee_claim"]), 0)
        for cell in plan["evaluations"]:
            self.assertNotIn("deterministic_reference", json.dumps(cell["request"]))


if __name__ == "__main__":
    unittest.main()
