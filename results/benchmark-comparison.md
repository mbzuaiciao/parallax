# Recorded reviewer assessments

Recorded verdicts are not automated accuracy scores. Consult reviewer/type metadata: assistant drafts are not independent human ratings. Identifier recognition checks catalog membership only; they do not verify the cited passage or whether it supports a claim.

## meta-capacity

Reviewer: Parallax assistant; source-based semantic review draft, not an independent human rating; type: assistant_draft; date: 2026-10-27.

Two successful calls. Disclosed parties, cap, tenor and reduction mechanism are preserved; the provider remains unnamed. Equity reasoning is too one-sided and overstates the exclusion of economic support; no aggregate accuracy score. All semantic verdicts are assistant drafts awaiting independent human review.

### Deterministic provenance/protocol checks

- Assessment binds recorded run bytes: True
- Assessment binds current reference bytes: True
- two_expected_perspectives: true
- requests_match_case_and_builder: true
- only_investor_phrase_differs: true
- source_versions_match_current_files: true
- statuses: {"equity_holder": "completed", "senior_unsecured_creditor": "completed"}
- response_text_present: {"equity_holder": true, "senior_unsecured_creditor": true}

### Explicitly unscorable fields

- expected_loss_or_probability: **unscorable** — No event probabilities, pricing model or joint-state estimates supplied.
- creditor_recovery_or_relative_priority: **unscorable** — Selected disclosures lack complete capital structure, asset coverage and intercreditor terms.
- equity_valuation_adjustment: **unscorable** — No valuation model, discount rates or security prices supplied.
- future_cash_payment_schedule: **unscorable** — No complete schedule or contract formula sufficient to derive exact future cash payments.

### Recorded review (semantic judgments require human validation)

#### equity_holder

- objective/obligors_beneficiaries: **supported** — Meta as purchaser and unnamed cloud provider as supplier/beneficiary. Neither imports Wagner's cross-filing Nebius identity. Exact obligor legal-entity scope remains undisclosed.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CAPACITY: recognized identifier = True; semantic support requires human review.
- objective/obligation_classification: **concern** — Correct contingent own purchase, but the direct-versus-contingent framing equates direct with currently due/non-cancelable. A contingent purchase can still be Meta's own contractual obligation. A legal debt guarantee is not established.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CAPACITY: recognized identifier = True; semantic support requires human review.
- objective/limits_triggers: **supported** — Correct reduction for provider third-party sales; no invented annual trigger, unilateral cancellation, exact five-year start date or payment schedule. Mere recognition as contingent does not make an obligation optional.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CAPACITY: recognized identifier = True; semantic support requires human review.
- objective/disclosed_amounts: **supported** — 14.72 billion over five years retained as an up-to obligation. 349.31 billion and 53.52/81.65 billion are correctly kept as neighboring aggregate context, not the case payment schedule. No unsupported annual allocation.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CONTEXT: recognized identifier = True; semantic support requires human review.
- objective/citations: **supported** — Cites the existing META_10Q identifier and actual Note 9 topic; equity also reproduces the supplied paragraph opening. These are manual source checks, not consequences of catalog membership.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CAPACITY: recognized identifier = True; semantic support requires human review.
- judgment/investor_implications: **concern** — Conditional cash/funding effects are sensible, but the equity discussion underplays the capacity/service consideration received. It offers a mostly cash-outflow thesis rather than a balanced cost-versus-use/value assessment; valuation is appropriately unquantified.
- judgment/missing_information: **supported** — Explicitly identifies absent delivery, pricing, timing, reduction calculation, identity, termination and priority information. Justifiably refuses probability-weighted exposure and recovery calculations; would also need issuer financial capacity.
- judgment/unsupported_assumptions: **concern** — Equity says analysis should not treat this as third-party credit support. Absence of a legal debt guarantee does not rule out economic demand support for a supplier. Its assertion that resale is a pre-payment reduction rather than recovery is a plausible interpretation, not an expressly disclosed settlement sequence.
#### senior_unsecured_creditor

- objective/obligors_beneficiaries: **supported** — Meta as purchaser and unnamed cloud provider as supplier/beneficiary. Neither imports Wagner's cross-filing Nebius identity. Exact obligor legal-entity scope remains undisclosed.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CAPACITY: recognized identifier = True; semantic support requires human review.
- objective/obligation_classification: **supported** — Correctly separates the contingent purchase from the neighboring non-cancelable aggregate and from a guarantee of another borrower. Direct-context terminology is not evidence of unilateral cancellation.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CAPACITY: recognized identifier = True; semantic support requires human review.
- objective/limits_triggers: **supported** — Correct reduction for provider third-party sales; no invented annual trigger, unilateral cancellation, exact five-year start date or payment schedule. Mere recognition as contingent does not make an obligation optional.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CAPACITY: recognized identifier = True; semantic support requires human review.
- objective/disclosed_amounts: **supported** — 14.72 billion over five years retained as an up-to obligation. 349.31 billion and 53.52/81.65 billion are correctly kept as neighboring aggregate context, not the case payment schedule. No unsupported annual allocation.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CONTEXT: recognized identifier = True; semantic support requires human review.
- objective/citations: **supported** — Cites the existing META_10Q identifier and actual Note 9 topic; equity also reproduces the supplied paragraph opening. These are manual source checks, not consequences of catalog membership.
  - Reviewer-entered citation META_10Q/Q_NOTE9_CAPACITY: recognized identifier = True; semantic support requires human review.
- judgment/investor_implications: **supported** — Conditional competition for operating cash flows and funding needs is justified. No relative ranking or numerical recovery is assumed; service/capacity received could matter economically but its value is not supplied.
- judgment/missing_information: **supported** — Explicitly identifies absent delivery, pricing, timing, reduction calculation, identity, termination and priority information. Justifiably refuses probability-weighted exposure and recovery calculations; would also need issuer financial capacity.
- judgment/unsupported_assumptions: **supported** — No material unsupported factual or ranking inference identified. Keeps resale mitigation and funding implications conditional; preserves provider anonymity. This is not proof that no error exists.

Pair consistency (recorded judgment): **supported** — Core disclosed facts and uncertainty remain stable across investor prompts. Different emphases do not justify different numerical exposures. Equity-specific economic omissions/overstatements are recorded separately, not a mechanical failure of evidence equality.

## coreweave-deposit

Reviewer: Parallax assistant; source-based semantic review draft, not an independent human rating; type: assistant_draft; date: 2026-10-27.

Two successful calls. The model distinguishes dated debt carrying values from the original deposit and future termination payments. The equity answer makes an unsupported termination-versus-hold cash-cost comparison; creditor settlement reasoning needs a countervailing cash-outflow qualification. Semantic records are assistant drafts, not human-adjudicated scores.

### Deterministic provenance/protocol checks

- Assessment binds recorded run bytes: True
- Assessment binds current reference bytes: True
- two_expected_perspectives: true
- requests_match_case_and_builder: true
- only_investor_phrase_differs: true
- source_versions_match_current_files: true
- statuses: {"equity_holder": "completed", "senior_unsecured_creditor": "completed"}
- response_text_present: {"equity_holder": true, "senior_unsecured_creditor": true}

### Explicitly unscorable fields

- expected_loss_or_probability: **unscorable** — No event probabilities, pricing model or joint-state estimates supplied.
- creditor_recovery_or_relative_priority: **unscorable** — Selected disclosures lack complete capital structure, asset coverage and intercreditor terms.
- equity_valuation_adjustment: **unscorable** — No valuation model, discount rates or security prices supplied.
- future_cash_payment_schedule: **unscorable** — No complete schedule or contract formula sufficient to derive exact future cash payments.

### Recorded review (semantic judgments require human validation)

#### equity_holder

- objective/obligors_beneficiaries: **supported** — CoreWeave is service/refund obligor; MagAI Ventures is depositor/refund beneficiary and approval party. Both treat Magnetar Loan as the disclosed label rather than infer an unstated corporate identity.
  - Reviewer-entered citation CRWV_10K/K_NOTE10_MAGAI: recognized identifier = True; semantic support requires human review.
- objective/obligation_classification: **concern** — Correct in-substance debt and conditional service/refund mechanics, but both list accounting/accretion as direct contractual obligations. Recording/carrying a liability and a historical payment are not separate contractual promises or new cash debts.
  - Reviewer-entered citation CRWV_10K/K_NOTE10_MAGAI: recognized identifier = True; semantic support requires human review.
- objective/limits_triggers: **supported** — Correct unused-deposit refund, bilateral termination rights, return multiplier, four-year term/two-year option, and January 2029 table maturity. Does not invent a reconciliation, default trigger or equal ranking.
  - Reviewer-entered citation CRWV_10Q/Q_NOTE10_TABLE: recognized identifier = True; semantic support requires human review.
- objective/disclosed_amounts: **supported** — 230 million initial deposit, December 2025 carrying 273 including 43 premium, June partial settlement 100, June 30 carrying 189 and 12 percent reproduced with dates/meanings. No fabricated 273-minus-100 reconciliation or forward payoff amount.
  - Reviewer-entered citation CRWV_10Q/Q_NOTE10_MAGAI: recognized identifier = True; semantic support requires human review.
- objective/citations: **supported** — Both use the two valid document IDs and correct Note 10 Magnetar subsection/debt-table locators. Exact table row and dated balances were manually checked; identifier recognition alone would not establish this.
  - Reviewer-entered citation CRWV_10Q/Q_NOTE10_TABLE: recognized identifier = True; semantic support requires human review.
- judgment/investor_implications: **concern** — Service consumption, interest expense and liquidity allocation are relevant to equity. However, claiming termination increases cash outflow versus holding to term is unsupported without premium/timing/extension terms; earlier settlement might reduce future accrual.
- judgment/missing_information: **supported** — Identifies full amended terms, calculation bases, notice periods, current-classification/maturity ambiguity, service uptake, priority and issuer liquidity/capital structure. Appropriate refusal of expected payout or recovery estimate.
- judgment/unsupported_assumptions: **concern** — The termination-versus-hold comparison has no disclosed counterfactual cash schedule. The stated absence of service revenue in June is carefully phrased as no disclosed revenue; the input only confirms no services at December 2025, so actual H1 usage remains unknown.
#### senior_unsecured_creditor

- objective/obligors_beneficiaries: **supported** — CoreWeave is service/refund obligor; MagAI Ventures is depositor/refund beneficiary and approval party. Both treat Magnetar Loan as the disclosed label rather than infer an unstated corporate identity.
  - Reviewer-entered citation CRWV_10K/K_NOTE10_MAGAI: recognized identifier = True; semantic support requires human review.
- objective/obligation_classification: **concern** — Correct in-substance debt and conditional service/refund mechanics, but both list accounting/accretion as direct contractual obligations. Recording/carrying a liability and a historical payment are not separate contractual promises or new cash debts.
  - Reviewer-entered citation CRWV_10K/K_NOTE10_MAGAI: recognized identifier = True; semantic support requires human review.
- objective/limits_triggers: **supported** — Correct unused-deposit refund, bilateral termination rights, return multiplier, four-year term/two-year option, and January 2029 table maturity. Does not invent a reconciliation, default trigger or equal ranking.
  - Reviewer-entered citation CRWV_10Q/Q_NOTE10_TABLE: recognized identifier = True; semantic support requires human review.
- objective/disclosed_amounts: **supported** — 230 million initial deposit, December 2025 carrying 273 including 43 premium, June partial settlement 100, June 30 carrying 189 and 12 percent reproduced with dates/meanings. No fabricated 273-minus-100 reconciliation or forward payoff amount.
  - Reviewer-entered citation CRWV_10Q/Q_NOTE10_MAGAI: recognized identifier = True; semantic support requires human review.
- objective/citations: **supported** — Both use the two valid document IDs and correct Note 10 Magnetar subsection/debt-table locators. Exact table row and dated balances were manually checked; identifier recognition alone would not establish this.
  - Reviewer-entered citation CRWV_10Q/Q_NOTE10_TABLE: recognized identifier = True; semantic support requires human review.
- judgment/investor_implications: **concern** — Competing recourse claim and termination liquidity risk are justified. Claiming reduced carrying amounts through settlements could improve availability is hedged but incomplete: paying cash also reduces liquid assets, so creditor benefit cannot be inferred from debt reduction alone.
- judgment/missing_information: **supported** — Identifies full amended terms, calculation bases, notice periods, current-classification/maturity ambiguity, service uptake, priority and issuer liquidity/capital structure. Appropriate refusal of expected payout or recovery estimate.
- judgment/unsupported_assumptions: **concern** — The potentially-improved-availability settlement inference needs the cash-use countereffect. The response otherwise appropriately distinguishes recourse classification from pari passu/unsecured status and says premium absent termination is not specified.

Pair consistency (recorded judgment): **supported** — Both preserve party roles, dated amounts, return/term options and unknown priority. Different investor concerns are reasonable; unsupported equity cost comparison and creditor settlement caveat are separate judgment concerns, not a changed principal or exposure estimate.
