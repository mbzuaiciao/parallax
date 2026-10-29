# Scientific validation v1 — audit reconciliation

October 29, 2026. Compared the current working tree with
`scientific-validation-v1-review.md` and
`scientific-validation-v1-ground-truth-audit.md`. This note is a reconciliation by
the preparing assistant, not independent human verification or execution approval.
Neither audit report was rewritten.

## Snapshot mismatch

| Finding repeated in the ground-truth audit | Working tree before this reconciliation | Disposition |
| --- | --- | --- |
| Meta M3 remains a core factual target | `core_factual_targets` and `source_checked_facts` contain only M1/M2. M3 is already in `evaluation_guidance`, type `inference_constraint`, with its substantive wording retained. | Already corrected; no further move needed. Omitting M3 is not a factual-coverage error. |
| Apple `short_quote` is empty | Populated with an Item 7 verbatim excerpt and a source-inspection record. | Already corrected; fixture unchanged. |
| Microsoft `short_quote` is empty | Populated with the Note 1 lease-recognition sentence and a source-inspection record. | Already corrected; fixture unchanged. The audit's proposed prose reconstruction of table cells was not substituted for this verbatim sentence. |
| There are 15 core factual targets, including M3 | There are 14 core factual targets, plus M3 evaluator guidance. | Audit tally describes the earlier target structure. |

The first review identified these defects before the minimal corrections. The
later ground-truth audit repeats those earlier descriptions despite the current
corrections. Its description therefore does not match the working tree. Neither
report binds its reviewed files with content hashes; an outdated or mixed snapshot
is the likely explanation, but the precise files actually inspected cannot be
reconstructed from the reports. This mismatch is not evidence that the current
corrections disappeared, nor does it invalidate every other audit observation.

The observed pre-reconciliation fixture SHA-256 values were:

- `apple.json`: `e1cd190d1c846b8838cf40b176e1d61f180af75f44be4640dc38a08081118eea`
- `microsoft.json`: `3a2ca03a35786750da9732ef73f6fe53529856913db1bc2c55788dd91a36786a`

Both remain unchanged. Future reviews should record the generated plan's hashes
and explicitly distinguish reference version, filing date and review date.

## Apple accounting distinction

The audit is right to challenge wording that could penalize an ordinary accounting
explanation: an unperformed ordinary executory purchase commitment generally does
not become a gross recognized payable solely because it has been agreed. A model
may explain that principle without supplying an exact carrying amount.

The audit goes further by recommending a definite issuer-specific zero. That does
not follow from the selected Item 7 disclosure. It reports manufacturing purchase
obligations and timing, rather than a reconciliation of recognized payables or
reserves. The same [Apple 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm),
Item 1A, paragraph under the inventory write-down and purchase-commitment
cancellation risk heading, describes accrual of cancellation-fee reserves for
excess orders. This supports caution about a blanket zero assertion; it does not
quantify a balance attributable to this selected commitment aggregate.

Separate the gross commitment, recognition of delivered goods/payables, and any
cancellation or loss accrual. This is a qualified interpretation, not a newly
verified accounting target. The selected evidence cannot establish the precise
overlap or balance, and this reconciliation does not assert that a positive
amount has been measured either. The audit's timing-based NVIDIA zero and Meta
nonrecognition statements likewise do not replace the existing evidence-limited
reference boundaries with certified carrying balances.

Only Apple's accounting statement/scoring rule and the protocol's corresponding
explanation needed clarification. Credit the qualified general principle and
justified uncertainty; continue to reject an unsupported exact balance. The Item
1A check is reconciliation context, outside the frozen model evidence: no response
is required to mention cancellation reserves absent from its supplied pack.

## Preservation and remaining review

All five `status` and `independent_verification` records remain unchanged and
provisional/pending. The audit's claims of verification are not human sign-off.
No core facts, historical results, evidence fixtures, prompts, conditions or sample
counts were changed. The design remains five cases × two conditions × three
repetitions, with 30 planned responses. Existing offline tests cover M3 placement,
populated quotes, provisional status, evidence equality and the 30-slot plan.

Ready for independent ground-truth review, not execution. Independent reference
approval and the previously documented provider-readiness gaps remain unresolved.
