# One real-world disclosure case: NVIDIA PORTS

This is a historical disclosure-comprehension evaluation of one arrangement, not
a new quantitative financial model or a statement about current NVIDIA risk.
The information cutoff is August 26, 2026. No synthetic cash pool, default probability,
loss estimate, creditor ranking or recovery waterfall is supplied.

## Provenance and selection

Alexander F. Wagner, *Leverage Beyond Debt: Evidence from the AI Build-Out (data)*,
2026, version 1.1, accompanies his working paper of the same title. The repository
describes the author's reading of filings, invites corrections, and does not claim
its annotations are adjudicated legal facts or statistically estimated risks.

Inspected snapshot: [`98c8bba76a453e117f4b07de1881e4f5e08dd8f6`](https://github.com/alex-wagner-research/leverage-beyond-debt/tree/98c8bba76a453e117f4b07de1881e4f5e08dd8f6),
retrieved October 27, 2026. Reviewed README, codebook, CITATION.cff, CHANGELOG,
LICENSE and the linked CSV tables. The snapshot contains 37 firm-period rows,
155 contracts, 243 instruments, 203 entities and 475 evidence passages. Its
[changelog](https://github.com/alex-wagner-research/leverage-beyond-debt/blob/98c8bba76a453e117f4b07de1881e4f5e08dd8f6/CHANGELOG.md)
describes v1.1 as an October revision without changes to values, rows or IDs.

Selected only contract `HL-0001` and instrument `HL-0001a`, the PORTS residual-value
guaranties. This is an intentionally well-documented, nonrandom selection; no
population-level model-accuracy claim follows. The cap, timing, triggers and
remedies can be checked against primary SEC disclosures, rather than accepting
the dataset's interpretation as ground truth.

Primary sources, independently opened and read:

- [August 17, 2026 Form 8-K, Item 1.01](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm): parties, cap, payment conditions, reimbursement and summary terms.
- [Form 10-Q, Note 17, SB Energy Corp. guarantees](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm): timing/phasing, covered payments, exclusivity and optional capacity. [SEC index](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/0001045810-26-000075-index.htm) confirms filing August 26, 2026 and reporting period July 26, 2026.
- [Exhibit 10.1, Form of Residual Value Guaranty](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda2027q2ex101.htm): sections 1, 2, 5, 8, 12 and 20(e) refine the summary. It is a partly redacted form, with blank execution/counterparty fields, not a complete executed agreement.

## Evidence separation and reference checks

[`nvidia_ports.json`](nvidia_ports.json) contains only a manually curated primary-source
pack: clearly labeled factual paraphrases, short quotations and document/provision
citations. Paraphrases are Parallax's adaptations of the disclosures, not verbatim
filings or Wagner's text. They preserve redactions and qualifications. This tests
reasoning over selected source context, **not blind extraction from full filings**;
curation and explicit prompt cautions make it an easier test. Full source URLs
allow inspection, but the model receives no browsing tools.

[`wagner_reference.json`](wagner_reference.json) is kept separate and is never
loaded by the prompt builder. It contains selected original string-valued columns
from the two research rows, evidence IDs/locators, source file hashes, attribution
and independently written codebook summaries. The dataset's converted-text line
numbers are not SEC HTML line numbers. One evidence note (`EV-0019`) expressly
identifies a coder's remedy-menu gloss; that gloss was not used as primary text.

Pre-specified checks, not numerical loss targets:

- Parties, contingent support, disclosed shared cap and delayed effectiveness must
  be checked against the primary documents, not inferred from a research label.
- Compare the extracted structure against the annotation's cap type, contingent
  flag, triggers, reimbursement, remedies and C2/L3 treatment. C2 excludes a
  not-yet-effective guarantee from the lower bound but includes it in gross/upper;
  a blank lower cell is not an observed zero liability. Dataset amounts are USD
  billions and its bounds are not probabilities, loss forecasts or GAAP balances.
- Independently assess equity versus NVIDIA senior unsecured creditor reasoning.
  Do not import the synthetic cases' equal-ranking assumption. Reimbursement is
  a contractual right, not assured collection from a stressed counterparty.
- Wrong-way and vendor-customer flags are qualitative researcher labels; evaluate
  any corresponding narrative cautiously, without treating correlation or loss
  magnitude as independently verified.

## Attribution and license

Credit: **Alexander F. Wagner, Leverage Beyond Debt: Evidence from the AI Build-Out
(data), 2026, version 1.1**, [source repository](https://github.com/alex-wagner-research/leverage-beyond-debt).
Associated work: Alexander F. Wagner, *Leverage Beyond Debt: Evidence from the AI
Build-Out*, working paper, 2026. The repository supplies no separate paper URL.

The dataset and its documentation are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The unchanged supplied legal text and disclaimer are in [CC-BY-4.0.txt](CC-BY-4.0.txt).
Changes: selected columns/rows were converted from CSV to JSON without changing
their string values, other arrangements omitted, and attribution, hashes, counts,
evidence locators and labeled codebook summaries added. Parallax's comparison is
an independent interpretation; neither Wagner nor his institutions endorse it.
No additional restrictions are imposed on the reused/adapted dataset material.
The upstream README excludes SEC filings themselves from its license; we do not
claim Wagner licenses the underlying company disclosures or relicense them here.

## Reproduce

```sh
uv sync --locked
uv run python -m parallax.real_world --preview
uv run --env-file .env python -m parallax.real_world --evaluate --output results/nvidia-ports-live.json
uv run python -m unittest discover -s tests -v
```

The live command makes one independent request assessing both NVIDIA investor
perspectives. It reuses the existing Meta client and checkpoint writer, records
the exact payload and source-pack SHA-256, preserves provider output unchanged,
and refuses an existing output path. Choose a fresh path to repeat. There are no
automatic retries, dataset ingestion, retrieval system or UI additions.
