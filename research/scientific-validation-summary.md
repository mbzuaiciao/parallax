# Scientific validation v1 and v1B — research phase closure

October 29, 2026. The **40 planned research responses are complete** and archived.
This closes the exploratory research phase; it initiates no further experiments
or React work. All five financial references remain provisional, AI-assisted and
pending independent human approval. Original outputs, scores, protocols and
historical fixtures are preserved byte-for-byte.

Closure validation: **67 existing offline tests passed**. Protected artifact hashes
match the pre-closure snapshot, and there are no tracked production, fixture or
frozen-protocol edits. The archive adds the previously untracked experimental
records, localized v1B preparation/test materials, and these closure records.

## Questions and design

Original question: Does existing Parallax guidance improve correctness and evidence
discipline when interpreting supplied corporate obligations relative to neutral
instructions? v1B asks whether negative constraints or positive analytical structure
contribute to that observed difference. The hypothesis is fewer material
unsupported assertions with guidance; **its mechanism was not established in v1**.

Five purposively selected arrangements cover contingent guaranties (NVIDIA), own
capacity purchases (Meta), recognized refundable-deposit debt (CoreWeave),
manufacturing commitments (Apple) and recognized operating leases (Microsoft).
Each answer covers shareholders and a hypothetical senior unsecured creditor.
Curated historical SEC evidence, rather than full filings or live retrieval, enters
all conditions. The same case evidence and settings are used across conditions.

| Prompt condition | Content | Responses |
|---|---|---:|
| v1 neutral | Ordinary financial analysis and evidence request | 5 cases × 3 = 15 |
| v1 guided | Existing positive analytical guidance plus negative constraint sentence | 5 × 3 = 15 |
| v1B A | Inherited positive structure, fact/interpretation, citations and uncertainty instructions; explicit prohibitions removed | 5 × 1 = 5 |
| v1B B | Exact neutral prompt plus original negative constraint sentence | 5 × 1 = 5 |

All **40/40 completed with HTTP 200 and normal `stop` termination**, no retries,
model substitutions or truncations. One earlier harmless API probe is outside this
research sample; it exhausted its 128-token budget without visible text and was
not replaced by a research response. No new API request was made during closure.

## Observed material-assertion results

Each cell is flagged answers / completed answers. Audit proposals are reported
separately from original ratings; B's disputed flag remains in its original count.

| Case | v1 neutral original → audit | v1 guided original → audit | A original | B original |
|---|---|---|---|---|
| NVIDIA PORTS | 3/3 → 3/3 | 1/3 → 0/3 | 1/1 | 1/1, disputed |
| Meta capacity | 2/3 → 1/3 | 0/3 → 0/3 | 1/1 | 0/1 |
| CoreWeave deposit | 3/3 → 3/3 | 0/3 → 0/3 | 0/1 | 0/1 |
| Apple manufacturing | 3/3 → 3/3 | 0/3 → 0/3 | 0/1 | 0/1 |
| Microsoft leases | 3/3 → 3/3 | 0/3 → 0/3 | 0/1 | 0/1 |

The original v1 descriptive counts are **14/15 neutral versus 1/15 guided**; the
separate audit proposes **13/15 versus 0/15**. A has **2/5**, B **1/5 disputed**.
These counts are not population error estimates or independently adjudicated
accuracy. No pooled 40-answer accuracy or independently certified average case
effect is claimed. The cases, rather than repeated answers, define the economic
comparison units.

### Original versus audit-proposed v1 scores

The [results audit](scientific-validation-v1-independent-results-audit.md) labels
itself independent. External human identity/certification is not established here;
its revisions are an attributed second assessment, not approved reference truth.
F/I/E/H/U are factual correctness, financial interpretation, evidence grounding,
unsupported-inference discipline and uncertainty, each 0–2, higher better.

| Answer | Original scores / flag | Audit-proposed scores / flag |
|---|---|---|
| R08, NVIDIA guided 1 | 2/0/0/0/0; yes | 2/2/2/2/2; no |
| R14, Meta neutral 2 | 2/0/1/0/0; yes | 2/1/1/1/1; no, in its individual discussion |

R08 describes contingent exposure as off-balance-sheet in a conditional strategic
passage; this need not assert a zero recognized balance. R14 distinguishes a
maximum purchase exposure from current expense/debt and explicitly disclaims
legal priming while discussing going-concern cash competition. Those are credible
reasons to question the original penalties. Ordinary executory accounting must
still be distinguished from certifying every related carrying balance as zero.
The 8-K Item 2.03 heading itself offers both direct-obligation and off-balance-sheet
categories; that heading alone cannot certify an exact recognized amount.

The audit's published NVIDIA guided mean changes from
2/1.33/1.33/1.33/1.33 to 2/2/2/2/2. Its published Meta neutral mean changes from
2/0.67/1/0.33/0.67 to **2/1/1.33/0.67/1**, but the R14 individual revision above
would instead yield **2/1/1/0.67/1** if other answers are unchanged. The extra
0.33 grounding increment is not assigned unambiguously to a response. Its broad
citation-format criticism is also not a reproducible complete revised scorecard:
original rationales cite unsupported extra claims as well as evidence linkage.
No invented correction is made. Other case/condition dimensional means are
unchanged in its published table. All original individual vectors appear below;
the audit's exact text remains preserved, including these inconsistencies.

### v1B dispute and usefulness

[Separate M04 closure review](scientific-validation-v1b-adjudication.md) retains
**disputed / genuinely indeterminate as a material error in the whole answer**.
The exact NVIDIA B phasing sentence says no payment occurs before commencement
and RFS. The primary form restricts the Covered Loss Amount, defines a redacted
pre-RFS payment, and leaves important provisos redacted. The answer explicitly
acknowledges that exception elsewhere. A blanket all-payment claim is unsupported;
a contextual statement about the main phased obligation is supportable. A public
redacted definition alone does not prove an actual early-payment obligation.
The original five zeros and flag are preserved; no binding replacement scores or
independent human adjudication are claimed. Sensitivity: accepting the narrow
reading would give B **0/5** flags rather than **1/5**.

Positive structure A earned supplemental usefulness **2 in all five cases**; B
scored **1 for NVIDIA and Meta, 2 in the other three**. These ratings are separate
from the frozen five-dimensional rubric, with no six-score total. A's useful
remaining analysis does not excuse its unsupported NVIDIA reimbursement-security
and Meta security/expected-burden assertions. B's NVIDIA inconsistency and Meta's
underdeveloped capacity-value tradeoff reduced completeness. Both Microsoft
answers received minor interpretation/grounding penalties without a material flag.
Qualified operational cash-pressure heuristics were not automatically treated as
legal priority claims. M06/M10 accounting scope, M09 operational-priority phrasing,
and M05 usefulness remain judgment-sensitive, as recorded in the assessment.

The v1 audit qualitatively describes useful guided scenarios, commercial benefits,
recognition distinctions and targeted abstention across the guided answers. v1's
original factual scores were 2 throughout, and guided financial interpretation was
2 except disputed R08. This is evidence that disciplined prompting can preserve
usable analysis here; it is not independently measured general reasoning ability.
No supplemental usefulness scores were retrofitted to the original 30 answers.

## Observations, hypotheses and warranted conclusion

**Observed:** Combined guidance was associated with fewer flagged assertions than
neutral in these five cases under both original and audit-proposed counts. B
avoided the particular security/expected-burden errors found in A's NVIDIA and
Meta answers. A provided broad usable coverage, while B also did so in three cases.
There was no wholesale refusal or abstention in either v1B condition.

**Hypothesis:** Negative constraints contribute to evidence discipline, and positive
structure may improve completeness. The observations are consistent with both.
They do not show that prohibitions primarily or definitively explain the v1 gap,
that positive structure is unnecessary, or that combining both has an additive or
synergistic effect. The audit's stronger mechanism claims are not adopted.

**Conclusion:** These are promising, narrow results for prompted evidence discipline
on curated disclosures. They do not demonstrate autonomous or general financial
reasoning, investment accuracy, legal/accounting certification, or performance on
unseen full filings. A negative/inconclusive causal decomposition is a legitimate
endpoint for this phase.

## Scientific limits and future research recommendations

References are provisional; the intended two independent human financial raters
and masked senior adjudicator were not supplied. Condition-masked AI review was
design-aware and answer style can reveal conditions; agreement is unavailable.
The v1B rubric applications explicitly distinguish commercial heuristics from legal
rank, so historical and new scores are not one fully harmonized adjudicated panel.
One draw per new cell versus three per historical cell, purposive five-case
selection, different collection windows, contamination/familiarity, unequal prompt
length/content, curated warnings and mutable provider internals limit inference.
A retains positive evidence/uncertainty instructions, so it is not pure formatting.
There is no simultaneous randomized four-arm factorial study or significance test.
Missing contract terms, redactions, recognition measurements and issuer-wide credit
inputs restrict financial conclusions. Existing synthetic arithmetic baselines do
not evaluate disclosure interpretation; no comparative baseline advantage was
measured.

Recommended next research, **subject to separate authorization**, is human
source/accounting approval and blinded response review using existing records
first, resolving M04 and the v1 audit's score inconsistency. Pre-register practical
materiality/heuristic boundaries and independent usefulness criteria before any
new data. Only then consider a balanced contemporaneous ablation with repeated
cells, genuinely new arrangements, and a separately scoped full-filing extraction
study. No extra calls or data expansion occur in this closure task.

## Reproducibility and preserved records

Both runs used `muse-spark-1.3` at
`https://api.meta.ai/v1/chat/completions`, temperature **0.7** and
`max_completion_tokens=8192`; other sampling parameters were omitted, n=1/default,
no model seed. Schedule seed 20261029 governs order, not stochastic output.
Completion usage includes reasoning; acceptance and normal termination below the
budget do not demonstrate 8192 visible tokens or an immutable backend.
[Preflight](scientific-validation-v1-api-preflight.md) preserves the documentation
and initial probe's limits.

Execution Git revision for both: `870a683cf1aaed6d54424a6b444f32eccd2bd9ec`.
v1: 2026-10-29T15:42:17.614857+00:00–2026-10-29T15:50:13.550407+00:00.
v1B: 2026-10-29T16:32:30.067591+00:00–2026-10-29T16:34:59.042157+00:00.
Both raw records retain exact pre-execution dirty/untracked status, rather than
claiming a clean execution checkout. Closure's parent is the same revision; its
archive commit is identified by Git history and the final delivery, avoiding a
self-referential embedded commit hash.

| Frozen protocol | SHA-256 |
|---|---|
| `protocols/scientific-validation-v1/protocol.md` | `baed5b4a23fab0e4642fb3292e015f00560c16f94bc6c76e818247b253a4c347` |
| `protocols/scientific-validation-v1b/protocol.md` | `3162a44db4188d770d2be3d30e76b4f79f2fcc082595cc509041e887ee5b6710` |

- v1 [raw requests/responses](scientific-validation-v1-pilot-20261029/raw.json),
  [plan](scientific-validation-v1-pilot-20261029/plan.json),
  [masked assessment](scientific-validation-v1-pilot-20261029/assessment.json),
  [revealed scores](scientific-validation-v1-pilot-20261029/revealed-assessment.json),
  [original report](scientific-validation-v1-pilot-results.md), and
  [audit](scientific-validation-v1-independent-results-audit.md).
- v1B [raw requests/responses](scientific-validation-v1b-20261029/raw.json),
  [frozen plan](../protocols/scientific-validation-v1b/plan.json),
  [masked assessment](scientific-validation-v1b-20261029/assessment.json),
  [revealed scores](scientific-validation-v1b-20261029/revealed-assessment.json),
  [report](scientific-validation-v1b-results.md), and
  [separate disputed assessment](scientific-validation-v1b-adjudication.md).
- [Readiness](scientific-validation-v1-readiness.md),
  [ground-truth audit](scientific-validation-v1-ground-truth-audit.md),
  [reconciliation](scientific-validation-v1-reconciliation.md), and
  [provisional references](../protocols/scientific-validation-v1/references.json).
- [Closure integrity manifest](scientific-validation-closure.json) records source,
  protocol, raw-response, score, audit and new-record hashes, exact checkout state,
  offline validation, and unresolved-dispute status. Existing run verification
  records remain historical snapshots. See Git history for the archive commit.

## All 40 original response-level results

These are the **unchanged frozen vectors**, including disputed flags, not a fresh
rescore. H=unsupported-inference discipline, higher better. Audit alternatives
for R08/R14 and M04's null closure disposition are described separately above.
Usefulness was added only in v1B; “not scored” is not zero.

| Study | Review | Case | Condition / repeat | F/I/E/H/U | Flag | Usefulness |
|---|---|---|---|---|---|---|
| v1 | R07 | nvidia-ports | neutral / 1 | 2/0/1/0/0 | yes | not scored |
| v1 | R09 | nvidia-ports | neutral / 2 | 2/0/1/0/0 | yes | not scored |
| v1 | R22 | nvidia-ports | neutral / 3 | 2/0/1/0/0 | yes | not scored |
| v1 | R08 | nvidia-ports | guided / 1 | 2/0/0/0/0 | yes | not scored |
| v1 | R03 | nvidia-ports | guided / 2 | 2/2/2/2/2 | no | not scored |
| v1 | R02 | nvidia-ports | guided / 3 | 2/2/2/2/2 | no | not scored |
| v1 | R13 | meta-capacity | neutral / 1 | 2/2/1/1/2 | no | not scored |
| v1 | R14 | meta-capacity | neutral / 2 | 2/0/1/0/0 | yes | not scored |
| v1 | R30 | meta-capacity | neutral / 3 | 2/0/1/0/0 | yes | not scored |
| v1 | R24 | meta-capacity | guided / 1 | 2/2/2/2/2 | no | not scored |
| v1 | R12 | meta-capacity | guided / 2 | 2/2/2/2/2 | no | not scored |
| v1 | R16 | meta-capacity | guided / 3 | 2/2/2/2/2 | no | not scored |
| v1 | R01 | coreweave-deposit | neutral / 1 | 2/0/1/0/0 | yes | not scored |
| v1 | R04 | coreweave-deposit | neutral / 2 | 2/0/1/0/0 | yes | not scored |
| v1 | R06 | coreweave-deposit | neutral / 3 | 2/0/1/0/0 | yes | not scored |
| v1 | R21 | coreweave-deposit | guided / 1 | 2/2/2/2/2 | no | not scored |
| v1 | R27 | coreweave-deposit | guided / 2 | 2/2/2/2/2 | no | not scored |
| v1 | R28 | coreweave-deposit | guided / 3 | 2/2/2/2/2 | no | not scored |
| v1 | R17 | apple-manufacturing | neutral / 1 | 2/0/1/0/0 | yes | not scored |
| v1 | R26 | apple-manufacturing | neutral / 2 | 2/0/1/0/0 | yes | not scored |
| v1 | R18 | apple-manufacturing | neutral / 3 | 2/0/1/0/0 | yes | not scored |
| v1 | R05 | apple-manufacturing | guided / 1 | 2/2/2/2/2 | no | not scored |
| v1 | R29 | apple-manufacturing | guided / 2 | 2/2/2/2/2 | no | not scored |
| v1 | R25 | apple-manufacturing | guided / 3 | 2/2/2/2/2 | no | not scored |
| v1 | R20 | microsoft-leases | neutral / 1 | 2/0/1/0/0 | yes | not scored |
| v1 | R10 | microsoft-leases | neutral / 2 | 2/0/1/0/0 | yes | not scored |
| v1 | R15 | microsoft-leases | neutral / 3 | 2/0/1/0/0 | yes | not scored |
| v1 | R19 | microsoft-leases | guided / 1 | 2/2/2/2/2 | no | not scored |
| v1 | R11 | microsoft-leases | guided / 2 | 2/2/2/2/1 | no | not scored |
| v1 | R23 | microsoft-leases | guided / 3 | 2/2/2/2/2 | no | not scored |
| v1B | M01 | nvidia-ports | A / 1 | 1/0/1/0/0 | yes | 2 |
| v1B | M04 | nvidia-ports | B / 1 | 0/0/0/0/0 | yes (disputed) | 1 |
| v1B | M03 | meta-capacity | A / 1 | 2/0/1/0/0 | yes | 2 |
| v1B | M05 | meta-capacity | B / 1 | 2/1/2/2/2 | no | 1 |
| v1B | M07 | coreweave-deposit | A / 1 | 2/2/2/2/2 | no | 2 |
| v1B | M08 | coreweave-deposit | B / 1 | 2/2/2/2/2 | no | 2 |
| v1B | M09 | apple-manufacturing | A / 1 | 2/2/2/2/2 | no | 2 |
| v1B | M02 | apple-manufacturing | B / 1 | 2/2/2/2/2 | no | 2 |
| v1B | M06 | microsoft-leases | A / 1 | 2/1/1/1/2 | no | 2 |
| v1B | M10 | microsoft-leases | B / 1 | 2/1/1/1/2 | no | 2 |
