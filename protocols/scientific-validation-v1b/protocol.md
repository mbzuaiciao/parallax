# Scientific validation v1B — prompt mechanism ablation

Frozen before v1B inference, October 29, 2026. Exploratory follow-up authorized by
the user: **five existing cases × two new conditions × one response = 10 calls**.
The original v1 protocol, provisional references, evidence, 30 raw responses and
ratings remain unchanged. No independent external human certification is claimed.

## Question, hypotheses and cases

Does the v1 improvement mainly reflect negative constraints, positive analytical
structure, or both? Negative constraints may reduce unsupported assertions; positive
structure may improve coverage and useful stakeholder analysis. Either, neither,
or both may help. One sample per case/condition cannot identify a definitive causal
decomposition, regardless of the earlier audit's stronger mechanism claims.

Reuse exactly NVIDIA PORTS, Meta capacity, CoreWeave deposit, Apple manufacturing,
and Microsoft operating leases, with the same historical cutoffs and curated
evidence bytes. Read v1's protocol, references, pilot report and independent-results
audit before freezing. All references stay provisional/pending; unknown carrying
amounts remain unknown rather than certified zeros. No extra cases, perspectives,
models, retrieval, calibration prompts, or repetitions.

## Exactly two new conditions

Requests reuse v1 `prepare.request_for`; only developer content changes. Both cover
equity investors and senior unsecured creditors. The companion plan snapshots all
ten full requests and hashes before inference, not just the templates.

**A — positive analytical structure only.** Preserve the original guided wording
for parties, direct/contingent obligations, triggers/terms, both stakeholder
perspectives, facts versus conditional interpretation, evidence, missing information
and structured presentation. Remove the entire original negative sentence and
the sentence saying no outside research/classifications are available; remove
“only” from the opening scope instruction. Remaining instructions, in order:

> Analyze the single financing arrangement in the supplied historical SEC-disclosure
> source pack, as of its analysis date. Identify contractual obligors and
> beneficiaries, distinguishing direct from contingent obligations. Explain payment
> triggers, effectiveness, contractual limits, recoveries, remedies and termination
> terms. Separately assess the implications for (1) an equity investor in {company}
> and (2) a senior unsecured creditor of {company}. Distinguish disclosed facts from
> conditional economic interpretations. Cite document IDs and provision locators.
> Disclose material missing terms and uncertainties preventing definitive
> quantitative risk assessment. Give a concise, structured analysis.

**B — negative constraints only.** Use the exact existing v1 neutral developer
instruction for both investor perspectives and append, verbatim, just this original
guided sentence:

> Use only the supplied evidence; do not infer redacted identities, invent financial
> inputs, assume a creditor ranking, or turn a disclosed cap into an expected loss
> or payable balance.

B adds no parties/triggers/response-outline instructions beyond neutral. A retains
positive evidence/uncertainty instructions, which themselves may improve discipline;
it is not a completely reasoning-neutral intervention. The shared curated evidence
also contains cautions and classifications. Length/content differ. These limits
preclude attributing every difference uniquely to prohibition versus structure.

## Sampling and execution

Use `muse-spark-1.3`, `https://api.meta.ai/v1/chat/completions`, temperature **0.7**,
`max_completion_tokens=8192`; keep every other parameter omitted as in v1.
References, previous answers, audit judgments and scores never enter requests.
No alternative backend. API acceptance was established in the v1 pilot, not a
guarantee of future availability or actual 8192-token generation.

Generate cells in reference-record order, A then B per case, and shuffle once with
`random.Random(20261029)`. Run IDs: `sv1b:case:A:1` / `sv1b:case:B:1`. The seed controls
order, not sampling. Every request is a fresh conversation. Exactly one HTTP
attempt per slot, no retries, redirects, replacements, or resumption. Errors and
truncations remain in their slots; missing answers get null scores, not perfect
hallucination scores. Preserve text from incomplete responses but exclude them
from complete-answer score summaries; report best/worst missing bounds.

Save the plan, Git revision/dirty state, protocol/code/source/v1-artifact hashes,
exact serialized request and raw provider object, response ID/model, usage, HTTP
status, finish reason and UTC times. Checkpoint before and after each call using
the existing client/checkpoint helpers. Stop on HTTP 400/401/403/429 or returned-model
drift; leave unattempted slots pending. Do not change settings to finish the grid.

## Evaluation frozen before outputs

Apply the **unchanged five v1 dimensions, each 0–2**: factual correctness, financial/
accounting interpretation, evidence grounding, unsupported inference, uncertainty/
abstention. Higher is better. Copy/reference the frozen v1 rubric by hash, rather
than replacing it. Primary endpoint: any material unsupported assertion in a
complete response, with source-linked quotation and rationale. Materiality retains
v1's obligor/mechanism/amount/date/recognition/cash-channel/investor-conclusion rule.

Pre-observation applications of that rubric, informed by the audit disagreements:

- Qualified commercial heuristics are interpretations: if payments are necessary
  to preserve operations, they may compete with cash for debt service. This is not
  an invented legal priority. Terms like “operationally senior” are not automatically
  errors; read the full context and any explicit legal-priority disclaimer.
- Flag unambiguous unsupported legal rank, compulsory relative payment sequence,
  concrete comparator maturity, or definitive recovery/LGD conclusion. A disclaimer
  does not cure a separate unequivocal legal-rank claim. A clearly hypothetical
  stress assumption is not an asserted observed recovery.
- An economic description of contingent exposure as “off-balance-sheet” does not
  by itself establish an exact-zero carrying claim. Credit ordinary qualified
  executory-contract accounting. Flag a definite issuer-specific zero/unrecognized
  balance only when asserted beyond the evidence; retain reference uncertainty.
- Generic qualified high-cost/specialty-financing commentary may be useful; it does
  not establish issuer distress or a quantified loss. Do not demand reference
  wording or penalize a justifiable economic channel because it is not a core fact.
- Conventional primary-filing/note/section citations qualify equally with schema
  IDs. Score semantic support, not citation style. Correct factual citations do
  not automatically substantiate additional legal or accounting assertions.
- Read actual context: quantify a cap as a cap, current versus undiscounted amounts
  distinctly, and dates accurately. Do not reward headings, terminology, verbosity
  or a generic disclaimer. Model answers and audit labels are not ground truth.

**Supplemental analytical usefulness/completeness (0–2), separate from the frozen
five-dimensional scores and primary endpoint:** 2 = usable explanation of the
mechanism plus both stakeholders, cash burdens/consideration or operating benefit,
and decision-relevant missing information; 1 = partially useful but a stakeholder,
material tradeoff or needed evidence is omitted, generic, or obscured by excessive
caution; 0 = no usable analysis or wholesale irrelevant/evasive content. Unsupported
speculation earns no usefulness credit. Do not create an aggregate six-score total.
For v1, report the audit's qualitative usefulness observations; no new numeric
usefulness scores are invented for historical responses.

After preserving raw outputs, assign shuffled unrelated review IDs, hiding A/B,
repeat, execution and provider metadata. Keep the mapping separate until all
ratings/excerpts/rationales are frozen and hashed. A single design-aware assistant
will review; style and prior design knowledge make masking imperfect. No independent
human rater or adjudicator is invented. Report uncertainty and disputed readings
explicitly; inter-rater agreement remains unavailable. Do not alter scores after
condition reveal. Unresolvable source disputes may remain unscorable/null.

## Analysis, limitations and stopping

Report completion/failure and the five scores plus supplemental usefulness for
each response, then A/B case flags (n/1). Show v1 neutral/guided n/3 descriptively,
preserving **both** original flags and the independent audit's R08/R14 alternatives.
The audit's assertion that neutral citations were downgraded solely for schema
formatting is disputed: original rationales cite unsupported extra claims too.
Do not silently adopt a revised v1 ground truth or scorecard, or treat a report
calling itself independent as human certification.

Report whether B suppresses unsupported assertions, A adds completeness/usefulness,
whether v1 combined guidance appears beneficial, and whether either new condition
over-abstains. Historical conditions were collected earlier with three repetitions
and disputed scoring; current judgments incorporate the above explicit distinction
between heuristics and legal rank. These are not simultaneous randomized four-arm
data under independently adjudicated labels. Do not pool all 40 answers into an
accuracy rate, claim statistical significance, rank models, or claim definitive
causal decomposition. Do not average the primary independently scorable-case effect
without independent adjudication. Curated packs, purposive selection, backend
uncertainty and one response per new cell limit inference.

Stop after the ten fixed slots and evaluation, or the specified blocking API
failure. A negative/inconclusive result is valid. No additional calls to improve
results, production changes, dependencies, commits or pushes.
