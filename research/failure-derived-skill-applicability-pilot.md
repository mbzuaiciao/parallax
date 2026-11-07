# Research objective: Failure-derived credit reasoning skill with applicability examples

**Status:** Proposed exploratory pilot; not yet executed.  
**Recorded:** 2026-11-07.  
**Inference provider:** Baseten (availability believed to end November 9, 2026; access must be verified before any call).  
**Scope:** One skill, three prompt/harness conditions, small held-out evaluation; no weight updates or autonomous harness mutation.

## Objective

Test whether a general credit-reasoning principle, extracted from an observed Parallax failure and accompanied by *positive and negative applicability examples*, improves the quality of financial analysis on unfamiliar cases compared with the existing harness and the principle alone.

This is a controlled **human-reviewed skill-design experiment**, not yet a demonstration of autonomous skill discovery, self-improving agents, or new model capabilities.

## Motivation and candidate skill

Historical reviews of NVIDIA, Meta, CoreWeave, and Disney/Hulu show cases of unsupported legal, accounting, and stakeholder conclusions, as well as useful analysis omitted when instructions become overly cautious. Existing assessments are mainly assistant-authored and provisional: they are starting points for proposing a skill, not independently adjudicated ground truth.

**Candidate principle:** Distinguish (1) contractual exposure or commitments, (2) recognized accounting liabilities and their dated carrying measurements, and (3) cash payment actually due under specified triggers and timing. Never substitute one measure for another without evidence.

**Positive applicability example (to be finalized without using evaluation answers):** A disclosed maximum contingent guarantee cap is not automatically a current cash payment or its recognized balance-sheet carrying value. Explain the trigger and explicitly state which measurements are unknown.

**Negative/boundary example (to be finalized):** When the disclosure explicitly establishes a presently due payment and its amount, do not withhold that obligation simply because some other contingent exposure or accounting measurement remains unknown. Apply uncertainty only to what is genuinely unresolved.

The examples must be **distinct from held-out cases**. The positive example illustrates appropriate use; the negative example illustrates how overapplication of the principle could lead to an omission. Neither example is a claim about a new issuer without source evidence.

## Experimental arms

| Arm | Intervention |
| --- | --- |
| A — Existing harness | Current Parallax instructions, unchanged. |
| B — Principle | Identical harness plus the general principle. |
| C — Principle with examples | Identical harness plus the exact same principle and one positive and one negative applicability example. |

Hold constant: model/version where possible, supplied case evidence, financial question, inference parameters, output requirements, and available tools. Record exact raw requests and responses. Prompt length differs across arms; therefore any observed C-versus-B difference cannot automatically be attributed uniquely to *negative* examples (rather than examples/extra tokens generally).

## Data and evidence

- Current five-case real-world workstation: NVIDIA PORTS, Meta cloud capacity, CoreWeave deposit, Apple purchase commitments, Microsoft leases.
- Existing historical benchmark registry contains **three** of those five; a scientific-validation protocol expands to five cases but is **design only** (5 cases × 2 prompts × 3 samples = 30 planned responses, not 30 unique disclosures).
- Synthetic Harbor and Cedar scenarios are distinct from real-world SEC disclosure cases.
- The separately archived Disney/Hulu Baseten pilot supplies a detailed *candidate failure* and claim-level audit, not an untouched test case.
- Existing source packs and assistant-authored assessments are not independently certified ground truth. Reference judgments must be verified against the relevant primary evidence before scoring.

The previously suggested **20 cases** was a prospective pilot size, not an existing count. Do not treat investor perspectives, repeated generations, or different prompt arms over the same case as independent disclosures. For a small pilot, create a modest set of *new, independently checked* held-out contractual scenarios with both applicability and nonapplicability examples; do not invent quantitative credit metrics or legal conclusions unsupported by the source.

## Evaluation

Predefine a simple case-level checklist before inference:
1. **Factual/evidential correctness:** contractual party/obligation/trigger/amount/timing supported by supplied evidence; separate wrong statements from unsupported claims and justified unknowns.
2. **Economic usefulness:** preserves material, source-supported stakeholder implications and doesn't replace them with generic caveats.
3. **Applicability and regressions:** uses the principle when relevant but does not suppress justified conclusions in nonapplicable cases.

Use paired comparisons for the **same case** across arms, show case-level reasons and original answer excerpts, and retain failures/omissions as well as improvements. Do not convert heterogeneous claim-group counts into accuracy scores or assert statistical significance from a small purposive pilot. Ideally use an independent evaluator blind to arm labels; if unavailable, label reviews preliminary/assistant-authored.

## Minimum execution sequence

1. Select **one** documented failure; draft and human-review principle plus two examples.
2. Create and source-check a small set of held-out cases before inspecting new outputs; include counterexamples where over-caution is harmful.
3. Freeze cases, references, exact instructions, scoring checklist, inference configuration, and request budget.
4. Verify Baseten model access and remaining credits, then run the three arms on exactly the frozen cases; preserve request/response provenance. Never automatically retry failed or timed-out calls.
5. Review each case across arms, report supported claims, unsupported claims, useful omissions, and regressions. Stop.

**Stopping rule:** Complete a single preregistered exploratory comparison, or stop early if suitable independent reference judgments or Baseten access are unavailable. No automated skill evolution, RL/SFT, multi-model comparison, dataset-building platform, or infrastructure expansion in this phase.

## Interpretation and next step

The motivating hypothesis is **C improves applicability boundaries and generalization without material regression relative to B and A**. A null or adverse result is a valid endpoint. A positive small pilot is only exploratory evidence, not a claim that the agent autonomously learns skills; that future capability would require an additional experiment where the agent itself proposes candidate principles and the promotion/rollback decision is evaluated on held-out data.

## Related repository material

- [Guidance ablation preliminary review](../results/guidance-ablation-v1-preliminary-review.md)
- [Existing benchmark method and limits](../docs/benchmark.md)
- [Scientific validation design-only protocol](../protocols/scientific-validation-v1/protocol.md)
- [Disney/Hulu Baseten audit PR #4](https://github.com/mbzuaiciao/parallax/pull/4)
- [Disney/Hulu contractual checks draft PR #6](https://github.com/mbzuaiciao/parallax/pull/6)

**This file records the research objective and plan only.** No live inference, benchmark edits, case fabrication, or implementation work accompanies it.
