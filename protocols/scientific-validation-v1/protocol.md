# Parallax scientific validation pilot — review protocol v1

Prepared October 29, 2026. **Design only; no responses collected.** This is a new
protocol, not a revision of `guidance-ablation-v1`. Stop after offline validation
and delivery for independent review. No paid calls, live experiments, commits or
pushes are authorized in this phase.
Minimal review corrections: October 29, 2026, addressing
`research/scientific-validation-v1-review.md`; the 5 × 2 × 3 design is unchanged.

## Question and hypothesis

Does existing Parallax analytical guidance improve the correctness and evidential
discipline of financial interpretations of supplied corporate disclosures compared
with neutral instructions? We hypothesize fewer material unsupported assertions
and better distinction between contractual exposure and recognized liability.
Null, mixed and adverse effects are valid outcomes. This tests an instruction
intervention on curated evidence, not autonomous discovery or full-filing extraction.

## Five cases and provenance

| Case | Selection rationale | Evidence and cutoff |
| --- | --- | --- |
| NVIDIA PORTS | Contingent guaranties; cap versus carrying amount | Existing pack, August 26, 2026 |
| Meta cloud capacity | Contingent own purchase with third-party sales offsets | Existing pack, July 30, 2026 |
| CoreWeave MagAI deposit | Recognized financing comparison; dated balances | Existing pack, August 12, 2026 |
| Apple manufacturing purchases | Purchase obligations with near-term concentration | New selected 10-K context, October 31, 2025 |
| Microsoft operating leases | Recognized lease liability versus undiscounted payments | New selected 10-K context, July 30, 2025 |

`references.json` contains five separate review records: source-linked factual
assertions, contractual obligations, accounting status, conditional stakeholder
interpretations, and unsupported conclusions. New evidence is in `apple.json` and
`microsoft.json`; the other three packs are referenced in place, unchanged.
The generated plan catalogs accessions, URLs, locators, filing dates and local
evidence hashes. URLs identify primary filings; local hashes identify supplied
packs, not full archived SEC HTML. Full filings are not sent to the model.

All five records are **provisional**. Primary passages were opened by the preparing
assistant on October 29, 2026; this is source inspection, not independent expert
verification. Existing `verified_facts` labels and the audit reports are not
authoritative ground truth. Do not promote assistant interpretations, Wagner
research codes, or model answers to verified facts. A future independent financial
reviewer must inspect primary passages, record name/date/locator and approve or
dispute each assertion before outcome scoring. A second reviewer checks accounting
and disputed assertions. Apply the adjudication rule below before declaring a
reference target unresolved. Only an unresolved material reference target, not an
ordinary rating disagreement, withholds that case's aggregate result. Retain the five-case roster;
do not substitute a convenient case or silently drop it. Freeze reviewed references
and hashes before any future experiment; revisions require a dated protocol version.
Meta M3 is an inference constraint about adjacent aggregate commitments, not an
affirmative term of the capacity contract. It is retained verbatim in evaluation
guidance, outside core factual targets. Omission of that warning earns no penalty;
misusing those aggregates as the capacity payment schedule remains an error.

Exclude Harbor and Cedar from the 30 responses: they are synthetic settlement
models, not corporate disclosures. Exclude duplicate Meta research rows describing
the same arrangement. Do not revive the earlier unretrievable Oracle candidate or
add cases, investor arms, models, raw-filing conditions or repetitions. Apple and
Microsoft broaden obligation types but are purposive additions, not representative
sampling. Distinct historical dates are intentional; each case uses its own cutoff.

Reviewed design inputs: `docs/benchmark.md`, both historical guidance-ablation
protocols, the three real-world packs and references, `research/independent-audit-antigravity.md`,
`research/post-audit-verification.md`, and `docs/post-audit-corrections.md`.
The post-audit documents resolve display/accession issues; they do not supply
independent ground truth or evidence of a prompt effect. Historical outputs and
assistant assessments cannot serve as any of the new observations or ratings.

## Conditions and controlled settings

Each response assesses **both equity holders and senior unsecured creditors**.
There is no separate investor condition. Five cases × two conditions × three
fresh conversations = **30 planned responses**, 15 per condition.

Guided developer instructions come verbatim from
`parallax.real_world.build_disclosure_request(case, company=...)` with perspective
`None`, including its existing analytical cautions. Neutral uses the existing
`parallax.ablation.NEUTRAL_TEMPLATE`, substituting the combined investor phrase:

> Analyze the supplied financing arrangement from the perspective of (1) an equity
> investor in {company} and (2) a senior unsecured creditor of {company}. Explain
> its economic significance, cite supporting evidence, and identify material uncertainties.

Neutral supplies no substantive analytical procedure, anticipated errors or target
answers. General requests for significance, evidence and uncertainty are held in
the task. Only the developer-message content differs within a case. The same
allowlisted user evidence bytes, requested model `muse-spark-1.3`, endpoint,
temperature **0.7** and maximum completion tokens **8192** apply to every cell.
Other sampling parameters are omitted identically. Documentation-only check on
October 29, 2026: Meta's [model catalog](https://dev.meta.ai/docs/models) lists
`muse-spark-1.3` for Chat Completions. Its [official parameter guide](https://dev.meta.ai/docs/protocols/chat-completions)
documents `POST https://api.meta.ai/v1/chat/completions`, developer/user messages,
temperature 0–2 (so 0.7 is within range), and integer `max_completion_tokens`.
Documented omitted defaults: `top_p=1`, `stream=false`, `n=1`; reasoning effort is
model-set and seed is null. Preserve these omissions across conditions. Meta
recommends temperature 1; retain the planned 0.7 to avoid changing the intervention.
The accessible guide does not establish a model-specific output maximum for 8192;
the [full API reference](https://dev.meta.ai/docs/api-reference/chat-completions)
shows an identity-confirmation gate. Numeric-limit compatibility, account access,
effective reasoning default and immutable backend version remain unverified.
**Not execution-ready:** resolve these through official specifications/account
information before a separately authorized run; no paid preflight was performed.
If incompatible, amend and refreeze before calls, without silently changing settings.
Record requested and returned model versions
separately; if returned version is absent, report that reproducibility limitation.
Stop on detected backend-version changes; do not pool versions.

No tools, browsing, reference records, annotations, ratings, baseline calculations,
historical answers or prior conversation turns enter requests. Existing packs
already contain accounting labels and caveats, so neutral remains conditioned on
curation. Guidance length and content change together; this design cannot identify
which instruction caused an effect.

## Repetitions, retention and masking

The offline preparation script shuffles all 30 cells once using Python
`random.Random(20261029)`. The seed controls order only, not model randomness.
Each cell has a stable `sv1:case:condition:repeat` identifier. Three repeats mean
three separate API requests with no shared history, cached answer reuse, chosen
best answer, or sampling-until-success. Repeats have identical request hashes
within a cell type; their run IDs differ. Independence is procedural, not a claim
about provider internals. A future run must use one frozen settings configuration
and a short continuous execution window, recording UTC timestamps.

Future execution requires separate authorization. Preserve exact request bytes,
protocol/source/code hashes, Python version, Git revision and dirty state, provider
response ID, returned model, raw response/usage, finish reason, timestamps and errors.
The plan supplies null metadata slots, not fabricated model outputs. Use the existing
client and checkpoint conventions if later authorized; no runner is added here.
The old ablation runner and blind-package CLI hardcode three cases and two investor
arms and must not be invoked for this design. `prepare.py` reuses prompt builders,
hash helpers and arithmetic directly, without changing those historical commands.

No retries or replacements: failures, refusals, missing text and truncations count
among the 30 attempted slots. Report completion rates by condition. An empty/error
slot has missing scores, not a perfect hallucination score; score a substantive
refusal for justified versus excessive abstention. Mark truncated answers incomplete,
retain visible assertions for the error log, and exclude them from complete-answer
score summaries. Report best/worst bounds assigning missing ordinal scores 0 and 2
and missing unsupported-assertion indicators 0 and 1. Pause on authentication,
quota or settings drift, preserve remaining pending slots, and report incomplete
design rather than claiming 30 completed responses.

Before future scoring, a controller assigns random unique review IDs and random
presentation order, keeping the ID/condition/run mapping outside the reviewer
package. Give raters only original response text/status, evidence, approved
reference facts and the rubric. Hide prompts, condition and repeat labels, provider
metadata, historical outcomes and this hypothesis section. Do not share stable arm
labels that reveal clusters. Answer style may still reveal guidance. Two independent
human financial reviewers rate separately before discussion; retain both ratings.
For disagreement on facts, materiality or scores, first compare answer excerpts
and primary passages. If discussion does not resolve it, a designated third senior
financial adjudicator, still masked to condition, makes the binding evidence-based
decision before unmasking; retain the original ratings and written rationale.
If the primary evidence itself cannot settle a reference target, the adjudicator
records that target as unresolved/unscorable rather than forcing a factual verdict.
Keep unaffected dimension ratings; withhold aggregates only as specified above. No
reviewers have yet been recruited; the preparing assistant supplies no ratings.

## Fixed rubric (all dimensions 0–2; higher is better)

Material means an error or omission changing the obligor, obligation mechanism,
amount/date, recognition status, cash-flow channel or investor conclusion. Optional
detail, length, formatting and prompt vocabulary earn no points. Use the case's
reference targets to fix coverage, not an expanding list of desired terms.

| Dimension | 2 | 1 | 0 |
| --- | --- | --- | --- |
| Factual correctness | Covers the record's core factual targets with correct entities, amounts, dates and conditions | Core mechanism correct; one material omission or only minor inaccuracies | Any material factual contradiction, or no usable core facts |
| Financial/accounting interpretation | Correctly distinguishes contractual exposure from recognized liabilities, including when carrying liability cannot be established, and explains warranted cash-use/service tradeoffs for both stakeholders | Sound but incomplete recognition distinction or one stakeholder channel missing | Material misclassification, double counting, invented recovery/priority, or no economic analysis |
| Evidence grounding | All material factual claims have semantically supporting primary-filing/note/section citations or equivalent internal document/locator citations | Some material claims unlinked or imprecise but traceable; none falsely attributed | Central claim falsely cited, unsupported by cited passage, or no usable citations |
| Unsupported inference/hallucination | No unsupported material assertion; possible channels clearly conditional | Only minor unsupported detail, without changing conclusion | Any unsupported material assertion or invented input, entity, ranking or quantitative result |
| Uncertainty/abstention | Identifies case-specific missing inputs and limits conclusions while using available facts | Generic caveat, missed important uncertainty, or excessive refusal despite usable evidence | Definite unsupported answer to a material unknown, or no usable treatment of uncertainty |

For NVIDIA, Meta and Apple, saying the supplied evidence cannot establish the
carrying liability satisfies the recognition component for full credit; a numeric
balance is not required. Unknown recognition is not the same as an unrecorded or
zero liability. An unsupported assertion of either earns no credit for that
component and is a material unsupported assertion. CoreWeave and Microsoft should
be assessed against the disclosed recognized amounts, subject to reference approval.
Full dimension credit still requires the stated stakeholder analysis.

For Apple, a qualified explanation that ordinary, unperformed executory purchase
commitments generally do not create a gross payable merely on signing is valid
accounting interpretation and earns recognition-component credit. That principle
does not establish an exact zero balance for all related obligations at period end:
delivered goods, cancellation fees or loss accruals can require separate recognition.
The supplied Item 7 passage does not quantify those balances. Do not penalize the
general principle or require a zero figure. See the [audit reconciliation](../../research/scientific-validation-v1-reconciliation.md)
for the snapshot mismatch and the distinction from issuer-specific measurement.

Conventional citations such as “Microsoft 2025 Form 10-K, Note 13” or “Apple 2025
Form 10-K, Item 7” qualify equally with schema IDs when the passage supports the
claim. Internal benchmark IDs, hyperlinks and prompt-specific citation syntax are
not required. A fabricated document, note or quotation earns no grounding credit
for the associated claim; a material fabrication also affects unsupported inference.
Reviewers must disregard headings, ordering, prose versus bullets and echoes of
guided terminology: score semantic claim content, not presentation style.

Scores are semantic judgments with an answer excerpt, reviewer-recorded source locator and
rationale for each dimension. Factual contradiction differs from omission; log
both. A material assertion contradicted by a source affects factual correctness;
an assertion exceeding evidence affects unsupported inference even if it might
be true. Apply both where appropriate; dimensions may correlate. Missing citations
alone affect grounding, not factual truth. Correct conditional scenarios are not
hallucinations. A blanket disclaimer does not cure an invented amount. Merely
repeating “contingent,” “cap,” “uncertainty,” or “pari passu” is never sufficient:
explain the mechanism against the case evidence. A correct, plain-language neutral
answer can earn full marks. Do not require a prediction, recommendation, numeric
loss or different stakeholder conclusions.

Use `unscorable` with null score for reference targets unresolved after adjudication,
not zero; an ordinary reviewer disagreement must follow the rule above. Ratings
start `not_reviewed`/null in the plan. The claim log records omission/contradiction/
unsupported assertion, materiality, response excerpt, source and rationale. The
binary primary endpoint is any material unsupported assertion in a complete
response, adjudicated independently of wording or length.

## Baseline comparison

There is no implemented deterministic disclosure extractor in this repository;
the audit's suggested regex/NER baseline is a proposal, not measured performance.
The existing `reference_calculations()` (Harbor) and `reference_values()` (Cedar)
are reused offline, with their outputs included in the preparation plan as scope
controls. Their complete synthetic inputs and equal-ranking, staged-recovery
assumptions support exact arithmetic, not primary-disclosure interpretation.
All five disclosure cases lack complete settlement inputs, so these baseline
tasks are **not applicable** there, rather than failed or zero-scoring. Do not
apply a synthetic waterfall to an issuer, demand economic prose from arithmetic,
or claim an LLM improvement over this baseline. The appendix is outside the 30
responses and supplies no new model calls or experimental conditions. Any future
synthetic arithmetic comparison requires its own authorization and protocol.

## Analysis, limitations and stopping rule

Primary: for each case, report material unsupported assertions as n/3 for each
condition, then guided-minus-neutral rate difference. Average those five case
differences with equal case weights only if all five are independently scorable;
otherwise give case results and identify the missing comparison explicitly.
Secondary: display all five dimension scores for every response, case/condition
means and ranges across three repeats, and guided-minus-neutral case means.
Report inter-rater exact agreement per dimension before adjudication with its
denominator, the claim/error log, disagreements, and completion/missing bounds.
No keyword score or total correctness percentage. Do not use repeat indices as
paired stochastic samples: requests are independent; comparisons pair at case
level. Do not treat 30 responses as 30 independent corporate cases.

With five purposive cases and three responses per arm, use descriptive estimates
and counterexamples only. No p-values, power claims, model leaderboard, population
causal claims, or post-hoc rubric changes. Report neutral performance in its own
right and guided performance as prompted assistance. Curation, unequal case
complexity, historical familiarity/contamination, imperfect masking, fallible
references and backend drift limit interpretation. This design was informed by
existing outcomes and audits and is not a prospective discovery study of those
same arrangements. No independent validation result exists yet.

Current stopping point: protocol, five provisional reference records, two new
evidence fixtures and reproducible 30-slot preparation plan pass offline checks
and are ready for independent review. Unresolved issues are independent approval
of all records, NVIDIA/Meta/Apple recognition amounts not established by selected
evidence, complete contract terms/ranking, reviewer recruitment, and provider
settings/version verification. Do not expand sample size or conditions to solve
these issues. Do not execute the plan, commit or push.

Offline reproduction from repository root (use the existing Python environment):

```sh
.venv/bin/python protocols/scientific-validation-v1/prepare.py > /tmp/parallax-sv1-plan.json
.venv/bin/python -m unittest discover -s tests -v
```

Preparation only prints JSON and computes local arithmetic/hashes; it never loads
credentials or invokes the API. Archive the reviewed plan separately before any
future authorized execution. The historical protocol's commit gate is unchanged.
