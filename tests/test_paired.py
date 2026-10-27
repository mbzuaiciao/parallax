from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from parallax.model_api import ModelAPIError
from parallax.paired import build_paired_request, load_pair, reference_values, run_pair


class PairedTests(unittest.TestCase):
    def setUp(self):
        self.pair = load_pair()

    def test_load_is_repeatable_and_only_guarantee_changes(self):
        self.assertEqual(self.pair, load_pair())
        original = deepcopy(self.pair)
        for perspective in ("equity_holder", "senior_unsecured_creditor"):
            a_request = build_paired_request(self.pair, "A", perspective)
            b_request = build_paired_request(self.pair, "B", perspective)
            self.assertEqual(a_request["messages"][0], b_request["messages"][0])
            a = json.loads(a_request["messages"][1]["content"])
            b = json.loads(b_request["messages"][1]["content"])
            self.assertIsNone(a["evidence"].pop("parent_guarantee"))
            self.assertEqual(b["evidence"].pop("parent_guarantee")["cap"], "80")
            a.pop("structure")
            b.pop("structure")
            self.assertEqual(a, b)
        self.assertEqual(self.pair, original)

    def test_reference_values_against_hand_calculation(self):
        a = reference_values(self.pair, "A")
        b = reference_values(self.pair, "B")
        for values in (a, b):
            self.assertEqual(values["group_gross_borrowing_principal"], "180.000000")
            self.assertEqual(values["subsidiary_unpaid_debt_after_liquidation"], "60.000000")
            self.assertEqual(values["subsidiary_equity_distribution"], "0.000000")
            self.assertEqual(values["lost_subsidiary_equity_distribution"], "30.000000")
            self.assertEqual(values["no_default_parent_equity_distribution"], "40.000000")
            self.assertEqual(values["parent_cash_pool"], "110.000000")
        self.assertEqual(a["parent_guarantee_claim"], "0.000000")
        self.assertEqual(a["parent_total_contractual_claims"], "100.000000")
        self.assertEqual(a["parent_bond_payment"], "100.000000")
        self.assertEqual(a["parent_equity_distribution"], "10.000000")
        self.assertEqual(a["parent_equity_decline_vs_no_default"], "30.000000")
        self.assertEqual(b["parent_guarantee_claim"], "60.000000")
        self.assertEqual(b["parent_total_contractual_claims"], "160.000000")
        self.assertEqual(Fraction(b["parent_bond_payment"]), Fraction(110 * 100, 160))
        self.assertEqual(Fraction(b["parent_guarantee_payment"]), Fraction(110 * 60, 160))
        self.assertEqual(b["parent_equity_distribution"], "0.000000")
        self.assertEqual(b["parent_equity_decline_vs_no_default"], "40.000000")
        self.assertEqual(b["subsidiary_lender_total_recovery"], "61.250000")
        for values in (a, b):
            paid = sum(Decimal(values[key]) for key in ("parent_bond_payment", "parent_guarantee_payment", "parent_equity_distribution"))
            self.assertEqual(paid, Decimal(110))
            self.assertEqual(paid + Decimal(values["subsidiary_lender_payment_from_subsidiary"]), Decimal(130))

    def test_references_are_not_in_prompts(self):
        self.pair["deterministic_reference"] = "DO_NOT_SEND"
        self.pair["expected_conclusion"] = "DO_NOT_SEND"
        for structure in ("A", "B"):
            for perspective in ("equity_holder", "senior_unsecured_creditor"):
                payload = json.dumps(build_paired_request(self.pair, structure, perspective))
                for excluded in ("DO_NOT_SEND", "deterministic_reference", "68.75", "41.25", "61.25"):
                    self.assertNotIn(excluded, payload)

    def test_invalid_pair_inputs(self):
        variants = []
        for group, field, value in (("parent", "standalone_cash_at_settlement", "NaN"),
                                    ("subsidiary", "parent_ownership_percent", "50"),
                                    ("default_scenario", "subsidiary_default", False)):
            pair = deepcopy(self.pair)
            pair["common"][group][field] = value
            variants.append(pair)
        pair = deepcopy(self.pair)
        pair["structures"]["B"]["extra_cash"] = "999"
        variants.append(pair)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pair.json"
            for pair in variants:
                path.write_text(json.dumps(pair))
                with self.assertRaises(ValueError):
                    load_pair(path)

    @patch.dict("os.environ", {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.paired.chat_completion")
    def test_four_requests_persist_unchanged_responses_and_errors(self, chat):
        def response(text, finish="stop"):
            return {"choices": [{"message": {"content": text}, "finish_reason": finish}]}
        chat.side_effect = [response("Unchanged answer, even if wrong"), ModelAPIError("HTTP 429"),
                            response("Partial answer", "length"), response("Fourth answer")]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            report = run_pair(self.pair, path)
            self.assertEqual(chat.call_count, 4)
            self.assertEqual([item["status"] for item in report["evaluations"]], ["completed", "error", "incomplete", "completed"])
            self.assertEqual(report["evaluations"][0]["model_generated"], response("Unchanged answer, even if wrong"))
            self.assertEqual(len({item["task_id"] for item in report["evaluations"]}), 4)
            self.assertEqual(json.loads(path.read_text()), report)
            self.assertNotIn("test-secret", path.read_text())
            for item in report["evaluations"]:
                self.assertFalse(item["deterministic_reference"]["sent_to_model"])
                self.assertEqual(item["request"], chat.call_args_list[report["evaluations"].index(item)].args[0])
            with self.assertRaises(FileExistsError):
                run_pair(self.pair, path)
            self.assertEqual(chat.call_count, 4)

    def test_preview_cli_reproduces_four_requests_without_a_key(self):
        result = subprocess.run([sys.executable, "-m", "parallax.paired", "--all"],
                                cwd=Path(__file__).resolve().parent.parent, text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(result.stdout), [build_paired_request(self.pair, s, p)
                         for s in ("A", "B") for p in ("equity_holder", "senior_unsecured_creditor")])
