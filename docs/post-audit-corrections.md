# Post-audit corrections — October 29, 2026

Scope: ENG-01, FIN-01, FIN-02, ENG-02 and scientific framing from
`research/independent-audit-antigravity.md`. No new experiment or live model call.
No repository AGENTS.md was present.

## Primary-source checks and corrections

The SEC archive documents below were opened and read on October 29, 2026.
Their issuer, form and reporting period agree with the existing case document
catalogs; reference facts resolve to those document IDs. The demo header accessions
were wrong and are corrected to:

| Issuer | Form | Accession | Primary document |
| --- | --- | --- | --- |
| NVIDIA | 8-K | 0001045810-26-000069 | [Item 1.01](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm) |
| NVIDIA | 10-Q | 0001045810-26-000075 | [Notes 8 and 17](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm) |
| Meta | 10-Q | 0001628280-26-050705 | [Note 9; also MD&A contractual commitments](https://www.sec.gov/Archives/edgar/data/1326801/000162828026050705/meta-20260630.htm) |
| CoreWeave | 10-K | 0001769628-26-000104 | [Note 10, Magnetar Loan](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) |
| CoreWeave | 10-Q | 0001769628-26-000366 | [Note 10, recourse debt table and Magnetar Loan](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm) |

**CoreWeave:** The annual note explicitly reclassifies the refundable deposit as
in-substance debt under ASC 470 following the February 2025 amendment. It reports
$273m at December 31, 2025, including $43m redemption premiums, and a $230m original
deposit with a termination multiplier equivalent to a 12% annual return. The
quarterly note reports a $100m June 2026 partial settlement and a $189m June 30
balance comprising unused deposit and accrued premiums; the table places it under
recourse debt, at 12%, maturing January 2029. The demo now separates the dated
amounts, labels the original deposit as financing received rather than a cap, and
presents recognized financing in the scenario view. The June premium component
and future payoff are not inferred. The existing case pack and reference facts
C4/C5 already distinguish the dates correctly; the audit's reference-dataset
period-conflation allegation is not supported by their current contents.

**NVIDIA:** The 8-K and Note 17 describe the $105bn PORTS cap and conditional
payments, not a separately measured PORTS liability balance. The signing was in
August, after the July 26 balance-sheet date. Note 8 describes credit derivatives
with insignificant fair values for a separate AI-cloud guarantee group, whose
$3.5bn exposure is separately listed in Note 17. That is not proof of PORTS
classification or a zero PORTS liability. The demo removes its unsupported zero
assertion and marks the carrying amount as not separately established. Neither a
zero nor a positive PORTS accounting balance is verified here. The preserved
Wagner annotation mentioning credit derivatives is research coding, not independent
evidence of PORTS accounting treatment. The current NVIDIA case paraphrases do
not themselves assert a zero recognized liability.

**Meta:** The disclosure states an up-to $14.72bn purchase amount over five years,
subject to third-party sales offsets. The overview now displays the complete
amount instead of the first whitespace-delimited word, “Up”.

## Scientific scope and preservation

README now explicitly distinguishes financial interpretation of curated disclosure
summaries from autonomous extraction or discovery in raw filings. CoreWeave remains
an on-balance-sheet comparison case. Both neutral and guided conditions remain
available and unchanged; neutral still receives curated evidence.

Cases, reference answers, research annotations, request builders, protocols,
assessment files, review packages, evaluation outputs and experimental results
are preserved byte for byte. No accounting ground truth was silently rewritten.
Independent human adjudication, larger samples and the other audit proposals
remain outside this correction scope; the existing pilot is not statistical or
independent validation. PORTS liability measurement remains unresolved.

## Verification

Focused offline regressions cover all catalog/header accessions, the exact Meta
metric, NVIDIA's unknown carrying amount, and CoreWeave's deposit/balance displays
across the affected views. Existing request-equality and ablation hash checks
continue to protect experimental compatibility. Full unittest discovery passes
58 tests. No dependency or infrastructure change.
