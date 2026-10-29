# Scientific validation v1 — exploratory pilot results

October 29, 2026. **30/30 planned responses collected; no API failures or retries.**
The provisional AI-assisted evaluation found fewer material unsupported assertions
with guidance in each of the five cases. This is a descriptive pilot using
assistant-prepared provisional references, not independently validated financial
accuracy or a confirmatory experiment. The protocol's independent-review aggregate
is withheld.

## Execution and preservation

- Five cases × two conditions × three repetitions; each answer covers equity and
  senior unsecured creditors. Exactly **30 HTTP attempts** in the preparation
  script's seeded order, no substitutions or additional model calls.
- Requested/returned model: `muse-spark-1.3` for every slot; direct endpoint
  `https://api.meta.ai/v1/chat/completions`; temperature **0.7**, maximum completion
  tokens **8192**, other parameters omitted as in the frozen plan.
- All slots: HTTP **200**, finish reason **stop**, nonempty visible response.
  Errors, refusals, truncations, missing answers and pending slots: **0**.
- Collection window: `2026-10-29T15:42:17.614857+00:00` to
  `2026-10-29T15:50:13.550407+00:00` (08:42–08:50 America/Los_Angeles).
- Usage: **21,798 prompt**, **116,360 completion**,
  **138,158 total** tokens. Completion usage includes **67,648**
  reported reasoning tokens. Individual completion usage ranged **2,821–5,111**.
  These calls confirm acceptance of the 8192 parameter, not actual generation of
  8192 tokens. No billing-cost estimate is asserted.
- Git revision: `870a683cf1aaed6d54424a6b444f32eccd2bd9ec`. At task start the only untracked
  file was the preflight report. Execution also records the untracked runner and
  exact pre-output working-tree state. The working tree was not clean, so Git HEAD
  alone does not identify the run; input, runner, client and plan hashes are saved.
- All readiness-record protocol/reference/fixture/code hashes and the preparation
  stdout hash matched before calls; protected hashes still match afterward.
  Authentication was available through ignored `.env`; credentials/headers were
  never stored or printed. No production behavior or historical result was changed.

The frozen preparation plan still records its earlier execution-disabled review
stage. It was preserved unchanged. The latest user instruction explicitly authorized
this exploratory run with provisional AI-assisted references, overriding the
independent-human-approval execution gate for this run only. It did not certify
references or alter case selection, conditions, settings, sampling or rubric.

## Case-level material unsupported-assertion rates

A flag means at least one material unsupported assertion in the complete answer,
not that all content was false. Rates below are **provisional assistant judgments**.
Each denominator is all three planned slots for that case/condition.

| Case | Neutral | Guided | Guided − neutral rate |
| --- | --- | --- | --- |
| nvidia-ports | 3/3 | 1/3 | -0.667 |
| meta-capacity | 2/3 | 0/3 | -0.667 |
| coreweave-deposit | 3/3 | 0/3 | -1.000 |
| apple-manufacturing | 3/3 | 0/3 | -1.000 |
| microsoft-leases | 3/3 | 0/3 | -1.000 |

There are no missing responses: completion is 3/3 in every case/condition. The
protocol's best/worst missing-data bounds therefore collapse to the displayed
case rates and score summaries. No five-case average, population effect, p-value,
power claim or model-ranking result is calculated; independent scorable-case
approval is absent. Repetition indices are not treated as paired random seeds.

## Factual and interpretive performance

Means with observed ranges in brackets; each dimension is 0–2, higher is better.
“No unsupported inference” is the rubric score, separate from the binary endpoint.

| Case | Condition | Factual | Interpretation | Grounding | No unsupported inference | Uncertainty |
| --- | --- | --- | --- | --- | --- | --- |
| nvidia-ports | neutral | 2.00 [2–2] | 0.00 [0–0] | 1.00 [1–1] | 0.00 [0–0] | 0.00 [0–0] |
| nvidia-ports | guided | 2.00 [2–2] | 1.33 [0–2] | 1.33 [0–2] | 1.33 [0–2] | 1.33 [0–2] |
| meta-capacity | neutral | 2.00 [2–2] | 0.67 [0–2] | 1.00 [1–1] | 0.33 [0–1] | 0.67 [0–2] |
| meta-capacity | guided | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] |
| coreweave-deposit | neutral | 2.00 [2–2] | 0.00 [0–0] | 1.00 [1–1] | 0.00 [0–0] | 0.00 [0–0] |
| coreweave-deposit | guided | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] |
| apple-manufacturing | neutral | 2.00 [2–2] | 0.00 [0–0] | 1.00 [1–1] | 0.00 [0–0] | 0.00 [0–0] |
| apple-manufacturing | guided | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] |
| microsoft-leases | neutral | 2.00 [2–2] | 0.00 [0–0] | 1.00 [1–1] | 0.00 [0–0] | 0.00 [0–0] |
| microsoft-leases | guided | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] | 2.00 [2–2] | 1.67 [1–2] |

Factual scores reflect correct coverage of the 14 frozen core targets—parties,
mechanisms, dates and amounts. They are not a percentage of all narrative claims
verified true. The main problems were ungrounded extensions of otherwise correct
facts, penalized in interpretation, grounding, unsupported inference and uncertainty.
The linked scorecard displays all five scores for every response, not only averages.

## Representative reasoning and judgment boundaries

- **Correct recognition:** CoreWeave guided R21 distinguishes the $230m receipt,
  $273m December balance/$43m premiums, $100m settlement and $189m June balance,
  explicitly calling them “accounting balances, not adjudicated recovery amounts.”
  Source: CRWV 10-K/10-Q Note 10. Guided R27 also preserves the unknown H1-2026
  consumption status rather than extending the December zero-services fact.
- **Correct neutral counterexample:** Meta neutral R13 states “no statement whether
  any portion is already accrued,” declines a reliable debt-equivalent, and
  separates the illustrative $2.94bn annual average from any payment schedule.
  Its generic rating/critical-vendor background is unsupported minor detail, but
  it does not impose a definite priority for this arrangement. It received no
  material-unsupported flag. Source: Meta 10-Q Note 9.
- **Correct uncertainty:** Apple guided R25 says accounting status—whether any
  portion is already accrued—is not stated, and explains cash competition without
  assigning creditor rank. Qualified ordinary executory-contract nonrecognition
  was credited in neutral Apple answers too; it was not itself counted as error.
- **Unsupported rank/recovery:** NVIDIA neutral R09 says a triggered claim is
  “ranking with senior unsecured claims” and LGD “would spike.” Neither relative
  ranking nor a recovery model is supplied. Microsoft neutral R15 says rent is
  paid “ahead of interest and principal on senior unsecured notes”; cash-flow
  classification does not establish that priority. Sources: NVIDIA Form §§5/8/12;
  Microsoft Note 13 and frozen unknowns.
- **Unsupported timing/date inference:** CoreWeave neutral R06 says the June
  settlement proves payment “before senior unsecured maturities,” although no
  comparator maturity schedule is supplied. Neutral R04 concludes “zero revenue
  conversion to date,” extending a December 2025 fact through the 2026 analysis
  cutoff. Sources: CRWV Note 10 at the two reporting dates.
- **Guidance was not flawless:** NVIDIA guided R08 says exposure “remains
  off-balance-sheet contingent” if the project performs, citing Note 17/Form §20(e),
  which do not establish PORTS carrying recognition. It was provisionally flagged
  as an unestablished accounting classification, despite otherwise strong mechanics
  and citations. This wording could also be read as an economic description of
  gross contingent exposure, so its materiality/recognition reading specifically
  requires independent human review. The other guided NVIDIA responses distinguish
  cap from accounting measurement without this claim.
- **Overcaution:** Microsoft guided R11 hesitates about whether the FY2026 maturity
  payment is undiscounted despite the table context; this lowered uncertainty to 1
  without inventing an amount or creating a material-unsupported flag.

A generic conditional discussion of liquidity competition was not treated as a
hallucination. A definite claim of legal or operational priority was flagged when
these particular contract/issuer inputs were absent. Ordinary accounting principles,
“debt-like” analogies and lack of schema IDs did not automatically lose points.
The complete source-linked excerpts/rationales are retained for human challenge.

## Evaluation provenance and limitations

Full raw provider objects were saved before scoring, including response IDs,
returned models, usage, finish reasons and complete visible response/reasoning
fields where returned. A separate shuffled package replaced run IDs with R01–R30
and hid condition, repeat, execution order and provider metadata. The condition
mapping was first read after all 30 ratings were saved and hashed:
`994200807e96e0d81adf182ebb699f5923e55f656ba25c7ae70be8db779cb01d`.
No ratings were changed after revealing conditions.

Masking was limited: the evaluator is the same design-aware Codex assistant,
execution progress was visible, and answer headings/style often reveal guidance.
There was **one AI-assisted review, no independent human rater or adjudicator**.
Inter-rater agreement is unavailable, not zero or perfect. All five reference
records remain provisional/pending and were not modified. Therefore all scores,
case differences and flags above remain preliminary; references, their accounting
interpretations and borderline materiality decisions may be disputed by experts.

Curated evidence already supplies classifications and caveats. The guided prompt
explicitly teaches many scored boundaries; the result concerns performance with
that compound guidance, not intrinsic or improved unaided financial reasoning.
Nonrandom cases, unequal complexity, familiar public disclosures, one model,
three samples per cell, correlated rubric dimensions and possible backend drift
limit generalization. No automated citation-name or keyword match was used to
assign correctness: the assistant read full visible answers and assessed semantic
support. Representative anchors were extracted after manual scores were assigned.

The existing deterministic Harbor/Cedar arithmetic appears in the frozen plan as
scope controls. It is not applicable to these five disclosures' missing settlement
inputs and was not given semantic-finance scores. No LLM-versus-arithmetic superiority
claim is supported.

## Artifacts and checks

- [Frozen preparation plan](scientific-validation-v1-pilot-20261029/plan.json)
- [Raw responses and execution metadata](scientific-validation-v1-pilot-20261029/raw.json)
- [One-shot execution adapter](scientific-validation-v1-pilot-20261029/execute.py)
  (refuses existing outputs; do not rerun to obtain replacement observations)
- [Masked review package](scientific-validation-v1-pilot-20261029/masked-review.json)
  and [controller mapping](scientific-validation-v1-pilot-20261029/mapping.json)
- [Frozen provisional assessments](scientific-validation-v1-pilot-20261029/assessment.json),
  [revealed assessments](scientific-validation-v1-pilot-20261029/revealed-assessment.json),
  [all-response scorecard](scientific-validation-v1-pilot-20261029/scorecard.md), and
  [case summary](scientific-validation-v1-pilot-20261029/case-summary.json)

65 existing offline tests passed before execution; execution adapter compiled.
Post-run local integrity checks verified one HTTP attempt per unique planned slot,
original request/order equality, model/settings equality, successful checkpoint
metadata, response completeness, protected hashes and assessment/reveal binding.
No further paid calls, benchmark runs, cases or repetitions were added. No commit
or push. Collection and available exploratory evaluation are complete.

The supported conclusion is narrow: on these curated packs, explicit guidance
was associated with fewer assistant-identified unsupported financial assertions.
The pilot does not independently establish financial accuracy or a generalizable
causal benefit. Negative or disputed judgments remain visible for independent review.
