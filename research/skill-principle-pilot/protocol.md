# Failure-derived credit reasoning pilot

Prepared November 7, 2026 for draft PR #7. This is a four-case exploratory comparison of a human-designed prompt intervention. The exact text and schedule are in [design.json](design.json), with [evidence packets](cases/) and [scoring references](references.md) frozen separately. A human should review the principle, examples and references before authorizing execution.

## Motivation and intervention

The Disney/Hulu audits found overstatements about accounting and legal entities alongside omitted cash-resource implications. In the explicit-uncertainty comparison, unsupported claim groups fell from seven to five while supported groups fell from 26 to 21. This motivates measuring both unsupported assertions and suppression. The historical counts describe individual semantic groups of varying importance. [Disney/Hulu draft PR #4](https://github.com/mbzuaiciao/parallax/pull/4)

- **A** uses the historical Baseten pilot's Parallax system instructions, with the dual equity/creditor comparison sentence removed so the common question sets the senior-unsecured-only scope. The remaining wording is identical. The earlier generic Disney/Hulu control is a separate prompt.
- **B** appends the exact frozen principle to A.
- **C** appends the same principle and then one positive and one boundary example. Both are fictional, with no issuer, dates, amounts or held-out answers.

The existing instruction already maps obligor, beneficiary, trigger, amount, timing, recourse and unknowns. It separates fact from inference and forbids assuming contractual commitments are recognized debt or double-counting amounts. The additional principle explicitly distinguishes dated carrying values from exposure, amounts due and actual cash paid, and asks the model to preserve supported conclusions. The contrast measures the incremental effect of making that guidance explicit. C versus B evaluates the examples as a bundle, including added prompt length. The two examples' individual effects cannot be identified.

## Execution

Four arrangements and three arms produce exactly 12 planned POST requests with one response per cell. The schedule is fixed and varies arm order across cases to reduce confounding by position. Cases and arms use separate requests with no conversation state, tools or retrieval. Model-facing content consists of the system prompt, the case question and the source-located evidence. Reference propositions, applicability labels, scoring rules and arm labels are excluded. Source URLs are provided for provenance. Judge against supplied text even when a fact is available elsewhere.

Every arm uses the same wording, focal entity, perspective, historical date, evidence and three-section format within a case. All calls use Baseten Chat Completions with model `meta-models/muse-spark-open-1026`, `reasoning_effort=low`, `max_completion_tokens=8192` and a 120-second client socket timeout. Other request options are omitted uniformly, including sampling parameters, seed, streaming and tools. Provider defaults and serving revision may vary outside the experiment's control. The historical client supplies the endpoint, model, Parallax instructions and evidence loader. The new runner handles transport and persistence to capture failures without changing the historical client.

From the repository root:

```sh
python3 research/skill-principle-pilot/run.py --offline > /tmp/parallax-pilot-requests.json
```

After human review, billing confirmation and explicit Prompt 2 approval, export the existing credential through the usual secure mechanism and run:

```sh
python3 research/skill-principle-pilot/run.py --execute-approved /tmp/parallax-pilot-attempt-01
```

Use a fresh attempt directory outside tracked files. The freeze manifest verifies the inputs, references, protocol, runner and historical prompt dependency. Preserve its digest and the git commit with the run. The runner writes the whole plan, each exact POST body before its call, provider response bodies as received, and a JSONL event log with UTC timestamps, requested and reported model IDs, finish reason and usage when available. Authentication headers are excluded. The directory is created exclusively with owner-only access. The runner sends one request at a time, disables redirects and makes no automatic retries. A provider error, transport failure, interruption, malformed or empty output, missing usage/model metadata, a change in the reported model ID between calls or a non-`stop` finish stops the attempt. Record unattempted cells and any interrupted cell with unknown provider-side status. Preserve partial artifacts. Further attempts or replacement samples require new approval. A complete comparison requires all 12 valid responses.

## Preregistered scoring checklist

Before reading outputs, a coordinator should prepare twelve case-labeled copies of visible answer text using shuffled opaque response IDs and retain the arm map separately. Preserve all answer text and citations. Omit request bodies, arm labels, provider metadata and reasoning traces from the review packet. Give reviewers the evidence and references. Use a human reviewer independent of prompt drafting when available. Save judgments before revealing the arm map. If independent review is unavailable, label the judgments preliminary and record the evaluator's role. Style and content may still suggest the prompt assignment.

For each completed answer, record the following with answer quotes and evidence IDs.

| Dimension | Rule |
| --- | --- |
| Unsupported claims | Split material assertions into distinct semantic propositions. Classify each as supported, justified conditional inference, unsupported, or contradicted. Count unsupported and contradicted separately, deduplicating repeated assertions. Note missing or wrong citations separately when the claim is substantively supported. |
| Evidence coverage | Mark each case-specific F1–F3 as covered, missing/partial, or misstated. Coverage requires the material qualifications and a relevant excerpt citation. Report covered out of three and identify missing or misstated items. |
| Economic usefulness | Mark U as covered, partial, or missing. Coverage requires at least the case-specific primary cash mechanism and its relevance to the named senior unsecured creditor with evidence and appropriate limits. Generic cautions receive no credit. Reasonable additional conditional implications may be recorded separately. |
| Suppression | Flag explicit withholding or unjustified qualification of a supported conclusion. Check for omitted or suppressed scheduled/triggered cash in case 03 F1 and case 04 F1, reported payment in 03 F3, and case-specific U in all four. Track omissions separately from explicit suppression. |

Report each arm within each case, with paired C–B, C–A and B–A comparisons for all dimensions. The preregistered hypothesis is that C improves applicability relative to both A and B. Describe a favorable pattern only if C shows at least one case-level improvement against each comparator in unsupported/contradicted claims or suppression, with no case-level regression against that comparator in unsupported/contradicted claims, F-item coverage, U, or suppression. Report mixed, adverse and null patterns explicitly. No combined score, hypothesis test, or claim of broad generalization. One response per cell leaves decoding variability unresolved. Previously unused here means unused in the tracked project evidence inspected.

## Account and cost readiness

On November 7, an authenticated, non-inference GET to `https://inference.baseten.co/v1/models` returned HTTP 200 and listed the exact historical ID as well as the public ID. The latter is the identifier in the public library. The account catalog does not establish that a completion will succeed or that exact-alias pricing matches the public model family. No completion was sent. [Baseten model library](https://www.baseten.co/library/muse-spark-open/)

The authenticated management GET to `/v1/billing/usage_summary` returned HTTP 403. The user reports approximately USD 100 in credit expiring November 9, 2026. Available balance, expiration and credit applicability remain to be confirmed in the workspace billing view. [Usage API](https://www.baseten.co/resources/changelog/retrieve-billing-usage-via-api), [Billing dashboard](https://www.baseten.co/resources/changelog/model-usage-dashboard-and-invoice-history/)

Budget estimate assumes uncached family pricing of USD 1.25 per million input tokens and USD 4.25 per million output tokens. The twelve requests contain about 32,000 message characters. A rough tokenizer allowance gives 6,000–12,000 input tokens across the grid. The historical complete Disney/Hulu calls used 2,163 and 2,785 completion tokens. A planning range of 1,500–3,000 per call gives 18,000–36,000 completion tokens total and about **USD 0.08–0.17**. At 98,304 completion tokens (12 × 8,192) and 12,000 input tokens the estimate is about **USD 0.43** at those rates. These are estimates, subject to tokenizer, reasoning-token billing, alias-specific terms and account credits. [Baseten public pricing](https://www.baseten.co/pricing/)
