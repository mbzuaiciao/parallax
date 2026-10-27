# Small real-world benchmark: scope and method

The registry contains three nonrandom AI-infrastructure arrangements. It is a
reproducible pilot, not a representative sample or a model leaderboard. Its
curated paraphrases and explicit prompt cautions make these easier than blind
full-filing extraction. The same assistant selected cases, checked sources and
drafted assessments: this is not independent human adjudication or an inter-rater
agreement study. Possible model familiarity with these disclosures is uncontrolled.

## Case format and separation

`cases/real_world/registry.json` defines stable keys, company, arrangement, cutoff,
investor perspectives, evidence/reference/annotation paths, provenance and material
limitations. Each evidence file contains the contractual context and primary SEC
URLs, accessions, filing dates and provision locators. Reference files hold manually
source-checked factual assertions, known location IDs, unknowns and judgment guidance.
Separate Wagner subsets retain research coding. Source accessions and local pack
hashes identify what was used; we do not claim to archive or hash full SEC HTML.

The request builder allowlists only case identity, arrangement, cutoff, preparation
and primary documents. The registry's research annotations, verified-fact assertions,
unknowns/guidance and previous responses are never passed to Muse Spark. Only the
investor phrase changes between each case's prompts; every other instruction,
API parameter and evidence byte is the same. The NVIDIA registry prompts are
byte-equivalent to the historical investor-pair requests; all legacy commands and
historical files remain intact. Streamlit is unchanged.

## Selection and primary evidence

- **NVIDIA PORTS**: existing historical guaranties, cutoff August 26, 2026. Existing
  [case provenance](../cases/real_world/README.md) and original results are preserved.
- **Meta capacity purchase**: cutoff July 30, 2026, [June 2026 10-Q, Note 9](https://www.sec.gov/Archives/edgar/data/1326801/000162828026050705/meta-20260630.htm).
  A contingent own purchase of capacity can support a supplier economically without
  being a legal guarantee of third-party borrowing. Wagner `HL-0047` and shared
  instrument `HL-0034b` describe the same arrangement; we count it once. The selected
  Meta paragraph does not name the provider. Wagner's Nebius attribution relies on
  cross-filing matching outside this pack, and its U4 coding is not proof of an
  express cancellation term in this passage. Neither identity nor unconditional
  amounts are silently added to model evidence.
- **CoreWeave capacity deposit**: cutoff August 12, 2026; [2025 10-K, Note 10](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm)
  supplies the mechanism, and [June 2026 10-Q, Note 10](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm)
  supplies the updated carrying value. Wagner `HL-0041` / `HL-0041a` records this as
  debt at carrying value. The actual counterparty in the notes is MagAI Ventures;
  the dataset's Magnetar role label does not justify an undisclosed corporate-identity
  inference. Keep the original deposit, dated carrying values, accrued premiums and
  partial settlement distinct. A table's recourse label or dataset `collateral_type`
  of `n/a` does not prove unsecured or equal claim ranking.

Both new cases use filed notes rather than complete executed contracts. Named
roles, amounts and classification facts were checked directly against the SEC
passages by the assistant, separately from research codes. This is not a second
independent human verification. The selection retains contract and timing gaps.
An Oracle purchase-commitment candidate was excluded when its large SEC filing
could not be retrieved reliably (browser size limit; direct retrieval HTTP 403),
rather than substituting the dataset's quotation for verified primary evidence.

## Assessment boundaries

Automation checks request/evidence equality, hashes, file/schema structure, expected
perspectives, completion statuses and response-text presence. It does not judge
obligors, legal classification, amounts in narrative context, or factual correctness.
Human-entered citation document/location IDs are checked against a case catalog:
that establishes recognized identifiers, **not** actual location or semantic support.

The five documentally checkable categories and three judgment categories are kept
separate. All are reviewed semantically by a named reviewer; `pair_consistency` is
also judgment-dependent. Supplied assessment records are explicitly `assistant_draft`,
not human ratings. Use [the Markdown review template](review-template.md) and the
CLI's JSON scaffold. Missing fields are printed as `missing`; unfinished or impossible
assessments stay `not_reviewed` or `unscorable`. No artificial accuracy percentages,
aggregate scores, matching heuristics or automated financial correctness claims.

The recorded-assessment summary preserves rationales, reviewer identity, uncertainty
and provenance checks. Its statuses are judgments, not verified labels. The full
assessment JSON also retains selected response excerpts and source references.

## Reproduction and metadata

```sh
uv sync --locked
uv run python -m parallax.benchmark list
uv run python -m parallax.benchmark preview nvidia-ports --perspective equity_holder
uv run python -m parallax.benchmark preview meta-capacity
uv run --env-file .env python -m parallax.benchmark run meta-capacity --output results/meta-repeat.json
uv run --env-file .env python -m parallax.benchmark run coreweave-deposit --output results/coreweave-repeat.json
uv run python -m parallax.benchmark assess-template meta-capacity --run results/meta-repeat.json --output assessments/meta-repeat.json
uv run python -m parallax.benchmark summary assessments/meta-capacity.json assessments/coreweave-deposit.json
uv run python -m unittest discover -s tests -v
```

Previews/listing/review commands need no API key. Each `run` makes two independent
calls using the existing client, with no automatic retry, and checkpoints successes,
errors and non-stop/truncated outputs. A failed or incomplete call produces a nonzero
CLI exit after both attempts. Existing output paths are never overwritten. The model
defaults remain unchanged; exact prompts are reproducible, sampled responses are not.

Run metadata records UTC times, source-pack/registry/reference/annotation hashes,
SEC accessions/URLs, pinned dataset version, requested model/endpoint, Python version,
Git revision/dirty flag and executable-file hashes. Provider IDs, returned model
and usage are retained in the raw JSON. Runs were made from a dirty working draft;
the recorded Git parent alone does not identify the final source. The runner's
report-label wording was clarified afterward; the saved runner hash identifies
the executed draft, not a claim of equality with final reporting code. Requests,
responses, case packs and reference bytes were not revised after submission.

## Attribution and licensing

Credit: **Alexander F. Wagner, Leverage Beyond Debt: Evidence from the AI Build-Out
(data), 2026, version 1.1**, [repository](https://github.com/alex-wagner-research/leverage-beyond-debt),
revision `98c8bba76a453e117f4b07de1881e4f5e08dd8f6`. The working paper has the same
author/title/year; the dataset's README, CITATION.cff, codebook, changelog and
LICENSE were inspected. It contains 155 arrangements across 37 sample firms.

The dataset/documentation are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The original [license and disclaimer](../cases/real_world/CC-BY-4.0.txt) remain unchanged.
Adaptations: two selected contract/instrument rows converted to JSON with original
string values and blanks preserved, source hashes/locators and attribution added;
independently written reference facts and codebook relationships are labeled
separately. No additional restrictions or endorsement are implied. Primary company
disclosures are separate from the dataset license; source packs are Parallax's
identified paraphrases and short quotes, not complete filings or Wagner's prose.
