# Three-case pilot: first expansion

**Outcome:** Four new calls were attempted; all four completed with finish reason
`stop` (Meta equity/creditor; CoreWeave equity/creditor). No retries or corrections
were submitted. The existing NVIDIA calls were not rerun or modified.

Original new runs:
[Meta](benchmark-meta-capacity-live.json), [CoreWeave](benchmark-coreweave-deposit-live.json).
Recorded assessment drafts:
[Meta](../assessments/meta-capacity.json), [CoreWeave](../assessments/coreweave-deposit.json).
[Reproducible comparison](benchmark-comparison.md) includes protocol/hash checks,
field-level rationales, recognized identifiers and explicit unscorable quantities.

## Findings — assistant draft, not human-adjudicated accuracy

| Mechanism | Source-based result | Main concerns |
| --- | --- | --- |
| Meta contingent capacity purchase | Both preserve the up-to amount, five-year horizon, third-party-sales reduction and unnamed provider. They distinguish the contingent arrangement from neighboring aggregate commitments; neither assumes a yearly payment allocation or imports Nebius's identity. | Equity blurs direct versus unconditional/currently due obligations, gives little weight to the capacity received, and too broadly excludes economic third-party support just because the arrangement is not a debt guarantee. Its pre-payment characterization of resale reduction is an interpretation rather than a disclosed settlement sequence. |
| CoreWeave deposit financing | Both preserve original deposit versus dated debt carrying values, premium/rate, partial settlement and termination/extension rights. They retain uncertainty about maturity/current-classification differences and do not infer priority from recourse presentation. | Both mix accounting presentation with contractual promises. Equity claims termination increases cash outflow relative to holding to term without a supporting counterfactual schedule. Creditor suggests settlement could improve other-creditor availability without explaining the cash-use countereffect; it is hedged but incomplete. |

Amounts and meanings were checked against the selected
[Meta Note 9](https://www.sec.gov/Archives/edgar/data/1326801/000162828026050705/meta-20260630.htm),
[CoreWeave annual Note 10](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm),
and [quarterly Note 10](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm).
No discrepancy was found in the explicitly reproduced amounts, units and dates.
No leverage, expected loss, valuation adjustment or creditor recovery ground truth
was constructed. Missing inputs make those quantities **unscorable**, not zero.

Citations use the supplied source IDs and recognizable Note 9/Note 10 subsections.
The assistant checked those locations manually; the program only checks the
catalog IDs entered in assessments. This is not automated citation validation.

Both cases change investor priorities without changing the principal disclosed
facts. The same conclusions about unknown ranking and unquantifiable expected
loss can reasonably appear for both investors. Neither legal claim priority nor
issuer solvency follows from these selected notes.

## Comparison with Wagner and experimental limits

Wagner's Meta `HL-0047` / shared `HL-0034b` codes an economic demand backstop;
the model correctly identifies a contingent own purchase but equity's categorical
rejection of support is too narrow economically. The annotation's Nebius identity
and U4 classification are researcher interpretations using additional context, not
secret factual answers the selected Meta paragraph establishes. CoreWeave
`HL-0041a` records debt carrying value; both model answers recognize that mechanism
and distinguish it from an unrecognized guarantee. Counterparty role labels and
dataset `n/a` cells do not prove undisclosed legal identities or collateral status.

This is a nonrandom, three-arrangement pilot with curated paraphrases, explicit
prompt cautions and one new response per investor/case. Source selection and semantic
assessment were drafted by the same assistant; no independent human rater has
adjudicated them. No accuracy percentage or causal investor-conditioning estimate
is justified. Full method, source selection and CC BY 4.0 attribution are in the
[benchmark documentation](../docs/benchmark.md). Original evidence/results/UI and
dependency versions are preserved.

**Suggested next experiment, not implemented:** preregister repeated samples of
these same investor prompts and have an independent, blinded human rater assess
them, to separate sampling variation from investor-conditioning effects.
