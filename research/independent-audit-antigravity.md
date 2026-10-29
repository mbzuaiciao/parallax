# Independent Scientific and Software Audit: Parallax

**Auditor:** Independent Scientific & Software Auditor  
**Date of Audit:** October 29, 2026  
**Repository:** `parallax`  
**Evaluation Scope:** Codebase implementation, benchmark methodology, financial/accounting validity, datasets, test suite, and scientific claims  
**Audit Constraints:** Zero modifications to source code, test suites, benchmark fixtures, or existing documentation. Purely local evaluation without external paid API calls or dependency changes.

---

## 1. Executive Assessment

Parallax is structured as an evaluation and exploration framework investigating how corporate financial obligations—specifically off-balance-sheet commitments, contingent guarantees, and subsidiary debt—affect different capital structure stakeholders (common equity holders and senior unsecured creditors). The project spans two synthetic settlement models (Harbor Components and Cedar Holdings), three real-world case studies adapted from academic literature (NVIDIA PORTS residual-value guaranties, Meta cloud-capacity purchase commitments, and CoreWeave refundable capacity deposit financing), a 12-cell prompt-guidance ablation experiment (`guidance-ablation-v1`), and a Bloomberg Terminal-inspired Streamlit workstation.

### Core Strengths
1. **Software Engineering & Hygiene:** The offline Python backend relies entirely on the standard library (`decimal`, `fractions`, `json`, `argparse`, `hashlib`, `urllib`). Dependencies are strictly locked via `uv.lock`. Test isolation is exemplary: all 55 unit tests run offline in ~3.4 seconds without external API calls or network access. API failure handling, checkpoint serialization via atomic replacement, and key preflight checks are well implemented.
2. **Explicit Uncertainty Disclosures:** Unlike many generative AI finance demos that fabricate quantitative debt ratios or expected losses, the codebase and documentation repeatedly emphasize that enterprise leverage (Debt/EBITDA), market default probabilities, loss given default (LGD), and creditor recovery rates are **unscorable** from isolated footnote disclosures.
3. **Reproducibility of Prompts and Data Artifacts:** Prompts are deterministic, inputs are SHA-256 hashed, and experiment metadata rigorously records Git commits, timestamps, and Python versions.

### Critical Scientific and Methodological Limitations
1. **The Benchmark Does Not Measure Information Extraction from Filings:** The real-world cases do not feed raw SEC filings (10-K/10-Q) to the language model. Instead, the model is provided with pre-digested, 150-word `factual_paraphrase` snippets manually written by the author. The entire extraction, filtering, and initial classification task was performed by humans before the model was invoked.
2. **Prompt Coaching / Boundary Leakage:** The developer system prompt explicitly tells the model what *not* to do ("do not infer redacted identities, invent financial inputs, assume a creditor ranking, or turn a disclosed cap into an expected loss or payable balance"). These negative constraints spoon-feed the model the precise evaluation criteria. When these guardrails are removed in the neutral ablation condition, the model immediately hallucinates (e.g., asserting *pari passu* status, labeling reimbursement as unsecured, claiming LGD is $105B, and inventing operating priority).
3. **Circular Ground Truth and Non-Independent Evaluation:** There is no automated scoring of semantic correctness or financial reasoning. The benchmark reference facts, the evaluation checklists, and the recorded qualitative assessments were all authored by the same LLM assistant. No independent blinded human domain expert has evaluated the outputs.
4. **Underpowered Sample Size:** The ablation study operates at $N=1$ sample per cell (12 total calls). Sampling variance cannot be separated from systematic prompt effects.
5. **Financial & Accounting Inconsistencies:** CoreWeave's recognized on-balance-sheet debt is mislabeled as having a "contractual cap" and conflates 2025 and 2026 premium figures. NVIDIA's guarantee liability is assumed to be $0 on the balance sheet without verification under ASC 460/815. Furthermore, `demo.py` hardcodes incorrect SEC accession numbers that contradict the underlying benchmark JSON files.

---

## 2. Actual Capabilities versus Claimed Capabilities

| Stated Ambition / Claim | Implemented Capability in Codebase | Auditor Evaluation |
|---|---|---|
| **"Evaluates how corporate financial obligations affect different stakeholders"** | Implements deterministic waterfall arithmetic for two toy synthetic cases; displays qualitative prompts for two investor classes on real cases. | **Partially supported.** Supported deterministically for simplified synthetic waterfalls; purely qualitative and unverified for real-world issuers. |
| **"Extraction of disclosed financial information beyond reported debt"** | Model receives a pre-written 1-paragraph summary (`factual_paraphrase`) where human researchers already extracted and classified the terms. | **Unsupported.** The system tests reading comprehension of human-curated summaries, not extraction from corporate filings. |
| **"Identifies economic obligations beyond reported debt"** | Real-world cases are drawn directly from Alexander F. Wagner's 2026 academic dataset (`leverage-beyond-debt`). | **Unsupported.** Human research identified the obligations; the model merely rephrased the selected notes. |
| **"Claims-oriented hierarchy distinguishing obligors, guarantees, priorities, and investor economic exposure"** | Streamlit UI displays a static claims stack table; models are prompted to discuss investor impact. | **Partially supported.** The model provides narrative discussion, but the benchmark code explicitly declares priority and recovery to be unscorable. |
| **"Preregistered prompt-guidance ablation evaluating model reliability"** | 12 cells (3 cases × 2 investors × 2 prompt conditions) executed once ($N=1$), saved with hashes, and qualitatively reviewed by the assistant. | **Methodologically limited.** Strong audit trail infrastructure, but $N=1$ provides zero statistical power; ratings are non-blinded assistant drafts. |
| **"Automated benchmark evaluation"** | `protocol_checks()` verifies request matching, parameter equality, source versions, and non-empty response text. | **Narrow engineering verification.** Automated checks verify protocol hygiene and schema structure only; they do not assess financial accuracy. |

---

## 3. Scientific Validity Findings

### Finding SCI-01 (Severity: High) — Answer-Space Leakage via Negative Prompt Coaching
- **File & Line:** `parallax/model_api.py:50-52` (`build_disclosure_request`)
- **Evidence:**
  ```python
  "Use only the supplied evidence; do not infer redacted identities, invent "
  "financial inputs, assume a creditor ranking, or turn a disclosed cap into "
  "an expected loss or payable balance. No outside research or dataset "
  "classifications are available. Give a concise, structured analysis."
  ```
- **Why it matters:** The benchmark claims to evaluate whether an LLM can distinguish contractual caps from expected losses and recognize missing information. However, the system prompt explicitly gives the model the negative rules of the test. When these negative instructions are removed in `NEUTRAL_TEMPLATE` (`parallax/ablation.py:20-23`), the model immediately commits the prohibited errors:
  - NVIDIA Creditor (Neutral, R001): Defaults to *pari passu* ranking, labels reimbursement as unsecured, and calls the $105B cap the "maximum LGD before recoveries."
  - Meta Creditor (Neutral, R003): Asserts "de facto" operating priority, mandatory funding/debt, and default-risk conclusions without evidence.
  - CoreWeave Equity (Neutral, R010): Introduces issuer-wide asset and debt figures absent from the prompt pack.
  The claimed capability of the model to navigate financial nuances is primarily a reflection of detailed prompt coaching rather than intrinsic financial reasoning.
- **Smallest appropriate correction:** Refactor the primary benchmark metric around the unguided/neutral condition, treating guided instructions as an upper-bound intervention rather than baseline capability.
- **Status:** Confirmed.

### Finding SCI-02 (Severity: High) — Pre-Digested Evidence Replaces Filing Extraction
- **File & Line:** 
  - `cases/real_world/nvidia_ports.json:16, 27, 37`
  - `cases/real_world/meta_capacity.json:17`
  - `cases/real_world/coreweave_deposit.json:17, 28`
- **Evidence:** The user prompt sent to the LLM does not contain SEC filings or complete footnote disclosures. It contains a field named `factual_paraphrase`. For example, in `coreweave_deposit.json`:
  ```json
  "factual_paraphrase": "In August 2024 CoreWeave entered a capacity/prepayment agreement with MagAI Ventures and received a $230 million refundable deposit... CoreWeave consequently classified the refundable deposit as in-substance debt under ASC 470, Sale of Future Revenue. On such termination, unused deposit is refunded with an increasing multiplier equivalent to a 12% annual return..."
  ```
- **Why it matters:** In real-world financial analysis, the core bottleneck is locating, parsing, interpreting, and connecting obscure disclosures buried across hundreds of pages of financial filings. In Parallax, a human researcher did 99.9% of that work, isolating the exact paragraphs and writing a synthesis. The LLM is only performing text summarization on a 150-word pre-digested snippet. Presenting this as evidence of an AI's ability to discover or evaluate obligations "beyond reported debt" is scientifically misleading.
- **Smallest appropriate correction:** Explicitly state in all documentation and benchmark descriptions that the benchmark measures reading comprehension on human-curated 150-word summaries, not extraction or discovery from SEC EDGAR filings.
- **Status:** Confirmed.

### Finding SCI-03 (Severity: High) — Circular Ground Truth and Absence of Objective Scoring
- **File & Line:**
  - `cases/real_world/nvidia_ports_reference.json:4`
  - `cases/real_world/meta_capacity_reference.json:4`
  - `cases/real_world/coreweave_deposit_reference.json:4`
  - `parallax/benchmark.py:128-156` (`protocol_checks`)
  - `assessments/guidance-ablation-v1-preliminary.json`
- **Evidence:**
  1. The reference ground-truth assertions were authored by the same AI assistant ("verified_by": "Parallax primary-disclosure manual check (assistant), 2026-10-27").
  2. The automated evaluation script (`protocol_checks`) only checks structural presence and SHA-256 hashes:
     ```python
     def protocol_checks(run):
         """Check bytes/structure only. These checks do not assess financial correctness."""
     ```
  3. The semantic assessments (`assessments/meta-capacity.json`, `assessments/coreweave-deposit.json`, `assessments/guidance-ablation-v1-preliminary.json`) were drafted and recorded by the same assistant.
- **Why it matters:** The evaluation loop is entirely closed and circular: the assistant authored the cases, authored the reference facts, designed the prompts, and assigned the evaluation ratings ("supported" vs "concern"). There is no independent human verification, no blinded adjudication, and no objective automated scoring rubric.
- **Smallest appropriate correction:** Replace assistant self-assessments with an independent, multi-annotator blinded review conducted by human financial analysts using the existing review package (`reviews/guidance-ablation-v1/`).
- **Status:** Confirmed.

### Finding SCI-04 (Severity: Medium) — Underpowered Experimental Sample Size ($N=1$)
- **File & Line:** `protocols/guidance-ablation-v1.json`, `protocols/guidance-ablation-v1.md:20`
- **Evidence:** The prompt guidance ablation evaluates 3 cases × 2 perspectives × 2 conditions = 12 cells, with exactly `samples = 1` per cell (12 API completions total).
- **Why it matters:** Language model output is stochastic. With a single sample per cell, the experiment has zero statistical power. Observed differences between guided and neutral answers (such as neutral creditor answers hallucinating *pari passu* status) may represent random sampling fluctuations rather than systematic treatment effects. Although the documentation includes disclaimers ("One sample per cell... no statistical significance is claimed"), the analysis in `results/guidance-ablation-v1-preliminary-review.md` draws broad qualitative conclusions across conditions.
- **Smallest appropriate correction:** Restrict all narrative reporting to anecdotal qualitative observations, or scale sample size (e.g. $N \ge 10$ per cell) using the implemented `--samples` framework before making comparative claims.
- **Status:** Confirmed.

---

## 4. Financial and Accounting Correctness Findings

### Finding FIN-01 (Severity: High) — Misclassification of On-Balance-Sheet Debt as "Beyond Debt" and Period-Conflated Accruals
- **File & Line:**
  - `parallax/demo.py:146-149` (`ISSUER_REGISTRY["coreweave-deposit"]`)
  - `cases/real_world/coreweave_deposit.json:17, 28`
  - `cases/real_world/coreweave_deposit_reference.json:65-69`
- **Evidence:**
  In `demo.py`:
  ```python
  "obligation_type": "Recognized in-substance debt financing",
  "reported_principal": "$189m carrying value as of 30 Jun 2026 (includes $43m accrued premiums)",
  "contractual_cap": "$230m original refundable deposit ($100m settled Jun 2026)",
  ```
- **Why it matters:**
  1. **Not an off-balance-sheet obligation:** CoreWeave’s refundable deposit was reclassified under ASC 470 as in-substance debt and explicitly reported on its balance sheet under "Recourse Debt" ($273M at Dec 31, 2025; $189M at June 30, 2026). Including CoreWeave in a benchmark studying "leverage beyond debt" without prominently clarifying that it is an on-balance-sheet negative control confuses users.
  2. **Terminology Distortion:** Calling the $230M deposit a "contractual cap" is financially incorrect. A refundable deposit balance subject to a 12% redemption return multiplier is a borrowing/deposit principal, not a liability "cap."
  3. **Period Conflation:** The text states that the $189M carrying value as of June 30, 2026 "includes $43m accrued premiums." In fact, the $43M premium was the figure as of December 31, 2025 (when carrying value was $273M = $230M deposit + $43M premium). Between December 2025 and June 2026, CoreWeave made a $100M settlement payment and accrued further premiums. Conflating the 2025 premium with the June 2026 carrying value is an accounting error in the reference dataset.
- **Smallest appropriate correction:** In `demo.py`, update `reported_principal` to accurately state that $189M is the carrying value as of June 30, 2026, remove the claim that it contains "$43m accrued premiums", and change the display label from "contractual_cap" to "original_deposit_received".
- **Status:** Confirmed.

### Finding FIN-02 (Severity: Medium) — Unsubstantiated Zero Balance-Sheet Liability Assumption for NVIDIA Residual Value Guarantee
- **File & Line:**
  - `parallax/demo.py:99`
  - `cases/real_world/nvidia_ports.json:27`
  - `cases/real_world/wagner_reference.json:68`
- **Evidence:** In `demo.py` line 99, `reported_principal` is defined as:
  ```python
  "reported_principal": "None ($0 recognized on balance sheet)"
  ```
  Meanwhile, `wagner_reference.json` line 68 notes:
  ```json
  "notes": "Guarantees classified as credit derivatives; GMV covers data center power and transmission costs; payment conditional on ready-for-service..."
  ```
- **Why it matters:** Under US GAAP (ASC 460-10-25 and ASC 815), guarantees and credit derivatives must be recognized as liabilities at fair value on the balance sheet at inception, even if the likelihood of payment is remote. While NVIDIA’s Note 17 reports the $105B maximum gross exposure in the commitments and contingencies note, asserting that "$0 is recognized on the balance sheet" assumes without evidence that NVIDIA recorded zero initial fair-value guarantee liability or derivative liability.
- **Smallest appropriate correction:** Clarify the description: "$0 debt principal recognized from this contract (fair value carrying amount of guarantee liability not separately extracted)."
- **Status:** Confirmed.

### Finding FIN-03 (Severity: Medium) — Synthetic Waterfall Imposes Non-Standard "Guarantee of Collection" Insolvency Mechanics
- **File & Line:**
  - `cases/subsidiary_pair.json:24, 34-35`
  - `parallax/paired.py:63-72`
  - `cases/harbor.json:19, 29-30`
  - `parallax/cli.py:68-74`
- **Evidence:** In Cedar Holdings (`subsidiary_pair.json`), the settlement sequence requires:
  ```json
  "First liquidate subsidiary and pay its lender from subsidiary proceeds. After this recovery, any parent guarantee claim becomes immediately due for the covered remaining shortfall. Finally settle parent claims and distribute any parent equity residual."
  ```
  The resulting guarantee claim is then pooled *pari passu* with the parent bond against standalone parent cash.
- **Why it matters:** In commercial lending and insolvency law:
  1. Corporate debt guarantees are standardly **guarantees of payment**, not **guarantees of collection**. Under a guarantee of payment, the lender has an immediate, unconditional right to demand payment from the parent upon subsidiary default, without exhausting remedies against the subsidiary first.
  2. Subsidiary bankruptcy typically triggers cross-default clauses under parent indentures, accelerating parent debt.
  3. Pro-rata pooling at a single terminal settlement date ignores the time value of money, administrative bankruptcy costs, and legal entity separateness in multi-jurisdiction insolvencies.
  While Parallax explicitly notes these are synthetic assumptions, calling this a benchmark for "how corporate obligations affect stakeholders" measures performance on an idiosyncratic artificial waterfall that conflicts with commercial credit practice.
- **Smallest appropriate correction:** Add a prominent note to `cases/subsidiary_pair.md` explaining that the synthetic case models an artificial "guarantee of collection" waterfall rather than a standard corporate guarantee of payment.
- **Status:** Confirmed.

---

## 5. Benchmark and Evidence-Grounding Findings

### Finding BENCH-01 (Severity: Medium) — Answer Leakage in Offline Task Generation
- **File & Line:** `parallax/cli.py:94-127` (`prepare_task`)
- **Evidence:**
  When generating tasks via `prepare_task()` or CLI `python -m parallax --all`, the output JSON includes:
  ```python
  "deterministic_reference": {
      "purpose": "Visible arithmetic checks for reasoning; not a hidden evaluation benchmark.",
      "rounding": "Amounts in case units and recovery percent rounded to six decimals, half-even. Calculate before rounding.",
      "values": calculations,
  }
  ```
- **Why it matters:** While `parallax/model_api.py` (`build_request`) strips `deterministic_reference` when submitting live calls to Meta Model API, any third-party benchmark harness that ingests the `--all` JSON array receives the exact numerical answers inside the prompt payload. If an LLM is evaluated on `prepare_task` output, it can echo the precomputed numbers directly.
- **Smallest appropriate correction:** Add an explicit `--hide-answers` flag or strip `deterministic_reference` by default from `prepare_task()`, requiring an opt-in `--include-answers` flag for inspection.
- **Status:** Confirmed.

### Finding BENCH-02 (Severity: Medium) — Citation Verification is Superficial Dictionary Lookup of Reviewer Entries
- **File & Line:** `parallax/benchmark.py:206-210`
- **Evidence:**
  ```python
  source = citation["document_id"]
  location = citation["location_id"]
  recognized = location in known and known[location]["document_id"] == source
  lines.append(f"  - Reviewer-entered citation {source}/{location}: recognized identifier = {recognized}; semantic support requires human review.")
  ```
- **Why it matters:** The benchmark does not automatically parse, extract, or verify citations from model outputs. Instead, a human reviewer must manually read the model’s response, find the citation, look up the location ID, and type it into a JSON template. The code only checks whether the reviewer-entered string matches a key in a 5-item dictionary (`8K_ITEM101`, `FORM_2`, etc.). This provides zero automated verification of factual grounding.
- **Smallest appropriate correction:** Clarify in `docs/benchmark.md` that citation checks validate the syntax of reviewer-entered metadata, not automated model citation grounding.
- **Status:** Confirmed.

### Finding BENCH-03 (Severity: Medium) — Simple Deterministic Rule Baselines Outperform LLM
- **File & Line:**
  - `parallax/cli.py:56-91` (`reference_calculations`)
  - `parallax/paired.py:53-94` (`reference_values`)
  - `cases/real_world/*.json`
- **Evidence:**
  1. In the synthetic cases (Harbor and Cedar), the deterministic functions `reference_calculations()` and `reference_values()` calculate exact settlement distributions in microseconds with 100% precision. The LLM in `results/first-live.json` and `results/subsidiary-pair-live.json` produced imprecise narrative approximations and citation slips.
  2. In the real-world cases, the input evidence is a ~150-word text summary containing explicit dollar amounts and entity names. A deterministic regex/NER rule baseline extracts the caps, entities, and triggers without hallucinating the unverified claims made by the LLM (e.g. inventing *pari passu* status or $105B LGD).
- **Why it matters:** Benchmark evaluation should demonstrate that generative AI provides marginal value over deterministic or rule-based baselines. Here, simple deterministic scripts outperform the LLM on arithmetic and waterfall allocations, and basic regex extractors match factual extraction without risk of financial hallucination.
- **Smallest appropriate correction:** Benchmark future LLM evaluations directly against a deterministic regex baseline and a deterministic arithmetic baseline.
- **Status:** Confirmed.

---

## 6. Engineering Findings

### Finding ENG-01 (Severity: Medium) — Inconsistent Provenance and Erroneous SEC Accessions Masked by Unit Tests
- **File & Line:**
  - `parallax/demo.py:96, 120, 144` (`ISSUER_REGISTRY`)
  - `tests/test_demo.py:149`
  - `cases/real_world/nvidia_ports.json:11, 22`
  - `cases/real_world/meta_capacity.json:11`
  - `cases/real_world/coreweave_deposit.json:11, 23`
- **Evidence:**
  `demo.py` hardcodes erroneous SEC accession numbers that contradict the primary benchmark evidence files:
  - NVIDIA: `demo.py:96` states `accession 0001045810-26-000085`. The actual accessions in `nvidia_ports.json` are `0001045810-26-000069` (Form 8-K) and `0001045810-26-000075` (Form 10-Q).
  - Meta: `demo.py:120` states `accession 0001326801-26-000078`. The actual accession in `meta_capacity.json` is `0001628280-26-050705`.
  - CoreWeave: `demo.py:144` states `accession 0001826543-26-000042`. The actual accessions in `coreweave_deposit.json` are `0001769628-26-000104` (Form 10-K) and `0001769628-26-000366` (Form 10-Q).
  In `tests/test_demo.py:149`, the test explicitly asserts the erroneous accession:
  ```python
  self.assertIn("0001045810-26-000085", text(app))
  ```
- **Why it matters:** This introduces a data integrity discrepancy between the Streamlit workstation and the underlying benchmark cases. Users inspecting the Financial Obligations tab in Streamlit are shown erroneous accession numbers. The unit test passes only because it was hardcoded to expect the erroneous value.
- **Smallest appropriate correction:** Correct the accession numbers in `demo.py` lines 96, 120, and 144 to match `cases/real_world/*.json`, and update `tests/test_demo.py:149` to assert the verified accession `0001045810-26-000075`.
- **Status:** Confirmed.

### Finding ENG-02 (Severity: Low) — Streamlit Metric String Splitting UI Bug
- **File & Line:** `streamlit_app.py:210, 212`
- **Evidence:**
  In `streamlit_app.py` line 210:
  ```python
  cols[0].metric("Disclosed Contractual Cap", issuer_data["contractual_cap"].split()[0])
  ```
  For Meta Platforms, `issuer_data["contractual_cap"]` is `"Up to $14.72bn over five years"`.
  Calling `.split()[0]` evaluates to `"Up"`.
  In line 212:
  ```python
  cols[2].metric("Direct Commitment", "None reported" if issuer_data["reported_principal"].startswith("None") else "$189m carrying")
  ```
  This hardcodes `"$189m carrying"` for any non-synthetic issuer whose principal string does not start with `"None"`.
- **Why it matters:** When viewing Meta Platforms in the Streamlit workstation, the top metric card renders:
  `Disclosed Contractual Cap: Up`
  This is a visible formatting glitch that undermines application polish.
- **Smallest appropriate correction:** Extract the dollar amount using regex or store clean display values (e.g. `"$14.72bn"`) in `ISSUER_REGISTRY`.
- **Status:** Confirmed.

### Finding ENG-03 (Severity: Low) — Commendable Offline Execution and Zero-Key Safety
- **File & Line:** `pyproject.toml`, `tests/`
- **Evidence:** The test suite uses mocking (`unittest.mock.patch`) and offline data fixtures across all 55 tests. Secret tokens are isolated to `.env` (ignored by Git) and never logged. Atomic file replacement prevents corrupted checkpoints during network timeouts.
- **Why it matters:** Software reliability, reproducibility, and security practices in Parallax are clean and conform to best practices.
- **Smallest appropriate correction:** None required.
- **Status:** Confirmed.

---

## 7. Test Execution Results

The unit test suite was executed locally using Python 3.13 via `uv run`:

```sh
uv run python -m unittest discover -s tests -v
```

### Execution Summary
- **Total Tests Executed:** 55
- **Passed:** 55
- **Failed:** 0
- **Errors:** 0
- **Skipped:** 0
- **Execution Time:** ~3.41 seconds
- **Network / API Calls:** 0 (all mocked)

### Test Coverage Breakdown
- `test_case.py` (9 tests): Deterministic loading, invalid decimal rejection, base waterfall, stress rational waterfall against exact Fraction arithmetic, cash conservation, claim capping, CLI reproducibility.
- `test_model_api.py` (7 tests): Request builder isolation, HTTP request construction, transport errors, checkpoint preservation on failure, missing key preflight.
- `test_paired.py` (6 tests): Subsidiary recourse pair loading, reference hand calculations, prompt isolation, failure handling, preview CLI.
- `test_real_world.py` (4 tests): Disclosure case loading, prompt exclusion of Wagner labels, single live request persistence, preview reproducibility.
- `test_investor_conditional.py` (4 tests): Independent investor prompts, exact evidence equality, failure checkpointing, CLI preview.
- `test_benchmark.py` (6 tests): Three-case registry loading, source cutoff validation, execution persistence, incomplete answer checkpointing, comparison reporting.
- `test_ablation.py` (6 tests): Twelve-cell matrix generation, preregistration verification, schedule replay, blind packaging, reveal verification.
- `test_demo.py` (13 tests): Streamlit AppTest coverage across all 5 analytical functions, ticker search, persistent context, planned perspective warnings, saved response inspection, mocked live inference.

---

## 8. Prioritized Minimal Corrections

The following prioritized corrections are recommended to achieve scientific validity and resolve defects, without requiring architectural redesigns:

1. **Refocus Benchmark Claims (Scientific Validity):**
   - Update `README.md` and `docs/benchmark.md` to state that Parallax evaluates **reading comprehension and prompt adherence on pre-digested 150-word factual summaries**, not the extraction or discovery of undisclosed obligations from corporate SEC filings.
2. **Standardize on Neutral Prompts as Primary Benchmark:**
   - Use the `neutral` instruction condition as the primary benchmark standard. Measure whether models can maintain financial discipline *without* negative prompt spoon-feeding.
3. **Conduct Independent Blinded Human Evaluation:**
   - Utilize the existing anonymized package (`reviews/guidance-ablation-v1/review.md`) to collect ratings from multiple independent human financial analysts, replacing assistant-authored evaluation drafts.
4. **Fix CoreWeave & NVIDIA Data Inconsistencies (Financial Correctness):**
   - Correct `demo.py` line 147 to remove the claim that the June 30, 2026 balance includes "$43m accrued premiums".
   - Re-label CoreWeave’s original deposit from "contractual_cap" to "original_deposit_received" and note that it serves as an on-balance-sheet debt control.
   - Refine NVIDIA’s "$0 recognized on balance sheet" statement to specify that it refers to borrowing principal rather than fair-value guarantee/derivative liabilities.
5. **Fix Accession Number Inconsistencies and Test Assertion (Engineering):**
   - In `parallax/demo.py`, update lines 96, 120, and 144 to match the verified SEC accession numbers in `cases/real_world/*.json`.
   - In `tests/test_demo.py:149`, update the test assertion to expect the verified accession number.
6. **Fix Streamlit Metric String Splitting (UI Bug):**
   - Update `streamlit_app.py:210` to display `"$14.72bn"` instead of `"Up"` for Meta Platforms.

---

## 9. Remaining Uncertainties

1. **Model Training Set Exposure:** The SEC filings for NVIDIA, Meta, and CoreWeave are historical public disclosures from August 2026. It is unknown whether the evaluated model (`muse-spark-1.3`) was trained on these exact disclosures or on Alexander F. Wagner's published dataset, which would introduce uncontrolled test set contamination.
2. **Behavior on Unseen Corporate Disclosures:** Because all three real-world cases are well-known AI-infrastructure financing arrangements from 2026, it remains uncertain how the model would perform on private credit arrangements, joint venture debt, or complex synthetic lease structures outside the AI sector.
3. **Multi-Turn Financial Interrogation:** Parallax currently evaluates single-turn completions. It remains untested whether structured multi-turn dialogue or self-critique could help an unguided model identify its own hallucinations (such as *pari passu* assumptions).

---

## 10. Final Recommendation

### Recommendation: **NOT YET SCIENTIFICALLY VALID**

**Justification:**
Parallax demonstrates strong software engineering, excellent offline test coverage, clean dependency management, and thoughtful UI design. However, as an empirical benchmark of AI capabilities for financial analysis and obligation identification, it is not yet scientifically valid for three fundamental reasons:

1. **Pre-Digested Inputs:** The benchmark does not test an LLM's ability to extract or identify obligations from financial disclosures; human researchers performed all extraction and classification prior to prompting.
2. **Negative Prompt Spoon-Feeding:** The guided prompts explicitly coach the model on the exact negative constraints being evaluated. When evaluated without these hints (the neutral condition), the model immediately fails and hallucinates legal priority and loss figures.
3. **Circular, Non-Independent Evaluation:** The ground-truth assertions, reference files, and evaluation ratings were all authored by the same LLM assistant that designed the system, evaluated on a single sample per cell ($N=1$), without independent blinded human adjudication.

**Pathway to "REVISE" / "ACCEPT":**
If the project authors formally adjust their claims to describe Parallax as an **exploratory qualitative workstation and prompt-sensitivity diagnostic tool for pre-curated financial notes**, fix the documented data and accession inconsistencies in `demo.py`, and recruit independent human financial experts to evaluate the blinded review package across multiple random samples ($N \ge 10$), the project will achieve scientific validity within that more realistic and well-defined scope.
