# Anonymized reviewer package

Conditions are anonymized. Review only this directory. Do not consult raw runs, prompts, protocol, mapping, outcome reports or historical model answers before recording assessments. Wording/style can still suggest a condition; blinding is not guaranteed.

Use review.json for the unchanged evidence and reference facts. Fill a COPY of assessment-template.json. No independent reviewer has been recruited or rated these answers. Do not use verbosity to assume quality. Fields can be missing or unscorable without being false.

## R001 · Arm Y · nvidia-ports · senior_unsecured_creditor

Completion status: completed

As of **2026-08-26**, on the supplied pack alone, a senior unsecured holder in NVIDIA should treat this as a **very large, long-dated, concentrated, wrong-way contingent commitment** - not debt today, but a potential future cash call that would compete directly for NVIDIA's unencumbered cash flow and assets.

This is selected disclosure context, not the complete filings or a complete executed contract. Dates and forecasts are those of the filings.

### 1. What NVIDIA promised

Structure: multiple **residual value guaranties** to SB Energy, including its affiliates, as Lessor for **~4.25 GW of IT load at the Portsmouth Site in Pike County, Ohio**.

* Tenant is **an affiliate of OpenAI Group PBC**. Tenant Parent separately guarantees all tenant lease obligations.
* Lessor: unnamed Delaware LLC in the form. Tenant / Tenant Parent identities are redacted in the form.

Mechanics from 8-K Item 1.01 filed 2026-08-17, Accession 0001045810-26-000069 and 10-Q Note 17 filed 2026-08-26, Accession 0001045810-26-000075:

> "NVIDIA's aggregate payment obligation is cumulatively capped at $105 billion for its initial commitment under the Agreements."

> "Our guarantees are limited to defined portions of lease and power payments"

Paraphrased terms supplied:

* **Not yet effective:** An Agreement generally becomes effective when its lease commences.
* **Payment conditions include lessor ready-for-service [RFS] requirements**, expected beginning in 2028 per 8-K summary.
* **Trigger:** tenant insolvency causing lease default OR failure to make lease payments.
* **Payment:** generally the shortfall between **guaranteed minimum lease value [GMV]** and replacement-lease or sale recoveries.
* **GMV covers data-center, power and transmission costs** - Sec.1(d) per form summary.
* **Remedies / loss mitigation:** assumption, reletting, sale, termination, or deferral up to a year with specified costs.
* **Shared cap** across related guaranties - Sec.1(d).
* **Termination of NVIDIA obligation:** lease commencement's 20th anniversary, tenant termination under lease terms, satisfactory OpenAI credit rating, and customary events.
* **Recourse:** OpenAI agrees to reimburse and indemnify amounts NVIDIA actually pays the Lessor. Form Sec.5: subrogation is postponed behind Landlord; recoupment is solely against Tenant / Tenant Parent.
* **Summary is qualified by the full agreement form** - Exhibit 10.1, nvda2027q2ex101.htm.

Phasing from 10-Q:

* Guarantee amounts **increase with completion of nine construction phases, the first expected in fiscal 2029, then decrease over each phase's twenty-year lease.**
* Guarantees **do not cover the entire site's cost or every tenant obligation.**
* In exchange, site **exclusively hosts NVIDIA AI infrastructure**, subject to limited exceptions. Form Sec.20(e): **exclusive NVIDIA reference architecture for at least twenty years.**
* NVIDIA also has a **sole-discretion option to provide phased credit support for approximately 3.8 additional GW.**
* The guarantee table includes the August signing even though report period ended July 26, 2026 - i.e. subsequent-event disclosure.

### 2. Economic significance to a senior unsecured creditor

**a) Scale and tenor create contingent leverage.**
$105bn cumulative cap for the initial 4.25 GW is by definition a tail-risk claim that, if triggered, would be material to liquidity, leverage and recovery for bondholders. It is 20-years per phase, phased over 9 phases. Exposure ramps as phases complete, then amortizes. You are underwriting ~20+ years of data-center / power residual value at one campus.

**b) It is credit enhancement for OpenAI, funded by NVIDIA.**
Economically NVIDIA is backstopping SB Energy against OpenAI-affiliate non-payment / insolvency. The 8-K trigger description and form Sec.12 detail confirm this is not a performance guarantee of construction, it is a financial shortfall guarantee: Covered Loss Amount requires RFS, and insolvency or monetary default requires Landlord's termination right and:

> "actually intends to terminate the Lease"

per Exhibit 10.1 Sec.12(a)(i)-(v) - not actual termination. Notice, cure and verification periods apply.

For a senior unsecured holder, that means:
* No collateral is described to secure you ahead of this claim. No seniority is disclosed. To the extent funded, it would compete pari passu for cash / enterprise value unless otherwise structured.
* After payment, NVIDIA's own recovery is weak: subrogation postponed behind Landlord, recoupment solely against Tenant / Tenant Parent. You rely on OpenAI chain for reimbursement.

**c) Wrong-way and concentration risk.**
Single site, single developer family (SB Energy + affiliates), single tenant family (OpenAI affiliate), ~4.25 GW, GMV including power/transmission, exclusive NVIDIA architecture.

If hyperscale AI demand, power economics, or OpenAI credit deteriorates, NVIDIA's core cash flow would likely be stressed at the same time the guarantee is called, and replacement-lease / sale recoveries - which offset NVIDIA's payment - would also be depressed. Collections do reduce Liability Cap dollar-for-dollar per Sec.8, and concurrent pursuit of tenant insurance and commercially reasonable Tenant Parent remedies is required for enforcement, but that is conditional on Guarantor keeping specified redacted payments current.

Optionality helps but does not eliminate: assumption, relet, sale, rejection or deferral up to one year gives NVIDIA time / loss-mitigation, but deferral has specified costs and relet/sale presumes a market for 4.25 GW of specialized load.

**d) Mitigants that matter to creditors:**

* Cap: $105bn cumulative for initial commitment; shared cap; limited to defined portions of lease/power payments, not whole site cost.
* Not effective until lease commencement + RFS; phased ramp, not immediate $105bn at risk.
* Shortfall basis - recoveries offset; enforcement must concurrently pursue insurance + Tenant Parent.
* 20-year amortization per phase; early termination events including satisfactory OpenAI credit rating - i.e. if OpenAI becomes strong enough, guarantee falls away.
* Commercial quid pro quo: 20-year exclusivity for NVIDIA infrastructure - supports future chip/system sales, but see uncertainties.
* Additional 3.8 GW is an option at sole discretion, not a commitment - you need to monitor exercise, not assume it.

### 3. Material uncertainties - you cannot size expected loss from this pack

1. **Redacted pricing:** Covered Loss Amount formula, discount rate and schedule values are redacted; GMV breakdown, redacted pre-RFS termination payment, Sec.2(c) treatment where some project costs do not reduce cap, Sec.8 cap qualifications, and specified deferral costs are all redacted. Cannot model timing or severity.

2. **Timing mismatch:** 8-K says RFS expected beginning in 2028; 10-Q says nine phases with first expected in fiscal 2029. Commencement, RFS definition, and ramp schedule are uncertain and drive when cap becomes live.

3. **Trigger / enforcement friction:** Requires RFS + insolvency-caused default or payment failure + notice/cure/verification + Landlord termination right + intent. Sec.8's requirement to pursue insurance / Tenant Parent remedies, and what "keeping specified redacted payments current" entails, leaves loss crystallization timing unclear.

4. **Recovery value:** Shortfall vs. relet or sale assumes price discovery for multi-GW AI campus including power/transmission. No disclosure of appraisals, relet assumptions, sale process, or who bears operating costs during relet.

5. **Counterparty chain opacity:** Tenant / Parent redacted in form; financial capacity of OpenAI affiliate, Tenant Parent guaranty, and OpenAI reimbursement/indemnity obligor not quantified. Threshold for "satisfactory OpenAI credit rating" to terminate is not supplied. Reimbursement is unsecured promise from same stressed credit that triggered payment.

6. **Power / transmission exposure:** GMV explicitly includes power and transmission costs. Power price, interconnection, regulatory risk at PORTS not disclosed.

7. **Exclusivity scope:** "exclusively hosts NVIDIA AI infrastructure, subject to limited exceptions" and 20-year exclusive reference architecture - exceptions, remedies for breach, and antitrust / customer-concentration implications unknown.

8. **Form vs. executed:** Execution date/counterparty blanks and confidentiality redactions remain; identities, schedules redacted; 8-K summary qualified by form. Final executed terms may differ.

9. **Expansion:** Terms, cap, pricing for optional ~3.8 GW undisclosed. Future exercise could materially increase contingent leverage beyond $105bn.

10. **Accounting / disclosure:** Pack references Note 17 maximum gross exposure table but does not supply table values, initial fair value, carrying amount, or whether/when accrual would be required. Creditor cannot assess P&L / balance-sheet recognition from pack alone.

**Creditor takeaway:** Treat $105bn as maximum loss-given-default before recoveries and reimbursement, phased and conditional, 20-year, single-name / single-site, with contractual mitigants but with core economics redacted and recovery fully levered to OpenAI and to residual value of AI data-center capacity. Monitor: RFS / phase completion, executed vs. form differences, unredacted GMV / discount / cap qualifications, Tenant Parent financials, OpenAI rating trigger, any exercise of the 3.8 GW option, and Note 17 exposure / fair-value updates.

## R002 · Arm Y · nvidia-ports · equity_holder

Completion status: completed

As of **2026-08-26**, based only on this selected disclosure pack, an NVIDIA equity holder should view this as a **very large, long-dated, contingent credit support** for AI-infrastructure demand, not as current debt.

### 1. What NVIDIA disclosed

NVIDIA entered multiple residual value guaranties with SB Energy, including its affiliates, as Lessor for **~4.25 GW of IT load at the Portsmouth Site in Pike County, Ohio**. An affiliate of OpenAI Group PBC is tenant.

> "NVIDIA's aggregate payment obligation is cumulatively capped at $105 billion for its initial commitment under the Agreements."
> - NVIDIA Form 8-K, Item 1.01, Aug 17, 2026 [0001045810-26-000069]

Key mechanics from the 8-K summary:

* **Effectiveness:** An Agreement generally becomes effective when its lease commences.
* **Pre-condition to payment:** lessor ready-for-service requirements, expected beginning in 2028.
* **Trigger:** tenant insolvency causing lease default or failure to make lease payments.
* **Payment:** NVIDIA pays generally the shortfall between guaranteed minimum lease value and replacement-lease or sale recoveries.
* **Post-trigger choices:** assumption, reletting, sale, termination, or deferral up to a year with specified costs.
* **End of obligation:** includes lease commencement's twentieth anniversary, tenant termination under lease terms, satisfactory OpenAI credit rating, and customary events.
* **Recourse:** OpenAI agrees to reimburse and indemnify amounts NVIDIA actually pays the Lessor.
* The summary is qualified by the full agreement form.

The 10-Q Note 17 adds phasing and scope, filed Aug 26, 2026 for period ended July 26, 2026:

* Each guarantee generally becomes effective at its lease commencement.
* Corresponding guarantee amounts **increase with completion of nine construction phases, the first expected in fiscal 2029, then decrease over each phase's twenty-year lease.**
* The guarantees **do not cover the entire site's cost or every tenant obligation.**

> "Our guarantees are limited to defined portions of lease and power payments"
> - NVIDIA Form 10-Q, Note 17, SB Energy Corp. guarantees [0001045810-26-000075]

### 2. Economic significance for equity

**a) Scale and duration of tail risk:**
$105bn cumulative cap for the initial 4.25 GW commitment is the maximum cash exposure, shared across related guaranties per Section 1(d). Duration is ~20 years per phase. With 9 phases ramping from 2028/2029, exposure could extend into the late 2040s-2050s. This creates long-dated, concentrated exposure to one site, one developer group, and one tenant group.

**b) Phased, amortizing profile, not day-one $105bn:**
Exposure ramps as phases complete, then amortizes over each 20-year lease. The 10-Q guarantee table includes the August signing even though the report period ended July 26, 2026 - i.e., investors saw the commitment before leases had commenced.

**c) Loss is shortfall net of recovery, not first-dollar full lease:**
GMV covers data-center, power and transmission costs per Form Sec 1(d). Covered Loss Amount formula, discount rate and schedule values are redacted, but structure is: guaranteed minimum value less replacement-lease or sale recoveries. Collections reduce Liability Cap dollar-for-dollar per Sec 8.

This limits loss if the campus can be relet or sold, but leaves equity exposed to residual-value risk for specialized AI data centers + power/transmission 10-20 years hence.

**d) Strategic consideration - demand lock-in:**
In exchange, the site exclusively hosts NVIDIA AI infrastructure, subject to limited exceptions.
Form Sec 20(e): exclusive NVIDIA reference architecture for at least twenty years.

For equity, the thesis is: NVIDIA is using its balance sheet to enable SB Energy to build, to secure ~4.25 GW of NVIDIA-platform demand anchored by an OpenAI affiliate. The cost is contingent downside if that tenant fails to pay.

**e) Layered but subordinated mitigants:**
* Tenant Parent separately guarantees all tenant lease obligations (recital B).
* Enforcement requires concurrent pursuit of tenant insurance and commercially reasonable Tenant Parent remedies, conditional on Guarantor keeping specified redacted payments current - Sec 8.
* OpenAI reimbursement/indemnity for amounts NVIDIA actually pays.
* Sec 5: subrogation is postponed behind Landlord; recoupment is solely against Tenant/Tenant Parent.

Equity cannot treat Parent guarantee + indemnity as eliminating risk: if trigger is insolvency/default of the OpenAI-affiliated tenant system, the indemnitor may be stressed at the same time, and NVIDIA stands behind the Landlord in priority.

**f) Embedded growth option:**
NVIDIA also has a sole-discretion option to provide phased credit support for **~3.8 additional GW**. That is optional upside for platform adoption, but if exercised would materially expand contingent exposure beyond the $105bn initial cap. Terms are not in this pack.

### 3. Material uncertainties - what you cannot model from this pack

1. **Quantification blocked by redactions:** Covered Loss Amount formula, discount rate, schedule values, redacted pre-RFS termination payment, Sec 2(c) project costs that do not reduce the cap, Sec 8 cap qualifications, and specified payments NVIDIA must keep current to enforce mitigants are all redacted. Execution date/counterparty blanks remain. This is a form, not the complete executed contract.

2. **Timing mismatch:** 8-K expects ready-for-service beginning in 2028; 10-Q says first of nine phases expected in fiscal 2029. Construction, lease commencement, and when the cap ramps cannot be reconciled here. Covered Loss Amount requires ready-for-service, but a pre-RFS termination payment is also defined - pre-delivery exposure is unclear.

3. **Trigger complexity:** Sec 12 requires notice, cure and verification periods. For insolvency or monetary default, Landlord must have termination right and:

> "actually intends to terminate the Lease"
> - Exhibit 10.1, Sec 12(a)(i)-(v)

Not actual termination. Equity cannot predict Landlord behavior, cure outcomes, or verification disputes.

4. **Recovery uncertainty:** Replacement rent and sale proceeds 10-20 years out for 4.25 GW of AI infrastructure + power assets are unknowable. Deferral up to one year comes with specified but redacted costs. Assumption/relet/sale/rejection economics are not disclosed.

5. **Counterparty credit opacity:** Landlord is an unnamed Delaware LLC; Tenant and Tenant Parent identities are redacted in the form (8-K/10-Q describe as SB Energy affiliates and OpenAI affiliate). No financials for Tenant, Tenant Parent insurance, or OpenAI indemnity capacity are in pack. "Satisfactory OpenAI credit rating" termination threshold is undefined.

6. **Partial coverage ambiguity:** Guarantees are limited to defined portions of lease and power payments and do not cover entire site cost or every tenant obligation. What is excluded, and whether excluded obligations could still impair project viability, is not disclosed. Limited exceptions to exclusivity are not disclosed.

For an equity holder: monitor lease commencements and phase completions, any exercise of the 3.8 GW option, changes in OpenAI / Tenant Parent credit, ready-for-service delays, and any unredacted schedules that allow expected-loss and cap-amortization modeling.

## R003 · Arm Y · meta-capacity · senior_unsecured_creditor

Completion status: completed

**Case: meta_capacity_2026_disclosure - Contingent cloud capacity purchase**
**Perspective: Senior unsecured creditor of Meta Platforms**
**Analysis as of disclosure: 2026-07-30**

This is analysis of historical disclosure only, not a complete contract or current status assessment.

### 1. What the arrangement is - and is not

As disclosed in Meta Platforms Form 10-Q for June 30, 2026 [Accession 0001628280-26-050705, filed 2026-07-30, period end 2026-06-30]:

> Note 9, Commitments and Contingencies, Leases and Contractual Commitments: paragraph beginning 'In addition, as of June 30, 2026'; also repeated in MD&A Contractual Obligations

Meta reports:

* **contingent obligations to purchase up to $14.72 billion of cloud capacity over five years**
* beginning with "In addition" - i.e. **separate from** the $349.31 billion of non-cancelable contractual commitments reported in the immediately preceding paragraph
* reducible by the clause:

> "which may be reduced if the cloud service provider is able to sell such capacity to other customers"

Critical for a senior unsecured holder:

* This is described as a **contingent purchase commitment**, not funded debt, not a lease liability on balance sheet, and:
* The passage **does not identify a guarantee of another borrower's debt**
* The passage **does not specify security or claim ranking, unilateral cancellation rights, detailed pricing or delivery schedule, or annual payments**

In other words: do not treat this as $14.72bn of par senior unsecured debt outstanding. Treat it as a disclosed off-balance-sheet / notes-disclosed potential future cash outflow that competes for the same enterprise cash flow that services your bonds.

### 2. Economic significance to a senior unsecured creditor

**a) Incremental liquidity / leverage risk, but modest vs. base commitments.**

The contingent $14.72bn over ~5 years (to ~2031) is incremental to $349.31bn of non-cancelable commitments across multiple categories.

$14.72 / $349.31 = ~4.2% increment to disclosed commitments. Illustrative straight-line average would be ~$2.9bn per year, but Meta **does not disclose annual payments** for this arrangement - actual timing could be lumpy and front- or back-loaded.

The context matters more than the increment: Meta already discloses $53.52 billion due in 2026 and $81.65 billion due in 2027 under non-cancelable commitments. A senior unsecured creditor must view the contingent capacity as potential additional strain on top of a very large, near-term, non-cancelable funding wall.

If the contingency is triggered, Meta must either fund from operating cash flow or raise additional debt, increasing probability of default (PD) and potentially increasing senior unsecured supply / diluting recovery.

**b) Conditionality mitigates, but does not eliminate, the risk.**

The obligation is capped at "up to" $14.72bn and "may be reduced if the cloud service provider is able to sell such capacity to other customers."

Economically this is similar to a take-or-pay / reservation with a mitigation / resale right for the provider. For you as creditor, this is better than a straight $14.72bn take-or-pay because:

* if cloud demand is strong, the provider can mitigate Meta's payment, and
* Meta presumably only draws if it needs AI / compute capacity to support growth.

It is worse than no commitment because if demand for that specific capacity is weak - precisely when Meta may also be under stress and does not need it - the provider will be unable to resell and Meta will bear the full cost.

**c) Hidden leverage.**

Because this is disclosed in Commitments and Contingencies, not as on-balance-sheet debt, traditional balance-sheet leverage ratios will understate economic leverage. In distress, executory purchase contracts for critical operating inputs often have *de facto* seniority to unsecured bonds - Meta must pay to keep operating, while bond coupons can be deferred in restructuring. The disclosure gives no ranking, but operationally this competes ahead of you for cash.

There is a potential credit positive: securing large-scale cloud capacity may support revenue / AI strategy. The disclosure does not allow assessment of return on that spend. From a creditor view, it signals continuation of a heavy investment cycle alongside the $349.31bn base.

**d) Variable-term limitation.**

Meta states for variable-term agreements, it does not estimate total obligation beyond minimum quantities and/or pricing as of the reporting date.

This means the $14.72bn should be read as a quantified maximum under current minimums, not a comprehensive forecast of all cloud spend. Actual cloud-related cash outflow over 5 years could differ.

### 3. Material uncertainties - what you cannot determine from this passage

A senior unsecured holder cannot quantify loss-given-default or covenant headroom impact because:

1. **Trigger and payment terms unknown:** What causes the contingent to become payable? Take-or-pay? Reservation fee vs. usage fee? Fixed vs. variable price? No delivery schedule or annual breakdown disclosed.

2. **Value of mitigation unknown:** Provider is unnamed in this passage. No history of its ability to resell, no formula for reduction, no floor. You cannot assume any reduction will occur.

3. **Optionality unknown:** No disclosure of unilateral cancellation, termination penalty, renewal, or cure rights. Do not assume Meta can walk away.

4. **Ranking / security unknown:** No statement of secured vs. unsecured, guarantee, or structural priority. Do not assume pari passu with your senior unsecured claim in bankruptcy; operating / trade claims and assumption / rejection of executory contracts will govern.

5. **Staleness and incompleteness:** This is a point-in-time disclosure as of June 30, 2026, filed July 30, 2026, based on a manually selected paraphrase and short quote. It is not the full contract. Status, amendments, drawdowns, or additional side agreements after that date are not in scope.

6. **Interaction with base commitments:** The $349.31bn, $53.52bn (2026) and $81.65bn (2027) figures are context only, across multiple categories. You cannot allocate how much of that base is also cloud / capex / leases, or whether the contingent capacity would substitute for or add to future capex.

**Bottom line for senior unsecured:** Add up to $14.72bn over 5 years of conditional, unranked operating cash outflow to your forward liquidity model, separate from $349.31bn non-cancelable commitments. Assume zero mitigation until proven, monitor 10-K/Q updates for actual purchases, changes in non-cancelable totals, debt issuance to fund commitments, and any naming of provider / pricing terms. Do not treat as funded debt for recovery analysis, but treat as a material potential drain on cash available for debt service with *de facto* operating priority.

## R004 · Arm X · nvidia-ports · equity_holder

Completion status: completed

**Concise Structured Analysis — As of 2026-08-26**

**Arrangement:** NVIDIA PORTS Technology Campus residual value guaranties for ~4.25 GW IT load at Portsmouth Site, Pike County, Ohio. Case: `nvidia_ports_2026_disclosure`.

> Source limitation: Historical primary-disclosure pack only - selected context, not complete filings or complete executed contract. The 8-K summary is qualified by the full agreement form. The Form of Guaranty retains execution blanks, confidentiality redactions, and redacted schedules.

### 1. Obligors and Beneficiaries — Direct vs Contingent

**Beneficiary / Lessor side:**
* SB Energy, including its affiliates, as Lessor [SEC_8K - Item 1.01, para. 'On August 17']. Landlord in the Form is an unnamed Delaware LLC [SEC_FORM - Opening/recitals A-B].
* No direct payment from NVIDIA disclosed pre-trigger. Landlord has conditions: ready-for-service requirements, notice/cure/verification, concurrent pursuit of other recoveries - see §3-4.

**Contingent obligor: NVIDIA as Guarantor**
* Identified as Guarantor in Form [SEC_FORM - Opening/recitals A-B].
* Obligation is contingent residual-value support, not a direct lease obligation. No payment due unless (a) Agreement effective and (b) Trigger Event + conditions satisfied.

**Direct lease obligors (not NVIDIA):**
* Tenant: described in 8-K/10-Q only as an affiliate of OpenAI Group PBC [SEC_8K - para. 'On August 17'; SEC_10Q - Note 17, para. 'SB Energy Corp. guarantees']. Tenant and Tenant Parent identities are redacted in the Form [SEC_FORM - Opening/recitals A-B].
* Do not infer redacted identities beyond that disclosure.
* Tenant Parent separately guarantees all tenant lease obligations per Recital B [SEC_FORM - recital B]. This is a separate contingent guarantee to Landlord, not to NVIDIA.

**Contingent reimbursement obligor to NVIDIA:**
* OpenAI agrees to reimburse and indemnify amounts NVIDIA actually pays the Lessor [SEC_8K - para. 'NVIDIA’s obligations']. Recoupment under Form is solely against Tenant/Tenant Parent, with subrogation postponed behind Landlord [SEC_FORM - Section 5].
* This is conditional on actual payment by NVIDIA; no amount disclosed as receivable.

**No current obligation:**
* NVIDIA sole-discretion option to provide phased credit support for ~3.8 additional GW [SEC_10Q - Note 17]. Disclosed fact: option, not commitment.

### 2. Effectiveness and Payment Triggers

**Effectiveness:**
* An Agreement generally becomes effective when its lease commences [SEC_8K - para. 'Pursuant to'; SEC_10Q - Note 17].
* Payment further conditions on lessor ready-for-service requirements, expected beginning in 2028 [SEC_8K - para. 'Pursuant to']. Form: Covered Loss Amount requires ready-for-service [SEC_FORM - Sections 1-2].

**Triggers:**
* Tenant insolvency causing lease default or failure to make lease payments [SEC_8K - para. 'Upon a Trigger Event'].
* Procedural qualifier: notice, cure and verification periods apply; for insolvency or monetary default Landlord must have termination right and:

> "actually intends to terminate the Lease" [SEC_FORM - Section 12(a)(i)-(v)]

* Disclosure states actual termination is not required, only right + intent. Full list of Trigger Events and cure periods not supplied in paraphrase.

**Payment mechanics disclosed:**
* NVIDIA pays generally the shortfall between guaranteed minimum lease value [GMV] and replacement-lease or sale recoveries [SEC_8K - para. 'Upon a Trigger Event'].
* GMV covers data-center, power and transmission costs [SEC_FORM - Section 1(d)].
* Formula, discount rate and schedule values are redacted [SEC_FORM - Sections 1-2]. A redacted pre-RFS termination payment is also defined [SEC_FORM - Section 2]. Cannot quantify.

### 3. Limits, Recoveries, Remedies, Termination

**Contractual limits — cap is maximum, not expected loss:**
* > "NVIDIA’s aggregate payment obligation is cumulatively capped at $105 billion for its initial commitment under the Agreements." [SEC_8K - para. 'NVIDIA’s aggregate']
* Shared cap across related guaranties [SEC_FORM - Section 1(d)].
* > "Our guarantees are limited to defined portions of lease and power payments" [SEC_10Q - Note 17]
* Guarantees do not cover entire site cost or every tenant obligation [SEC_10Q - Note 17].
* Phasing: amounts increase with completion of nine construction phases, first expected in fiscal 2029, then decrease over each phase's 20-year lease [SEC_10Q - Note 17]. Table includes August signing though 10-Q period ended July 26, 2026 [SEC_10Q - Note 17].
* Section 2(c): some project costs do not reduce cap; Section 8 cap qualifications redacted [SEC_FORM - Sections 2, 8].

**Recoveries / mitigation — conditional, not assured:**
* Replacement relet or sale proceeds netted in shortfall calculation [SEC_8K - para. 'Upon a Trigger Event'].
* Collections reduce Liability Cap dollar-for-dollar [SEC_FORM - Section 8].
* Enforcement requires concurrent pursuit of tenant insurance and commercially reasonable Tenant Parent remedies, conditional on Guarantor keeping specified redacted payments current [SEC_FORM - Section 8]. Redacted payments prevent assessment of this condition.
* No creditor ranking inferred. Only disclosed priority term: subrogation postponed behind Landlord [SEC_FORM - Section 5].

**Remedies / options on trigger:**
* Assumption, reletting, sale, termination, or deferral up to a year with specified costs [SEC_8K - para. 'NVIDIA’s obligations']; Form adds rejection as option variant [SEC_FORM - Section 12]. Specified costs redacted.

**Termination of NVIDIA obligations:**
* Lease commencement's 20th anniversary, tenant termination under lease terms, satisfactory OpenAI credit rating, and customary events [SEC_8K - para. 'NVIDIA’s obligations']. Threshold for satisfactory rating, lease termination rights, and customary events not supplied.

**Commercial exchange:**
* Site exclusively hosts NVIDIA AI infrastructure, subject to limited exceptions [SEC_10Q - Note 17]; exclusive NVIDIA reference architecture for at least 20 years [SEC_FORM - Section 20(e)]. Exceptions undisclosed.

### 4. Implications for NVIDIA Equity Investor

**Disclosed facts:**
* Long-dated, phased contingent exposure: max $105bn cumulative for initial 4.25 GW, effective only at lease commencement, RFS from 2028 expected, 9 phases from FY2029 expected, 20-year amortization per phase.
* Limited scope: defined portions only.
* Offsets depend entirely on third parties and markets: relet/sale, insurance, Tenant Parent, OpenAI reimbursement/indemnity.
* Additional 3.8 GW is optional at NVIDIA discretion, not a liability at analysis date.

**Conditional economic interpretations — not disclosed facts:**
* *If* no trigger occurs, *then* cash impact is zero, with potential benefit from exclusive infrastructure hosting / architecture lock-in. Value of exclusivity cannot be quantified from pack.
* *If* trigger occurs, *then* loss equals shortfall formula up to cap, less uncertain recoveries. Cap must not be read as payable balance or expected loss.
* Reimbursement value is conditional on OpenAI/tenant credit at time of stress — precisely when collectability is most uncertain. No provision, reserve, or fair value disclosed in pack.
* Deferral/assumption options could alter timing but require specified (redacted) costs.

### 5. Material Missing Terms Preventing Quantitative Risk Assessment

* Redacted: Covered Loss Amount formula, discount rate, GMV schedules, pre-RFS payment, Liability Cap qualifications, redacted current-payment condition, specified deferral/option costs.
* Unsupplied: full Lease, Tenant Parent guarantee terms, insurance coverage, definition of ready-for-service, notice/cure durations, customary termination events, satisfactory credit-rating threshold, relet/sale market assumptions, power/transmission cost pass-throughs, limited exceptions to exclusivity.
* Form vs executed: execution date/counterparty blanks remain; final executed Agreements may differ.
* No inputs supplied to model probability, timing, recovery rate, or present value. Definitive expected-loss or liquidity analysis is not possible on supplied evidence alone.


## R005 · Arm Y · coreweave-deposit · senior_unsecured_creditor

Completion status: completed

**CoreWeave - MagAI Refundable Capacity Deposit / "Magnetar Loan"**
**View: Senior Unsecured Creditor | Analysis as of 2026-08-12**

Based solely on the two selected primary disclosures provided - not the complete amended agreement and not a solvency model.

### 1. What it is in economic substance

Despite being documented as a capacity / prepayment agreement, this is **in-substance recourse debt**, not non-refundable deferred revenue or equity.

Supporting evidence:

* August 2024: CoreWeave received **$230 million refundable deposit** from MagAI Ventures under a capacity/prepayment agreement. Unused funds refundable at term end. Portfolio-company consumption to be negotiated individually, subject to MagAI approval, and deducted from the deposit. [CRWV_10K, Note 10 Magnetar Loan subsection, 10-K for 12/31/2025 filed 2026-03-02]
* Initial term 4 years, MagAI can extend 2 years. Available capacity may, by agreement with MagAI, serve other customers with specified profit sharing. [CRWV_10K]
* February 2025 amendment added **termination-for-convenience rights for both parties**. CoreWeave consequently classified the deposit as **in-substance debt under ASC 470, Sale of Future Revenue**. [CRWV_10K]
* On such termination, unused deposit is refunded with an **increasing multiplier equivalent to a 12% annual return**. Premium accretion is recognized as **interest expense**. [CRWV_10K]
* June 2026 10-Q debt table lists the obligation as **"Magnetar Loan" under recourse debt, January 2029 maturity, 12% effective interest rate**, $273 at 12/31/2025 and $189 at 6/30/2026, dollars in millions. [CRWV_10Q, Note 10 recourse debt table + Magnetar Loan subsection, 10-Q for 6/30/2026 filed 2026-08-12]

> URL: https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm ; https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm

For a senior unsecured creditor, the label "deposit" is irrelevant. Accounting, recourse classification, and cash economics all point to financing.

### 2. Why it matters to a senior unsecured creditor

**a) It competes directly for the recourse recovery pool.**
The June 2026 note places the Magnetar Loan **under recourse debt**. That means it is a claim against CoreWeave itself, not non-recourse to a project SPV. It therefore dilutes or competes with senior unsecured claims, rather than being structurally subordinated beneath them.

**b) It has functioned as expensive debt with no operating offset.**
At 12/31/2025 **no services had been provided**. The carrying amount was **debt, current $273 million including $43 million redemption premiums**. In other words, $230 million cash in had accreted to $273 million owed with zero consumption to reduce the refund obligation. [CRWV_10K]

Accretion at 12% runs even if GPUs are never consumed by MagAI portfolio companies. That increases leverage and interest expense with no corresponding EBITDA.

**c) It is put-like / demand-like liquidity risk.**
Termination-for-convenience plus refund of unused deposit + 12% multiplier is economically a put. MagAI can force cash out. CoreWeave also has a termination right per the February 2025 amendment, but a senior unsecured holder cannot control when MagAI exercises.

This was not theoretical: **In June 2026 CoreWeave paid $100 million to MagAI in partial settlement**, reducing the carrying amount. At 6/30/2026 the remaining obligation was **$189 million, consisting of unused refundable deposit plus accrued redemption premiums through that date**. [CRWV_10Q]

Cash already left the enterprise ahead of any senior unsecured maturity, and $189 million plus future 12% accretion remains.

**d) Classification as current at YE 2025 signals near-term refinancing pressure.**
$273 million was shown as **debt, current** at 12/31/2025. The June 2026 table shows a **January 2029 maturity**. The selected excerpts do not reconcile that shift - whether by amendment, partial paydown, waiver of demand feature, or reclassification. From a senior unsecured view, either outcome is negative: demandable within 12 months, or termed out to January 2029 at 12% adding to the 2029 maturity wall.

**e) Asset and revenue encumbrance.**
Capacity was reserved for MagAI-approved use. Use for other customers requires MagAI agreement and triggers **specified profit sharing**. [CRWV_10K] That constrains CoreWeave's ability to redeploy what is presumably scarce GPU capacity to maximize unencumbered cash flow available to all recourse creditors.

In short: $230M of upfront liquidity came at the cost of a recourse, 12%, potentially demandable $273M -> $189M after $100M cash paid, with operating flexibility ceded to MagAI.

### 3. Material uncertainties - what the selected notes do NOT establish

A senior unsecured creditor **cannot determine recovery or relative priority** from these excerpts alone. The preparation notes expressly flag this:

* **Detailed termination notice periods, collateral and relative claim ranking are not provided** in the selected 10-K subsection. [CRWV_10K factual paraphrase]
* These note disclosures **do not provide a forward payment schedule or a recovery estimate for a hypothetical senior unsecured creditor**. [CRWV_10Q factual paraphrase]

Specifically missing:

1.  **Security / seniority:** Is the Magnetar Loan secured, guaranteed, or subject to liens on GPUs, receivables, or other collateral that would prime senior unsecured notes? Is it pari, senior, or contractually subordinated?
2.  **Put mechanics:** Notice period, conditions, cure, whether MagAI's termination right is unconditional, and whether CoreWeave's own termination right can force a settlement on the same 12% terms.
3.  **Full cash to settle:** $189 million at 6/30/2026 is unused deposit + accrued premiums *through that date*. Future accretion to January 2029 or to an earlier put date is not disclosed in the excerpts. Total ultimate cash could materially exceed $189 million if not consumed.
4.  **Consumption prospect:** MagAI approval is required deal-by-deal. No disclosure here on probability, pricing, or timing of future service credits that would reduce cash refund.
5.  **Profit-share drag:** Formula and volume of capacity subject to sharing if reallocated - i.e., how much margin leaks to MagAI.
6.  **Covenants / cross-default:** Events of default, cross-acceleration to senior unsecured indentures, or vice versa.
7.  **Maturity reconciliation:** Relationship between 4-year initial term from August 2024, 2-year MagAI extension option, February 2025 amendment, June 2026 partial settlement, prior current classification, and current January 2029 table maturity.

These are selected notes, not the complete amended capacity agreement. No research annotations or issuer solvency model were included.

### 4. Creditor takeaway

Treat the $189 million June 2026 balance as **live recourse debt at 12% with embedded put risk and capacity encumbrance**, not as customer deferred revenue. It has already consumed $100 million of cash in June 2026, accretes regardless of utilization, and directly reduces cash available for senior unsecured service and recovery.

Before sizing senior unsecured exposure, demand: full amended MagAI agreement, collateral and guarantee schedule, intercreditor / subordination analysis, complete Note 10 maturity and current vs. non-current breakdown at 6/30/2026, forward accretion schedule to January 2029 and to a put scenario, and any side letters on capacity reservation and profit sharing.


## R006 · Arm X · meta-capacity · senior_unsecured_creditor

Completion status: completed

**Concise Structured Analysis — As of 2026-07-30**

**Case:** `meta_capacity_2026_disclosure` — Meta contingent purchase of cloud capacity
**Source pack only:** `META_10Q` — Meta Platforms Form 10-Q for June 30, 2026, Accession 0001628280-26-050705, filed 2026-07-30, period-end 2026-06-30
**Provision locators:** Note 9, Commitments and Contingencies, Leases and Contractual Commitments: paragraph beginning ‘In addition, as of June 30, 2026’; also repeated in MD&A Contractual Obligations

This is historical disclosure context, not a complete contract. Only the contingent cloud-capacity arrangement is in scope.

### 1. Disclosed facts

* **Existence and measurement as of reporting date:** As of June 30, 2026, Meta reports contingent obligations to purchase **up to $14.72 billion** of cloud capacity **over five years** [META_10Q, Note 9 - In addition paragraph].
* **Reduction feature:** Amount quoted as:
> "which may be reduced if the cloud service provider is able to sell such capacity to other customers" [META_10Q, Note 9 - In addition paragraph]
* **Separate context, not part of case:** Immediately preceding paragraph separately reports $349.31 billion of non-cancelable contractual commitments, with $53.52 billion and $81.65 billion due in 2026 and 2027 respectively. The contingent paragraph begins ‘In addition’ [META_10Q, Note 9 - Leases and Contractual Commitments]. Per preparation instruction, those aggregates are context only.
* **Measurement limit for variable terms:** For variable-term agreements, Meta does not estimate total obligation beyond minimum quantities and/or pricing as of the reporting date [META_10Q, Note 9 - In addition paragraph].
* **No guarantee disclosed:** Passage does not identify a guarantee of another borrower's debt [META_10Q, Note 9 - In addition paragraph].

### 2. Obligors vs. beneficiaries — direct vs. contingent

* **Contingent obligor:** Meta — reports contingent obligation to purchase capacity [META_10Q, Note 9 - In addition paragraph].
* **Contingent beneficiary:** Unnamed cloud service provider — provider is unnamed in this passage; identity must not be inferred [META_10Q, Note 9 - In addition paragraph].
* **Direct obligation under this arrangement:** **None disclosed.** The $14.72 billion is described as contingent, up to a cap, not as non-cancelable. The $349.31 billion non-cancelable total is a separate, neighboring disclosure and is not attributed to this arrangement.
* **Third-party direct / guarantee obligor:** None disclosed for this arrangement.

### 3. Payment triggers, effectiveness, limits

* **Effectiveness:** Disclosed as existing as of June 30, 2026, reported July 30, 2026 [META_10Q, filed_on / period_end]. Commencement date, delivery schedule, and conditions precedent are not disclosed.
* **Payment trigger:** Not fully specified. Disclosure establishes only a contingent purchase requirement up to a cap, subject to reduction if provider resells capacity. The contractual events that would make any portion unconditionally payable, take-or-pay mechanics, minimum-take definitions, and pricing/delivery terms are not disclosed [META_10Q, Note 9 - In addition paragraph].
* **Contractual limit (cap, not payable balance):**
  - Up to $14.72 billion over five years [META_10Q, Note 9 - In addition paragraph].
  - Further limited for variable-term agreements to minimum quantities and/or pricing as of reporting date — i.e., disclosed figure does not include variable amounts beyond minimums [META_10Q, Note 9 - In addition paragraph].
  - No annual payment schedule for this arrangement is specified.

The cap must not be read as an expected loss or amount owed.

### 4. Recoveries, remedies, termination

* **Contractual reduction / mitigation:** The sole disclosed mitigant is potential reduction if the provider sells such capacity to other customers [META_10Q, Note 9 - In addition paragraph]. This is a reduction of Meta's purchase requirement, not a creditor recovery against Meta.
* **Creditor recoveries / set-off / collateral:** Not disclosed. Passage does not specify security or claim ranking [META_10Q, Note 9 - In addition paragraph].
* **Remedies for non-performance / non-payment:** Not disclosed.
* **Termination / unilateral cancellation rights:** Not disclosed for this contingent arrangement.

### 5. Implications for a senior unsecured creditor of Meta Platforms — conditional only

No ranking, security, or priority of this arrangement relative to senior unsecured claims is disclosed. No definitive priority conclusion can be drawn.

Conditional economic interpretations, **not disclosed facts**:

* **IF** any portion becomes payable, it would represent incremental future cash outflow in addition to the separately disclosed non-cancelable commitments, potentially reducing cash available for operating needs and debt service during the five-year window.
* **IF** the full $14.72 billion cap were triggered without reduction, liquidity pressure would be larger than if partially reduced or untriggered — but timing within the five years is undisclosed, so near-term refinancing / liquidity impact cannot be quantified.
* The resale-reduction feature **could** lower realized outflow, but the amount, likelihood, and timing of third-party sales are undisclosed, so no net exposure can be estimated.
* The variable-term measurement limit means actual economic exposure could differ from the disclosed up-to amount in either direction depending on undisclosed minima vs. future variable terms — direction and magnitude unknown.

None of the above converts the $14.72 billion cap into a payable balance or expected loss.

### 6. Material missing terms preventing quantitative risk assessment

All from absence in [META_10Q, Note 9 - In addition paragraph; MD&A Contractual Obligations]:

* Annual / quarterly payment schedule and five-year start-end dates
* Detailed pricing, delivery / acceptance, and take-or-pay vs. optional-take mechanics
* Precise trigger definitions and conditions for payment vs. non-payment
* Formula / verification for resale reduction; provider resale obligation vs. option
* Minimum quantity / minimum price components underlying the $14.72B
* Unilateral cancellation, termination fee, cure periods, remedies
* Security, collateral, covenants, and claim ranking vs. senior unsecured debt
* Probability of trigger, discounting, and counterparty performance risk

Without these, definitive assessment of timing, probability-weighted cash outflow, and recovery for a senior unsecured creditor is not possible on supplied evidence alone.


## R007 · Arm Y · meta-capacity · equity_holder

Completion status: completed

As an equity holder in Meta Platforms, you are the residual claimant - you care about future Free Cash Flow to Equity after all prior cash claims are paid. This disclosure is one of those prior claims.

### 1. What is disclosed

Per Meta Platforms Form 10-Q for June 30, 2026:

**Accession 0001628280-26-050705, filed 2026-07-30, period end 2026-06-30**
**Locator: Note 9, Commitments and Contingencies, Leases and Contractual Commitments: paragraph beginning 'In addition, as of June 30, 2026'; also repeated in MD&A Contractual Obligations**

> "which may be reduced if the cloud service provider is able to sell such capacity to other customers"

Factual substance provided:

* As of June 30, 2026, contingent obligations to purchase **up to $14.72 billion of cloud capacity over five years**.
* Reducible if the provider is able to sell such capacity to other customers.
* Provider is unnamed in this passage.
* Purpose, pricing/delivery schedule, and annual payment profile are not specified in the passage.

This is **only** the contingent cloud-capacity arrangement. It is in scope. Neighboring aggregates are context only.

Critical separation language:

The immediately preceding paragraph separately reports **$349.31 billion of non-cancelable contractual commitments** across multiple categories, with **$53.52 billion and $81.65 billion due in 2026 and 2027 respectively**.

The contingent capacity paragraph begins **'In addition'**.

That is, the $14.72bn is **additive to**, not included in, the $349.31bn non-cancelable total.

Full disclosure: https://www.sec.gov/Archives/edgar/data/1326801/000162828026050705/meta-20260630.htm

This is a historical SEC disclosure excerpt, not a complete contract and not a current-status assessment.

### 2. Economic significance to equity

This is not described as debt or as a guarantee of another borrower's debt. The passage does not identify a debt guarantee. Economically, however, it functions like off-balance-sheet operating leverage:

**a) Scale of future cash claim:**
Up to $14.72bn over 5 years is material in absolute terms. Relative to the disclosed non-cancelable base, it is ~4.2% incremental ($14.72 / $349.31).

If spread evenly, that would imply ~$2.9bn/year average, but **the passage does not specify annual payments** - you cannot assume linearity for liquidity or DCF modeling.

**b) Duration and inflexibility:**
5-year tenor extends the commitment horizon beyond the near-term concentration already disclosed for the non-cancelable book ($53.52bn in 2026, $81.65bn in 2027). It locks in future demand for third-party cloud capacity, increasing fixed-like costs and reducing flexibility to cut cash outflow in a downturn.

For valuation, that means lower distributable cash flow in scenarios where the contingency is triggered, less capacity for buybacks/dividends, and higher operating risk.

**c) Partial mitigant - resale clause:**
The obligation "may be reduced if the cloud service provider is able to sell such capacity to other customers."

That is downside protection for equity vs. a pure take-or-pay: if Meta does not need the capacity, third-party resale can reduce the cash outflow. Management considered it material enough to repeat in MD&A Contractual Obligations, i.e., relevant to liquidity analysis.

**d) Strategic signal, not proof:**
Locking up to $14.72bn of third-party capacity for 5 years implies management expects sustained need for external compute/storage. The passage does not state purpose, e.g. AI training/inference, business continuity, or other, so an investor cannot infer return on this spend from this disclosure alone.

### 3. Material uncertainties - what you cannot determine from this passage

1.  **Trigger and true exposure:** Contingent vs. non-cancelable. What causes the full $14.72bn to become payable vs. a lesser amount? Maximum is stated as "up to," but minimum is not stated.

2.  **Resale mechanism:** How likely is resale? Who decides, at what price, and who bears the shortfall if resale is at a lower price or fails? No history or probability is provided.

3.  **Timing:** No annual payments for this arrangement. You cannot assess near-term liquidity pressure or discount the cash flows accurately.

4.  **Pricing:** Fixed price vs. variable price. The disclosure notes that for variable-term agreements, Meta does not estimate total obligation beyond minimum quantities and/or pricing as of the reporting date. Whether and how that policy interacts with this cap is unclear from the excerpt.

5.  **Exit rights:** No unilateral cancellation rights, termination penalties, or delivery failure remedies are specified.

6.  **Seniority:** No security or claim ranking is specified. You cannot assume it is senior secured debt or otherwise; treat as an unsecured executory purchase commitment unless proven otherwise.

7.  **Counterparty concentration:** Provider unnamed in this passage. You cannot assess counterparty risk, dependence, or related-party issues.

For an equity model: include up to $14.72bn as an additional, contingent future cash outflow over 5 years, separate from the $349.31bn non-cancelable commitment, with timing unknown and with an unquantified potential reduction for third-party resale. Do not model it as funded debt or as a third-party debt guarantee - no evidence for that is provided.

## R008 · Arm X · coreweave-deposit · equity_holder

Completion status: completed

**Analysis as of 2026-08-12 - Single Arrangement Only**

**Arrangement:** CoreWeave MagAI refundable capacity deposit, accounted for as in-substance debt.

Scope is limited to two selected note disclosures. This is not the complete amended agreement or a solvency model.

### 1. Disclosed Facts with Sources

**Formation and economics:**

* Aug 2024: CoreWeave entered capacity / prepayment agreement with MagAI Ventures and received $230 million refundable deposit [CRWV_10K, Note 10, Debt, Magnetar Loan subsection].
* Cloud services for portfolio companies to be negotiated individually, subject to MagAI approval, with consumption deducted from deposit and unused funds refundable at term end [CRWV_10K, Note 10, Debt, Magnetar Loan subsection].
* At Dec 31, 2025 no services had been provided [CRWV_10K, Note 10, Debt, Magnetar Loan subsection].
* Available capacity may, by agreement with MagAI, serve other customers with specified profit sharing [CRWV_10K, Note 10, Debt, Magnetar Loan subsection].

**Term and amendment:**

* Initial term 4 years, with MagAI able to extend 2 years [CRWV_10K, Note 10, Debt, Magnetar Loan subsection].
* Feb 2025 amendment gave both parties certain termination-for-convenience rights [CRWV_10K, Note 10, Debt, Magnetar Loan subsection].

**Accounting and carrying amounts:**

* Classified as in-substance debt under ASC 470, Sale of Future Revenue. Note heading is "Magnetar Loan" [CRWV_10K, Note 10, Debt, Magnetar Loan subsection].
* At Dec 31, 2025: debt, current was $273 million including $43 million redemption premiums. Premium accretion was interest expense [CRWV_10K, Note 10, Debt, Magnetar Loan subsection].
* June 2026: CoreWeave paid $100 million to MagAI Ventures in partial settlement under the amended capacity agreement, reducing debt carrying amount [CRWV_10Q, Note 10, Debt: Magnetar Loan subsection].
* At June 30, 2026: remaining obligation was $189 million, consisting of unused refundable deposit plus accrued redemption premiums through that date. Premium accretion recognized as interest expense [CRWV_10Q, Note 10, Debt: Magnetar Loan subsection].
* Debt table (dollars in millions): Magnetar Loan listed under recourse debt, with January 2029 maturity, 12% effective interest rate, 189 at June 30, 2026 and 273 at Dec 31, 2025 [CRWV_10Q, Note 10, Debt: recourse debt table, Magnetar Loan row].

These note disclosures do not provide a forward payment schedule or a recovery estimate for a hypothetical senior unsecured creditor [CRWV_10Q, Note 10, Debt: recourse debt table, Magnetar Loan row, and Magnetar Loan subsection].

Detailed termination notice periods, collateral and relative claim ranking are not provided in this selected subsection [CRWV_10K, Note 10, Debt, Magnetar Loan subsection].

### 2. Obligors vs Beneficiaries

**Direct:**

* Obligor: CoreWeave - to hold refundable deposit, to make capacity available subject to individual negotiation / MagAI approval, to refund unused funds at term end, and to refund with multiplier on termination, and to share profit if capacity re-used for others by agreement.
* Beneficiary: MagAI Ventures named as counterparty receiving refund / premium and approval rights.

**Contingent:**

* CoreWeave obligation to pay increasing multiplier equivalent to 12% annual return is triggered only on such termination. Unused deposit refund at term end is triggered at term end to extent not consumed.
* MagAI extension right for 2 years is an option held by MagAI, not an obligation of MagAI disclosed.
* Use of capacity for other customers and profit sharing applies only if agreed with MagAI.
* Individual service delivery obligations arise only if individually negotiated and approved - none had been provided at Dec 31, 2025.

No other guarantors, collateral providers or beneficiaries are disclosed in the selected notes.

### 3. Triggers, Effectiveness, Limits, Recoveries, Remedies, Termination

**Payment triggers - Disclosed Fact:**
* Consumption: if services are negotiated, approved and delivered, amount deducted from deposit.
* Term end: unused funds refundable.
* Termination-for-convenience by either party after Feb 2025 amendment: unused deposit refunded with increasing multiplier equivalent to 12% annual return.
* Partial settlement: $100 million paid June 2026 under amended agreement.

**Effectiveness:**
* Original agreement Aug 2024; termination rights added Feb 2025; carrying amounts measured Dec 31, 2025 and June 30, 2026; maturity shown as Jan 2029 in June 2026 table.

**Contractual limits - Disclosed Fact:**
* Initial cash in: $230 million.
* Carrying amounts: $273 million at Dec 31, 2025; $189 million at June 30, 2026 after $100 million payment.
* Effective rate shown as 12% in table; termination multiplier described as equivalent to 12% annual return.
* These are accounting carrying amounts including accrued redemption premium, not disclosed as a cap on loss or as a confirmed cash payable on immediate termination at analysis date.

**Recoveries / Remedies:**
* None disclosed in selected notes. No recovery estimate, no collateral description, no default remedies, no covenants disclosed.

**Termination:**
* Both parties have certain termination-for-convenience rights post-amendment. On termination, formula is unused deposit + increasing multiplier. Notice periods, fees beyond multiplier, and settlement timing not disclosed.

### 4. Implications for CoreWeave Equity Investor

Distinguishing fact from conditional interpretation:

**Fact:** Obligation is presented as recourse debt, current at Dec 31, 2025 ($273M), and as $189M recourse debt at June 30, 2026 with Jan 2029 maturity and 12% effective rate.

**Conditional interpretation:** *If* termination is exercised, equity would face cash outflow of unused deposit plus accrued 12%-equivalent premium, reducing cash available to equity and potentially requiring refinancing. The $100M June 2026 payment demonstrates such cash use can occur before maturity. This is not a forecast that termination will occur.

**Fact:** Premium accretion is interest expense; no service revenue from this deposit through Dec 31, 2025.

**Conditional interpretation:** *If* no services are consumed, the arrangement functions economically like interest-bearing debt rather than revenue-generating prepayment, creating expense drag without offsetting gross profit. *If* services are later negotiated and consumed, portion would reduce refundable balance.

**Fact:** Re-use of capacity for others requires MagAI agreement with specified profit sharing; extension is at MagAI option.

**Conditional interpretation:** *If* CoreWeave wants flexibility to reallocate capacity, value to equity depends on undisclosed profit-share and approval terms, which could limit upside.

No inference is made about seniority, collateral coverage, or expected loss.

### 5. Material Missing Terms - Preventing Definitive Quantitative Risk Assessment

* Termination conditions, notice periods, settlement timing, and whether $189M at June 30, 2026 equals cash due on immediate termination.
* How 12% multiplier accrues/compounds after June 30, 2026 and treatment of the June $100M partial settlement in that calculation.
* Pricing, volume, and approval standards for individual service orders and deduction mechanics.
* Profit-sharing formula for re-use.
* Extension economics, fees, and renegotiation rights.
* Collateral, guarantees, covenants, events of default, other remedies, and relative ranking vs other recourse / non-recourse debt.
* Forward payment schedule and tax / fee treatment.

Without these, carrying amount cannot be converted to a definitive future cash outflow, timing, or recovery analysis.

## R009 · Arm X · meta-capacity · equity_holder

Completion status: completed

**Concise Structured Analysis — As of 2026-07-30**

**Case:** `meta_capacity_2026_disclosure` — Meta contingent purchase of cloud capacity
**Source pack only:** `META_10Q` [Accession 0001628280-26-050705, Filed 2026-07-30, Period-end 2026-06-30]

### 1. Scope and Status

Historical SEC-disclosure analysis only. This is not a complete contract and not a current-status assessment.

Only arrangement in scope is the contingent cloud-capacity purchase. Neighboring aggregate figures are context, not a second case.

### 2. Disclosed Facts [META_10Q]

**Locator:** Note 9, Commitments and Contingencies, Leases and Contractual Commitments: paragraph beginning “In addition, as of June 30, 2026”; also repeated in MD&A Contractual Obligations.

* As of June 30, 2026, Meta reports contingent obligations to purchase **up to $14.72 billion** of cloud capacity **over five years**.
* Reduction feature, short quote: *“which may be reduced if the cloud service provider is able to sell such capacity to other customers”*.
* Paragraph begins **“In addition”** — disclosed as separate from immediately preceding paragraph reporting **$349.31 billion** of non-cancelable contractual commitments across multiple categories, with **$53.52 billion** and **$81.65 billion** due in 2026 and 2027 respectively.
* For variable-term agreements, Meta does not estimate total obligation beyond minimum quantities and/or pricing as of the reporting date.
* Provider is **unnamed in this passage**.
* Passage does **not** identify a guarantee of another borrower’s debt.

No inference of provider identity, no creditor ranking, and no conversion of cap to payable balance is permitted on this evidence.

### 3. Obligors and Beneficiaries

**Direct vs. Contingent distinction:**

* **Contingent obligor:** Meta Platforms — obligation to purchase cloud capacity up to $14.72B is described as contingent, not as non-cancelable.
* **Contingent beneficiary:** Unnamed cloud service provider — would receive purchase payments if obligation becomes payable and to extent not mitigated by sales to others.
* **Direct obligations:** The $349.31B non-cancelable commitments are direct, but are **not** this arrangement. They are cited only to show this $14.72B is additional and contingent, not included in that total per “In addition” language.

No guarantor, co-obligor, or guarantee of third-party debt is disclosed for this arrangement.

### 4. Terms — Triggers, Effectiveness, Limits, Recoveries, Remedies, Termination

**Payment triggers:** Not fully defined. Disclosed trigger is in substance the contingent purchase obligation for cloud capacity. Specific events, delivery/acceptance conditions, take-or-pay mechanics, or minimum-use thresholds are not disclosed.

**Effectiveness / tenor:** Reported as existing as of June 30, 2026, with a five-year horizon. Exact start/end dates, delivery schedule, and annual payment profile for this arrangement are not disclosed.

**Contractual limits:**
* Upper bound: up to $14.72B over five years.
* Downward adjustment only: may be reduced if provider sells such capacity to other customers. Amount or formula for reduction not disclosed.
* Measurement limit: for variable-term agreements, disclosure limited to minimum quantities and/or pricing as of reporting date. Applicability of that methodology sentence specifically to the $14.72B calculation is not clarified in the paraphrase.

**Recoveries / mitigation:**
* Only disclosed mitigation is the provider resale reduction feature above. No security, collateral, set-off, or post-payment recovery rights disclosed.

**Remedies and termination:**
* Not disclosed. No information on breach remedies, unilateral cancellation rights, termination fees, detailed pricing, security or claim ranking.

### 5. Implications for an Equity Investor in Meta Platforms

**Disclosed facts:**
* Contingent exposure cap of $14.72B over five years, separate from $349.31B non-cancelable commitments.
* Exposure is reducible, but reducible amount is undisclosed.

**Conditional economic interpretations — not disclosed facts, only if-then:**
* *If* the contingency is triggered in full and resale mitigation is zero, *then* cash outflows up to the cap over five years would reduce cash available for capex, buybacks, or other distributions versus a no-trigger scenario.
* *If* material resale to other customers occurs, *then* actual outflow could be materially below $14.72B, but magnitude cannot be quantified from disclosure.
* *If* capacity is needed for operations/AI growth, *then* payments may correspond to receipt of usable capacity rather than pure loss; disclosure does not state value-for-money or whether capacity is incremental.

The $14.72B must not be treated as a liability, expected loss, or payable balance. Timing of any impact on free cash flow and earnings cannot be determined without annual schedule.

### 6. Material Missing Terms and Uncertainties Preventing Quantitative Risk Assessment

Per `META_10Q` paraphrase, the following are not specified for this arrangement:

1. Annual payments or delivery/pricing schedule
2. Precise trigger definitions and conditions precedent
3. Probability of payment; expected vs. maximum outcome
4. Extent/likelihood of provider resale mitigation
5. Cancellation, termination, renewal, and remedy terms
6. Security, seniority, or claim ranking — no assumption permitted
7. Whether variable-term minimum-quantity methodology constrains the $14.72B figure

Without these, no definitive assessment of timing, likelihood, net cash cost, or equity value impact is possible from supplied evidence alone.


## R010 · Arm Y · coreweave-deposit · equity_holder

Completion status: completed

From the perspective of a CoreWeave common equity holder, this is **expensive, recourse financing senior to equity, not revenue**.

### 1. What it is economically

In August 2024 CoreWeave received **$230 million cash as a refundable capacity deposit** from MagAI Ventures.

Disclosed terms:

* To be applied to future cloud services for MagAI portfolio companies, to be **negotiated individually and subject to MagAI approval**, with consumption deducted from the deposit.
* Unused funds **refundable at term end**. Initial term 4 years, with **MagAI able to extend 2 years**.
* Available capacity **may, by agreement with MagAI, serve other customers with specified profit sharing**.

> Source: CRWV Form 10-K for 12/31/2025, filed 2026-03-02, Note 10, Debt, Magnetar Loan subsection. Accession 0001769628-26-000104. https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm

A February 2025 amendment gave **both parties certain termination-for-convenience rights**. After that, CoreWeave reclassified the deposit as **in-substance debt under ASC 470, Sale of Future Revenue**.

On such termination, unused deposit is refunded **with an increasing multiplier equivalent to a 12% annual return**.

That reclassification is critical for equity analysis: accounting concluded this is not deferred revenue / customer prepay. It is a financing where future revenue, if any, is pledged to settle a debt.

### 2. Why it matters to equity

**a) Senior, recourse claim - 12% cost:**

In the June 30, 2026 10-Q debt table, the item labeled **"Magnetar Loan" is listed under recourse debt, with January 2029 maturity, 12% effective interest rate**, $189 million at June 30, 2026 and $273 million at December 31, 2025.

> Source: CRWV Form 10-Q for 6/30/2026, filed 2026-08-12, Note 10, Debt table and Magnetar Loan subsection. Accession 0001769628-26-000366. https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm

Recourse matters because much of CoreWeave's asset-level debt is non-recourse. A recourse obligation is a claim against the enterprise as a whole, directly ahead of equity in a stress scenario.

**b) No operating offset so far, but interest accretes:**

At December 31, 2025 **no services had been provided**; **debt, current was $273 million including $43 million redemption premiums**. Premium accretion was **interest expense**.

In other words: $230M cash in, ~$43M non-cash interest accrued by year-end 2025, with zero deducted revenue to equity holders. Interest accretion reduces net income attributable to common.

**c) Ongoing cash drain:**

In June 2026 CoreWeave **paid $100 million to MagAI Ventures in partial settlement** under the amended agreement, reducing carrying amount.

At June 30, 2026 the **remaining obligation was $189 million, consisting of unused refundable deposit plus accrued redemption premiums** through that date. Premium accretion continued as interest expense.

Math check illustrates cost: $273M at 12/31/25 - $100M cash paid = $173M, vs. $189M reported, implying ~$16M of additional accretion in H1 2026 - consistent with 12% compounding on a large balance.

For equity, this is deleveraging at the cost of $100M of liquidity in one month.

**d) Counterparty optionality and encumbered capacity:**

* Future consumption is not committed - individually negotiated + MagAI approval required.
* CoreWeave cannot freely redeploy reserved capacity to higher-paying customers without MagAI agreement and profit-sharing.
* Both sides can terminate for convenience, and MagAI controls the 2-year extension.

Equity bears the downside of that optionality: if MagAI terminates, CoreWeave must refund cash + 12% premium; if MagAI extends / withholds approval, capacity remains encumbered.

### 3. Material uncertainties - what these selected notes do NOT establish

Based on this limited record as of analysis date 2026-08-12, an equity holder cannot determine:

1. **Liquidity timing:** Why $273M was classified as **debt, current** at 12/31/25 while the table shows **January 2029 maturity**. This suggests callability within 12 months, but **detailed termination notice periods are not provided** in this selected subsection.

2. **Security and seniority:** **Collateral and relative claim ranking are not provided** in this selected subsection. You cannot assume pari, senior, or subordinated status versus other recourse debt.

3. **Full cash schedule:** The disclosures **do not provide a forward payment schedule**. You cannot model whether the remaining $189M accretes to a larger amount to Jan 2029, is payable on demand, or will be partly settled by services.

4. **Nature of June 2026 $100M payment:** Described only as partial settlement under amended agreement. Whether it reflects negotiated de-risking, a partial termination exercise, or a prelude to full termination is not disclosed here.

5. **Operating upside:** Profit-sharing percentages, capacity amounts, pricing for portfolio-company services, and likelihood of any future consumption offset are not disclosed here.

6. **Recovery analysis:** These notes **do not provide a recovery estimate for a hypothetical senior unsecured creditor**, let alone residual value to equity.

This analysis is limited to the two manually selected primary SEC note disclosures. It is not the complete amended agreement, and not an issuer solvency model. Equity holders should monitor the full credit agreement exhibit, liquidity / going-concern footnote, statement of cash flows for premium vs. principal characterization, and any related-party disclosure for MagAI/Magnetar, plus current vs. non-current classification in future quarters.


## R011 · Arm X · coreweave-deposit · senior_unsecured_creditor

Completion status: completed

**Concise Structured Analysis — As of 2026-08-12**
**Case: `coreweave_deposit_2026_disclosure` — CoreWeave MagAI refundable capacity deposit and in-substance debt**

Scope limited to supplied pack: two selected note disclosures, not the complete amended agreement. No solvency model provided.

### 1. Disclosed Arrangement and Effectiveness

**[FACT - CRWV_10K, Note 10, Debt, Magnetar Loan subsection]:**
- August 2024: CoreWeave entered capacity/prepayment agreement with MagAI Ventures and received $230 million refundable deposit.
- Portfolio-company cloud services to be negotiated individually, subject to MagAI approval, with consumption deducted from deposit.
- Unused funds refundable at term end.
- Initial term 4 years, with MagAI able to extend 2 years.
- Available capacity may, by agreement with MagAI, serve other customers with specified profit sharing.
- February 2025 amendment gave both parties certain termination-for-convenience rights.
- CoreWeave classified the refundable deposit as in-substance debt under ASC 470, Sale of Future Revenue.
- At December 31, 2025 no services had been provided; debt, current was $273 million including $43 million redemption premiums. Premium accretion was interest expense.

**[FACT - CRWV_10Q, Note 10, Debt: recourse debt table, Magnetar Loan row, and Magnetar Loan subsection]:**
- June 2026: CoreWeave paid $100 million to MagAI Ventures in partial settlement under the amended capacity agreement, reducing debt carrying amount.
- At June 30, 2026 remaining obligation was $189 million, consisting of unused refundable deposit plus accrued redemption premiums through that date. Premium accretion recognized as interest expense.
- Debt table (dollars in millions): Magnetar Loan listed under recourse debt, January 2029 maturity, 12% effective interest rate, 189 at June 30, 2026 and 273 at December 31, 2025.

Label note: 10-K and 10-Q subsections are headed “Magnetar Loan” / short_quote “Magnetar Loan” but describe agreement with MagAI Ventures. Pack does not explain the naming relationship. No identity inference made.

### 2. Obligors and Beneficiaries — Direct vs Contingent

**Direct obligor disclosed:**
- CoreWeave — obligor for refund of unused deposit and for in-substance debt carrying amounts above. Recourse debt categorization disclosed in 10-Q table.

**Direct beneficiary disclosed:**
- MagAI Ventures — recipient of $230m deposit refund rights, 12%-equivalent multiplier on termination, $100m partial settlement, future services subject to its approval, and agreed profit sharing if capacity reallocated.

**Direct obligations [FACT]:**
- Refund unused funds at term end.
- Recognized debt carrying amounts: $273m at 2025-12-31; $189m at 2026-06-30 after $100m payment.

**Contingent obligations [FACT, terms incomplete]:**
- On termination-for-convenience: refund unused deposit with increasing multiplier equivalent to 12% annual return.
- Future service delivery/consumption deductions — contingent on individual negotiations and MagAI approval.
- Profit sharing on reallocation of available capacity to other customers — contingent on agreement with MagAI; formula not disclosed.
- 2-year extension — at MagAI option; exercise status not disclosed.

No other guarantors, collateral providers, or beneficiaries disclosed in selected subsections.

### 3. Payment Triggers, Limits, Recoveries, Remedies, Termination

**Payment triggers [FACT]:**
- Individual service approvals → consumption deducted from deposit.
- Term-end → refund of unused funds.
- Exercise of termination-for-convenience by either party (post-Feb 2025 amendment) → refund of unused deposit plus multiplier.
- Amended-agreement partial settlement → $100m paid June 2026.

**Contractual limits [FACT]:**
- Initial cash receipt $230m.
- Term: 4-year initial; MagAI 2-year extension right.
- Table maturity: January 2029; 12% effective interest rate.
- No forward payment schedule disclosed. Carrying amounts are accounting measures at period-ends, not disclosed caps on future cash payable and not expected-loss estimates.

**Recoveries [FACT + MISSING]:**
- CoreWeave recovery offsets: consumption deductions and specified profit sharing — mechanics/amounts not disclosed.
- MagAI recovery: unused deposit + 12%-equivalent premium on termination; term-end refund.
- No collateral, security, or recovery estimate for hypothetical senior unsecured creditor disclosed. 10-Q expressly provides no forward payment schedule or recovery estimate.

**Remedies:** Not provided in selected subsections. No events of default, covenants, enforcement rights, or intercreditor terms disclosed.

**Termination [FACT + MISSING]:**
- Both parties have certain termination-for-convenience rights per Feb 2025 amendment.
- Consequence: unused deposit refunded with increasing multiplier equivalent to 12% annual return.
- Detailed notice periods, conditions precedent, calculation definition of “unused” after services/partial settlement, and fees/costs not provided.

### 4. Implications for a Senior Unsecured Creditor of CoreWeave

Distinguishing fact from conditional interpretation:

**Disclosed facts relevant to creditor analysis:**
- Obligation is presented as recourse debt and as debt, current at Dec 31, 2025, then $189m at June 30, 2026 with Jan 2029 maturity in table.
- Accretion of redemption premium as interest expense increased carrying amount ($43m included at Dec 31, 2025).
- $100m cash outflow in June 2026 reduced carrying amount but consumed liquidity.

**Conditional economic interpretations — not disclosed facts, require assumptions not in pack:**
- *IF* recourse implies claim against general corporate assets, *THEN* the MagAI/Magnetar Loan could compete with other unsecured claims for the same asset pool, potentially diluting recoveries. Ranking versus senior unsecured is **not disclosed — no conclusion on priority, pari passu, or subordination assumed**.
- *IF* termination-for-convenience is exercised, *THEN* timing could accelerate versus term-end and amount would include 12%-equivalent accretion, increasing near-term cash demand versus service-consumption path. Ultimate cash payable on such trigger is **not quantified** in disclosures.
- *IF* services are consumed or capacity is reallocated with profit sharing, *THEN* refund exposure could be reduced. No services had occurred by Dec 31, 2025; post-Dec 2025 service/consumption status (other than $100m settlement) not disclosed.
- Carrying amounts ($273m / $189m) must not be treated as payable balances, caps, or expected losses.

### 5. Material Missing Terms and Uncertainties Preventing Definitive Quantitative Risk Assessment

- Complete amended capacity agreement, including termination notice periods, termination conditions, and “unused deposit” definition.
- Calculation mechanics of increasing multiplier beyond “equivalent to 12% annual return” / 12% effective rate.
- Profit-sharing formula, consumption pricing, and MagAI approval standards.
- Collateral/security, covenants, defaults, remedies.
- Relative claim ranking / intercreditor priority vs senior unsecured.
- Forward payment schedule, extension exercise, post-June 30, 2026 developments.
- Issuer liquidity, total capital structure, and asset values — no solvency model in pack.

For those reasons, no definitive quantum of risk, timing of cash outflow, or recovery for a senior unsecured creditor can be derived from supplied evidence alone.


## R012 · Arm X · nvidia-ports · senior_unsecured_creditor

Completion status: completed

**Concise Structured Analysis — As of 2026-08-26**

**Arrangement:** NVIDIA PORTS Technology Campus residual value guaranties for ~4.25 GW IT load at Portsmouth Site, Pike County, Ohio.

This pack is selected disclosure context, not complete filings or complete executed contract. The 8-K summary is qualified by the full agreement form. Dates/forecasts are filing dates only.

### 1. Parties — Obligors vs. Beneficiaries

**Direct obligors disclosed:**

* Tenant — to Lessor/Landlord for lease payments. Tenant identified in narrative disclosure as "affiliate of OpenAI Group PBC" [SEC_8K - Item 1.01: Residual Value Guaranties, para. `On August 17`]. In Form, Tenant identity is redacted — do not infer which affiliate [SEC_FORM - Opening/recitals A-B].
* Tenant Parent — separately guarantees "all tenant lease obligations" [SEC_FORM - recital B]. Identity redacted — do not infer.
* Lessor/Landlord — must satisfy ready-for-service and other lease duties before Guarantor exposure. Narrative Lessor: "SB Energy, including its affiliates" [SEC_8K - Item 1.01, para. `On August 17`]. Form Landlord: "unnamed Delaware LLC" [SEC_FORM - Opening/recitals A-B]. Do not equate redacted LLC to a specific SB entity beyond disclosed group.

**Contingent obligors:**

* NVIDIA as Guarantor [SEC_FORM - Opening/recitals A-B; SEC_10Q - Note 17, Guarantees, para. headed `SB Energy Corp. guarantees`]. Obligation is contingent, not a direct lease debt. Becomes effective generally only at lease commencement [SEC_8K - Item 1.01, para. `Pursuant to`; SEC_10Q - Note 17].
* OpenAI — agrees "to reimburse and indemnify amounts NVIDIA actually pays the Lessor" [SEC_8K - Item 1.01, para. `NVIDIA's obligations`]. This is a contingent reimbursement to NVIDIA, not a direct obligation to Lessor. Exact OpenAI obligor entity and agreement terms not in pack.

**Beneficiaries:**

* Primary: Lessor/Landlord — recipient of any Guarantor shortfall payment [SEC_8K - Item 1.01, para. `Upon a Trigger Event`; SEC_FORM - Sections 1-2].
* Secondary / commercial: NVIDIA — site "exclusively hosts NVIDIA AI infrastructure, subject to limited exceptions" [SEC_10Q - Note 17] and exclusive NVIDIA reference architecture for at least twenty years [SEC_FORM - Section 20(e)]. This is disclosed commercial benefit, not a credit recovery.

### 2. Effectiveness and Payment Triggers

**Effectiveness — disclosed fact:**

* Each Agreement "generally becomes effective when its lease commences" [SEC_8K; SEC_10Q].
* Payment requires lessor ready-for-service [RFS]; expected beginning in 2028 [SEC_8K - Item 1.01, para. `Pursuant to`; SEC_FORM - Sections 1-2].
* Nine construction phases; guarantee amounts increase with completion, first expected fiscal 2029, then decrease over each phase's twenty-year lease [SEC_10Q - Note 17]. 10-Q period ended July 26, 2026 but table includes August signing [SEC_10Q - factual context].

**Triggers — disclosed fact:**

* "tenant insolvency causing lease default or failure to make lease payments" [SEC_8K - Item 1.01, para. `Upon a Trigger Event`].
* Form adds process conditions: notice, cure and verification periods apply; for insolvency or monetary default, Landlord must have termination right and "actually intends to terminate the Lease" — not actual termination [SEC_FORM - Section 12(a)(i)-(v)].
* A redacted pre-RFS termination payment is also defined, but formula not disclosed [SEC_FORM - Sections 1-2].

**Payment measure — disclosed fact:**

* NVIDIA pays "generally the shortfall between guaranteed minimum lease value [GMV] and replacement-lease or sale recoveries" [SEC_8K - Item 1.01, para. `Upon a Trigger Event`].
* GMV covers data-center, power and transmission costs [SEC_FORM - Section 1(d)].
* Covered Loss Amount formula, discount rate and schedule values are redacted; Covered Loss Amount requires RFS [SEC_FORM - Sections 1-2; redacted schedules].
* Guarantees are "limited to defined portions of lease and power payments" and "do not cover the entire site's cost or every tenant obligation" [SEC_10Q - Note 17].

### 3. Contractual Limits

**Disclosed fact — cap is maximum, not payable balance:**

> "NVIDIA's aggregate payment obligation is cumulatively capped at $105 billion for its initial commitment under the Agreements." [SEC_8K - Item 1.01, para. `NVIDIA's aggregate`]

* Shared cap across related guaranties [SEC_FORM - Section 1(d)].
* Some project costs do not reduce cap; Section 8 cap qualifications redacted [SEC_FORM - Section 2(c); Section 8].
* Phase profile: exposure builds with phases then amortizes over 20 years per phase [SEC_10Q - Note 17].

Do not interpret $105bn as expected loss, liability accrued, or amount due.

### 4. Recoveries and Mitigants

**Disclosed facts:**

* Collections reduce Liability Cap dollar-for-dollar [SEC_FORM - Section 8].
* Landlord enforcement requires concurrent pursuit of tenant insurance and commercially reasonable Tenant Parent remedies, conditional on Guarantor keeping specified redacted payments current [SEC_FORM - Section 8]. Specified payments redacted.
* Subrogation postponed behind Landlord; recoupment solely against Tenant/Tenant Parent [SEC_FORM - Section 5].
* OpenAI reimbursement/indemnity for amounts actually paid [SEC_8K - Item 1.01].

No collateral, security, set-off, or priority of reimbursement/subrogation vs. other creditors disclosed.

### 5. Lessor Remedies on Trigger

**Disclosed facts [SEC_8K - Item 1.01; SEC_FORM - Section 12]:**

* assumption, reletting, sale, termination/rejection, or deferral up to a year with specified costs.
* Specified deferral costs redacted.

Remedies determine replacement-lease/sale recoveries that reduce shortfall, but valuation mechanics not disclosed.

### 6. Termination / Expiry and Optionality

**Disclosed termination events [SEC_8K - Item 1.01, para. `NVIDIA's obligations`]:**

* lease commencement's twentieth anniversary,
* tenant termination under lease terms,
* satisfactory OpenAI credit rating,
* customary events.

Rating threshold, lease termination rights, and customary events not disclosed.

**Optionality — not an obligation:**

* NVIDIA has "sole-discretion option to provide phased credit support for approximately 3.8 additional GW" [SEC_10Q - Note 17]. Terms, cap, pricing not disclosed. Do not add to $105bn exposure.

### 7. Implications for Senior Unsecured Creditor of NVIDIA

**Disclosed facts relevant to credit:**

* Contingent, long-dated exposure: RFS from 2028, first phase FY2029, 20-year tenor per phase implies horizon into 2040s-2050s if phases stagger; no payment due absent effectiveness + RFS + Trigger + process conditions.
* Maximum contractual quantum for initial commitment is $105bn gross before recoveries, reimbursements, and cap reductions. This is not a balance-sheet liability amount in the pack.

**Conditional economic interpretation — not disclosed fact:**

* *If* leases commence, RFS is met, and a Trigger occurs, *then* creditor would face: (a) potential large cash outflow equal to shortfall up to remaining cap, increasing claims on enterprise cash flow; (b) delayed/uncertain recoveries because subrogation is junior to Landlord, recoupment is only vs. Tenant/Tenant Parent, and OpenAI reimbursement depends on OpenAI performance; (c) timing risk from up-to-1-year deferral and relet/sale execution.
* *If* no Trigger occurs, cash impact is zero and exclusive-use benefit remains commercial only.
* Mitigants that *could* reduce loss — replacement rent/sale proceeds, insurance, Tenant Parent pursuit, OpenAI indemnity — are disclosed as concepts only; amounts, enforceability and timing are undisclosed.

No ranking conclusion: pack does not disclose priority of guaranty vs. senior unsecured notes, covenants, cross-default, funding commitments, or liquidity backstop. Do not assume pari passu, senior, subordinated, or secured treatment.

### 8. Material Missing Terms / Uncertainties Preventing Quantitative Risk Assessment

* Redacted economics: Covered Loss Amount formula, GMV schedules, discount rate, pre-RFS payment, deferral costs, keep-current payments, Section 8 cap qualifications.
* Unfiled operative documents: executed leases, Tenant Parent guarantee, tenant insurance, OpenAI reimbursement/indemnity agreement, power/transmission cost components.
* Undefined triggers/thresholds: RFS criteria, cure/verification periods, "satisfactory" OpenAI rating, tenant lease termination rights, customary termination events, Landlord termination-right standard.
* Valuation/enforcement: replacement lease/sale process, who controls relet/sale, appraisal method, collection allocation, dollar-for-dollar cap-reduction timing.
* Counterparty/credit: redacted Tenant/Tenant Parent/Landlord identities, tenant and OpenAI credit capacity, SB Energy performance risk.
* Accounting/timing: recognition, cash-settlement timing, currency, tax, treatment of phased build and 20-year amortization.
* Future option: terms for optional 3.8 GW support.

Without these, no expected loss, probability-weighted exposure, liquidity impact, or rating effect can be definitively quantified from this pack alone.
