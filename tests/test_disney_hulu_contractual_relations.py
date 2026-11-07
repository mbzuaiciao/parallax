"""Illustrative synthetic values only: none are SEC financial claims."""

from copy import deepcopy
from decimal import Decimal as D
import hashlib
import unittest

from experiments.disney_hulu_contractual_relations import (
    APPRAISAL_TOP_UP, EVIDENCE_PATH, INITIAL_PAYMENT, SOURCES,
    appraisal_top_up, initial_payment,
)


def synthetic(record, **operands):
    scenario = deepcopy(record)
    scenario["operands"].update(operands)
    return scenario


class ContractualRelationshipsTests(unittest.TestCase):
    def test_smaller_offset_increases_initial_payment(self):
        for offset, expected in ((D(20), D(80)), (D(5), D(95)), (D(0), D(100))):
            with self.subTest(offset=offset):
                self.assertEqual(initial_payment(synthetic(
                    INITIAL_PAYMENT, guaranteed_purchase_price=D(100),
                    unpaid_contributions_at_payment=offset,
                )), expected)

    def test_floor_gives_zero_top_up_only_and_above_floor_is_incremental(self):
        # Coherent synthetic gross = 25% of 400 = 100; net initial = 80.
        initial = initial_payment(synthetic(
            INITIAL_PAYMENT, guaranteed_purchase_price=D(100),
            unpaid_contributions_at_payment=D(20),
        ))
        for value, expected_top_up in ((D(300), D(0)), (D(400), D(0)), (D(440), D(10))):
            with self.subTest(value=value):
                top_up = appraisal_top_up(synthetic(
                    APPRAISAL_TOP_UP, ownership_fraction=D("0.25"),
                    equity_fair_value=value, guaranteed_floor=D(400), finally_determined=True,
                ))
                self.assertEqual(top_up, expected_top_up)
                # Only these two purchase components; excludes tax sharing.
                self.assertEqual(initial + top_up, D(80) + expected_top_up)
                self.assertGreater(initial + top_up, 0)

    def test_initial_payment_does_not_wait_for_appraisal(self):
        initial = synthetic(INITIAL_PAYMENT, guaranteed_purchase_price=D(100),
                            unpaid_contributions_at_payment=D(20))
        for final in (None, False, True):
            with self.subTest(final=final):
                appraisal = synthetic(
                    APPRAISAL_TOP_UP, ownership_fraction=D("0.25"),
                    equity_fair_value=D(440), guaranteed_floor=D(400),
                    finally_determined=final,
                )
                expected = D(10) if final is True else None
                self.assertEqual(appraisal_top_up(appraisal), expected)
                self.assertEqual(initial_payment(initial), D(80))
        self.assertNotIn("finally_determined", INITIAL_PAYMENT["operands"])

    def test_each_missing_operand_produces_unknown(self):
        cases = (
            (INITIAL_PAYMENT, initial_payment, dict(guaranteed_purchase_price=D(100),
                                                   unpaid_contributions_at_payment=D(20))),
            (APPRAISAL_TOP_UP, appraisal_top_up, dict(ownership_fraction=D("0.25"),
                equity_fair_value=D(440), guaranteed_floor=D(400), finally_determined=True)),
        )
        for record, evaluate, values in cases:
            for name in values:
                with self.subTest(operand=name):
                    self.assertIsNone(evaluate(synthetic(record, **{**values, name: None})))
        self.assertIsNone(initial_payment())
        self.assertIsNone(appraisal_top_up())

    def test_nonfinal_appraisal_cannot_fix_top_up(self):
        for final in (None, False):
            for value in (D(300), D(400), D(440)):
                with self.subTest(final=final, value=value):
                    self.assertIsNone(appraisal_top_up(synthetic(
                        APPRAISAL_TOP_UP, ownership_fraction=D("0.25"),
                        equity_fair_value=value, guaranteed_floor=D(400), finally_determined=final,
                    )))

    def test_exact_verified_packet_and_references_are_preserved(self):
        self.assertEqual(hashlib.sha256(EVIDENCE_PATH.read_bytes()).hexdigest(),
                         "257d156976133d160bfd9c20cbef56db9af14b5713faf9b97337ce500bd262e5")
        self.assertEqual(len(SOURCES), 7)
        self.assertEqual(SOURCES["E4"]["source"],
            "https://www.sec.gov/Archives/edgar/data/1744489/000174448923000206/dis-20231101.htm")
        self.assertEqual(SOURCES["E4"]["locator"], "Item 8.01, paragraphs 2–3 (initial payment)")
        for record in (INITIAL_PAYMENT, APPRAISAL_TOP_UP):
            for reference in record["source_ids"]:
                self.assertIn(reference.split(".")[0], SOURCES)


if __name__ == "__main__":
    unittest.main()
