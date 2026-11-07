# Muse Spark reasoning-skill replication results

On November 7, 2026, Parallax sent all 12 frozen requests once, in order, to Meta's proprietary Model API at commit `c920458`. All returned HTTP 200, model `muse-spark-1.3`, a nonempty assistant answer, usage, and finish reason `stop`. No retries, redirects, errors, truncated completions, substitutions, or extra inference requests occurred. The runner verified the grid digest, endpoint, prior smoke result, and credential presence in the ignored and untracked `.env`. It proceeded without checking account quota. The preflight estimate was USD 0.432792 with 12,000 uncached input tokens and all 98,304 possible completion tokens, within the USD 1 authorization. [Preflight](preflight.json) · [Frozen plan](plan.json) · [Exact request bodies and raw responses](./) · [Timestamped status log](status.jsonl)

The client spent 460.314 seconds in the 12 requests. Meta reported 7,667 input tokens, zero cached, and 52,511 completion tokens, including 34,503 reasoning tokens. This implies **USD 0.2327555** at standard list rates. Actual charges and available quota remain unverified. [Archive verification and usage](verification.json) · [Meta pricing](https://dev.meta.ai/docs/pricing-rate-limits)

## Preliminary scoring

The same assistant administered the run and scored the visible text in shuffled, case-labeled packets with opaque IDs. The assessment and packet were hashed before opening the arm map. Wording can suggest condition assignment. The original references and rubric were used, and no independent adjudication was initiated. [Masked packet](masked-review.json) · [Claim-level scoring](masked-assessment.md) · [Pre-reveal hashes](masked-assessment.sha256) · [Arm map](reveal-map.json) · [Frozen rubric](../../skill-principle-pilot/protocol.md#preregistered-scoring-checklist)

Every answer covered all three factual items and the primary creditor mechanism. No scored omissions were found. Across arms, Sempra's scheduled and reported cash and Sanofi's triggered tender cash remained explicit, although some statements weakened supported conclusions elsewhere in the same answers.

| Case | Arm | Unsupported | Contradicted | F items covered | Creditor usefulness | Excessive qualifications |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| Boeing | A | 2 | 0 | 3/3 | Covered | 0 |
| Boeing | B | 0 | 0 | 3/3 | Covered | 0 |
| Boeing | C | 0 | 0 | 3/3 | Covered | 0 |
| Starbucks | A | 5 | 0 | 3/3 | Covered | 0 |
| Starbucks | B | 3 | 1 | 3/3 | Covered | 1 |
| Starbucks | C | 4 | 0 | 3/3 | Covered | 0 |
| Sempra | A | 0 | 0 | 3/3 | Covered | 3 |
| Sempra | B | 2 | 1 | 3/3 | Covered | 1 |
| Sempra | C | 0 | 0 | 3/3 | Covered | 1 |
| Sanofi | A | 0 | 0 | 3/3 | Covered | 1 |
| Sanofi | B | 0 | 0 | 3/3 | Covered | 0 |
| Sanofi | C | 0 | 0 | 3/3 | Covered | 0 |

## Within-Muse comparisons

Factual coverage, creditor usefulness, and omissions tied throughout. The table lists changes in the other scored dimensions.

| Case | B versus A | C versus B | C versus A |
| --- | --- | --- | --- |
| Boeing | Two fewer unsupported propositions. | Tied. | Two fewer unsupported propositions. |
| Starbucks | Two fewer unsupported propositions, one more contradiction, and one more excessive qualification. | One more unsupported proposition, one fewer contradiction, and one fewer excessive qualification. | One fewer unsupported proposition. |
| Sempra | Two more unsupported propositions and one more contradiction, with two fewer excessive qualifications. | Two fewer unsupported propositions and one fewer contradiction. | Two fewer excessive qualifications. |
| Sanofi | One fewer excessive qualification. | Tied. | One fewer excessive qualification. |

C improved on A in at least one scored dimension in each case without a scored regression. C improved on B in Sempra and reduced contradictions and excessive caution in Starbucks. It also added an unsupported proposition in Starbucks compared with B. The result is **mixed and misses the preregistered favorable criterion**, which required no case-level regression against either comparator.

## Comparison with Beam

Both runs missed the favorable criterion, with different regressions. Beam C reduced unsupported claims versus A on Boeing, Starbucks, and Sempra. It added caution on Sempra and lost factual coverage and added unsupported claims on Sanofi, with the Sanofi findings corroborated in the separate AI re-adjudication. Muse C reduced unsupported claims versus A on Boeing and Starbucks and reduced excessive caution on Sempra and Sanofi. All three Muse Sanofi answers preserved the one-CVR-per-eligible-share entitlement, and none had a scored unsupported proposition there. Muse's C-versus-B regression was on Starbucks, where it added an unsupported claim while removing a contradiction and an excessive qualification. Beam C and B tied on the Starbucks scoring dimensions. Creditor usefulness was covered throughout both runs. [Beam results](../../beam-ollama-issue-9/scientific-attempt-01/report.md) · [Independent Sanofi AI review](../../sanofi-re-adjudication-issue-11/report.md)

The exact messages and order match, but serving configurations differ. Beam ran through Ollama Cloud with provider defaults and no explicit completion cap. Muse ran through Meta's first-party API with provider defaults and an 8,192-token cap that includes reasoning. Neither reported model ID identifies an immutable serving revision. Token counts are provider-specific. One sample per cell leaves decoding variability unresolved, and the extra prompt length and overlap with the baseline limit attribution to the examples. Public filing exposure during training is unknown. Both original reviews were preliminary, administered and scored by the same assistant within each run. The separate second AI rating covers Beam Sanofi only. The observed case patterns cannot separate model effects from serving settings, sampling, or evaluator judgments.

The experiment stopped after the single authorized grid.
