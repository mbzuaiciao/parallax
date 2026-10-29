# Scientific validation v1B — exploratory results

Exactly **10/10 planned calls completed**, with HTTP 200, `finish_reason=stop`,
returned model `muse-spark-1.3`, temperature 0.7 and `max_completion_tokens=8192`.
No retries, substitutions, benchmark additions or extra evaluation API calls.
The frozen, condition-masked AI review flags two A answers and one B answer;
the B flag has a documented scope ambiguity. This suggests a useful role for
negative constraints, but does **not** establish that they primarily caused v1's
improvement. All financial references and response judgments remain provisional.

## Provenance and execution

Execution: 2026-10-29T16:32:30.067591+00:00 through 2026-10-29T16:34:59.042157+00:00.
Git revision: `870a683cf1aaed6d54424a6b444f32eccd2bd9ec` on `main`. The initial working tree had
untracked v1 preflight/audit/pilot records; the pre-inference snapshot also lists
this study's new files. The complete exact status is retained in
[raw.json](scientific-validation-v1b-20261029/raw.json), not described as clean.
No tracked file, historical result, reference or production behavior was changed.
All five references were provisional/pending, with AI-assisted review and no
independent external human certification; their bytes/statuses remain unchanged.

Authentication was available from the ignored local `.env`; credentials are absent
from artifacts. Endpoint: `https://api.meta.ai/v1/chat/completions`.
Every request used the frozen settings, fresh conversation and identical case
evidence across A/B. Model acceptance of 8192 was observed in these requests; none
is proof of generating a full 8192 visible tokens. All terminated normally below
the limit. Provider usage includes completion accounting beyond visible prose;
no visible/reasoning-token equivalence is assumed.

| Condition | Prompt tokens | Completion tokens | Total tokens |
|---|---:|---:|---:|
| A — positive structure | 3698 | 20556 | 24254 |
| B — negative constraints | 3518 | 19506 | 23024 |
| Total | 7216 | 40062 | 47278 |

The [frozen protocol](../protocols/scientific-validation-v1b/protocol.md) and
[plan](../protocols/scientific-validation-v1b/plan.json) specify the exact wording,
schedule, ten wire requests, evidence/code/reference and historical artifact
hashes. Plan SHA-256:
`8e4142d34e1a4c15419a850a6ad770527833d8a5ac9325eb025c77254f13034a`.
Protocol SHA-256: `3162a44db4188d770d2be3d30e76b4f79f2fcc082595cc509041e887ee5b6710`.
Raw SHA-256: `60c70d1c1e48131a72315f38e478d009e30f896018bddffeaadff50c0d26afb4`.
The adapter records one HTTP attempt, run/provider IDs, UTC times, status, returned
model, usage, finish reason, full provider object and complete visible answer per
slot. Raw outputs were saved before scoring. All protected hashes matched after
execution and again at final offline verification.

## Review and four-condition comparison

The [masked package](scientific-validation-v1b-20261029/masked-review.json) omits
conditions and execution/provider identifiers. All ten ratings, rationales and
claim excerpts were frozen before opening the separate mapping; assessment hash:
`7075a37e4f5f9346b18ae3721eef4aeb3a2e8461ee9b68165aa72d219f1de1c3`.
See [masked assessment](scientific-validation-v1b-20261029/assessment.json),
[revealed scorecard](scientific-validation-v1b-20261029/scorecard.md), and
[case-level data](scientific-validation-v1b-20261029/case-summary.json).
Masking is imperfect: one design-aware assistant can recognize prompt styles.
There is no independent human scorer, adjudicator or inter-rater agreement.

Each cell below is **material flags / completed responses; factual / financial
interpretation mean**, both scores 0–2, higher better. Historical v1 cells retain
original ratings; parenthetical audit alternatives affect flags only here.
These are descriptive, differently sampled and partly disputed judgments, not
comparable independently validated error-rate estimates.

| Case | v1 neutral, 3 draws | v1 guided, 3 draws | v1B A, 1 draw | v1B B, 1 draw |
|---|---|---|---|---|
| NVIDIA | 3/3; 2.00/0.00 | 1/3; 2.00/1.33 (audit: 0/3) | 1/1; 1.00/0.00 | 1/1; 0.00/0.00 † |
| Meta | 2/3; 2.00/0.67 (audit: 1/3) | 0/3; 2.00/2.00 | 1/1; 2.00/0.00 | 0/1; 2.00/1.00 |
| CoreWeave | 3/3; 2.00/0.00 | 0/3; 2.00/2.00 | 0/1; 2.00/2.00 | 0/1; 2.00/2.00 |
| Apple | 3/3; 2.00/0.00 | 0/3; 2.00/2.00 | 0/1; 2.00/2.00 | 0/1; 2.00/2.00 |
| Microsoft | 3/3; 2.00/0.00 | 0/3; 2.00/2.00 | 0/1; 2.00/1.00 | 0/1; 2.00/1.00 |

† NVIDIA B's categorical timing claim is flagged under the broad reading. A human
may instead read it as restricted to the main Covered Loss mechanism. Under that
narrow reading, the B flagged-answer count would be zero rather than one; the
frozen scorecard has not been changed to select this favorable interpretation.
No independently adjudicated primary aggregate or effect estimate is available.

All five dimensions appear separately for every new answer in the scorecard.
Factual and interpretation scores need not move together: Meta A preserves the
reported facts while making unsupported legal/expected-burden conclusions. The
NVIDIA B timing contradiction drives its low scores, rather than an absence of
useful content throughout the answer. Microsoft A/B each retain correct reported
amounts but receive 1 for interpretation, grounding and unsupported-inference
because of minor measurement/equity-offset extrapolation; neither gets a material
flag. Uncertainty scores are 2 for seven answers and 0 for the three materially
flagged answers: generic caveats do not cure the specific unsupported conclusions.

Supplemental usefulness/completeness: A = 2 in each of five cases; B = 1 for NVIDIA
and Meta, 2 for CoreWeave, Apple and Microsoft. This is separate from the frozen
five scores and never added into a six-score total. Correct remaining analysis
can be useful even when another passage is wrong; speculation earns no extra
usefulness credit. Mean visible character length was 7754 for A and
6421 for B, reported as a length confound, not an evaluation metric.
No numeric usefulness ratings were retrofitted to v1. Its audit describes greater
guided completeness, but that qualitative judgment is neither independent source
certification nor a four-arm scored completeness comparison.

## What the responses show

- **Unsupported legal and expectation assertions:** NVIDIA A (M01) says
  “OpenAI reimbursement is an unsecured claim”; SEC_FORM §§5/8 and the selected
  pack do not establish reimbursement security. It also dates signing to August
  26 rather than August 17. Meta A (M03) says the arrangement is “unsecured and
  non-guarantee in nature on disclosed terms”; the non-guarantee characterization
  is supported, security is not. Its “expected burden < $14.72bn” conclusion is
  also not established by merely possible resale mitigation without probabilities.
- **Disputed cash timing:** NVIDIA B (M04) says “No payment before lease commencement
  and ready-for-service”, while itself acknowledging a redacted pre-RFS termination
  payment defined in SEC_FORM. That broad absolute conflicts with the selected
  form. Whether the sentence implicitly refers only to the main phased guarantee
  remains unresolved, and merits human contract review.
- **Correct financial distinctions:** Both CoreWeave answers preserve $230m
  received, $273m/$43m at December 2025, $100m June settlement and $189m June
  carrying amount. They distinguish ASC 470 debt from revenue and decline to infer
  seniority from recourse classification. Both Apple answers distinguish gross
  procurement commitments from funded debt, retain unknown recognition details,
  and avoid claiming an exact-zero balance. Both Microsoft answers preserve
  $22,861m PV versus $25,481m gross payments and $6,111m FY2026 payments.
- **Useful heuristics retained:** Microsoft A labels going-concern payment
  competition as conditional/general and explicitly says relative recovery is
  unknown. Apple A distinguishes economic supply continuity from unknown legal
  seniority. These were not flagged solely for operational-priority language.
  A generic disclaimer would not rescue the separate explicit unsecured claims
  in NVIDIA A or Meta A.
- **Incomplete or imprecise reasoning:** Meta B correctly declines to assert a
  revenue-growth outcome but barely explores the conditional operating value of
  receiving capacity. That lowers completeness, not factual or hallucination
  credit. Microsoft A's “current = PV of next-12-months” is not established by the
  aggregate discount reconciliation; Microsoft B's “partly offset” ROU asset
  wording overstates the known net-equity direction despite a later explicit
  limitation. These accounting readings remain open for human review.

## Interpretation, disagreements and limits

B avoided the unsupported security/expected-burden claims seen in A for NVIDIA
and Meta; it did not eliminate every possible error. A provided usable broad
coverage in all five cases, but B was also fully useful in three. Two B answers
had a missing tradeoff or a cash-timing inconsistency; there was no wholesale
abstention in either condition. The sample therefore supports neither “structure
is unnecessary” nor “negative constraints alone are sufficient.” v1 combined
guidance appears compatible with both discipline and coverage, subject to its
historical scoring disputes. It does not prove synergy or additive causation.

The v1 audit recommends unflagging R08 (NVIDIA guided) and R14 (Meta neutral).
Both alternatives remain visible above; original v1 files were not edited.
Its claim that neutral evidence grounding was downgraded solely for schema-style
citations is disputed: original rationales also identify unsupported additional
claims. Conventional primary citations receive equal credit here. The audit's
stronger definitive mechanism claims are not adopted. This is AI-assisted
reconciliation, not an invented independent adjudication.

Remaining disagreements include M04's scope, the minor-versus-material accounting
readings in M06/M10, the complete-context interpretation of M09's economic
priority wording, and M05's tradeoff completeness. No human resolution is claimed;
all are documented in the frozen assessment. No scoring rule or reference was
changed after observing outputs or revealing conditions.

One response per new cell, purposive/curated evidence, unverified provisional
references, model/backend sampling variability, different collection times and
prompt lengths, and clarification of heuristic handling limit cross-study
comparability. A retains positive evidence/uncertainty instructions; even the
shared evidence contains cautions. This is not a simultaneously randomized
four-arm factorial experiment and cannot isolate a definitive causal mechanism
or support statistical significance. A rescore of historical responses under
these clarifications was not performed. Source-level uncertainties remain those
in the frozen references, including redacted contract terms, unknown carrying
balances, priority and issuer-wide financial inputs.

Offline checks: all 67 tests passed before inference; final suite/integrity status
is recorded in [verification.json](scientific-validation-v1b-20261029/verification.json).
Only localized protocol/preparation/test/run/report files were created; no new
dependencies, production changes, historical modifications, commits or pushes.
The fixed ten calls and evaluation are complete. No additional sampling is planned.
