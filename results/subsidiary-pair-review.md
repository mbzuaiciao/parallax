# Subsidiary-recourse pair: manual evaluation

October 27, 2026 (America/Los_Angeles). All four independent `muse-spark-1.3`
requests completed with finish reason `stop`, without retries. Exact requests and
unchanged provider responses: [subsidiary-pair-live.json](subsidiary-pair-live.json).
References specified before submission: [case and calculations](../cases/subsidiary_pair.md).
All amounts below are USD millions; references were never sent to the model.

## Reference comparison

Both structures have parent cash 110, parent bond 100, subsidiary debt 80 and
subsidiary liquidation proceeds 20. Only B adds a parent guarantee. Subsidiary
lender first receives 20, leaving 60 unpaid and zero subsidiary equity. In B,
parent claims become 160 and share cash at `110/160 = 68.75%`.

| Live task | Parent guarantee claim: reference / model | Parent bond cash: reference / model | Guarantee cash: reference / model | Parent equity: reference / model |
| --- | --- | --- | --- | --- |
| A / equity | 0 / 0 | 100 / 100 | 0 / 0 | 10 / 10 |
| A / creditor | 0 / 0 | 100 / 100 | 0 / 0 | 10 / 10 |
| B / equity | 60 / 60 | 68.75 / 68.75 | 41.25 / 41.25 | 0 / 0 |
| B / creditor | 60 / 60 | 68.75 / 68.75 | 41.25 / 41.25 | 0 / 0 |

All four also correctly calculate the no-default comparison: subsidiary equity
distribution 30, parent cash 140, bond payment 100 and parent equity 40. Thus
parent equity loses 30 in A despite no subsidiary-debt liability, versus 40 in B.
Both B answers give subsidiary lender total recovery `20 + 41.25 = 61.25`,
or 76.56% of 80 at their reported precision.

## Five requested assessments

| Criterion | Observed result |
| --- | --- |
| Subsidiary debt versus parent obligations | All four distinguish the subsidiary's 80 debt from the parent's 100 bond. All report group gross borrowing principal as 180, not a single parent claim. |
| Guarantee creates parent payment obligation | A answers leave parent guarantee claims at zero. B answers identify the enforceable 60 parent claim after subsidiary recovery and distinguish it from 41.25 cash actually paid. |
| Shareholder loss without parent liability | Both A answers explicitly explain the lost subsidiary distribution: parent equity falls from 40 to 10 without parent payment of the subsidiary's 60 shortfall. |
| Effect on parent unsecured creditors | A answers keep the bond whole and identify indirect exposure through distributions. B answers correctly identify equal-ranked guarantee dilution and a 31.25 bond shortfall. |
| Paired facts preserved | Saved common evidence is identical after removing `parent_guarantee`. Responses retain both debt principals, cash inputs, ownership, zero interest, legal separation and payment priorities; none introduces a bailout or extra assets. |

The responses emphasize the selected investor while also discussing the other
class, as requested. This shows correct conditional analysis on these supplied
terms; it does not establish broader or repeatable model performance.

## Errors and unsupported conclusions

- **Numerical errors:** None observed in the reported claims, payments, recoveries,
  no-default comparisons or cash-conservation checks.
- **Legal-structure errors:** No material error observed. Ownership alone does not
  become parent liability; the B guarantee is correctly treated as a separate
  obligation. The stipulated enforceability is accepted without inventing recourse.
- **Investor-perspective reasoning:** No material allocation error observed. One
  sentence in B/creditor says full payment is “conditional on no subsidiary
  shortfall.” Read as a necessary condition, that is too broad: parent cash has
  10 headroom over the bond, so a guarantee claim up to 10 could coexist with full
  payment. The computed outcomes for the supplied two states are correct; this is
  a scope/wording caveat, not an observed arithmetic failure.
- **Citation accuracy:** All four cite `evidence.provenance`, but `provenance` is
  top-level in the user JSON. A/creditor and B/equity also put investor metadata
  under `evidence`; those fields are top-level. These are invalid field paths,
  not evidence of financial or legal misunderstanding.

No model response was corrected or resubmitted. No inference about market returns,
accounting recognition or general legal enforceability is warranted from this run.
All 22 deterministic and mocked tests pass. Original Harbor result files remain
byte-for-byte unchanged; `.env` remains ignored and untracked, and the saved
paired report was checked for the absence of the API key.
