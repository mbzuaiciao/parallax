from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from parallax.cli import DEFAULT_CASE, load_case, prepare_task, reference_calculations


ROOT = Path(__file__).resolve().parent.parent


class CaseTests(unittest.TestCase):
    def setUp(self):
        self.case = load_case()

    def test_loading_is_deterministic_and_independent(self):
        self.assertEqual(self.case, load_case(DEFAULT_CASE))
        self.assertEqual(self.case["reported_debt"]["principal"], "100")
        self.assertEqual(self.case["contingent_guarantee"]["cap"], "40")
        self.case["reported_debt"]["principal"] = "999"
        self.assertEqual(load_case()["reported_debt"]["principal"], "100")

    def test_invalid_case_data_is_rejected(self):
        variants = []
        for value in ("-1", "NaN", "Infinity", "nonsense", 100):
            case = deepcopy(self.case)
            case["reported_debt"]["principal"] = value
            variants.append(case)
        for field, value in (("schema_version", 2), ("scenarios", {}), ("perspectives", {})):
            case = deepcopy(self.case)
            case[field] = value
            variants.append(case)
        case = deepcopy(self.case)
        case["scenarios"]["stress"]["distributor_default"] = "false"
        variants.append(case)
        variants.append({})
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            for case in variants:
                with self.subTest(case=case):
                    path.write_text(json.dumps(case), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_case(path)

    def test_base_reference_values(self):
        result = reference_calculations(self.case, "base")
        expected = {
            "reported_debt_principal": "100.000000",
            "bond_coupon_due": "5.000000",
            "bond_contractual_claim": "105.000000",
            "guarantee_contractual_claim": "0.000000",
            "total_contractual_claims": "105.000000",
            "distributable_cash": "150.000000",
            "bond_payment": "105.000000",
            "guarantee_payment": "0.000000",
            "bond_shortfall": "0.000000",
            "bond_recovery_percent": "100.000000",
            "equity_residual": "45.000000",
            "no_guarantee_bond_payment": "105.000000",
            "no_guarantee_equity_residual": "45.000000",
        }
        self.assertEqual(result, expected)

    def test_stress_against_independent_rational_waterfall(self):
        result = reference_calculations(self.case, "stress")
        # Independent hand calculation in exact fractions, not Decimal algorithm reuse.
        expected = {
            "bond_coupon_due": Fraction(5),
            "bond_contractual_claim": Fraction(105),
            "guarantee_contractual_claim": Fraction(40),
            "total_contractual_claims": Fraction(145),
            "bond_payment": Fraction(110 * 105, 145),
            "guarantee_payment": Fraction(110 * 40, 145),
            "bond_shortfall": Fraction(105 * 35, 145),
            "bond_recovery_percent": Fraction(110 * 100, 145),
            "equity_residual": Fraction(0),
            "no_guarantee_bond_payment": Fraction(105),
            "no_guarantee_equity_residual": Fraction(5),
        }
        for key, exact in expected.items():
            self.assertLessEqual(abs(Fraction(result[key]) - exact), Fraction(1, 2_000_000), key)
        self.assertEqual(result["bond_payment"], "79.655172")
        self.assertEqual(result["guarantee_payment"], "30.344828")
        self.assertEqual(result["bond_recovery_percent"], "75.862069")

    def test_cash_conservation_and_claim_limits(self):
        for scenario in ("base", "stress"):
            result = {key: Decimal(value) for key, value in reference_calculations(self.case, scenario).items()}
            self.assertEqual(result["bond_payment"] + result["guarantee_payment"] + result["equity_residual"], result["distributable_cash"])
            self.assertLessEqual(result["bond_payment"], result["bond_contractual_claim"])
            self.assertLessEqual(result["guarantee_payment"], result["guarantee_contractual_claim"])

    def test_trigger_cap_and_recovery_netting(self):
        inputs = self.case["scenarios"]["stress"]
        for default, due, recoveries, expected in (
            (False, "100", "0", "0.000000"),
            (True, "100", "0", "40.000000"),
            (True, "50", "35", "15.000000"),
            (True, "50", "60", "0.000000"),
        ):
            inputs.update(distributor_default=default, covered_debt_due=due, lender_recoveries=recoveries)
            self.assertEqual(reference_calculations(self.case, "stress")["guarantee_contractual_claim"], expected)

    def test_four_tasks_preserve_evidence_and_do_not_mutate_case(self):
        original = deepcopy(self.case)
        tasks = [prepare_task(self.case, p, s) for p in ("equity_holder", "senior_unsecured_creditor") for s in ("base", "stress")]
        self.assertEqual(len({task["task_id"] for task in tasks}), 4)
        for task in tasks:
            self.assertEqual(set(task["case_evidence"]["scenarios"]), {task["scenario"]})
            self.assertEqual(task["case_evidence"]["reference_facts"], original["reference_facts"])
            self.assertEqual(task["deterministic_reference"]["values"], reference_calculations(original, task["scenario"]))
            self.assertEqual(task, prepare_task(self.case, task["perspective"], task["scenario"]))
        self.assertEqual(self.case, original)
        tasks[0]["case_evidence"]["reported_debt"]["principal"] = "1"
        self.assertEqual(self.case, original)
        with self.assertRaises(ValueError):
            prepare_task(self.case, "unknown", "base")
        with self.assertRaises(ValueError):
            prepare_task(self.case, "equity_holder", "unknown")

    def test_cli_all_matches_four_individual_runs_byte_for_byte(self):
        def run(*args):
            return subprocess.run([sys.executable, "-m", "parallax", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        output = run("--all")
        self.assertEqual(output, run("--all"))
        for task in json.loads(output):
            single = run("--perspective", task["perspective"], "--scenario", task["scenario"])
            self.assertEqual(single, json.dumps(task, indent=2, sort_keys=True) + "\n")

    def test_cli_invalid_selection_and_missing_file(self):
        for args in ([], ["--all", "--scenario", "base"], ["--perspective", "unknown", "--scenario", "base"], ["--all", "--case", str(ROOT / "missing.json")]):
            result = subprocess.run([sys.executable, "-m", "parallax", *args], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("error:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
