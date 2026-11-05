# Disney/Hulu Baseten A/B experiment

November 5, 2026. **The authorized low-reasoning follow-up produced two complete, usable answers.** Parallax improves organization and coverage but introduces unsupported economic conclusions; this pair does not establish a correctness advantage.

## Evidence and method

Branch: `experiment/disney-hulu-baseten-ab`, based on `a28f993b87c7a041e12cab3c57423ebd1239ca98`. No applicable `AGENTS.md` was found in the repository, nested directories or checked ancestors on either inspection.

The unchanged [evidence JSON](disney-hulu-baseten-evidence.json) contains seven verified excerpts from [September 8 Form 8-K, Item 8.01](https://www.sec.gov/Archives/edgar/data/1744489/000119312523231673/d541232d8k.htm), [November 1 Form 8-K, Item 8.01](https://www.sec.gov/Archives/edgar/data/1744489/000174448923000206/dis-20231101.htm), and [November 21 fiscal 2023 Form 10-K, Note 2, Hulu LLC, pp. 99–100](https://www.sec.gov/Archives/edgar/data/1744489/000174448923000216/dis-20230930.htm). Each paragraph was checked against direct SEC downloads after whitespace normalization; the JSON records URLs, filing locators, accessions and download hashes. Information cutoff remains November 21, 2023. September 30 measurements remain dated balances. Research interpretations and reference answers were excluded from model inputs.

Both attempts used `meta-models/muse-spark-open-1026`, identical seven-excerpt user messages, unchanged baseline/Parallax system prompts, and the same provisional qualitative evaluation dimensions. No explicit temperature or seed is set. The only runner changes were `reasoning_effort="low"` and `max_completion_tokens=8192` for the follow-up.

## Initial attempt: completion-budget failure

[Original raw results](../results/disney-hulu-baseten-ab-20261105.json) remain unchanged. The initial invocation used 4,096 completion tokens and no explicit reasoning effort.

| Condition | Finish reason | Completion tokens | Reasoning tokens | Visible answer |
| --- | --- | --- | --- | --- |
| Baseline | `length` | 4,096 | 4,093 | Null |
| Parallax | `length` | 4,096 | 3,002 | 4,255 characters, truncated mid-sentence |

These outcomes are consistent with reasoning consuming the shared completion budget: approximately 99.9% for baseline and 73.3% for Parallax. Both exhausted the limit. This supports a budget diagnosis, not proof that reasoning effort alone caused the failures. There was no valid pair to compare. The original runner checks nonempty content but does not reject `length`, so its successful exit was insufficient validation.

## Authorized follow-up: complete pair

Executed with `uv run --env-file .env python /tmp/parallax_disney_guarded_run.py`. This temporary local wrapper called the existing runner's `load_excerpts` and `run_call` functions once per condition, checkpointed each raw response, and would stop before another request if an answer were empty or did not end with `stop`. It changed no request fields. The ignored local `.env` supplied the API key without printing it.

[New raw requests and responses](../results/disney-hulu-baseten-ab-20261105-low-8192.json):

| Condition | Finish reason | Prompt tokens | Completion tokens | Reasoning tokens | Visible characters |
| --- | --- | --- | --- | --- | --- |
| Baseline | `stop` | 2,157 | 2,163 | 532 | 7,078 |
| Parallax | `stop` | 2,208 | 2,785 | 385 | 10,380 |

Both answers reach their conclusions and cover the requested topics. Saved requests confirm that only the two authorized inference fields changed from each prior request; evidence, model and prompts are identical. Exactly two new API requests were made, with no retries.

## Qualitative financial-reasoning comparison

A subsequent [claim-by-claim economic error audit for Issue #2](disney-hulu-baseten-economic-claims-audit.md) records exact model excerpts, evidence locators and adjudications. It separates supported payment mechanics from unsupported stakeholder extrapolations and treats proposed prompt effects as hypotheses, not demonstrated causes. Its detailed classifications refine the preliminary observations below.

Unblinded assistant evaluation against the excerpts; no numerical scores or independent adjudication.

| Dimension | Baseline | Parallax |
| --- | --- | --- |
| Factual correctness | Correct floor, gross/net estimates, offset condition, payment deadlines, tax sharing, dated $9.1bn carrying amount and earnings attribution. Later says appraisal “completes in 2024,” strengthening a disclosed expectation into certainty. | Preserves the same principal facts and explicitly distinguishes valuation date, payment date and expected appraisal timing. Both compress the appraisal averaging rule in a way that could more clearly retain its third-appraiser condition. |
| Obligation classification | Separates purchase payment, contingent top-up and tax sharing; identifies redeemable noncontrolling interest, without expressly explaining why it is not borrowing. | More explicit contractual obligation map and warning against classifying the commitment as recognized debt. However, the obligor row groups parent and subsidiaries together; E1/E3 identify subsidiary participants and do not establish direct parent recourse for every component. |
| Unsupported claims | Generally cautious, but calls the conditional net estimate a material obligation of approximately $8.61bn in its creditor section. Its closing claim that any funding-risk analysis must await appraisal is too broad: initial liquidity exposure can already be discussed conditionally. | Says an additional cash outflow “further reduces equity value,” without accounting for acquired ownership economics, funding or future cash flows. This does not follow from cash expenditure alone. It also calls tax sharing a reduction in “operating cash flow” without evidence of cash-flow classification, and asserts an accounting-entry-before-payment possibility not established by the excerpts. “Separate line from debt” is not directly shown in the supplied excerpts, although E7 names the balance-sheet classification. |
| Stakeholder analysis | Correctly avoids inventing funding, ranking or recoveries, but says no creditor consequence can be drawn, omitting useful conditional liquidity analysis. Equity treatment focuses on accounting rather than ownership benefits. | Explains competition for liquidity and avoids assuming pari passu ranking or new debt. More useful coverage, but overstates equity-value harm and does not establish whether the transaction creates or destroys value. Its mandatory net-payment language also loses some capital-call conditionality. |
| Double-counting | Does not add the valuation floor, consideration and carrying amount as separate exposures; no inflated aggregate is reported. | Explicitly separates whole-Hulu floor, NBCU share, offset and incremental top-up, and distinguishes carrying amount from debt. No duplicated numerical exposure total. The phrase “total enterprise equity value” is imprecise: the filing specifies equity fair value. |

Both retain uncertainty about final appraisal, tax-sharing dollars, funding and creditor terms. Parallax's heading “Initial Payment is NOT $9.17B gross” is too categorical: the net amount can approach the gross amount if capital calls are paid before settlement, as its next sentence acknowledges. Neither answer supplies a justified contractual maximum or expected-loss estimate.

## Limitations and stopping boundary

One case and one answer per condition, fixed baseline-first order, different instruction lengths, selected excerpts, and unblinded evaluation cannot establish general performance or error rates. Both reasoning effort and token limit changed, so their separate causal effects cannot be identified. Provider-reported token counts are observations, not access to internal reasoning. The complete contract and creditor instruments remain unavailable; omissions do not establish absent legal rights. No later transaction outcome or current-status claim is used.

Stopped after the two complete follow-up responses and this evaluation. No further requests, token increases, prompt changes, frontend, infrastructure, fine-tuning or unrelated edits. At completion of the inference stage, no commit, push or merge had been performed. The later Issue #2 documentation audit is linked above. The API key was checked for absence from generated artifacts.

Integrity: evidence SHA-256 `257d156976133d160bfd9c20cbef56db9af14b5713faf9b97337ce500bd262e5`; original results `4e7817ca1896d532b24a4263cf541e3f04aa62f8996b10b936103ab5a45d8629`; follow-up results `81f5d6e9c9808a4ecf69ec0014f3f05f43d2eb41c3166c592a47e96c517e619c`.
