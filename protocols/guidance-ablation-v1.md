# Preregistered prompt-guidance ablation — v1

Written before the twelve new live calls. This narrative and its JSON companion
must match committed Git bytes before the runner starts. No outcomes belong here.

## Hypothesis and controlled conditions

Removing detailed developer guidance may reduce coverage of contractual conditions
and uncertainty, or increase unsupported financial assertions. It may also produce
more natural investor-specific economic discussion. Correct neutral answers and
identical warranted conclusions across investors are valid results. No directional
effect, significance claim or overall accuracy percentage is required.

Use exactly the existing NVIDIA PORTS, Meta capacity-purchase and CoreWeave deposit
source packs, registry, historical cutoffs, references and two issuer investor
identities. One new sample per case × investor × condition = **12 independent calls**.
Historical guided calls are supplementary only, not replacements for new guided
calls or matched observations in this experiment.

**Guided:** the developer message from `parallax.benchmark.request_for` is preserved
exactly. The companion JSON snapshots each full instruction and request hash.

**Neutral:** replace only that developer message with this template, substituting
the same investor identity (including the same company name):

> Analyze the supplied financing arrangement from the perspective of {investor}.
> Explain its economic significance, cite supporting evidence, and identify material uncertainties.

No extra cautions, anticipated errors or target conclusions are added to neutral.
The user evidence message, model `muse-spark-1.3`, endpoint, token budget and all other
request parameters remain byte-identical within a case/investor pair. API sampling
defaults are unchanged. No seed guaranteeing model determinism is asserted.
Neither prompt receives annotations, reference facts, historical answers or reviews.

## Schedule, retention and repetitions

Shuffle the complete matrix once with execution seed `20261027` before submission;
the JSON records the exact schedule. Each cell is a fresh conversation, with no
carryover response or automatic retry. Preserve exact requests and full provider
JSON, status, error/incomplete results, timestamps, source/protocol hashes and code
revision. Report every attempt; absent or truncated answers do not silently vanish.
Interrupted cells remain in-progress/pending; restarting is not automatic resumption.

The runner accepts future repetition counts, but this preregistration permits
**one** only. Future repetitions require a new committed protocol with the matching
sample count; do not run them during this milestone. Do not alter source packs,
prompts, evaluation criteria or references in reaction to results.

## Prespecified review criteria

Reuse the existing five documentally checkable categories:
`obligors_beneficiaries`, `obligation_classification`, `limits_triggers`,
`disclosed_amounts`, `citations`. These still require source-based semantic review;
word matches and recognized citation IDs do not prove correctness or claim support.

Reuse the three judgment categories: `investor_implications`, `missing_information`,
`unsupported_assumptions`, plus case/condition consistency between perspectives.
Equity discussion should weigh disclosed consideration and possible cash burdens;
creditor discussion should consider liquidity and claim uncertainty without invented
priority or recovery. Similar conclusions may be appropriate. Differences in length
alone are neither benefit nor failure.

Record `supported`, `concern`, `missing`, `unscorable`, or `not_reviewed`, with literal
answer anchors and primary-source rationale where material. `Supported` is scoped
review judgment, not a claim that every statement is true. Mixed correct/error
content can be `concern`, and the rationale must distinguish the two.

- **Omission:** available, material evidence is not discussed. Use `missing` for an
  absent category; if partially covered, explain the omission without calling the
  unmentioned fact false. Optional detail and verbosity are not mandatory targets.
- **Incorrect assertion:** a stated claim conflicts with evidence. Use `concern`
  and identify the claim/provision. Do not manufacture ground truth to find errors.
- **Unsupported confidence:** definite accounting, payment, legal or quantitative
  conclusions exceed the evidence even if not demonstrably false. Separate these
  from appropriately qualified possibilities and justified refusals to quantify.
- **Investor-specific omissions:** flag failure to discuss material consideration,
  cash-use tradeoffs or claim uncertainty pertinent to that investor. Explain the
  economic channel rather than demanding a different number or recommendation.
- **Missing inputs:** unknown ranking, probabilities, future payments and recoveries
  are `unscorable` where not disclosed, not zero-valued answers or model mistakes.
- **Citations:** assess source ID, provision location and whether the passage supports
  the assertion separately. Broad correct citations can be adequate; do not require
  clause-level precision when the source pack provides only a note-level locator.

## Review preparation and unblinding

Generate unique response IDs, randomized presentation order and two anonymized arm
labels. Hide developer prompts, true conditions, execution index, timestamps,
provider IDs and token usage. A separate controller mapping retains randomization
seed and condition identities. The reviewer package may contain company, investor,
cutoff, unchanged evidence, reference facts, completion status and original answer
text. Errors/incomplete answers remain visible; missing text is not invented.

Give a future independent reviewer **only** that package, not raw runs, this protocol,
mapping, outcome reports or historical answers. Record category rationales and
case/arm pair consistency before using the reveal command. The reveal gate binds
assessment bytes and checks completion of review fields; it cannot prove a reviewer
did not access the mapping. Answer style can itself reveal a condition, so masking
is imperfect. Within-answer words are not redacted to make masking appear stronger.

No human reviewers are invented. The initial comparison will be clearly labeled
**preliminary assistant review, not an independent blinded human rating**. The
assistant authored the design and may infer condition from response style even if
it records assessments on anonymized IDs before opening the mapping. A reusable
blank template stays separate from any assistant-filled assessment.

## Analysis plan and limitations

Describe coverage, factual drift, unsupported claims, uncertainty, evidence quality
and investor-priority differences within each matched pair. Assess consistency
between investor answers within condition. Do not compute overall accuracy,
p-values, significance, causal population effects or an aggregate ranking from
one sample. Report uncertainty and counterexamples, not only the hypothesized effect.

Curated paraphrases already name mechanisms and contain caveats, so neutral developer
instructions do **not** create unguided evidence. This isolates developer-guidance
removal conditional on that pack, not unaided full-filing extraction. Cases are
nonrandom, model familiarity/contamination is uncontrolled, generation is sampled,
and response lengths may differ. Reference interpretations and assistant judgments
remain fallible. Reusing a reference set and same reviewer limits independence.
Retain historical guided results only as contextual supplementary comparisons.
