# Parallax — Independent React Workstation Acceptance Audit

**Auditor:** Independent Software & Financial-Data Auditor  
**Date:** October 29, 2026  
**Repository:** `mbzuaiciao/parallax`  
**Target Commit:** `607ba06931aa361c287ad664db479ad8422c1994`  
**Evaluation Scope:** React Evidence Workstation (Phase 1), Python Workstation API adapter, SEC disclosures, accounting classifications, regression test suites, and visual/usability ergonomics.  
**Audit Constraints:** Zero modifications to application code, tests, financial records, or existing research artifacts. Local verification only. No commit or push.

---

## Executive Summary & Audit Conclusion

An independent software and financial-data audit was conducted on the Parallax React workstation at commit `607ba06931aa361c287ad664db479ad8422c1994`. The workstation was evaluated across five core dimensions:
1. **Financial Data Integrity** across all five covered cases (NVIDIA, Meta, CoreWeave, Apple, Microsoft).
2. **Frontend/Backend Consistency** between `parallax/workstation.py`, local source JSON fixtures, and `frontend/src/App.tsx`.
3. **Visual and Usability Review** via live browser inspection on both desktop and mobile viewports.
4. **Regression Verification** across the Python standard-library suite, React/Vitest suite, TypeScript compilation, Vite production build, and Streamlit `AppTest` regression coverage.
5. **Findings and Remediation Analysis**.

### Final Audit Determination: **ACCEPT**

The Phase 1 React evidence workstation fulfills all stated functional, accounting, architectural, and data-integrity acceptance criteria:
- Disclosed amounts are verified verbatim against local SEC source packs without mathematical fabrication or unauthorized transformations.
- Contractual commitments, contingent guarantees, and recognized liabilities are strictly delineated.
- Unknown accounting carrying values are explicitly displayed as unknown and never coerced to zero.
- Primary SEC EDGAR accessions and URLs are fully grounded and functional.
- AI-assisted interpretations are prominently segregated from factual evidence with multi-cue visual indicators and explicit disclaimer notices.
- All 75 Python tests, 13 React unit/integration tests, TypeScript validation, and production build checks pass cleanly with zero regressions.

---

## 1. Financial Data Integrity

Each of the five corporate disclosure cases was audited across its source fixture, API adapter representation (`parallax/workstation.py`), scientific reference catalog (`protocols/scientific-validation-v1/references.json`), and React presentation (`frontend/src/App.tsx`).

### Case-by-Case Integrity Matrix

| Issuer | Form & Reporting Period | Disclosed Amount(s) | Accounting Classification | Distinctions & Boundaries | SEC Accession & EDGAR Status |
|---|---|---|---|---|---|
| **NVIDIA** (`NVDA`) | Form 8-K (Item 1.01, 2026-08-17); Form 10-Q (Note 17, Period end 2026-07-26, Filed 2026-08-26) | `$105 billion` (Initial shared contractual cap) | `not_established` (Carrying amount unknown) | Shared residual value guarantee cap for IT load at PORTS facility; contingent on lessor ready-for-service (2028+). OpenAI is tenant/primary obligor; reimbursement is a claim, not cash received. Note 8 credit derivatives for unrelated cloud guarantees are not PORTS evidence. August execution follows July 26 balance-sheet date. | Accession `0001045810-26-000069` (8-K) & `0001045810-26-000075` (10-Q); URLs resolve to valid SEC EDGAR directory paths. |
| **Meta Platforms** (`META`) | Form 10-Q (Note 9, Period end 2026-06-30, Filed 2026-07-30) | `$14.72 billion` (Contingent capacity purchases) | `not_established` (Carrying amount unknown) | Executory cloud capacity purchase commitment over five years; reducible by third-party sales offsets. No guarantee of another entity's debt. Neighboring $349.31B aggregate commitments are context, not this arrangement's schedule. | Accession `0001628280-26-050705`; URL resolves to Note 9 in SEC EDGAR archive. |
| **CoreWeave** (`CRWV`) | Form 10-K (Note 10, Period end 2025-12-31, Filed 2026-03-02); Form 10-Q (Note 10, Period end 2026-06-30, Filed 2026-08-12) | `$230 million` (Original deposit); `$189 million` (June 30, 2026 balance); `$273 million` (Dec 31, 2025 balance); `$100 million` (June 2026 settlement) | `disclosed_recognition_pending_independent_verification` (Recognized in-substance debt under ASC 470) | Refundable deposit reclassified as recourse debt following Feb 2025 termination-for-convenience amendment. 12% effective annual return multiplier. June 2026 partial settlement ($100m) reduced debt to $189m. Explicitly marked as recognized financing, not a cap or hidden off-balance-sheet debt. | Accession `0001769628-26-000104` (10-K) & `0001769628-26-000366` (10-Q); URLs resolve to Note 10 in SEC EDGAR archive. |
| **Apple** (`AAPL`) | Form 10-K (Item 7, Period end 2025-09-27, Filed 2025-10-31) | `$56.2 billion` (Manufacturing obligations); `$55.4 billion` (Payable within 12 months) | `not_established` (Carrying amount unknown) | Executory manufacturing commitments for component sourcing and assembly. Unperformed executory contracts do not create gross balance-sheet payables on signing. Not additional funded debt. Carrying balance of related accruals is unknown from Item 7. | Accession `0000320193-25-000079`; URL resolves to Item 7 in SEC EDGAR archive. |
| **Microsoft** (`MSFT`) | Form 10-K (Notes 1 & 13, Period end 2025-06-30, Filed 2025-07-30) | `$22,861 million` (Recognized liability); `$5,424 million` (Current); `$17,437 million` (Noncurrent); `$25,481 million` (Undiscounted payments); `$6,111 million` (FY2026 payments) | `disclosed_recognition_pending_independent_verification` (Recognized operating lease liabilities under ASC 842) | Operating lease present-value carrying liability ($22,861m) distinguished from undiscounted cash obligations ($25,481m before $2,620m imputed interest). FY2026 cash schedule ($6,111m) distinguished from current carrying balance ($5,424m). Undiscounted payments are not added as separate debt. | Accession `0000950170-25-100235`; URL resolves to Notes 1 and 13 in SEC EDGAR archive. |

### Detailed Verification Points

1. **Exact-Text Match Rule:**
   In `parallax/workstation.py` (lines 69-73), every amount string must match verbatim within the cited document's `factual_paraphrase` or `short_quote`. If text drifts or is omitted, the adapter fails closed, setting `value: None` and `status: "unavailable"`. All 13 configured amounts match their source strings exactly.
2. **Commitment vs. Guarantee vs. Recognized Liability:**
   - Contractual commitments (Apple, Meta) are identified as executory purchase agreements.
   - Contingent guarantees (NVIDIA) are identified as residual value guaranties with trigger events, landlord termination intent requirements, and ready-for-service conditions.
   - Recognized liabilities (CoreWeave, Microsoft) are explicitly identified as on-balance-sheet debt (ASC 470) and operating lease obligations (ASC 842), preventing double-counting.
3. **Non-Conflation of Reporting Periods:**
   - CoreWeave clearly separates the August 2024 initial transaction, December 31, 2025 balance ($273m), June 2026 partial settlement ($100m), and June 30, 2026 carrying balance ($189m). Rows display distinct context notes; amounts are not summed across periods.
   - NVIDIA highlights that the August 17, 2026 agreement postdates the July 26, 2026 balance-sheet cutoff date, preventing retroactive balance-sheet attribution.
4. **Zero-Coercion Safeguards:**
   - In `frontend/src/App.tsx` (lines 36-38, 55, 65-70), when `accounting.status === "not_established"`, the workstation renders `"Carrying amount unknown"` with an amber indicator tag. Under no condition is missing evidence rendered as `$0` or interpreted as evidence of nonrecognition.
5. **Separation of Source Facts and AI Interpretations:**
   - **Disclosed Facts (Category 01, Teal):** Source-pack excerpts, amounts, dates, and primary SEC links.
   - **Conditional Interpretation (Category 02, Blue):** Investor perspective narratives. Accompanied by a persistent notice: *"Existing AI-assisted research reference. Provisional; independent human approval pending. These statements are interpretations, not verified disclosure facts."*
   - **Unknown / Unsupported (Category 03, Amber):** Explicit enumeration of missing contract schedules, uncalculated leverage ratios, and unquantified recovery rates.

---

## 2. Frontend / Backend Consistency

### API Routes & Schema Conformance

The Python standard-library backend (`parallax/workstation.py`) exposes two read-only endpoints:
- `GET /api/cases`: Returns catalog array of 5 case summaries.
- `GET /api/cases/{key}`: Returns case details including documents, amounts, accounting metadata, interpretations, limitations, and SHA-256 integrity digests.
- Other paths return HTTP 404; non-GET methods return HTTP 501.

| Field in API JSON | TypeScript Type (`types.ts`) | UI Render Element (`App.tsx`) | Status |
|---|---|---|---|
| `key`, `ticker`, `company` | `string` | Header, Sidebar button, Title | Exact match |
| `arrangement` | `string \| null` | Arrangement summary (Box 3) | Exact match |
| `analysis_as_of` | `string \| null` | Case meta ("Historical cutoff") | Exact match |
| `amounts` | `Array<{label, value, context, status}>` | Summary card, Amount table | Exact match |
| `documents` | `Array<Document>` | Source passage cards, Accessions | Exact match |
| `accounting` | `{status, statement}` | Recognition status box, Section 02 | Exact match |
| `interpretations` | `{equity, senior_unsecured_creditor}` | Investor perspective toggle panel | Exact match |
| `limitations` | `string[]` | Section 03 bullet list | Exact match |
| `evidence_sha256`, `reference_sha256` | `string` | Provenance `<details>` element | Exact match |

### Evidence Preservation & Text Integrity

- **Expandable Passages:** Each document card encapsulates its evidence in a native `<details className="source-passage">` element. By default, it is collapsed to preserve screen hierarchy.
- **Verbatim Paragraph Segmentation:** `EvidencePassage` utilizes the ECMAScript Internationalization API (`Intl.Segmenter` with `granularity: "sentence"`) to divide long paraphrases into readable 2-sentence paragraphs. Character-for-character comparison between the unsegmented source text and the rendered DOM text confirms that zero characters, spaces, or punctuation marks are added, removed, or mutated.
- **Direct SEC Linking:** `SourceLink` verifies that every URL begins with `https://www.sec.gov/Archives/edgar/` before rendering a link with `target="_blank"` and `rel="noreferrer"`. If absent or malformed, it falls back to `<span className="muted">Source unavailable</span>`.

### Interactive Controls & State Machine

1. **Investor Perspective Switcher:**
   - Defaults to `equity`. Clicking `senior_unsecured_creditor` updates the state, updates the `aria-pressed` attribute, and immediately renders the creditor narrative inside an `aria-live="polite"` region.
2. **Search & Filter:**
   - Real-time search matches against company name, ticker, and arrangement description.
   - When no matches exist (e.g. searching "Tesla" or "uncovered"), the list displays `<p className="empty" role="status">No matching cases. Try another company or ticker.</p>`. Clearing the query instantly restores the 5 cases.
3. **Asynchronous Cancellation & Concurrency:**
   - Both `/api/cases` and `/api/cases/{key}` instantiate an `AbortController`. Rapid switching between cases cancels inflight requests. Vitest tests confirm that stale responses from prior selections cannot overwrite newly selected cases.
4. **Error Handling & Retry:**
   - Simulating service failure renders an accessible alert panel (`role="alert"`) informing the user that the Python service on port 8001 is unavailable, accompanied by a functional "Retry loading" button.

### Configuration Parity

- `frontend/vite.config.ts`: Configures `server.port = 5174` and `preview.port = 4174` with `strictPort: true` and proxies `/api` to `http://127.0.0.1:8001`.
- `parallax/workstation.py`: Defaults to port `8001` on loopback `127.0.0.1`.
- Both defaults explicitly avoid port collisions with Metis (`8000` / `5173`).

---

## 3. Visual and Usability Review

The application was inspected locally across both the Vite development server (port 5174) and the Python production static server (port 8001) using headless Chrome (`--virtual-time-budget=5000 --headless=new`).

### Information Hierarchy & Readability

- **Restrained Dark Theme:** Background `#0c1118`, surface panel `#111a25`, border `#2a3646`, body text `#d7dfe9`. High contrast ratio complies with WCAG AA standards.
- **Three-Tier Header:** Immediate visual orientation through three distinct panels:
  1. *Contractual exposure / disclosed measure* (e.g. $105 billion cap, $25,481m undiscounted payments).
  2. *Recognition status* (e.g. Carrying amount unknown, $22,861m recognized liability).
  3. *Obligation type* (Concise summary of legal/commercial form).
- **Categorization Badges:** Disclosed facts (teal `#8bcbbf`), conditional interpretations (blue `#9bb8e0`), and evidence limitations/unknowns (amber `#d1b887`) allow an analyst to immediately identify what is legally committed, what is accounting debt, and what is unverified.
- **Scroll Containment:** The disclosed amount table is wrapped in a dedicated `.table-wrap` container with `overflow: auto`. On narrow viewports, tabular data scrolls internally without causing page-wide horizontal blowout.

### Viewport Responsiveness

- **Desktop (1440px):** Two-column split layout (`grid-template-columns: minmax(0, 1.65fr) minmax(300px, 1fr)`). The primary evidence column sits on the left; investor interpretation, recognition boundaries, and limitations occupy the sticky right rail.
- **Tablet / Intermediate (1150px):** Sidebar narrows to 220px; analysis column reflows to a 2-column subgrid below the evidence.
- **Mobile (390px):** Single-column stacked layout (`@media(max-width: 700px)`). The sidebar collapses into a top grid of buttons; the arrangement summary shifts from a 3-column row to a vertically stacked panel. Chrome headless viewport evaluation confirms that the root document `scrollWidth` remains exactly 390px with zero horizontal page spill.

### Accessibility Audit

- **Skip Navigation:** Keyboard users can trigger a skip link (`.skip-link:focus`) at `top: 12px` to bypass the sidebar and jump straight to `<main id="main">`.
- **Focus Indicators:** Explicit outline rings (`outline: 2px solid #97d9cc; outline-offset: 4px`) are applied across buttons, inputs, links, and summaries.
- **ARIA Semantics:**
  - Case library buttons have `aria-current="true"` when active.
  - Perspective toggle buttons use `aria-pressed="true" / "false"`.
  - Dynamic interpretation text is wrapped in an `aria-live="polite"` region.
  - Search input has an associated `<label>` and `type="search"`.
  - Data table includes an accessible `.sr-only` `<caption>` and explicit `scope="col"` / `scope="row"` headers.

---

## 4. Regression Checks & Scientific Integrity

All automated test suites and build pipelines were executed from the repository root:

```sh
# 1. Full Python standard-library suite
uv run python -m unittest discover -s tests -v

# 2. React Vitest test suite
npm test --prefix frontend

# 3. TypeScript validation & Vite production build
npm run build --prefix frontend
```

### Test Results Summary

1. **Python Unit Tests:** **75 / 75 PASSED** in 4.36s.
   - Includes all 58 legacy benchmark and case tests.
   - Includes 7 workstation adapter tests verifying port defaults, case cataloging, exact-text validation, unavailable handling, and HTTP route isolation.
   - Includes 10 scientific validation tests (`test_scientific_validation.py` and `test_scientific_validation_v1b.py`).
2. **React Vitest Tests:** **13 / 13 PASSED** across 2 test files in 1.19s.
   - Validates selection of all five cases, amount table grounding, SEC links, investor perspective toggling, unknown/missing field fallbacks, summary cards, passage expansion, search filtering, retry recovery, and race-condition cancellation.
3. **Production Build:** **CLEAN BUILD** in 461ms.
   - `tsc --noEmit` completed with zero TypeScript errors.
   - `vite build` generated client assets (`dist/index.html` 0.50 kB, CSS 10.80 kB, JS 235.59 kB).
4. **Streamlit Regression Check:**
   - `tests/test_demo.py` ran through `streamlit.testing.v1.AppTest` and passed all navigation, search, capital structure, and AI diagnostics tests without exception.
5. **Scientific Artifact Integrity:**
   - SHA-256 verification of `protocols/scientific-validation-v1/references.json`, evidence files, and fixtures confirmed zero modifications. No research results, model ablation logs, or benchmark fixtures were changed.

---

## 5. Findings Classification

Findings are classified according to the audit criteria:
- **BLOCKER:** Incorrect financial information, misleading accounting representation, or broken core functionality.
- **MATERIAL:** Significant data-integrity or usability defect.
- **MINOR:** Cosmetic or nonessential improvement.

### Summary of Audit Findings

| ID | Category | Severity | Description | Status |
|---|---|---|---|---|
| — | Financial Integrity | **BLOCKER** | None identified. | **PASS** |
| — | Core Functionality | **BLOCKER** | None identified. | **PASS** |
| — | Usability / Data Integrity | **MATERIAL** | None identified. | **PASS** |
| **OBS-01** | Operational | **MINOR** | Minimal HTTP server returns HTTP 501 for `HEAD` requests. | Non-blocking observation |
| **OBS-02** | Functional Search | **MINOR** | Sidebar search filters case header fields, not nested passage body text. | Designed behavior for Phase 1 |
| **OBS-03** | Deployment | **MINOR** | Production HTML asset references assume root path (`/`). | In-scope for local loopback |

### Observations Detail

#### Finding OBS-01 (Severity: MINOR — Operational)
- **File & Line:** `parallax/workstation.py:111-133` (`Handler.do_GET`)
- **Reproducible Evidence:** Executing `curl -I http://127.0.0.1:8001/` returns `HTTP/1.0 501 Unsupported method ('HEAD')` because `Handler` only implements `do_GET`.
- **Impact:** None on browser users or React application functionality, which exclusively use `GET`. CLI tools checking health via `HEAD` receive a 501 code.
- **Smallest Necessary Correction:** If desired in future maintenance, define `do_HEAD(self)` to delegate to `do_GET` without writing the response body. This is not a blocker for Phase 1 acceptance.

#### Finding OBS-02 (Severity: MINOR — Functional Scope)
- **File & Line:** `frontend/src/App.tsx:143` (`filtered = catalog.filter(...)`)
- **Reproducible Evidence:** Searching for passage-specific terms (such as an accession number or "MagAI") in the sidebar search box does not return the case unless the term appears in `company`, `ticker`, or `arrangement`.
- **Impact:** None for Phase 1 catalog navigation. Users find cases by company name or ticker as expected. Full-text search across disclosure bodies is outside Phase 1 scope.
- **Smallest Necessary Correction:** Optional future enhancement to index document locators and accession numbers in the search filter.

#### Finding OBS-03 (Severity: MINOR — Deployment Scope)
- **File & Line:** `frontend/vite.config.ts`, `frontend/dist/index.html`
- **Reproducible Evidence:** Build emits root-relative asset URLs (`/assets/...`).
- **Impact:** Perfectly functional when served from the root of `127.0.0.1:8001` or `127.0.0.1:4174`. Hosting behind a reverse-proxy subpath (e.g. `/parallax/`) would require configuring `base` in Vite.
- **Smallest Necessary Correction:** In-scope as designed for local Phase 1 loopback workstation.

---

## Phase 1 Acceptance Checklist

- [x] **NVIDIA Case:** Disclosed cap ($105B) verified; carrying liability correctly marked unknown; Note 8 / Note 17 distinctions preserved.
- [x] **Meta Case:** Contingent capacity commitment ($14.72B) verified; carrying liability correctly marked unknown; aggregate commitments separated.
- [x] **CoreWeave Case:** In-substance debt under ASC 470 verified; $230m original deposit labeled as financing; Dec 2025 ($273m) and June 2026 ($189m) balances separated without conflation.
- [x] **Apple Case:** Manufacturing purchase obligations ($56.2B) verified; executory nature clarified; carrying liability marked unknown rather than zero.
- [x] **Microsoft Case:** Commenced operating lease carrying liability ($22,861m) and undiscounted payments ($25,481m) paired without confusion; current liability ($5,424m) and FY2026 payments ($6,111m) clearly distinguished.
- [x] **SEC EDGAR Grounding:** All 8 document accessions and URLs match primary filings.
- [x] **Unknown Representation:** Unknown amounts are never represented as zero.
- [x] **AI Interpretation Segregation:** Clear visual and textual distinction between primary evidence, conditional interpretations, and limitations.
- [x] **Frontend/Backend Consistency:** Catalog, case payloads, passage expansion, and perspective toggles function correctly.
- [x] **Automated Regression Suite:** 75/75 Python tests, 13/13 React tests, and Streamlit `AppTest` regression checks pass.
- [x] **Build & Typing:** TypeScript type checking and Vite production build pass cleanly.

---

## Audit Recommendation

**ACCEPT**

The Parallax React workstation at commit `607ba06931aa361c287ad664db479ad8422c1994` satisfies all Phase 1 acceptance criteria. It presents corporate financial obligations with strict accounting rigor, preserves historical evidence without mutation, and introduces zero regressions into the existing benchmark suite.
