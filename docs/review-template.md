# CASE — contractual-obligation review

- Reviewer, review type (`human` or `assistant_draft`), date:
- Run path and SHA-256; evidence/reference versions:
- Status of each attempted call (include failures and truncation):
- Information cutoff; primary source documents/provisions:

## Documentally checkable properties — requires source comparison

| Field | Recorded status | Response excerpt | Primary document/provision | Rationale |
| --- | --- | --- | --- | --- |
| Obligors / beneficiaries | not_reviewed | | | |
| Direct / contingent / optional obligations | not_reviewed | | | |
| Contractual limits / triggers | not_reviewed | | | |
| Explicit disclosed amounts, units and dates | not_reviewed | | | |
| Citation identifiers, location and claim support | not_reviewed | | | |

These properties can be checked against disclosures, but free-text identification
and citation support are semantic tasks. The tool does **not** mark them correct.
Use `supported`, `concern`, `missing`, `unscorable`, or `not_reviewed`; explain scope.
Unknown security, probabilities or recovery amounts are not zero-valued targets.
Capture errors separately from absent input; do not penalize a justified refusal
to quantify. Recognized source/location IDs alone do not validate any claim.

## Judgment-dependent review

- Investor implications: justified focus, benefits versus burdens, no forced differences.
- Missing information: acknowledged, missed, or insufficient to assess.
- Unsupported assumptions / overconfidence: quote and explain.
- Pair consistency: facts preserved; justified shifts versus changed facts.
- Comparison to Wagner: agreement and disagreements, separating researcher coding
  from independently checked primary facts. Do not import undisclosed identities.

## Findings and limits

Concise result; unresolved disagreements; missing/unscorable fields; next experiment.
No composite accuracy score. Identify assistant drafts honestly; a human second
rater should independently check primary sources before treating them as ratings.

Use `uv run python -m parallax.benchmark assess-template CASE --run RUN.json
--output assessments/NEW.json` for a machine-readable draft, then record the same
review content there. Add human-entered citations as document/location IDs from the
case reference catalog. `summary` renders recorded assessments and protocol checks,
not automated factual grading.
