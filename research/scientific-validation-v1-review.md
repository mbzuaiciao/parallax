# Independent Scientific Protocol Review: Parallax Scientific Validation Pilot v1

**Reviewer:** Independent Scientific & Methodological Reviewer  
**Date of Review:** October 29, 2026  
**Repository:** `parallax`  
**Target Protocol:** `protocols/scientific-validation-v1/protocol.md`  
**Target Artifacts:**  
- `protocols/scientific-validation-v1/references.json`
- `protocols/scientific-validation-v1/prepare.py`
- `protocols/scientific-validation-v1/apple.json`
- `protocols/scientific-validation-v1/microsoft.json`
- `tests/test_scientific_validation.py`
**Historical Context:**  
- `protocols/guidance-ablation-v1.md` / `protocols/guidance-ablation-v1.json`
- `research/independent-audit-antigravity.md` (October 29, 2026)
- `research/post-audit-verification.md` (Commit `f2c65e3`)
- `docs/post-audit-corrections.md`
- `cases/real_world/*.json`

---

## Executive Summary & Review Verdict

This independent scientific review evaluates the proposed **Parallax Scientific Validation Pilot v1** (`scientific-validation-v1`). The protocol is designed to test whether Parallax's developer analytical guidance improves the evidential discipline and factual correctness of language model interpretations of corporate financial disclosures compared to a neutral instruction baseline, evaluated across five real-world cases with three repetitions per cell ($N = 30$ planned responses).

### Summary Assessment Across the Five Review Objectives

1. **Research Question & Construct Validity:** The experiment primarily tests **negative constraint compliance on pre-curated 150-word text summaries**, rather than autonomous financial reasoning about economic leverage, contractual mechanics, or filing discovery. The guided prompt explicitly tells the model what *not* to do ("do not infer redacted identities, invent financial inputs, assume a creditor ranking, or turn a disclosed cap into an expected loss"), while the neutral prompt omits these negative constraints. Conflating prompt obedience with evidential financial discipline remains a central construct validity limitation.
2. **Independent Ground Truth:** All five reference records in `references.json` are **provisional**, authored by an AI assistant on October 29, 2026, and explicitly unverified by an independent human financial expert (`"reviewer": null`, `"decision": "pending"`). Executing live calls before freezing reviewed, verified references violates the protocol's own gating condition (line 44). Furthermore, for three of the five cases (NVIDIA, Meta, Apple), recognized accounting liabilities are "not established" in the evidence, creating a severe scoring contradiction against a rubric that demands distinguishing contractual exposure from recognized balance-sheet liabilities.
3. **Experimental Fairness:** The guided condition delivers a compound intervention of 11 distinct instructions (125 words) compared to 3 instructions (35 words) in the neutral condition. Moreover, `apple.json` and `microsoft.json` leave the `short_quote` fixture field blank (`""`), introducing structural evidence asymmetry across cases. The curated paraphrases themselves leak negative facts (e.g. explicitly stating that cancellation rights, pricing, and ranking are absent).
4. **Evaluation Validity:** The rubric contains substantial dimensional correlation and lacks an operational definition for "material unsupported assertion" (the primary binary endpoint). Disagreements between independent raters currently trigger an `unscorable` classification that threatens to withhold entire cases from the evaluation. Crucially, the prompt-induced structural formatting (numbered headings, structured categories) creates an unmistakable stylistic fingerprint that undermines rater blinding.
5. **Reproducibility & Execution Readiness:** The offline preparation script (`prepare.py`) and test suite (`test_scientific_validation.py`) exhibit excellent software engineering and determinism. However, the requested model (`muse-spark-1.3`), endpoint, and sampling parameters (`temperature=0.7`, `max_completion_tokens=8192`) have not been verified against live API schema requirements. Under the protocol's strict "no-retry, no-replacement" rule, an invalid parameter risks failing all 30 attempted slots immediately.

---

### Final Verdict: **REVISE BEFORE EXECUTION**

The protocol is not approved for live execution in its current state. Four **BLOCKER** findings must be resolved before model calls may be initiated:
1. **BLOCKER GT-01:** Ground-truth reference records must be independently reviewed, approved, and frozen by a human financial expert prior to execution, as required by the protocol's own gating rule.
2. **BLOCKER GT-02 / EVAL-01:** The rubric and reference boundary for "distinguishing contractual exposure from disclosed recognition" must be reconciled for cases where recognition is not established (NVIDIA, Meta, Apple) to eliminate an impossible scoring paradox.
3. **BLOCKER FAIR-01:** The rubric must be adjusted so that neutral responses are not penalized under Evidence Grounding (Dimension 3) for omitting schema-specific document IDs (`MSFT_10K`) that the neutral prompt never requested.
4. **BLOCKER REP-01:** API parameter support (`temperature=0.7`, `max_completion_tokens=8192`) and model availability must be preflight-verified against provider specifications to prevent immediate batch failure.

Once these minimal corrections are implemented and refrozen, the protocol can proceed to execution as a descriptive, exploratory pilot.

---

## Detailed Review Findings

```
========================================================================================
FINDING TAXONOMY:
- BLOCKER:   Must be corrected before model execution.
- IMPORTANT: Materially affects scientific interpretation but does not prevent a pilot.
- OPTIONAL:  Worthwhile future improvement.
========================================================================================
```

---

## 1. Research Question and Construct Validity

### Research Question Formulation
The protocol investigates:
> *"Does existing Parallax analytical guidance improve the correctness and evidential discipline of financial interpretations of supplied corporate disclosures compared with neutral instructions? We hypothesize fewer material unsupported assertions and better distinction between contractual exposure and recognized liability."* (`protocol.md:10-13`)

### Construct Validity Assessment
Construct validity assesses whether the operational test actually measures the theoretical construct: **unaided financial reasoning and evidential discipline regarding corporate contractual obligations**.

#### Finding RQ-01 (IMPORTANT) — Negative Constraint Compliance Masquerading as Evidential Discipline
- **Category:** Construct Validity  
- **Severity:** IMPORTANT  
- **Evidence:**  
  In [`parallax/real_world.py:67-70`](file:///Users/xq/Documents/GitHub/parallax/parallax/real_world.py#L67-L70), the guided developer instruction dictates:
  ```text
  "Use only the supplied evidence; do not infer redacted identities, invent financial inputs, 
  assume a creditor ranking, or turn a disclosed cap into an expected loss or payable balance."
  ```
  In [`parallax/ablation.py:20-23`](file:///Users/xq/Documents/GitHub/parallax/parallax/ablation.py#L20-L23), the neutral instruction asks:
  ```text
  "Analyze the supplied financing arrangement from the perspective of (1) an equity investor in {company} 
  and (2) a senior unsecured creditor of {company}. Explain its economic significance, cite supporting evidence, 
  and identify material uncertainties."
  ```
  The primary endpoint is:
  ```text
  "The binary primary endpoint is any material unsupported assertion in a complete response..." (protocol.md:165)
  ```
- **Analysis:**  
  When an LLM refrains from assuming *pari passu* ranking or calling a cap an expected loss under the guided condition, it is simply following explicit negative instructions. In the neutral condition, the model is asked to act as a senior unsecured creditor; under standard credit analysis conventions, an analyst evaluates where the claim sits in the capital structure. Without a negative constraint, the model attempts to answer the perspective prompt by supplying standard legal assumptions (*pari passu*, unsecured).
  
  Therefore, the experiment does not isolate whether guidance develops "financial reasoning." It measures **prompt-constraint obedience**. The model's success in the guided arm is achieved through rule-following compliance, while its failure in the neutral arm is driven by the prompt omitting the boundary rules.
- **Impact on Pilot:** Results cannot be interpreted as proving that the model has acquired intrinsic financial evidential discipline. They must be reported as the efficacy of explicit negative guardrails.

#### Finding RQ-02 (IMPORTANT) — Reading Comprehension of Pre-Digested Summaries Replaces Filing Extraction
- **Category:** Construct Validity  
- **Severity:** IMPORTANT  
- **Evidence:**  
  The supplied evidence consists of short, manually paraphrased snippets:
  - `apple.json`: 55 words summarizing Apple's manufacturing purchase commitments.
  - `microsoft.json`: 68 words summarizing operating lease balances and payments.
  - `meta_capacity.json`: 152 words summarizing Note 9.
  - `coreweave_deposit.json`: Two short note excerpts.
  In `meta_capacity.json` and `coreweave_deposit.json`, the paraphrases explicitly state:
  ```text
  "The passage does not specify annual payments for the contingent arrangement, unilateral cancellation 
  rights, its detailed pricing or delivery schedule, security or claim ranking." (meta_capacity.json:17)
  
  "Detailed termination notice periods, collateral and relative claim ranking are not provided in this 
  selected subsection." (coreweave_deposit.json:17)
  ```
- **Analysis:**  
  The model is not evaluating primary SEC EDGAR disclosures or raw footnote tables. Human annotators have already extracted the relevant numbers, classified the obligation, and explicitly written into the prompt text what is missing. When the model states that "pricing and cancellation rights are undisclosed," it is not exercising financial judgment about contractual ambiguity; it is extracting statements directly provided in the user prompt.
- **Impact on Pilot:** The experiment tests reading comprehension and text summarization on curated 100-word snippets, not autonomous disclosure analysis.

#### Finding RQ-03 (OPTIONAL) — Uncontrolled Test Set Contamination and Memorization
- **Category:** Construct Validity  
- **Severity:** OPTIONAL  
- **Evidence:**  
  The five corporate disclosures involve prominent public companies:
  - Apple Form 10-K (filed October 31, 2025)
  - Microsoft Form 10-K (filed July 30, 2025)
  - NVIDIA Form 8-K/10-Q (filed August 2026)
  - Meta Form 10-Q (filed July 2026)
  - CoreWeave Form 10-K/10-Q (filed March/August 2026)
  In addition, Alexander F. Wagner's academic dataset (`leverage-beyond-debt`, version 1.1) was published on GitHub in October 2026.
- **Analysis:**  
  In the historical preliminary review (`results/guidance-ablation-v1-preliminary-review.md:39`), the neutral model introduced issuer-wide asset and debt figures for CoreWeave that were absent from the prompt pack. This demonstrates that the model possesses external pre-trained knowledge about these specific issuers. Memorization can allow the model to succeed or fail based on training set recall rather than evidence synthesis.

---

## 2. Independent Ground Truth & Provisional Reference Records

The review examined all five provisional reference records in [`protocols/scientific-validation-v1/references.json`](file:///Users/xq/Documents/GitHub/parallax/protocols/scientific-validation-v1/references.json).

```
========================================================================================
SUMMARY OF PROVISIONAL REFERENCE RECORDS:
Total Records: 5
Independent Reviewer Status: ALL PENDING ("reviewer": null, "decision": "pending")
Preparer: Codex assistant (October 29, 2026); no human domain expert sign-off.
========================================================================================
```

### Case-by-Case Audit of Reference Records

#### 1. NVIDIA PORTS (`nvidia-ports`)
- **Primary Sources:** SEC Form 8-K (Item 1.01, 2026-08-17), Form 10-Q (Note 17, 2026-08-26), Form of Agreement (Exhibit 10.1).
- **Supported Primary Facts:**
  - `N1`: NVIDIA guarantees defined lease-related obligations to SB Energy lessors; OpenAI affiliate is tenant; OpenAI undertakes reimbursement. (Supported by 8-K Item 1.01).
  - `N2`: Initial cumulative cap of $105B across initial guaranties; effectiveness tied to lease commencement and ready-for-service conditions. (Supported by 8-K Item 1.01).
  - `N3`: Default triggers require landlord termination right and intent plus notice/cure; remedies qualify exposure. (Supported by Form Ex. 10.1 Sections 2, 8, 12).
- **Accounting Liability Status:** `"not_established"`. The 8-K describes an August signing occurring after the July 26 balance-sheet date. Carrying liability is not established in the supplied pack.
- **Missing Evidence in Pack:** Redacted payment schedules, discount rate, loss formula, pre-RFS termination formula, and counterparty credit rating.
- **Circularity / Pre-Judged Conclusions:** Reference asserts: *"Do not infer all obligations become immediately payable or all reimbursement is recoverable."* This targets the exact error committed by the neutral model in historical ablation run R001.

#### 2. Meta Cloud Capacity (`meta-capacity`)
- **Primary Sources:** SEC Form 10-Q (Note 9, 2026-07-30).
- **Supported Primary Facts:**
  - `M1`: Meta is purchaser of up to $14.72B cloud capacity over five years; provider is unnamed in note. (Supported by Note 9).
  - `M2`: Third-party capacity sales may reduce contingent purchase obligations. (Supported by Note 9).
  - `M3`: Neighboring $349.31B aggregate commitments and $53.52B/$81.65B schedules are separate context, not the capacity schedule. (Supported by Note 9).
- **Accounting Liability Status:** `"not_established"`. Disclosed cap is not a carrying measurement.
- **Missing Evidence in Pack:** Provider identity (Nebius in Wagner dataset), pricing, annual delivery schedule, cancellation terms, security/priority.
- **Circularity / Pre-Judged Conclusions:** Target `M3` is not an affirmative contract term; it is an explicit distractor instructing the model not to look at the preceding paragraph. The reference explicitly notes: *"No forced borrowing, debt equivalence, de facto operating priority, expected loss or default probability is verified."* This assumes the rejection of Alexander Wagner's academic coding (`U4/L3`, non-cancelable debt-equivalent) and the neutral model's finding of operating priority.

#### 3. CoreWeave Refundable Deposit (`coreweave-deposit`)
- **Primary Sources:** SEC Form 10-K (Note 10, 2026-03-02), Form 10-Q (Note 10, 2026-08-12).
- **Supported Primary Facts:**
  - `C1`: $230M refundable deposit received from MagAI Ventures; consumption reduces deposit; unused refundable. (Supported by 10-K Note 10).
  - `C2`: February 2025 termination-right amendment led to in-substance debt classification under ASC 470; termination multiplier equivalent to 12% annual return. (Supported by 10-K Note 10).
  - `C3`: December 31, 2025 debt was $273M including $43M premiums. (Supported by 10-K Note 10).
  - `C4`: June 2026 settlement was $100M; June 30 remaining carrying obligation was $189M including unused deposit and accrued premiums. (Supported by 10-Q Note 10).
- **Accounting Liability Status:** `"disclosed_recognition_pending_independent_verification"`. Recognized debt is $273M (Dec 2025) and $189M (June 2026).
- **Missing Evidence in Pack:** Full termination procedures, collateral, relative creditor ranking, forward payment schedule.
- **Circularity / Pre-Judged Conclusions:** The reference notes: *"Do not assign the December $43m premiums to the June balance. Do not infer coupon cash schedule from effective return, future payoff, equal ranking, or unsecured status."* This targets the exact post-audit defect and historical neutral errors.

#### 4. Apple Manufacturing Purchases (`apple-manufacturing`)
- **Primary Sources:** SEC Form 10-K (Item 7 MD&A, 2025-10-31, accession `0000320193-25-000079`).
- **Supported Primary Facts:**
  - `A1`: Manufacturing purchase obligations are $56.2B at September 27, 2025; $55.4B payable within 12 months. (Supported by Item 7).
  - `A2`: Purchases involve outsourced manufacturing/assembly/testing and component suppliers. (Supported by Item 7).
- **Accounting Liability Status:** `"not_established"`. The passage does not establish recognized liabilities or overlap with accounts payable.
- **Missing Evidence in Pack:** Counterparties, cancellation rights, penalty clauses, pricing, collateral, liability overlap, recovery.
- **Factual & Structural Defects:**
  1. `apple.json` has **`short_quote: ""`** (empty string).
  2. The record contains only **2 factual targets**, compared to 3 or 4 in other cases.
  3. The reference asserts: *"Do not equate the disclosed obligation with additional debt or assert zero recognition."*

#### 5. Microsoft Commenced Operating Leases (`microsoft-leases`)
- **Primary Sources:** SEC Form 10-K (Note 1 and Note 13, 2025-07-30, accession `0000950170-25-100235`).
- **Supported Primary Facts:**
  - `L1`: Operating lease liability is $22,861M at June 30, 2025: $5,424M current and $17,437M noncurrent. (Supported by Note 13).
  - `L2`: Undiscounted operating payments $25,481M less $2,620M imputed interest reconcile to the liability; fiscal 2026 payments are $6,111M. (Supported by Note 13).
  - `L3`: Recognition at commencement uses present value of lease payments. (Supported by Note 1).
- **Accounting Liability Status:** `"disclosed_recognition_pending_independent_verification"`. Recognized liability is $22,861M.
- **Missing Evidence in Pack:** Lessor identities, relative ranking, default remedies.
- **Factual & Structural Defects:**
  1. `microsoft.json` has **`short_quote: ""`** (empty string).
  2. `L1`, `L2`, and `L3` are near-verbatim transcriptions of the 68-word paraphrase provided to the model in `microsoft.json`.

---

### Critical Ground Truth Findings

#### Finding GT-01 (BLOCKER) — Provisional Reference Records Lack Independent Ground Truth and Protocol Self-Contradicts on Gating
- **Category:** Ground Truth  
- **Severity:** BLOCKER  
- **Evidence:**  
  In [`protocols/scientific-validation-v1/references.json`](file:///Users/xq/Documents/GitHub/parallax/protocols/scientific-validation-v1/references.json), all five cases state:
  ```json
  "status": "provisional",
  "independent_verification": {
    "reviewer": null,
    "date": null,
    "decision": "pending",
    "method": "Inspect primary source for each factual assertion; record approval or dispute with locator before outcome scoring."
  }
  ```
  In [`protocols/scientific-validation-v1/protocol.md:44-46`](file:///Users/xq/Documents/GitHub/parallax/protocols/scientific-validation-v1/protocol.md#L44-L46):
  ```text
  "Freeze reviewed references and hashes before any future experiment; revisions require a dated protocol version."
  ```
- **Why it is a BLOCKER:**  
  The protocol explicitly forbids conducting experiments against unverified references. If live calls are executed against provisional reference targets that are later disputed or amended by independent human reviewers, the SHA-256 bindings in `prepare.py` (`files_sha256`, `source_versions`) will be broken. Worse, post-hoc adjustments to reference targets after observing model responses would introduce serious confirmation bias. An empirical benchmark cannot execute model evaluations against unratified ground truth.
- **Smallest Possible Correction:**  
  Before executing any live model calls, a designated independent human financial reviewer must inspect the primary SEC filings, record formal approval or dispute for each target in `references.json`, update `"status"` from `"provisional"` to `"verified"`, and re-freeze the plan hashes via `prepare.py`.

#### Finding GT-02 (BLOCKER) — Impossible Scoring Paradox for Unrecognized Liabilities (Apple, Meta, NVIDIA)
- **Category:** Ground Truth & Evaluation Validity  
- **Severity:** BLOCKER  
- **Evidence:**  
  In `references.json`:
  - Apple: *"This passage does not separately establish recognized liabilities or overlap with accounts payable. Do not equate the disclosed obligation with additional debt or assert zero recognition."* (`references.json:294-296`)
  - Meta: *"The selected passage does not establish a separately recognized carrying liability for this arrangement; the disclosed cap is not that measurement."* (`references.json:146-148`)
  - NVIDIA: *"No separately measured PORTS carrying liability established by this supplied pack. Neither zero nor the cap is a verified accounting balance."* (`references.json:75-77`)
  In `protocol.md:145`, the Rubric for Dimension 2 (Financial/accounting interpretation) requires:
  - **Score 2:** *"Distinguishes contractual exposure from disclosed recognition and explains warranted cash-use/service tradeoffs for both stakeholders"*
  - **Score 0:** *"Material misclassification, double counting, invented recovery/priority, or no economic analysis"*
- **Why it is a BLOCKER:**  
  This creates an unresolvable scoring paradox:
  1. Under US GAAP (ASC 440), executory manufacturing purchase commitments (Apple) are off-balance-sheet commitments; they have **$0 recognized liability** on the balance sheet until delivery occurs. If an intelligent financial analyst or LLM correctly applies US GAAP and states "this obligation is not recognized on the balance sheet," Parallax's reference explicitly forbids that answer: *"Do not... assert zero recognition."*
  2. If the model treats it as a balance sheet liability, it is penalized for "equating disclosed obligation with additional debt."
  3. If the model says nothing about balance-sheet recognition, it fails Dimension 2 Score 2 ("Distinguishes contractual exposure from disclosed recognition").
  4. The reference boundary claims: *"Accounting conclusions not established here are unknown, not zero."* But in financial accounting, when an analyst evaluates a commitments note, determining that it is *off-balance-sheet* ($0 debt liability) is the fundamental analytical task. Penalyzing both affirmative zero recognition and debt recognition while demanding a distinction between exposure and recognition makes consistent scoring impossible.
- **Smallest Possible Correction:**  
  Clarify in `references.json` and the Dimension 2 rubric that for cases where liabilities are not recognized (Apple, Meta, NVIDIA), explicitly stating that **the footnote reflects an off-balance-sheet contractual commitment with no carrying debt liability established in the disclosure** earns full credit (Score 2) for the recognition distinction.

#### Finding GT-03 (IMPORTANT) — Distractor Negative Facts Mislabeled as Core Factual Targets
- **Category:** Ground Truth  
- **Severity:** IMPORTANT  
- **Evidence:**  
  In Meta (`meta-capacity`), core factual target `M3` is:
  ```text
  "The neighboring $349.31 billion aggregate commitments and 2026/2027 amounts are separate context, 
  not the capacity arrangement payment schedule." (references.json:132-134)
  ```
- **Analysis:**  
  `M3` is not a contractual fact about Meta's cloud capacity arrangement. It is a negative warning about an adjacent, unrelated paragraph that the human preparer chose to include in `meta_capacity.json`. Elevating "do not look at the neighboring paragraph" to one of three core factual targets penalizes a model that produces a clean, focused analysis of the capacity agreement without mentioning irrelevant surrounding disclosures.
- **Smallest Possible Correction:**  
  Move `M3` from `core_factual_targets` to `material_uncertainties_and_unsupported_conclusions` or evaluation notes.

---

## 3. Experimental Fairness

### Comparison of Prompt Conditions

```
========================================================================================
CONDITION PROMPT COMPARISON:
Guided Developer Prompt: 125 words, 11 explicit procedural & negative constraints.
Neutral Developer Prompt: 35 words, 3 high-level instructions.
User Evidence Payload:    100% byte-for-byte identical (verified by unittest).
========================================================================================
```

#### Finding FAIR-01 (BLOCKER) — Asymmetric Prompts Lead to Unfair Scoring Penalties Under Rubric
- **Category:** Experimental Fairness  
- **Severity:** BLOCKER  
- **Evidence:**  
  In [`protocols/scientific-validation-v1/protocol.md:146`](file:///Users/xq/Documents/GitHub/parallax/protocols/scientific-validation-v1/protocol.md#L146), the rubric for Dimension 3 (Evidence grounding) states:
  - **Score 2:** *"All material factual claims have semantically supporting supplied document/locator citations"*
  - **Score 1:** *"Some material claims unlinked or imprecise but traceable; none falsely attributed"*
  - **Score 0:** *"Central claim falsely cited, unsupported by cited passage, or no usable citations"*
  In `prepare.py`:
  - Guided Developer Prompt explicitly commands: `"Cite document IDs and provision locators."`
  - Neutral Developer Prompt only says: `"cite supporting evidence"`.
- **Why it is a BLOCKER:**  
  The neutral prompt does not instruct the model to use Parallax's custom schema document IDs (`MSFT_10K`, `AAPL_10K`) or specific provision locators. If a neutral completion cites supporting evidence using standard financial prose (e.g., *"According to Note 13 of Microsoft's 2025 Form 10-K..."*), an independent rater strictly applying Dimension 3 could assign a score of 1 or 0 for failing to provide document/locator IDs. The rubric penalizes the neutral model for omitting an idiosyncratic formatting requirement that was never requested.
- **Smallest Possible Correction:**  
  Explicitly amend the rubric for Dimension 3 (Evidence grounding) to state that standard prose citations naming the primary filing and footnote section (e.g. "Note 13", "Item 7") satisfy Score 2 equally with schema document IDs (`MSFT_10K`), ensuring neutral responses are not penalized for prompt formatting differences.

#### Finding FAIR-02 (IMPORTANT) — Missing `short_quote` in New Cases Creates Cross-Case Evidence Asymmetry
- **Category:** Experimental Fairness  
- **Severity:** IMPORTANT  
- **Evidence:**  
  In `protocols/scientific-validation-v1/apple.json:16`:
  ```json
  "short_quote": "",
  ```
  In `protocols/scientific-validation-v1/microsoft.json:16`:
  ```json
  "short_quote": "",
  ```
  In `cases/real_world/nvidia_ports.json:15, 26, 36`:
  ```json
  "short_quote": "NVIDIA’s aggregate payment obligation is cumulatively capped at $105 billion...",
  "short_quote": "Our guarantees are limited to defined portions of lease and power payments",
  "short_quote": "actually intends to terminate the Lease"
  ```
  In `cases/real_world/meta_capacity.json:16`:
  ```json
  "short_quote": "which may be reduced if the cloud service provider is able to sell such capacity to other customers"
  ```
- **Analysis:**  
  In the three historical cases, the model receives explicit verbatim quotations alongside paraphrases. In the two new cases, `short_quote` is left completely blank. This provides verbatim textual anchor points for some cases but not others, creating structural evidence asymmetry across the benchmark.
- **Smallest Possible Correction:**  
  Populate `short_quote` in `apple.json` with a verbatim excerpt from Item 7 (e.g. `"manufacturing purchase obligations were $56.2 billion"`) and in `microsoft.json` with Note 13 text (e.g. `"Operating lease liabilities of $22,861 million"`).

---

## 4. Evaluation Validity & Rater Adjudication

### Rubric Analysis

| Dimension | Score 2 Criteria | Score 1 Criteria | Score 0 Criteria | Reviewer Threat |
|---|---|---|---|---|
| **1. Factual Correctness** | Covers core factual targets with correct entities, amounts, dates | Core mechanism correct; one material omission | Material contradiction or no usable facts | Omission vs contradiction overlap |
| **2. Financial Interpretation** | Distinguishes exposure from recognition; explains tradeoffs | Sound but incomplete distinction; one stakeholder missing | Misclassification, double counting, invented priority | **BLOCKER GT-02:** Unrecognized liabilities paradox |
| **3. Evidence Grounding** | All claims have semantically supporting citations | Claims unlinked/imprecise but traceable | Central claim falsely cited or no citations | **BLOCKER FAIR-01:** Neutral prompt didn't ask for IDs |
| **4. Unsupported Inference** | No unsupported material assertion; conditional channels | Minor unsupported detail without changing conclusion | Any unsupported material assertion, ranking, or result | Conflated with Dimension 1 & 2 |
| **5. Uncertainty/Abstention** | Identifies case-specific missing inputs; limits conclusions | Generic caveat; missed important uncertainty | Definite unsupported answer to material unknown | Pre-digested prompts spoon-feed missing inputs |

#### Finding EVAL-01 (BLOCKER) — Flawed Adjudication Mechanism and Destructive Case-Withholding Rule
- **Category:** Evaluation Validity  
- **Severity:** BLOCKER  
- **Evidence:**  
  In [`protocols/scientific-validation-v1/protocol.md:41-43`](file:///Users/xq/Documents/GitHub/parallax/protocols/scientific-validation-v1/protocol.md#L41-L43):
  ```text
  "A second reviewer checks accounting and disputed assertions. Unresolved items remain unscorable; 
  if a material target is disputed, withhold that case's aggregate result."
  ```
  In lines 187-188:
  ```text
  "Average those five case differences with equal case weights only if all five are independently 
  scorable; otherwise give case results and identify the missing comparison explicitly."
  ```
- **Why it is a BLOCKER:**  
  The protocol contains no operational mechanism (such as a third senior referee or majority voting) to resolve rater disagreements on whether an assertion is material or unsupported. Instead, it mandates that any disputed material target forces the entire case to be withheld.
  
  In a small 5-case study, withholding a single case eliminates **20% of the entire dataset** (6 responses) and prevents the primary endpoint (average guided-minus-neutral difference) from being calculated. This creates an unacceptably fragile evaluation design where a single rater dispute invalidates the aggregate experiment.
- **Smallest Possible Correction:**  
  Define an explicit adjudication procedure: if two independent raters disagree after discussion, a designated third senior adjudicator reviews the claim and issues a binding determination, ensuring that complete responses are not arbitrarily dropped from the study.

#### Finding EVAL-02 (IMPORTANT) — Prompt-Induced Stylistic Signatures Compromise Rater Blinding
- **Category:** Evaluation Validity  
- **Severity:** IMPORTANT  
- **Evidence:**  
  In the historical preliminary review ([`results/guidance-ablation-v1-preliminary-review.md`](file:///Users/xq/Documents/GitHub/parallax/results/guidance-ablation-v1-preliminary-review.md)), responses produced under guided prompts exhibited clear structural artifacts:
  - Explicit section headings mirroring the 11 prompt instructions: "Contractual Obligors", "Direct vs Contingent", "Triggers and Limits", "Equity Perspective", "Senior Unsecured Creditor Perspective".
  - Literal echoes of prompt phrases: "reimbursement is a right, not cash collected", "not an expected loss".
  Neutral responses produced conversational prose without structured headings.
- **Analysis:**  
  Even if run IDs, conditions, and prompts are removed from reviewer packages, human financial raters will immediately recognize the condition from the structural formatting of the text. Rater blinding is therefore nominal rather than effective, exposing subjective ratings to cognitive expectation bias.
- **Smallest Possible Correction:**  
  Instruct raters explicitly in the rating guidelines to disregard formatting, headings, and organizational style, focusing strictly on semantic claim content.

---

## 5. Reproducibility & Execution Readiness

### Plan Generation and Baseline Analysis

The offline plan script [`protocols/scientific-validation-v1/prepare.py`](file:///Users/xq/Documents/GitHub/parallax/protocols/scientific-validation-v1/prepare.py) was executed and validated:
- Generates exactly 30 evaluation cells (5 cases × 2 conditions × 3 repeats).
- Schedule randomization seed `20261029` is completely deterministic.
- File and evidence hashes bind the experimental inputs.
- All 63 offline unit tests pass in 3.58s.
- Deterministic synthetic arithmetic baselines (Harbor and Cedar) are properly scoped as `not_applicable` to corporate disclosure interpretation.

```
========================================================================================
REPRODUCIBILITY CHECK:
Offline Plan Verification: PASS (30 planned slots, zero live API calls).
Test Suite:                PASS (63 tests passing, zero network/credentials).
Deterministic Baseline:    PASS (harbor/cedar arithmetic scoped strictly outside disclosures).
========================================================================================
```

#### Finding REP-01 (BLOCKER) — Unverified Model Parameter Support Risks Total Batch Failure
- **Category:** Technical Reproducibility  
- **Severity:** BLOCKER  
- **Evidence:**  
  In `protocol.md:81-84`:
  ```text
  "Actual provider defaults and temperature support have not been verified in this offline phase: 
  document them before future execution; if unsupported, amend and refreeze the design before any 
  call rather than silently omitting the temperature."
  ```
  In `prepare.py:33, 89`:
  ```python
  request["temperature"] = 0.7
  "max_completion_tokens": 8192,
  ```
  In `protocol.md:115-116`:
  ```text
  "No retries or replacements: failures, refusals, missing text and truncations count among the 30 attempted slots."
  ```
- **Why it is a BLOCKER:**  
  `prepare.py` injects `temperature: 0.7` and `max_completion_tokens: 8192` into every request payload sent to `https://api.meta.ai/v1/chat/completions` for model `muse-spark-1.3`. In many chat-completion endpoints, parameter support varies: some APIs require `max_tokens` instead of `max_completion_tokens`, and reasoning/specialized models frequently reject `temperature` values other than 1.0 or omit temperature entirely.
  
  Because the protocol strictly prohibits retries, replacements, or restarts, submitting an unsupported parameter could cause all 30 requests to return immediate HTTP 400 Bad Request errors, consuming and failing the entire experimental budget.
- **Smallest Possible Correction:**  
  Conduct an authorized single-request parameter schema check (or verify against official provider API documentation) to confirm that `model: "muse-spark-1.3"`, `temperature: 0.7`, and `max_completion_tokens: 8192` are accepted without error before freezing the execution configuration.

#### Finding REP-02 (IMPORTANT) — Underpowered Sample Size ($N=3$ Per Cell) Precludes Statistical Claims
- **Category:** Statistical Validity  
- **Severity:** IMPORTANT  
- **Evidence:**  
  The experiment evaluates 5 cases × 2 conditions × 3 repetitions = 30 total calls (15 per condition; 3 per cell).
  `protocol.md:197-199` acknowledges:
  ```text
  "With five purposive cases and three responses per arm, use descriptive estimates and counterexamples 
  only. No p-values, power claims, model leaderboard, population causal claims, or post-hoc rubric changes."
  ```
- **Analysis:**  
  At $N=3$ per cell, language model generation variance at temperature 0.7 is substantial. A difference of 1 error (e.g. 0/3 vs 1/3) represents a 33% swing. The protocol commendably disclaims p-values and population inferences, but the sample size remains too small to establish statistical significance.
- **Impact on Pilot:** The experiment can only provide anecdotal qualitative comparisons and counterexamples.

---

## Consolidated Findings Matrix

| Finding ID | Severity | Category | Description | Minimal Required Correction |
|---|---|---|---|---|
| **GT-01** | **BLOCKER** | Ground Truth | References are provisional assistant drafts; no independent expert sign-off. Protocol requires freezing verified references before execution. | Have an independent human financial reviewer inspect primary sources, approve targets, and update status to verified. |
| **GT-02** | **BLOCKER** | Ground Truth / Rubric | Impossible scoring paradox for unrecognized liabilities (Apple, Meta, NVIDIA): reference forbids asserting zero recognition while rubric demands distinction. | Clarify that stating "no carrying liability is established in disclosure" or "off-balance-sheet commitment" earns full credit. |
| **FAIR-01** | **BLOCKER** | Experimental Fairness | Neutral prompt does not request schema document IDs (`MSFT_10K`), but rubric Dimension 3 penalizes responses lacking them. | Amend Dimension 3 rubric so standard filing/note citations (e.g. "Note 13") receive Score 2 equally with schema IDs. |
| **REP-01** | **BLOCKER** | Reproducibility | Temperature 0.7 and `max_completion_tokens` on `muse-spark-1.3` are unverified. Strict no-retry rule risks 100% batch HTTP 400 failure. | Verify provider parameter schema before execution to ensure payload fields are supported. |
| **RQ-01** | **IMPORTANT** | Construct Validity | Experiment measures negative prompt constraint obedience rather than intrinsic financial reasoning. | Frame conclusions around prompt-guardrail compliance rather than autonomous evidential capability. |
| **RQ-02** | **IMPORTANT** | Construct Validity | Benchmark tests reading comprehension on curated 100-word snippets that already disclose missing facts. | Maintain clear documentation that Parallax does not evaluate filing discovery or autonomous extraction. |
| **GT-03** | **IMPORTANT** | Ground Truth | Meta target `M3` is a distractor warning about an adjacent paragraph rather than an affirmative contract term. | Move `M3` from core factual targets to evaluation guidance. |
| **FAIR-02** | **IMPORTANT** | Fairness | `short_quote` is blank (`""`) in Apple and Microsoft, creating structural evidence asymmetry against historical cases. | Populate `short_quote` in Apple and Microsoft with verbatim primary disclosure text. |
| **EVAL-01** | **IMPORTANT** | Evaluation | Disagreements between raters withhold entire cases without an adjudication tie-breaker, risking 20%+ data loss. | Add a designated senior adjudicator to make binding determinations on contested claims. |
| **EVAL-02** | **IMPORTANT** | Evaluation | Prompt-induced structural headings compromise rater blinding. | Train raters to disregard formatting and headings when scoring claims. |
| **REP-02** | **IMPORTANT** | Reproducibility | $N=3$ repetitions per cell provide descriptive qualitative comparisons only; no statistical power. | Adhere strictly to protocol disclaimers forbidding p-values and population claims. |
| **RQ-03** | **OPTIONAL** | Construct Validity | Uncontrolled training set exposure on prominent megacap tech issuers. | Test private credit or obscure middle-market disclosures in future versions. |
| **REP-03** | **OPTIONAL** | Software | `prepare.py` only prints the plan; no execution runner script exists for the 30-slot design. | Write and test an execution runner when live calls are authorized. |

---

## Final Recommendation & Conditions for Pilot Execution

### Final Determination: **REVISE BEFORE EXECUTION**

The proposed validation experiment represents a significant methodological advance over previous iterations: it establishes a deterministic 30-slot preparation plan, locks offline test execution, introduces two valuable new accounting cases (Apple purchase commitments and Microsoft operating leases), properly scopes synthetic arithmetic baselines outside disclosure interpretation, and implements pre-blinded rating templates.

However, executing live model calls against the protocol in its current form would violate the protocol's own gating rules and risk severe validity failures due to the four identified blockers.

### Mandatory Pre-Execution Conditions
Before model execution is authorized, the following revisions must be made and committed:

1. **Ratify Ground Truth (GT-01):** An independent human financial reviewer must inspect the primary SEC filings, approve or dispute the factual assertions and accounting classifications in `protocols/scientific-validation-v1/references.json`, update `"status"` from `"provisional"` to `"verified"`, and re-freeze the plan.
2. **Resolve the Recognition Scoring Paradox (GT-02 / EVAL-01):** Update `references.json` and the Dimension 2 rubric to explicitly specify how unestablished/off-balance-sheet liabilities (Apple, Meta, NVIDIA) should be scored, ensuring that stating the footnote reflects an unrecorded commitment is credited rather than penalized.
3. **Align Evidence Grounding Rubric (FAIR-01):** Amend the Dimension 3 scoring guidelines so that neutral responses using standard prose citations (e.g. *"Form 10-K, Note 13"*) are scored on an equal footing with guided responses using schema IDs (`MSFT_10K`).
4. **Preflight Provider Parameters (REP-01):** Verify the Meta Model API documentation or conduct an authorized preflight parameter check to ensure that `model: "muse-spark-1.3"`, `temperature: 0.7`, and `max_completion_tokens: 8192` are valid request parameters before initiating the 30 non-retryable slots.
5. **Populate Fixture Quotations (FAIR-02):** Fill the empty `short_quote` fields in `apple.json` and `microsoft.json` with verbatim primary disclosure excerpts to maintain cross-case consistency.

Upon satisfaction of these five conditions, the Parallax Scientific Validation Pilot v1 will be fully sound for authorized live execution as an exploratory qualitative evaluation.