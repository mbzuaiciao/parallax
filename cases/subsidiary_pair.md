# Subsidiary debt: contractual liability versus economic exposure

This reference was specified before the live requests. All figures and legal
premises are synthetic; no real-company or general legal/accounting claim is made.
See [subsidiary_pair.json](subsidiary_pair.json) for the complete contractual inputs.
All amounts are USD millions, settled on December 31, 2027.

## Paired design

Cedar Holdings owns 100% of Cedar Operations. Parent has 110 of standalone net
cash and a 100 senior unsecured bond. Subsidiary owes 80 to an external lender;
its default liquidation produces 20. Both debts bear zero interest and are due
at settlement. Parent cash excludes the subsidiary and all value of its stake.
Pay subsidiary lender first, then settle parent claims. No other claims, cash
flows, support commitments or legal recourse exist.

**A:** Subsidiary debt is legally non-recourse to parent; no parent guarantee exists.
**B:** The only changed input is an enforceable parent guarantee of unpaid subsidiary
principal after subsidiary liquidation, capped at 80. This creates a parent claim
that ranks equally with the parent bond and settles simultaneously. There is no
double recovery, reimbursement or remaining subsidiary asset recovery. The cap
limits the claim; it does not promise full payment when parent cash is insufficient.
Entity separation and enforceability are stipulated facts, not matters the model
must infer from an unspecified jurisdiction.

Both cases include the same no-default comparison: subsidiary proceeds would be
110, while all other financial inputs and contractual terms stay fixed. This is
a same-date conditional comparison, not a historical carrying value, probability,
return or market valuation. It creates a measurable foregone subsidiary equity
distribution without assuming that ownership itself creates parent liability.

## Independently checkable reference answers

Subsidiary default pays `min(20, 80) = 20` to its lender and leaves no subsidiary
equity distribution. Remaining subsidiary debt is `80 - 20 = 60` in both cases.

| Quantity | A: no guarantee | B: parent guarantee |
| --- | ---: | ---: |
| Parent bond contractual claim | 100 | 100 |
| Subsidiary debt contractual claim | 80 | 80 |
| Group gross borrowing principal (defined sum) | 180 | 180 |
| Subsidiary lender payment from subsidiary | 20 | 20 |
| Subsidiary equity distribution to parent | 0 | 0 |
| Triggered contractual claim against parent under guarantee | 0 | 60 |
| Total parent contractual claims | 100 | 160 |
| Parent cash pool in default | 110 | 110 |
| Parent bond payment | 100 | 68.75 |
| Parent bond claim recovery | 100% | 68.75% |
| Guarantee cash payment from parent | 0 | 41.25 |
| Subsidiary lender total cash recovery across entities | 20 | 61.25 |
| Parent equity distribution in default | 10 | 0 |
| No-default subsidiary equity distribution | 30 | 30 |
| No-default parent equity distribution | 40 | 40 |
| Decline in parent equity distribution versus no default | 30 | 40 |

In B, parent claims share cash at `110 / (100 + 60) = 0.6875`. Thus bond payment
is `100 × 0.6875 = 68.75`, and guarantee payment is `60 × 0.6875 = 41.25`.
Both parent claims receive 68.75% of what is owed. Subsidiary lender receives
`20 + 41.25 = 61.25` of its original 80, leaving 18.75 unpaid. Total cash distributed
across the two entities is 130 in either case; the guarantee reallocates it.

In the no-default comparison, subsidiary equity distributes `110 - 80 = 30`,
so parent equity receives `110 + 30 - 100 = 40` in both structures. In A, subsidiary
default removes that 30 distribution and reduces parent equity to 10 without any
parent contractual liability for subsidiary debt. B additionally reduces parent
equity by 10 and parent bond payment by 31.25 relative to A, totaling the 41.25
guarantee payment. The subsidiary-equity loss and the guarantee are distinct channels.

Group gross borrowing principal remains 180: adding the guarantee claim to that sum
would double count recourse on the same underlying subsidiary debt. Parent contractual
claims do differ, 100 versus 160 after subsidiary recovery. Neither is a supplied
debt-to-EBITDA ratio or a statement about accounting recognition. A parent creditor
has indirect economic exposure to lost subsidiary distributions in either structure,
even though the stipulated A cash pool still pays its bond in full.

## Reproduce

```sh
uv sync --locked
uv run python -m parallax.paired --all
uv run python -m unittest discover -s tests -v
uv run --env-file .env python -m parallax.paired --evaluate --output results/subsidiary-pair-live.json
```

The preview contains only model payloads. References are computed locally and saved
alongside, never inside, live requests. Requests are independent, ordered A/equity,
A/creditor, B/equity, B/creditor. Only `evidence.parent_guarantee` changes between
paired evidence objects; structure identifiers are metadata. Existing results are
preserved, and output filenames cannot be overwritten.
