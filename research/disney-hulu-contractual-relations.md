# Disney/Hulu: two deterministic contractual relationships

November 5, 2026. Implements [Issue #5](https://github.com/mbzuaiciao/parallax/issues/5). Six offline tests pass for two hand-authored relationships. This demonstrates their arithmetic and unknown propagation under supplied scenarios; it does not test or establish improved LLM accuracy.

Read the seven verified excerpts, [original claim-level audit](disney-hulu-baseten-economic-claims-audit.md), [explicit-uncertainty audit](disney-hulu-explicit-uncertainty-audit.md), and pilot report before implementation. No applicable `AGENTS.md` was found in the repository or checked ancestors. The separate feature branch starts at `a6504c13d4acdeba941d36eb15371d1feda19060`, the committed research head of archival draft PR #4. The new draft PR targets that archival branch to isolate this experiment's diff; it depends on that research becoming available on main. PR #4 and preexisting local edits are untouched.

## Representation and evidence

[Implementation](../experiments/disney_hulu_contractual_relations.py) contains two dictionaries with source IDs, conditions, operands, formulas and qualifications, plus two specific evaluators. `SOURCES` resolves E1–E7 to the unchanged packet's exact SEC URL, original filing locator and verbatim text. Paragraph/sentence suffixes use the completed audits' local excerpt convention. `None` explicitly means unknown, not zero or absence of an obligation. Dollar arithmetic uses standard-library `Decimal`; no model or network call is involved.

| Relationship | Evidence and qualifications | Computation |
| --- | --- | --- |
| Initial payment after the disclosed November 1 exercise | E3.p1; E4.p1–2, [November 1 8-K, Item 8.01, filing paragraphs 1–3](https://www.sec.gov/Archives/edgar/data/1744489/000174448923000206/dis-20231101.htm); E6.p4, [2023 10-K, Note 2, Hulu LLC, printed p. 99](https://www.sec.gov/Archives/edgar/data/1744489/000174448923000216/dis-20230930.htm). Due on/before December 1, 2023, also described as within 30 days of exercise. Offset only the outstanding NBCU capital-call contributions payable to Disney remaining unpaid on the payment date. | Guaranteed purchase price minus that unpaid offset. Appraisal completion is not an input or prerequisite. |
| Additional appraisal top-up | E5.s1–2, same November 1 8-K, filing paragraph 4; E6.p5. Final equity value above the guaranteed floor triggers the incremental payment within 45 days of final determination. E2.p1–3, [September 8 8-K, Item 8.01, filing paragraphs 3–5](https://www.sec.gov/Archives/edgar/data/1744489/000119312523231673/d541232d8k.htm), preserves the September 30 measurement date for November exercise and agreed appraisal procedure/assumptions. | Operative NBCU ownership fraction times the excess of final equity fair value over floor; zero top-up at/below floor. This reconciles E5's appraised share less guaranteed purchase price with E6's share of the difference, using the same operative ownership basis. |

The records retain the appraisal qualifications rather than computing an appraisal: disagreement leads to party-appointed banks; determinations not within 10% lead to a third bank and averaging the closest two. Valuation includes audited historical results, going concern and continued availability of Disney-provided assets, contract rights and IP on terms consistent with past practice. Expected determination sometime in 2024 (E6.p4) is not an assured completion date.

Only the contractual whole-Hulu equity floor of $27.5 billion is populated from the evidence. Exact gross purchase price, payment-date unpaid balance, operative ownership fraction, final valuation and completion status remain unknown. The rounded 33% is subject to dilution (E1.p1/E3.p1); approximate gross/net/offset reports are not converted into exact operands or reverse-engineered into an ownership fraction. The test pins the original packet SHA-256, `257d156976133d160bfd9c20cbef56db9af14b5713faf9b97337ce500bd262e5`.

## Synthetic results — not SEC claims

All numbers below are illustrative substitutions, in consistent USD units. For the top-up scenarios the hypothetical floor is 400, ownership fraction 0.25 and gross purchase price 100. These are not estimates of Hulu values.

| Scenario | Initial payment | Appraisal top-up |
| --- | ---: | ---: |
| Gross 100, unpaid offset 20 | 80 | Unknown without final appraisal inputs |
| Same gross, smaller offset 5 | 95 | Unknown without final appraisal inputs |
| Same gross, zero unpaid offset | 100 | Unknown without final appraisal inputs |
| Offset 20; final equity value 300, below hypothetical floor 400 | 80 | 0 |
| Offset 20; final equity value 400, equal to floor | 80 | 0 |
| Offset 20; final equity value 440, above floor | 80 | 10 |

For the last three rows, the sum of these two purchase-payment components is respectively 80, 80 and 90; zero top-up does not mean zero purchase consideration. Tax sharing is excluded, so these are not all-in transaction costs. The offset is not deducted a second time from the top-up.

Tests also remove each operand in turn, returning unknown rather than invented amounts. Pending appraisal remains unknown even if a hypothetical valuation is supplied below/equal/above floor. Initial payment stays 80 across unknown, pending and final appraisal status. The functions assume consistent nonnegative monetary inputs and a valid fractional ownership basis; they do not validate contracts or resolve inconsistent scenarios. Missing operands conservatively yield unknown even where additional symbolic reasoning could establish a result.

Run from repository root: `python3 -m unittest discover -s tests -p test_disney_hulu_contractual_relations.py -v` (6 tests passed).

## Connection to the observed errors and limits

- Historical P19's categorical gross/net heading is bounded by the zero-offset test; P20's smaller-offset implication is preserved. Explicit-uncertainty U20 omitted that useful implication. Holding gross fixed, smaller unpaid contributions increase this initial payment; this says nothing about aggregate economic cost because contributions may also have been received.
- U25 incorrectly made both initial payment and top-up contingent on appraisal. Separate evaluators and appraisal-status tests prevent that coupling in this implementation. U09/U10's distinction between incremental top-up and total consideration is retained explicitly.
- B21 and U04/U30 show how conditional rounded estimates can become fixed amounts. Unknown exact operands prevent that conversion here. B17/P29/U31's appraisal timing/estimation overstatements are avoided by preserving the expectation and leaving actual final status unknown; hypothetical calculations do not assert earlier estimation was impossible.
- P28/P32/P35/P38/P40 and U05/U31 involve valuation, accounting, liquidity or classification claims beyond these formulas. This experiment makes none of those determinations. It does not identify exact legal obligors, parent recourse, recognized debt, funding, creditor priority, shareholder-value changes or cash-flow classification. E7's dated $9.1 billion carrying amount is not a payment operand. E5.s3/E7.p1's separate tax-sharing arrangement is outside scope.

This is a manual, single-case contractual transcription against curated evidence as of November 21, 2023, not independent legal adjudication, automatic extraction, a valuation model or an LLM intervention. It cannot establish that a payment occurred, resolve missing dilution terms or produce actual final amounts. Evidence, earlier results and audits remain unchanged. Stop rule met: exactly two relationships represented, tested and documented; no additional financial rules or model calls.
