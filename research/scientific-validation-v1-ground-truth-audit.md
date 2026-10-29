# Independent Ground-Truth Verification: Parallax Scientific Validation Pilot v1

**Reviewer:** Independent Financial Research Reviewer  
**Date of Audit:** October 29, 2026  
**Repository:** `parallax`  
**Target Reference File:** `protocols/scientific-validation-v1/references.json`  
**Target Fixtures:**  
- `cases/real_world/nvidia_ports.json`
- `cases/real_world/meta_capacity.json`
- `cases/real_world/coreweave_deposit.json`
- `protocols/scientific-validation-v1/apple.json`
- `protocols/scientific-validation-v1/microsoft.json`
**Scoring Context:** `protocols/scientific-validation-v1/protocol.md`  
**Primary Regulatory Source:** U.S. Securities and Exchange Commission (SEC) EDGAR System  

---

## 1. Executive Summary & Verification Scope

This independent ground-truth verification audits the five provisional reference records in [`protocols/scientific-validation-v1/references.json`](file:///Users/xq/Documents/GitHub/parallax/protocols/scientific-validation-v1/references.json). As mandated by scientific audit standards, all facts and constraints were established directly from primary, authoritative SEC regulatory filings prior to evaluating the provisional reference records.

### Verification Summary

```
========================================================================================
AUDIT SUMMARY:
Total Cases Audited:           5
Total Core Factual Targets:    15 assertions
Primary Regulatory Filings:    8 unique filings/exhibits inspected directly via SEC EDGAR
Overall Factual Grounding:     13 / 15 Core Targets VERIFIED directly against primary text
                                2 / 15 Core Targets VERIFIED WITH QUALIFICATION (Meta M3, CoreWeave C2)
                                0 / 15 Core Targets UNSUPPORTED or CONTRADICTED
Accounting Constraint Status:   1 Severe Defect (Apple: Contradictory "zero recognition" constraint)
                                1 Structural Defect (Meta M3: Editorial distractor mislabeled as core target)
                                2 Fixture Data Omissions (Apple & Microsoft: empty short_quote fields)
========================================================================================
```

### Sign-Off Readiness Summary

| Case Key | Company | Arrangement | Core Facts Status | Accounting Status | Ready for Human Sign-Off? |
|---|---|---|---|---|---|
| `microsoft-leases` | Microsoft | Commenced Operating Leases | 3/3 VERIFIED | 1/1 VERIFIED | **YES** (after populating fixture `short_quote`) |
| `coreweave-deposit` | CoreWeave | Refundable Deposit & Debt | 4/4 VERIFIED | 1/1 VERIFIED | **YES** |
| `nvidia-ports` | NVIDIA | PORTS Residual Value Guaranties | 3/3 VERIFIED | 1/1 VERIFIED W/ QUAL | **YES WITH QUALIFICATIONS** |
| `meta-capacity` | Meta Platforms | Contingent Cloud Capacity | 2/2 VERIFIED, 1 QUAL | 1/1 VERIFIED | **YES WITH CORRECTIONS** (reclassify target M3) |
| `apple-manufacturing` | Apple | Manufacturing Purchase Obligations | 2/2 VERIFIED | 1 CONTRADICTED | **REVISE BEFORE SIGN-OFF** (correct zero-recognition constraint) |

---

## 2. Independent Factual Baseline Across the Five Cases

Before evaluating the assistant-authored reference records, the primary disclosures were independently retrieved from SEC EDGAR and analyzed under standard corporate finance and US GAAP reporting frameworks.

```
========================================================================================
PRIMARY SEC FILINGS INSPECTED:
1. Apple Inc. Form 10-K (FY ended Sept 27, 2025, filed Oct 31, 2025; CIK 0000320193; acc: 0000320193-25-000079)
2. Microsoft Corp. Form 10-K (FY ended June 30, 2025, filed July 30, 2025; CIK 0000789019; acc: 0000950170-25-100235)
3. NVIDIA Corp. Form 8-K (Event date Aug 17, 2026, filed Aug 17, 2026; CIK 0001045810; acc: 0001045810-26-000069)
4. NVIDIA Corp. Form 10-Q (Period ended July 26, 2026, filed Aug 26, 2026; CIK 0001045810; acc: 0001045810-26-000075)
5. NVIDIA Corp. Form of Guaranty Ex. 10.1 (Filed Aug 26, 2026; CIK 0001045810; acc: 0001045810-26-000075)
6. Meta Platforms, Inc. Form 10-Q (Period ended June 30, 2026, filed July 30, 2026; CIK 0001326801; acc: 0001628280-26-050705)
7. CoreWeave, Inc. Form 10-K (FY ended Dec 31, 2025, filed March 2, 2026; CIK 0001769628; acc: 0001769628-26-000104)
8. CoreWeave, Inc. Form 10-Q (Period ended June 30, 2026, filed Aug 12, 2026; CIK 0001769628; acc: 0001769628-26-000366)
========================================================================================
```

### Key Independent Findings by Obligation Type

1. **Executory Manufacturing Commitments (Apple):** Disclosed under Item 7 MD&A ("Contractual Cash Requirements"). Under US GAAP (ASC 440), executory purchase commitments for future production are unperformed contractual promises. They are **off-balance-sheet commitments** ($0 balance sheet liability) until goods are delivered and title passes, at which point accounts payable or accrued liabilities are recognized. Total manufacturing commitments were $56.2B as of September 27, 2025, with $55.4B (98.6%) payable within 12 months.
2. **Commenced Operating Leases (Microsoft):** Disclosed under Part II, Item 8, Note 1 (Policy) and Note 13 (Leases). Under ASC 842, operating leases are recognized on the balance sheet at commencement date at the present value of lease payments. As of June 30, 2025, recognized operating lease liabilities totaled $22,861M ($5,424M current, $17,437M noncurrent). Undiscounted cash payments total $25,481M ($6,111M in fiscal 2026), reconciled by $2,620M of imputed interest. In addition, uncommenced leases (primarily datacenters) total $92.7B.
3. **Refundable Deposit and In-Substance Recourse Debt (CoreWeave):** Disclosed in Note 10 of both 2025 Form 10-K and Q2 2026 Form 10-Q. Originally a $230M customer deposit from MagAI Ventures in August 2024. Following a February 2025 amendment granting termination-for-convenience rights with a 12% return multiplier, CoreWeave reclassified the deposit as on-balance-sheet **in-substance debt under ASC 470**. Carrying amount was $273M at December 31, 2025 (including $43M accrued redemption premiums) and $189M at June 30, 2026 (reflecting a $100M cash settlement payment in June 2026).
4. **Contingent Capacity Purchases (Meta):** Disclosed in Note 9 ("Commitments and Contingencies") of Q2 2026 Form 10-Q. Meta discloses contingent obligations to purchase up to $14.72B of cloud capacity over 5 years, reducible if the provider sells capacity to other customers. The cloud provider is unnamed. The arrangement is an executory, contingent commercial purchase commitment, not a loan guarantee or debt. No recognized balance sheet liability is established for this contingent purchase.
5. **Residual Value Guaranties (NVIDIA):** Disclosed in Form 8-K (Item 1.01/2.03) and Form 10-Q (Note 17). Signed on August 17, 2026, subsequent to the July 26, 2026 balance sheet date. Multi-year credit support up to a $105B cumulative cap for 4.25 GW of IT load at SB Energy's PORTS campus. Tenant is an OpenAI affiliate; OpenAI agrees to reimburse NVIDIA. NVIDIA guarantees shortfalls in guaranteed minimum lease value upon tenant default, with ready-for-service conditions starting in 2028 (fiscal 2029). As of the July 26, 2026 financial statements, it was an uncommenced subsequent commitment with no balance-sheet liability recognized.

---

## 3. Case-by-Case Verification & Assertion Audit

### Case 1: NVIDIA PORTS (`nvidia-ports`)

```
========================================================================================
CASE 1: NVIDIA PORTS Residual Value Guaranties
Company: NVIDIA Corporation
Analysis Cutoff: August 26, 2026
Primary Disclosures: Form 8-K (Aug 17, 2026); Form 10-Q (Note 17, Aug 26, 2026); Exhibit 10.1
========================================================================================
```

#### Detailed Target Audit

| Target ID | Reference Assertion in `references.json` | Status | Primary SEC Location | Exact Primary Citation / Audit Rationale |
|---|---|---|---|---|
| **N1** | *"NVIDIA guarantees defined lease-related obligations to SB Energy lessors; an OpenAI affiliate is tenant and OpenAI undertakes reimbursement."* | **VERIFIED** | Form 8-K, Item 1.01, Residual Value Guaranties | *"On August 17, 2026, NVIDIA entered into multiple residual value guaranties (collectively, the 'Agreements') with SB Energy (the 'Lessor')... An affiliate of OpenAI Group PBC... will be the tenant... OpenAI has agreed to reimburse and indemnify NVIDIA for any and all amounts actually paid by NVIDIA to the Lessor under the Agreements."* |
| **N2** | *"Initial cumulative cap is $105 billion across the initial guaranties; effectiveness/payment have lease-commencement and ready-for-service conditions."* | **VERIFIED** | Form 8-K, Item 1.01, paras 3-5; Form 10-Q, Note 17, p. 19 | *"NVIDIA’s aggregate payment obligation is cumulatively capped at $105 billion for its initial commitment under the Agreements. NVIDIA’s payment obligations are subject to specified conditions, including... ready-for-service conditions... expected beginning in 2028. An Agreement generally will become effective upon commencement of the applicable lease."* Form 10-Q Note 17 confirms $105.0B cap across nine phases. |
| **N3** | *"Default triggers require landlord termination right and intent plus contractual procedure; remedies and recoveries qualify exposure."* | **VERIFIED** | Form 8-K, Item 1.01, para 6; Form Exhibit 10.1, Sec. 2, 8, 12 | Form 8-K: *"in the event of (i) OpenAI’s insolvency... or (ii) OpenAI’s failure to make payments... NVIDIA will pay an amount generally equal to any shortfall between the guaranteed minimum value of a lease... and amounts recovered through a replacement lease or sale."* Form Ex. 10.1 Sec. 12(a)(i) requires Landlord to have right and actual intent to terminate, plus notice and cure rights. |

#### Contractual Obligations and Recognized Liabilities
- **Contractual Obligations:** Contingent payment guarantee backing tenant lease obligations, triggered only upon tenant insolvency or payment default, conditioned on ready-for-service delivery. NVIDIA holds structured remedy elections (lease assumption, reletting, sale, 1-year deferral). Exposure is mitigated by replacement lease/sale proceeds and OpenAI indemnification.
- **Recognized Accounting Liabilities:** **VERIFIED WITH QUALIFICATION**. The reference states: *"No separately measured PORTS carrying liability established by this supplied pack. Neither zero nor the cap is a verified accounting balance."*  
  *Audit Qualification:* Form 8-K Item 2.03 formally categorizes the agreements under *"Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement"*. Because the agreements were executed on August 17, 2026, after the July 26, 2026 period-end, Note 17 treats them as a subsequent event disclosure with zero carrying liability recognized on the July 26 balance sheet. The reference assertion is correct that the pack establishes no positive carrying balance, but should explicitly cite Item 2.03 and Note 17's subsequent-event status.

#### Material Uncertainties and Boundaries
- Disclosures omit executed discount rates, Covered Loss Amount formulas, scheduled termination values, pre-RFS termination payment figures (all redacted in Exhibit 10.1), OpenAI's independent creditworthiness, and landlord recovery estimates.
- **Stakeholder Distinctions:** Equity holders gain commercial exclusivity (site exclusively hosts NVIDIA compute for 20 years) against multi-decade contingent liquidity exposure. Senior unsecured creditors face potential claims competing with other recourse obligations, but timing, default probability, and recovery cannot be determined from disclosures.

---

### Case 2: Meta Cloud Capacity (`meta-capacity`)

```
========================================================================================
CASE 2: Meta Contingent Cloud Capacity Purchases
Company: Meta Platforms, Inc.
Analysis Cutoff: July 30, 2026
Primary Disclosures: Form 10-Q (Note 9, p. 23; MD&A, p. 47, July 30, 2026)
========================================================================================
```

#### Detailed Target Audit

| Target ID | Reference Assertion in `references.json` | Status | Primary SEC Location | Exact Primary Citation / Audit Rationale |
|---|---|---|---|---|
| **M1** | *"Meta is purchaser of up to $14.72 billion cloud capacity over five years; the provider is unnamed in the selected passage."* | **VERIFIED** | Form 10-Q, Note 9, p. 23; MD&A, p. 47 | *"In addition, as of June 30, 2026, we have contingent obligations to purchase up to $14.72 billion of cloud capacity over a five-year period, which may be reduced if the cloud service provider is able to sell such capacity to other customers."* Provider is unnamed in the text. |
| **M2** | *"Third-party capacity sales may reduce the contingent purchase obligation."* | **VERIFIED** | Form 10-Q, Note 9, p. 23 | *"...which may be reduced if the cloud service provider is able to sell such capacity to other customers."* |
| **M3** | *"The neighboring $349.31 billion aggregate commitments and 2026/2027 amounts are separate context, not the capacity arrangement payment schedule."* | **VERIFIED WITH QUALIFICATION** | Form 10-Q, Note 9, p. 23 | Preceding paragraph states: *"As of June 30, 2026, we had $349.31 billion of non-cancelable contractual commitments... with approximately $53.52 billion and $81.65 billion due in 2026 and 2027, respectively. In addition... we have contingent obligations..."*<br>*Audit Qualification:* While factually accurate that $349.31B covers overall contractual commitments, `M3` is an editorial distractor rather than an affirmative contract term (see Section 5). |

#### Contractual Obligations and Recognized Liabilities
- **Contractual Obligations:** Executory contingent purchase obligation of up to $14.72B over 5 years. Variable depending on provider third-party sales. It is an own-purchase commitment, not a loan guarantee or debt assumption.
- **Recognized Accounting Liabilities:** **VERIFIED**. Disclosed strictly under "Commitments and Contingencies" (ASC 440). No recognized balance sheet liability or carrying value exists for this unperformed contingent purchase.

#### Material Uncertainties and Boundaries
- Disclosures omit supplier identity, pricing unit economics, annual draw schedules, minimum take-or-pay thresholds, and cancellation provisions.
- **Stakeholder Distinctions:** Equity holders bear cash outflow risks if capacity is unutilized, offset by operational compute availability. Senior creditors face variable liquidity demands; however, asserting that this creates "de facto debt" or priority over unsecured bonds is completely unsupported by primary disclosures.

---

### Case 3: CoreWeave Refundable Deposit (`coreweave-deposit`)

```
========================================================================================
CASE 3: CoreWeave MagAI Refundable Capacity Deposit & In-Substance Debt
Company: CoreWeave, Inc.
Analysis Cutoff: August 12, 2026
Primary Disclosures: Form 10-K (Note 10, March 2, 2026); Form 10-Q (Note 10, Aug 12, 2026)
========================================================================================
```

#### Detailed Target Audit

| Target ID | Reference Assertion in `references.json` | Status | Primary SEC Location | Exact Primary Citation / Audit Rationale |
|---|---|---|---|---|
| **C1** | *"CoreWeave received a $230 million refundable deposit from MagAI Ventures; consumption reduces the deposit and unused funds are refundable."* | **VERIFIED** | Form 10-K, Note 10, p. 119 | *"The Company received a refundable deposit of $230 million in connection with the MagAI Capacity Agreement. Any consumption of cloud services by MagAI Ventures... is deducted from this deposit amount, with the unused portion refunded back to MagAI Ventures at the end of the contractual term."* |
| **C2** | *"The February 2025 termination-right amendment led to in-substance debt classification under ASC 470; termination multiplier is equivalent to a 12% annual return."* | **VERIFIED WITH QUALIFICATION** | Form 10-K, Note 10, p. 119 | *"In February 2025, the MagAI Capacity Agreement was amended to provide certain termination for convenience rights... the Company now considers the refundable deposit received from Magnetar to be in-substance debt (the 'Magnetar Loan') under ASC 470, Sale of Future Revenue... refunded along with a specified multiplier that increases over the term of the arrangement that equates to a 12% annual rate of return."*<br>*Audit Qualification:* The note refers to the counterparty as both "MagAI Ventures" and "Magnetar". The reference is verified, but should record both names. |
| **C3** | *"December 31, 2025 debt was $273 million including $43 million premiums."* | **VERIFIED** | Form 10-K, Note 10, p. 114, 119 | Form 10-K table (p. 114): *"Magnetar Loan | January 2029 | 12% | $273 [million]"*. Text (p. 119): *"As of December 31, 2025, the Company had $273 million classified as debt, current, including $43 million of redemption premiums, on the consolidated balance sheets."* |
| **C4** | *"June 2026 settlement was $100 million; June 30 remaining carrying obligation was $189 million including unused deposit and accrued premiums."* | **VERIFIED** | Form 10-Q, Note 10, p. 16, 23 | Form 10-Q table (p. 16): *"Magnetar Loan | Jan 2029 | 12% | 189 at June 30, 2026 | 273 at December 31, 2025"*. Text (p. 23): *"In June 2026, the Company paid $100 million to MagAI Ventures in partial settlement... The remaining obligation as of June 30, 2026 was $189 million, consisting of the unused refundable deposit amount, together with accrued redemption premiums..."* |

#### Contractual Obligations and Recognized Liabilities
- **Contractual Obligations:** Commercial cloud capacity reservation agreement convertible to repayment obligation with 12% return multiplier upon termination for convenience. Initial 4-year term with 2-year extension option.
- **Recognized Accounting Liabilities:** **VERIFIED**. Recognized on balance sheet as recourse debt ($273M at Dec 31, 2025; $189M at June 30, 2026). Premium accretion recognized as interest expense. CoreWeave serves as an on-balance-sheet debt control case, not an off-balance-sheet guarantee.

#### Material Uncertainties and Boundaries
- Disclosures omit detailed collateral pledges, relative creditor ranking within recourse debt, specific service utilization schedules, and full termination notice mechanics.
- **Stakeholder Distinctions:** Equity holders bear financing cost (12% return accretion and cash drain on settlement/termination). Senior creditors face recognized competing recourse debt, but legal seniority/subordination is not established by the selected note disclosures.

---

### Case 4: Apple Manufacturing Purchases (`apple-manufacturing`)

```
========================================================================================
CASE 4: Apple Manufacturing Purchase Obligations
Company: Apple Inc.
Analysis Cutoff: October 31, 2025
Primary Disclosures: Form 10-K (Item 7 MD&A, p. 25, filed Oct 31, 2025)
========================================================================================
```

#### Detailed Target Audit

| Target ID | Reference Assertion in `references.json` | Status | Primary SEC Location | Exact Primary Citation / Audit Rationale |
|---|---|---|---|---|
| **A1** | *"Manufacturing purchase obligations are $56.2bn at September 27, 2025; $55.4bn payable within 12 months."* | **VERIFIED** | Form 10-K, Item 7, p. 25 | *"As of September 27, 2025, the Company had manufacturing purchase obligations of $56.2 billion, with $55.4 billion payable within 12 months."* |
| **A2** | *"Purchases involve outsourced manufacturing/assembly/testing and component suppliers."* | **VERIFIED** | Form 10-K, Item 7, p. 25 | *"The Company utilizes several outsourcing partners to manufacture subassemblies for the Company’s products and to perform final assembly and testing of finished products. The Company also obtains individual components for its products from a wide variety of individual suppliers."* |

#### Contractual Obligations and Recognized Liabilities
- **Contractual Obligations:** Forecasted component procurement and assembly commitments with contract manufacturers. Disclosed in Item 1A as typically covering requirements up to 150 days, with cancellation fee reserves accrued for excess orders.
- **Recognized Accounting Liabilities:** **CONTRADICTED / INDETERMINATE IN REFERENCE RECORD**.  
  *Evidence from Primary Filings:* Manufacturing purchase obligations disclosed under Item 7 MD&A are executory commitments governed by ASC 440. Under US GAAP, unperformed commitments are **off-balance-sheet commitments** ($0 balance-sheet debt liability). Delivered inventory creates Accounts Payable on the balance sheet, but the $56.2B commitment itself is not on the balance sheet.  
  *Audit Finding:* In `references.json:294-296`, the reference states:  
  ```text
  "This passage does not separately establish recognized liabilities or overlap with accounts payable. 
  Do not equate the disclosed obligation with additional debt or assert zero recognition."
  ```  
  Prohibiting an assertion of "zero recognition" is **CONTRADICTED by US GAAP**. For unperformed purchase commitments, zero balance-sheet liability recognition is the standard accounting treatment. Penalizing a model for stating that purchase commitments are not recognized liabilities on the balance sheet is a fatal benchmark defect (see Section 5).

#### Material Uncertainties and Boundaries
- Disclosures omit supplier identities, unit costs, cancellation penalty schedules, and specific overlap with period-end accounts payable.
- **Stakeholder Distinctions:** Near-term concentration ($55.4B within 12 months) requires massive operational liquidity, directly impacting working capital and cash available for equity share repurchases ($89.3B in 2025) and creditor debt service. Countervailing operating cash inflows from hardware sales are absent from this isolated subsection.

---

### Case 5: Microsoft Operating Leases (`microsoft-leases`)

```
========================================================================================
CASE 5: Microsoft Commenced Operating Leases
Company: Microsoft Corporation
Analysis Cutoff: July 30, 2025
Primary Disclosures: Form 10-K (Note 1, p. 61; Note 13, p. 77-78, July 30, 2025)
========================================================================================
```

#### Detailed Target Audit

| Target ID | Reference Assertion in `references.json` | Status | Primary SEC Location | Exact Primary Citation / Audit Rationale |
|---|---|---|---|---|
| **L1** | *"Operating lease liability is $22,861m at June 30, 2025: $5,424m current and $17,437m noncurrent."* | **VERIFIED** | Form 10-K, Note 13, p. 77 | Balance sheet table: *"Other current liabilities: $5,424 [million]; Operating lease liabilities: $17,437 [million]; Total operating lease liabilities: $22,861 [million]."* |
| **L2** | *"Undiscounted operating payments $25,481m less $2,620m imputed interest reconcile to the liability; fiscal 2026 payments are $6,111m."* | **VERIFIED** | Form 10-K, Note 13, p. 78 | Maturity table: *"Year Ending June 30, 2026: $6,111; Total lease payments: $25,481; Less imputed interest: (2,620); Total: $22,861 [million]."* |
| **L3** | *"Recognition at commencement uses present value of lease payments."* | **VERIFIED** | Form 10-K, Note 1, p. 61 | *"Operating lease ROU assets and liabilities are recognized at commencement date based on the present value of lease payments over the lease term."* |

#### Contractual Obligations and Recognized Liabilities
- **Contractual Obligations:** Commenced lease agreements for datacenters, corporate offices, and R&D facilities. Remaining terms up to 20 years. Undiscounted contractual payments total $25,481M.
- **Recognized Accounting Liabilities:** **VERIFIED**. Fully recognized on-balance-sheet operating lease liabilities of $22,861M under ASC 842 ($5,424M current, $17,437M noncurrent), backed by $24,823M ROU assets.

#### Material Uncertainties and Boundaries
- Disclosures omit individual lessor identities, lease termination penalty formulas, and creditor recovery rankings. In addition, Note 13 discloses $92.7B of uncommenced leases that are outside the scope of commenced liabilities.
- **Stakeholder Distinctions:** Operating lease payments are senior operational requirements necessary to maintain facility access, constraining liquidity. For senior creditors, lease liabilities represent debt-like fixed obligations, but legal remedies upon default differ from funded bond debt (subject to statutory damage caps under Section 502(b)(6) of the U.S. Bankruptcy Code).

---

## 4. Assertion Classification Summary

Across the five cases, all reference targets and constraints were classified under the mandated five-tier audit rubric:

```
========================================================================================
CLASSIFICATION BREAKDOWN:
- VERIFIED:                    13 assertions (86.7%)
- VERIFIED WITH QUALIFICATION:  2 assertions (13.3%) [Meta M3, CoreWeave C2]
- UNSUPPORTED:                  0 assertions
- CONTRADICTED:                 0 core factual targets (1 accounting constraint contradicted: Apple)
- INDETERMINATE:                0 assertions
========================================================================================
```

| Case Key | Target | Reference Assertion Text | Audit Classification |
|---|---|---|---|
| `nvidia-ports` | `N1` | Defined lease guaranties; OpenAI tenant; reimbursement undertaking | **VERIFIED** |
| `nvidia-ports` | `N2` | $105B initial cumulative cap; commencement & RFS conditions | **VERIFIED** |
| `nvidia-ports` | `N3` | Default triggers require termination right/intent; remedies qualify | **VERIFIED** |
| `meta-capacity` | `M1` | Up to $14.72B over 5 years; provider unnamed in note | **VERIFIED** |
| `meta-capacity` | `M2` | Third-party capacity sales reduce purchase obligation | **VERIFIED** |
| `meta-capacity` | `M3` | $349.31B aggregate commitment is separate context | **VERIFIED WITH QUALIFICATION** |
| `coreweave-deposit` | `C1` | $230M refundable deposit; consumption reduces; unused refundable | **VERIFIED** |
| `coreweave-deposit` | `C2` | Feb 2025 amendment led to ASC 470 debt; 12% return multiplier | **VERIFIED WITH QUALIFICATION** |
| `coreweave-deposit` | `C3` | Dec 31, 2025 debt was $273M including $43M premiums | **VERIFIED** |
| `coreweave-deposit` | `C4` | June 2026 settlement $100M; June 30 remaining debt $189M | **VERIFIED** |
| `apple-manufacturing` | `A1` | Manufacturing purchase obligations $56.2B; $55.4B within 12 mos | **VERIFIED** |
| `apple-manufacturing` | `A2` | Outsourced manufacturing partners and component suppliers | **VERIFIED** |
| `microsoft-leases` | `L1` | Operating lease liability $22,861M: $5,424M current, $17,437M noncurrent | **VERIFIED** |
| `microsoft-leases` | `L2` | Undiscounted payments $25,481M less $2,620M interest; FY26 $6,111M | **VERIFIED** |
| `microsoft-leases` | `L3` | Recognition at commencement based on present value | **VERIFIED** |

---

## 5. Audit of Interpretation Constraints & Unfair Negative Targets

The audit identified three major structural flaws where reference records unfairly constrain financial interpretation or penalize correct domain reasoning:

### 1. The Contradictory Apple "Zero Recognition" Constraint
- **Target Record:** `protocols/scientific-validation-v1/references.json:294-296`
- **Reference Assertion:**
  ```text
  "recognized_accounting_liabilities": {
    "status": "not_established",
    "statement": "This passage does not separately establish recognized liabilities or overlap with accounts payable. 
                 Do not equate the disclosed obligation with additional debt or assert zero recognition."
  }
  ```
- **Auditor Evaluation:** **FATAL EVALUATION CONTRADICTION**.  
  Under US GAAP (ASC 440), executory manufacturing purchase commitments are off-balance-sheet arrangements. For goods not yet manufactured or delivered, the recognized balance-sheet liability is **$0**. An expert financial analyst or well-trained model that states:
  > *"These manufacturing purchase commitments are off-balance-sheet executory contracts with zero recognized liability on the balance sheet as of September 27, 2025"*
  would be penalized under Parallax's current constraint (*"Do not... assert zero recognition"*). At the same time, if the model treats it as debt, it is penalized for *"equating disclosed obligation with additional debt"*. The reference benchmark simultaneously demands an accounting distinction under Dimension 2 while prohibiting the correct GAAP answer.
- **Correction:** Delete the prohibition *"or assert zero recognition"*. Replace with: *"The footnote reflects an off-balance-sheet executory commitment with $0 carrying debt liability recognized on the balance sheet."*

### 2. Meta `M3`: Elevating an Editorial Distractor to a Core Target
- **Target Record:** `protocols/scientific-validation-v1/references.json:132-134` (`M3`)
- **Reference Assertion:**
  ```text
  "The neighboring $349.31 billion aggregate commitments and 2026/2027 amounts are separate context, 
  not the capacity arrangement payment schedule."
  ```
- **Auditor Evaluation:** **UNFAIR NEGATIVE TARGET**.  
  The $349.31B figure appears in an entirely separate preceding paragraph of Note 9. It is not part of the capacity agreement. The human preparer of `meta_capacity.json` chose to paste that adjacent paragraph into the prompt pack. Promoting a warning *not* to read that adjacent paragraph into one of only three "core factual targets" unfairly penalizes a model that produces a rigorous, clean analysis of the capacity agreement without discussing irrelevant neighboring disclosures.
- **Correction:** Remove `M3` from `core_factual_targets`. Retain it as evaluation rater guidance under `material_uncertainties_and_unsupported_conclusions`.

### 3. Missing `short_quote` in Apple and Microsoft Fixtures
- **Target Fixtures:** `apple.json:16`, `microsoft.json:16`
- **Auditor Evaluation:** **DATA INTEGRITY OMISSION**.  
  Both files leave `"short_quote": ""` as an empty string, whereas the three historical cases provide verbatim quotes. This creates an unnecessary data schema asymmetry.
- **Correction:** Populate `apple.json` with `"manufacturing purchase obligations of $56.2 billion, with $55.4 billion payable within 12 months"` and `microsoft.json` with `"Operating lease liabilities of $22,861 million: $5,424 million other current liabilities and $17,437 million operating lease liabilities"`.

---

## 6. Primary Source Provenance & Locator Catalog

The following authoritative catalog provides exact primary-source URLs, accessions, and locators for each verified disclosure:

```
========================================================================================
AUTHORITATIVE PRIMARY-SOURCE CATALOG:

1. Apple Inc. (CIK 0000320193)
   - Filing: Form 10-K for FY ended Sept 27, 2025 (filed Oct 31, 2025)
   - Accession: 0000320193-25-000079
   - URL: https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm
   - Locators:
     * Item 7, MD&A, Contractual Cash Requirements, Manufacturing Purchase Obligations (p. 25)
     * Item 7, MD&A, Other Purchase Obligations & Deemed Repatriation Tax (p. 25)
     * Item 1A, Risk Factors, Inventory and Component Supply Commitments (p. 8)

2. Microsoft Corporation (CIK 0000789019)
   - Filing: Form 10-K for FY ended June 30, 2025 (filed July 30, 2025)
   - Accession: 0000950170-25-100235
   - URL: https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm
   - Locators:
     * Note 1, Summary of Significant Accounting Policies, Leases (p. 61)
     * Note 13, Leases, Supplemental Balance Sheet Information Table (p. 77)
     * Note 13, Leases, Maturity Table of Lease Liabilities (p. 78)
     * Note 13, Leases, Undiscounted Uncommenced Leases Narrative (p. 78)

3. NVIDIA Corporation (CIK 0001045810)
   - Filing: Form 8-K (Event date Aug 17, 2026, filed Aug 17, 2026)
   - Accession: 0001045810-26-000069
   - URL: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm
   - Locators:
     * Item 1.01, Residual Value Guaranties (paras 1-8)
     * Item 2.03, Creation of a Direct Financial Obligation or Off-Balance Sheet Arrangement
   - Filing: Form 10-Q for Period ended July 26, 2026 (filed Aug 26, 2026)
   - Accession: 0001045810-26-000075
   - URL: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm
   - Locators:
     * Note 17, Guarantees, SB Energy Corp. guarantees & Maximum Gross Exposure Table (p. 19)
     * Part I, Item 2, MD&A, Unconditional Purchase Obligations & Commitments (p. 27-28)
   - Filing: Form of Residual Value Guaranty (Exhibit 10.1)
   - Accession: 0001045810-26-000075, Document: nvda2027q2ex101.htm
   - Locators: Recitals A-E; Sections 1, 2, 5, 8, 12, 13, 20

4. Meta Platforms, Inc. (CIK 0001326801)
   - Filing: Form 10-Q for Period ended June 30, 2026 (filed July 30, 2026)
   - Accession: 0001628280-26-050705
   - URL: https://www.sec.gov/Archives/edgar/data/1326801/000162828026050705/meta-20260630.htm
   - Locators:
     * Note 9, Commitments and Contingencies, Leases and Contractual Commitments (p. 23)
     * Part I, Item 2, MD&A, Contractual Commitments (p. 47)

5. CoreWeave, Inc. (CIK 0001769628)
   - Filing: Form 10-K for FY ended Dec 31, 2025 (filed March 2, 2026)
   - Accession: 0001769628-26-000104
   - URL: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm
   - Locators: Note 10, Debt, Total Principal Table (p. 114) & Magnetar Loan Subsection (p. 119)
   - Filing: Form 10-Q for Period ended June 30, 2026 (filed Aug 12, 2026)
   - Accession: 0001769628-26-000366
   - URL: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm
   - Locators: Note 10, Debt, Recourse Debt Table (p. 16) & Magnetar Loan Subsection (p. 23)
========================================================================================
```

---

## 7. Recommendations for Smallest Necessary Corrections

To achieve complete evidentiary grounding and eliminate evaluation paradoxes, the following minimal adjustments are recommended:

1. **Fix Apple Accounting Statement in `references.json`:**
   - *Current:* `"Do not equate the disclosed obligation with additional debt or assert zero recognition."`
   - *Correction:* `"The footnote reflects an off-balance-sheet executory commitment with $0 carrying debt liability recognized on the balance sheet. Do not equate the disclosed commitment with funded balance-sheet debt."`
2. **Reclassify Meta Target `M3` in `references.json`:**
   - Remove `"M3"` from `core_factual_targets`.
   - Reclassify `M3` under `material_uncertainties_and_unsupported_conclusions` as context rater guidance.
3. **Populate `short_quote` in Apple and Microsoft Fixtures:**
   - In `protocols/scientific-validation-v1/apple.json`, populate `short_quote` with: `"manufacturing purchase obligations of $56.2 billion, with $55.4 billion payable within 12 months"`.
   - In `protocols/scientific-validation-v1/microsoft.json`, populate `short_quote` with: `"operating lease liabilities of $22,861 million: $5,424 million current and $17,437 million noncurrent"`.
4. **Clarify NVIDIA Balance-Sheet Status in `references.json`:**
   - Add explicit citation to Form 8-K Item 2.03 and Form 10-Q Note 17 confirming that the August 17 agreement is an off-balance-sheet arrangement as of the July 26, 2026 reporting period.
5. **Update Hash Snapshot in `prepare.py`:**
   - After applying the text corrections, re-run `python protocols/scientific-validation-v1/prepare.py` to freeze the verified hashes.

---

## 8. Final Case-by-Case Sign-Off Determination

```
========================================================================================
FINAL AUDIT DETERMINATION:

1. microsoft-leases:    READY FOR SIGN-OFF (Cleanest record; 100% verified against Note 1/13).
2. coreweave-deposit:    READY FOR SIGN-OFF (Fully verified across 10-K and 10-Q recourse debt notes).
3. nvidia-ports:         READY FOR SIGN-OFF (Verified across 8-K, 10-Q Note 17, and Exhibit 10.1).
4. meta-capacity:        READY FOR SIGN-OFF WITH CORRECTION (Reclassify distractor target M3).
5. apple-manufacturing:  REVISE BEFORE SIGN-OFF (Correct contradictory "zero recognition" rule).
========================================================================================
```

### Conclusion
The empirical foundation of the five cases is authentic, authoritative, and supported by primary SEC filings. Once the contradictory Apple zero-recognition constraint is corrected and Meta target `M3` is moved to rater guidance, all five cases will be fully ready for formal independent human expert sign-off.