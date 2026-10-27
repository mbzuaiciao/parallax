# Prompt guidance ablation: preliminary assistant comparison

**One sample per cell; 12/12 new calls completed, no retries or incomplete outputs.**
Model: `muse-spark-1.3`. This is an assistant-authored source-pack review, **not an
independent blinded human rating**. No overall accuracy percentage, statistical
significance or population-level effect is claimed.

## Audit trail and review status

The [protocol](../protocols/guidance-ablation-v1.md) and
[prompt/source snapshots](../protocols/guidance-ablation-v1.json) were committed and
pushed as `3ed7db3f2a4df733f16a1e3b08cb37496fc6250a` before the first submission.
The run began at that revision with a clean working tree. The
[original requests and full provider responses](guidance-ablation-v1-live.json)
retain every attempt, timestamps, source versions/hashes, request parameters,
completion status and code/client hashes. Exactly twelve calls were made: three
cases × two investors × two instructions. No repeated samples were executed.

[Reviewer materials](../reviews/guidance-ablation-v1/review.md) contain randomized
answer order, anonymized arm labels, unchanged answer text, evidence/reference
facts and a blank template. Give a future reviewer only that directory. The
[controller mapping](guidance-ablation-v1-condition-map.json), this report, raw run,
protocol and historical answers must be withheld until assessments are recorded.
[Assistant assessments](../assessments/guidance-ablation-v1-preliminary.json) were
recorded on anonymous IDs before the reveal command generated the
[hash-bound reveal](guidance-ablation-v1-revealed.json). Arm X is guided; Arm Y is
neutral. The assistant designed the experiment and could infer conditions from
style; this sequence does not establish independent blinding. No human reviewer
has been recruited or rated these answers. The original blank template remains blank.

## Matched comparisons

| Case and investor | Guided answer | Neutral answer | Preliminary difference |
|---|---|---|---|
| NVIDIA equity | R004 | R002 | Both identify contingent support, exclusivity benefit, reimbursements and discretionary expansion. Guided says no-trigger cash impact is zero despite unknown pre-RFS/other costs. Neutral calls105bn maximum cash exposure and says optional support would materially expand exposure beyond it, without terms establishing the magnitude. |
| NVIDIA senior unsecured | R012 | R001 | Both explain cash-call and recovery timing. Guided explicitly refuses a creditor-ranking conclusion. Neutral defaults to pari passu, labels reimbursement unsecured, and calls105bn maximum LGD before recoveries. These conclusions are not established by the pack. |
| Meta equity | R009 | R007 | Both retain14.72bn/five years, provider anonymity and resale reduction. Guided recognizes usable capacity rather than pure loss; neutral emphasizes distribution/flexibility costs and defaults to an unsecured executory contract despite missing security terms. Guided's categorical “must not be treated as a liability” is itself too broad. |
| Meta senior unsecured | R006 | R003 | Guided discusses conditional liquidity and unknown ranking but omits the commercial value of capacity. Neutral adds “de facto” operating priority, presumed need-based drawing, mandatory funding/debt and default-risk conclusions. Its zero-mitigation prescription is an assumption, not evidence. |
| CoreWeave equity | R008 | R010 | Both preserve already-recognized recourse financing and dated balances,12% return and100m settlement. Guided keeps refinancing/service scenarios conditional. Neutral attributes a16m roll-forward residual entirely to accretion and introduces issuer-wide asset-debt facts absent from the pack. |
| CoreWeave senior unsecured | R011 | R005 | Both cover termination liquidity, service deductions and unknown priority. Neutral nevertheless excludes structural subordination and compares settlement to unspecified unsecured maturities. Guided incorrectly treats profit sharing/reallocation as a possible refund/recovery offset; no such mechanism is disclosed. |

### Contractual identification and numeric reasoning

The basic mechanisms survived neutral instructions: NVIDIA residual-value guaranties,
Meta's own contingent capacity purchases, and CoreWeave's recognized in-substance
recourse debt. None substituted a named supplier for Meta's undisclosed provider.
Core amounts and dated balances remained stable across perspectives and conditions.
A contractual cap, carrying value and actual cash settlement were generally kept
separate; neutral NVIDIA's LGD formulation is a notable conceptual exception.

No clear arithmetic mistake was found in the shown calculations. Neutral Meta's
14.72/349.31 ≈4.2% and14.72/5 ≈2.9bn are correctly calculated, explicitly illustrative,
and are not a disclosed annual payment schedule or a leverage ratio. Neutral
CoreWeave's273−100 leaves173 and189−173=16 is also correct arithmetic. Calling all16
additional accretion requires a complete roll-forward; that attribution and implied
compounding are unsupported, rather than a numerical subtraction error.

A post-reveal reading also notes a taxonomy weakness: guided CoreWeave answers list
recognized carrying amounts alongside “direct obligations”; accounting measurement
is not an additional contractual promise. The pre-reveal assessments are preserved
unchanged; this additional observation is identified as post-reveal, not retroactively
presented as a masked judgment. Guided NVIDIA creditor similarly lists Tenant Parent
among direct obligors while describing its separate guarantee. These do not change
the correctly identified issuer obligations, but show guidance does not ensure clean
classification.

### Investor consequences, omissions and confidence

Both arms change priorities sensibly without changing the evidence: equity focuses
on distributions, financing cost, service economics and exclusivity; creditors focus
on liquidity calls, competing claims and reimbursement timing. Different final
recommendations or numerical exposures are not required.

The clearest sensitivity is **confidence in extrapolation**, particularly neutral
creditor statements about rank, default risk, funding and recovery. Neutral answers
also offer useful commercial narratives, while sometimes assuming demand, inflexibility
or current accounting not disclosed. A conditional scenario is legitimate; a statement
that the provider *will* bear/transfer all cost, or that cash *must* be funded through
operating cash or new debt, needs more evidence.

Omissions are not false assertions. Guided Meta creditor's failure to weigh capacity
consideration and neutral Meta equity's lack of an explicit offsetting-value discussion
are coverage concerns. Conversely, default unsecured/pari-passu conclusions are
unsupported assertions. NVIDIA's repeated guided “no trigger → zero cash” claim is
overconfident given redacted pre-RFS/keep-current terms, not simply omitted detail.
CoreWeave's guided profit-share offset error is a counterexample to any claim that
guidance uniformly improves reasoning.

### Uncertainty, citations and cross-investor consistency

All twelve acknowledge important absent inputs: complete contracts, precise payment
mechanics, counterparty capacity, priority and future schedules. Several neutral
answers contradict their own ranking caveats later. A missing disclosure is not zero.
Payment probabilities/expected losses, creditor recoveries, valuation adjustments and
full future cash schedules remain **unscorable**, with no numeric ground truth assigned.

Document IDs or exact accessions/URLs and supplied note/section locations correspond
to the source packs. No invented source was identified. Neutral often uses broader
note-level citations; that is not automatically an error. Unsupported conclusions do
not acquire support from adjacent correct citations. This review checks those supplied
locations and factual support in the packs; it does not claim independent verification
of every phrase against complete filings. Some quoted text is taken from supplied
paraphrases and should not be assumed to be verbatim SEC text. Fiscal2029 and
calendar2028 forecasts are not inherently conflicting dates.

Within each arm, issuer, mechanism, amounts and core terms are stable across investors.
Changes in economic emphasis are justified; new legal ranking or payment facts are
not justified merely by changing investor perspective.

## Supplementary history and limits

The earlier NVIDIA investor-pair and Meta/CoreWeave benchmark runs remain unchanged.
Their [NVIDIA review](nvidia-ports-investor-pair-review.md) and
[three-case review](benchmark-review.md) are supplementary context, not additional
matched observations. The earlier drafts already noted classification, one-sided
commercial analysis and settlement interpretations; the new guided sample does not
eliminate those concerns. Do not pool historical runs to manufacture replication.

This compares developer instructions conditional on highly curated evidence that
already names mechanisms and cautions about missing terms. It is not evidence of
unaided extraction from filings. One sampled response per cell, nonrandom companies,
possible model familiarity, imperfect masking and assistant judgment limit inference.
Reference provenance remains Wagner v1.1, revision
`98c8bba76a453e117f4b07de1881e4f5e08dd8f6`, CC BY4.0, as recorded in the unchanged packs.
No new financial ground truth, company, source or model was introduced.

**Next experiment, not implemented:** preregister repeated independent samples of
this same matrix and obtain independently recorded masked reviews before revealing
conditions. That would test whether the apparent reduction in unsupported creditor
inferences persists across sampling variation, without expanding the sample of cases.
