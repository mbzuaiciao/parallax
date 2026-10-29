# Independent Post-Audit Verification: Commit `f2c65e3`

**Auditor:** Independent Scientific & Software Auditor  
**Date of Verification:** October 29, 2026  
**Repository:** `parallax`  
**Target Commit:** `f2c65e3e627785a432b39108808555e1173dc0c7` ("Correct audited disclosure provenance and financial displays")  
**Baseline Audit Report:** [`research/independent-audit-antigravity.md`](file:///Users/xq/Documents/GitHub/parallax/research/independent-audit-antigravity.md)  
**Correction Record:** [`docs/post-audit-corrections.md`](file:///Users/xq/Documents/GitHub/parallax/docs/post-audit-corrections.md)  
**Verification Scope:** Narrowly scoped verification of post-audit corrections; no code, test, or existing document modifications made during verification.

---

## 1. Executive Summary

This post-audit verification evaluates commit `f2c65e3`, authored by Codex on October 29, 2026, in response to the findings documented in [`research/independent-audit-antigravity.md`](file:///Users/xq/Documents/GitHub/parallax/research/independent-audit-antigravity.md).

The commit addresses the immediate software engineering defects (`ENG-01`, `ENG-02`), financial/accounting mischaracterizations (`FIN-01`, `FIN-02`), and scientific disclosure framing (`SCI-01`, `SCI-02`). Across all targeted areas:
- Erroneous SEC EDGAR accession numbers in [`parallax/demo.py`](file:///Users/xq/Documents/GitHub/parallax/parallax/demo.py) were corrected to match the primary-source documents in [`cases/real_world/*.json`](file:///Users/xq/Documents/GitHub/parallax/cases/real_world/).
- CoreWeave's financial presentation was overhauled to reflect that it is an on-balance-sheet comparison case; the misleading "contractual cap" label was replaced with "Original Deposit Received", and the period-conflated "$43m accrued premiums" text was removed.
- NVIDIA's unsupported "$0 recognized on balance sheet" assertion was excised and replaced with an explicit statement that the PORTS guarantee liability carrying amount is not separately established.
- Meta's contractual cap metric display was fixed to render the full string `"Up to $14.72bn over five years"` without whitespace truncation.
- The repository [`README.md`](file:///Users/xq/Documents/GitHub/parallax/README.md) was updated to transparently clarify that Parallax tests interpretation of curated 150-word disclosure summaries rather than autonomous filing extraction or discovery.
- All experimental source packs, prompts, protocols, reference answers, and historical model outputs remain 100% byte-for-byte identical to their pre-commit state.
- All 58 unit tests (including 3 new regression tests) pass deterministically offline in ~3.6s.

No new material defects were introduced. The stopping rule is satisfied: commit `f2c65e3` is recommended for **ACCEPTANCE**, and the audit cycle is concluded.

---

## 2. Finding-by-Finding Assessment

| Original Finding ID | Severity | Category | Status in Commit `f2c65e3` | Summary Evaluation |
|---|---|---|---|---|
| **ENG-01** | Medium | Software Engineering | **RESOLVED** | Primary SEC accession numbers in `demo.py` now match `cases/real_world/*.json`. Circular test in `test_demo.py` replaced with comprehensive accession-matching regression tests. |
| **ENG-02** | Low | Software Engineering | **RESOLVED** | Metric rendering in `streamlit_app.py` preserves full text without whitespace splitting; Meta renders `"Up to $14.72bn over five years"`. |
| **FIN-01** | High | Financial Correctness | **RESOLVED** | CoreWeave reclassified as on-balance-sheet comparison case; deposit labeled as financing received rather than a cap; 2025/2026 balances and settlements disentangled. |
| **FIN-02** | Medium | Financial Correctness | **RESOLVED** | Unsupported "$0 recognized on balance sheet" claim removed; carrying amount explicitly qualified as not separately established. |
| **SCI-02** | High | Scientific Validity | **RESOLVED** *(Scope Framing)* | `README.md` explicitly states the benchmark uses curated summaries and does not test autonomous extraction from SEC filings. |
| **SCI-01** | High | Scientific Validity | **RESOLVED** *(Scope Framing)* | `README.md` explicitly notes that guided results reflect explicit analytical prompting rather than unaided model capability. |
| **SCI-03 / SCI-04** | High / Med | Scientific Validity | **Outside Scope** *(Documented)* | Human rater adjudication and $N > 1$ sampling remain documented research limitations for future work, properly disclosed in `docs/post-audit-corrections.md`. |
| **FIN-03 / BENCH-01..03** | Medium | Financial / Benchmark | **Outside Scope** *(Documented)* | Synthetic collection-guarantee mechanics and baseline comparisons remain documented design constraints, not modified in this narrow correction. |

---

## 3. Verification of Specific Corrections

### Task 2: SEC Accession Numbers against Primary Evidence
The accession numbers in `ISSUER_REGISTRY` ([`parallax/demo.py#L96-L144`](file:///Users/xq/Documents/GitHub/parallax/parallax/demo.py#L96-L144)) were verified against the primary document catalogs in [`cases/real_world/*.json`](file:///Users/xq/Documents/GitHub/parallax/cases/real_world/):

1. **NVIDIA PORTS:**
   - Catalog (`nvidia_ports.json`): Form 8-K accession `0001045810-26-000069`; Form 10-Q accession `0001045810-26-000075`.
   - `demo.py:96`: Corrected to `"SEC Form 8-K / 10-Q (accessions 0001045810-26-000069 / 0001045810-26-000075)"`.
   - Result: **VERIFIED**.
2. **Meta Platforms:**
   - Catalog (`meta_capacity.json`): Form 10-Q accession `0001628280-26-050705`.
   - `demo.py:120`: Corrected to `"SEC Form 10-Q (Note 9, accession 0001628280-26-050705)"`.
   - Result: **VERIFIED**.
3. **CoreWeave:**
   - Catalog (`coreweave_deposit.json`): Form 10-K accession `0001769628-26-000104`; Form 10-Q accession `0001769628-26-000366`.
   - `demo.py:144`: Corrected to `"SEC Form 10-K / 10-Q (Note 10, accessions 0001769628-26-000104 / 0001769628-26-000366)"`.
   - Result: **VERIFIED**.

Regression test `test_registry_provenance_matches_primary_document_accessions` in [`tests/test_demo.py`](file:///Users/xq/Documents/GitHub/parallax/tests/test_demo.py#L157-L163) programmatically asserts this correspondence across all registered real-world cases.

### Task 3: CoreWeave Revised Financial Terminology & Period Balances
In [`parallax/demo.py`](file:///Users/xq/Documents/GitHub/parallax/parallax/demo.py#L144-L162) and [`streamlit_app.py`](file:///Users/xq/Documents/GitHub/parallax/streamlit_app.py#L210-L650):
1. **Label Correction:** Mislabeled "contractual cap" was replaced with `amount_label = "Original Deposit Received"` and `disclosed_amount = "$230m original refundable deposit ($100m settled Jun 2026)"`.
2. **Accrual Decoupling:** The inaccurate text `"(includes $43m accrued premiums)"` was removed from the June 30, 2026 balance. The reported principal now reads:
   ```python
   "reported_principal": "$189m carrying value as of 30 Jun 2026 ($273m at 31 Dec 2025; $100m settled Jun 2026)"
   ```
3. **On-Balance-Sheet Status:** The summary now states: `"On-balance-sheet comparison case: a refundable capacity deposit, amended with termination rights and accounted for as in-substance debt."`
4. **Scenario View Alignment:** [`streamlit_app.py#L628-L644`](file:///Users/xq/Documents/GitHub/parallax/streamlit_app.py#L628-L644) introduces dedicated matrix rows for CoreWeave clearly marking it as on-balance-sheet recourse debt rather than an activated contingent guarantee claim.
- Result: **VERIFIED**.

### Task 4: NVIDIA Liability Qualification
In [`parallax/demo.py#L99`](file:///Users/xq/Documents/GitHub/parallax/parallax/demo.py#L99):
- The unsupported assertion `"None ($0 recognized on balance sheet)"` was removed.
- Replaced with:
  ```python
  "reported_principal": "PORTS guarantee liability carrying amount not separately established"
  ```
- In [`streamlit_app.py#L220`](file:///Users/xq/Documents/GitHub/parallax/streamlit_app.py#L220), `cols[2]` renders `"Carrying amount not established"`.
- [`docs/post-audit-corrections.md#L35-L45`](file:///Users/xq/Documents/GitHub/parallax/docs/post-audit-corrections.md#L35-L45) thoroughly explains why Note 8 credit-derivative references for unrelated cloud guarantees do not establish a $0 or positive carrying value for the August PORTS commitment.
- Result: **VERIFIED**.

### Task 5: Meta Display Correction & Regression Test
In [`streamlit_app.py#L209-L211`](file:///Users/xq/Documents/GitHub/parallax/streamlit_app.py#L209-L211):
- The code no longer uses whitespace `.split()[0]`. It renders:
  ```python
  cols[0].metric(issuer_data["amount_label"], issuer_data["disclosed_amount"])
  ```
  rendering `"Disclosed Contractual Cap: Up to $14.72bn over five years"`.
- In [`tests/test_demo.py#L165-L169`](file:///Users/xq/Documents/GitHub/parallax/tests/test_demo.py#L165-L169), regression test `test_meta_overview_preserves_complete_contractual_cap` explicitly checks:
  ```python
  self.assertEqual(cap.value, "Up to $14.72bn over five years")
  ```
- Result: **VERIFIED**.

### Task 6: README Accurate Framing of Curated Disclosures
In [`README.md#L12-L23`](file:///Users/xq/Documents/GitHub/parallax/README.md#L12-L23):
- README adds prominent upfront clarification:
  > *"The three real-world cases use **curated disclosure summaries**: manually selected short quotations and factual paraphrases, rather than raw SEC filings. They test financial interpretation of supplied summaries, not autonomous information extraction, filing discovery or retrieval. Human/assistant preparation already selects and organizes the relevant terms. Both neutral and guided experimental conditions are preserved; even neutral prompts receive these curated summaries, and guided results measure performance with explicit analytical instructions, not unaided capability. CoreWeave is an on-balance-sheet comparison case, not an extra hidden debt layer."*
- Lines 338 and 401 echo this qualification ("using curated summaries prepared from SEC disclosures, rather than raw filings").
- Result: **VERIFIED**.

### Task 7: Protocol, Answer, and Output Preservation
A strict Git tree comparison between commit `f2c65e3` and `origin/main` (`b4fc014`) confirms:
```sh
git diff origin/main..f2c65e3 -- cases protocols results assessments reviews parallax/cli.py parallax/paired.py parallax/real_world.py parallax/benchmark.py parallax/ablation.py parallax/evaluate.py parallax/model_api.py
```
- **Zero changes** occurred in any prompt templates, request builders, case JSON files, protocol snapshots, reference answers, assessment files, reviewer packages, or saved evaluation runs.
- Compatibility with historical benchmark data and experimental preregistrations is fully preserved.
- Result: **VERIFIED**.

---

## 4. Test Suite Execution Results

Running the full unittest discovery with Python 3.13:

```sh
uv run python -m unittest discover -s tests -v
```

```text
Ran 58 tests in 3.614s

OK
```

All 58 tests passed (up from 55 in the initial audit, reflecting the three new regression tests). No deprecation warnings, unhandled exceptions, or regressions were detected.

---

## 5. Verification Conclusion and Recommendation

The post-audit corrections in commit `f2c65e3`:
1. Directly and cleanly resolve the identified engineering and display defects (`ENG-01`, `ENG-02`).
2. Correct the accounting inaccuracies regarding CoreWeave and NVIDIA in the interactive workstation (`FIN-01`, `FIN-02`).
3. Accurately scope and qualify the scientific claims in the project documentation (`SCI-01`, `SCI-02`).
4. Preserve all underlying research data, test suites, and experimental compatibility byte for byte.
5. Introduce no new material defects.

### Final Determination: **ACCEPT COMMIT `f2c65e3`**

The audit cycle is now concluded. No further code or documentation changes are required.
