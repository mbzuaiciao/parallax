# Scientific validation v1 — final readiness record

Prepared October 29, 2026 from the current working tree. **Ready for human financial
sign-off review; not approved for execution. API readiness preflight remains required.**
This is an assistant-prepared readiness assessment, not independent human approval.
No AGENTS.md was found in the repository or inspected ancestor directories.

## Frozen scope and revision

Five disclosure cases × neutral/guided conditions × three independent repetitions =
**30 planned responses**, each covering equity and senior unsecured creditors.
No design, prompt, generation-setting, fixture, reference-status or historical-result
changes were made for this readiness record. All five references remain provisional,
with reviewer/date null and decision pending. The existing preparation script reports
execution_authorized=false and execution_ready=false; zero responses are collected.

Git HEAD: `f2c65e3e627785a432b39108808555e1173dc0c7`. The tree contains untracked experimental
and research materials, so HEAD alone does **not** identify this review snapshot.
The SHA-256 values below bind the actual local bytes. They do not hash full SEC
filings or certify source truth. Recompute after any human-approved correction.
Python used for offline validation: `3.13.12`.

## Financial corrections and citation coverage

All five records reflect the reconciled accounting boundaries. NVIDIA/Meta carrying
amounts remain unestablished by the selected evidence; neither a contractual cap
nor disclosure placement proves a zero carrying balance. Apple accepts ordinary
executory-contract nonrecognition as a qualified accounting explanation while
reserving judgment on exact related payables/reserves. CoreWeave is recognized
in-substance debt; Microsoft is recognized operating lease liability. These remain
provisional interpretations pending expert approval, not new certifications.

Citation tracing passed for **14/14 core factual targets**, plus Meta M3 evaluator
guidance: every target has a document ID resolving to a primary SEC URL/accession
and a nonempty provision locator. All evidence documents have nonempty short quotes.
The case checklist below also maps material narrative/recognition assertions to
primary provisions. Conditional investor implications are interpretations, not
additional factual targets. Citation presence is not independent semantic approval;
the human reviewer must check that each cited passage supports the full assertion.

The [ground-truth audit](scientific-validation-v1-ground-truth-audit.md) describes
15 targets and blank Apple/Microsoft quotes, unlike the current files. The
[reconciliation](scientific-validation-v1-reconciliation.md) documents this mismatch:
M3 is already guidance, not a core target, and both quotes are populated. Audit
claims of verification and exact zero balances do not override current references.
Neither audit identifies its inspected snapshot with hashes.

## Case-by-case human financial sign-off checklist

For each row, approve or dispute **each target and the accounting/scoring boundary**;
record reviewer name, date, source locator, decision and rationale. Check both
stakeholder channels as conditional interpretations, without requiring a unique
wording, prediction, numeric loss, or unsupported creditor priority. Use the
protocol's second-reviewer/adjudication procedure for disagreements. Blank decisions
below mean pending, not approval. General GAAP interpretation, especially Apple's
executory-contract distinction, requires human review of applicable guidance;
selected disclosure prose alone is not a complete recognition analysis.

| Case / pending decision | Primary provisions and accessions | Financial checklist and remaining uncertainties |
| --- | --- | --- |
| NVIDIA — reviewer/date/decision: ___ | [8-K Item 1.01](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000069/nvda-20260817.htm), `0001045810-26-000069`; [10-Q Note 17](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm) and [Exhibit 10.1 §§2, 8, 12](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda2027q2ex101.htm), `0001045810-26-000075` | Check N1–N3: parties/reimbursement, initial shared $105bn cap, effectiveness/RFS, default and remedy conditions. Note 17 supports phasing/commercial exclusivity context. Confirm August signing versus July balance-sheet date without treating timing or Item 2.03's broad heading as a measured carrying balance. Missing: redacted formulas, executed terms, ranking, collectibility and loss inputs. |
| Meta — reviewer/date/decision: ___ | [10-Q Note 9](https://www.sec.gov/Archives/edgar/data/1326801/000162828026050705/meta-20260630.htm), contingent paragraph and preceding aggregate commitments, `0001628280-26-050705` | Check M1/M2: up to $14.72bn over five years, third-party sales offsets, unnamed provider. Confirm own capacity purchase versus another borrower's guarantee, and evidence-limited recognition status. M3 remains guidance only; omission is not a factual-coverage error. Missing: identity, pricing, annual schedule, cancellation terms and priority. |
| CoreWeave — reviewer/date/decision: ___ | [2025 10-K Note 10, Magnetar Loan](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm), `0001769628-26-000104`; [June 2026 10-Q Note 10, recourse table/subsection](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm), `0001769628-26-000366` | Check C1–C4: $230m received; amended termination/refund rights, ASC 470 and 12% return; $273m December balance including $43m premiums; $100m June settlement and $189m June balance. Confirm interest accretion and no duplicate hidden debt. Review the note's MagAI/“Magnetar Loan” terminology without assuming undisclosed corporate identity. Missing: full termination mechanics, collateral, relative priority and forward payoff. |
| Apple — reviewer/date/decision: ___ | [2025 10-K Item 7, Manufacturing Purchase Obligations](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm), `0000320193-25-000079`; Item 1A cancellation-risk paragraph is reconciliation context only | Check A1/A2 and verbatim quote: $56.2bn at September 27, 2025, $55.4bn within 12 months; manufacturing/component roles. Approve ordinary unperformed commitment accounting separately from an exact issuer liability measurement. Item 1A mentions cancellation-fee reserve accrual, not its amount attributable to this aggregate. Missing: payable overlap, reserve balances, detailed terms and ranking. Do not require model mention of Item 1A absent from its pack. |
| Microsoft — reviewer/date/decision: ___ | [2025 10-K Note 1, Leases; Note 13, operating lease balance and maturity columns](https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm), `0000950170-25-100235` | Check L1–L3 and Note 1 quote: $22,861m recognized, $5,424m current plus $17,437m noncurrent; $25,481m payments less $2,620m interest; $6,111m fiscal 2026 payments; commencement/present-value policy. Keep cash timing, carrying amount and finance lease column distinct. Missing: individual lessors, penalties, priority and recoveries. |

Source limitations are retained across all cases: curated summaries rather than
full executed contracts; no archived full-filing hashes; no issuer-wide default,
recovery or valuation model. A human may approve the uncertainty boundary without
inventing a carrying balance. Material reference disputes must be resolved or
explicitly left unscorable before a future execution freeze.

## Provider compatibility and remaining preflight

Official documentation rechecked October 29, 2026; no API request was sent.
The [model catalog](https://dev.meta.ai/docs/models) lists `muse-spark-1.3`
for Chat Completions. The [parameter guide](https://dev.meta.ai/docs/protocols/chat-completions)
documents `POST https://api.meta.ai/v1/chat/completions`, developer/user messages,
and temperature 0–2: planned **0.7** is in range. Keep the planned setting despite
Meta's recommendation of 1.0. Omitted defaults are top_p=1, stream=false, n=1,
seed=null and model-set reasoning effort; do not change omissions between arms.

The directly accessible [request schema](https://dev.meta.ai/docs/api-reference/chat-completions/schemas)
confirms integer `max_completion_tokens`, counting visible output **and reasoning**.
This updates the earlier observation that the API-reference landing page presented
an identity gate: the linked schema is readable, but supplies no model-specific
maximum establishing acceptance of **8192**. Parameter names/types are compatible
with published specifications; actual account access, token-limit acceptance,
effective reasoning default and immutable backend identity remain unverified.

**API readiness preflight is still required before execution.** Seek authenticated
official model-limit/account information first. Any billable validation needs
separate authorization; none is performed or authorized by this document. Do not
silently use an experimental slot as a probe, replace a failed slot, add conditions,
or alter the 30-response design. Preserve exact requests and returned model/status
metadata; if compatibility requires changed settings, amend and refreeze before calls.

## Offline checks and approval gate

`.venv/bin/python -m unittest discover -s tests -v`: **65 tests passed** on October
29, 2026. Existing API tests use mocks. Additional local checks confirmed citation
resolution, nonempty quotes, five provisional/pending records, and a reproducible
30-slot preparation plan with no provider responses. These validate preparation
and preservation, not semantic financial accuracy.

Human sign-off may proceed using this snapshot. Execution remains blocked until
explicit human approval of references, accounting review/dispute resolution,
refreezing of reviewed bytes, provider readiness verification and separate execution
authorization. The earlier three-case ablation runner is not the five-case runner;
no runner or new infrastructure is added here. No paid calls, commits or pushes.

## SHA-256 review snapshot

Paths below are repository-relative. `references.json` binds all five records;
individual status fields remain unchanged. Report itself is excluded to avoid a
self-referential hash. Audit/reconciliation hashes bind the context actually read.

| File | SHA-256 |
| --- | --- |
| `protocols/scientific-validation-v1/protocol.md` | `baed5b4a23fab0e4642fb3292e015f00560c16f94bc6c76e818247b253a4c347` |
| `protocols/scientific-validation-v1/references.json` | `8ca40b4aa203b589718903fb7ed0c6a973b843187053a40404388a060d1fae03` |
| `cases/real_world/nvidia_ports.json` | `6734c41c86eba5c2f1a6eba5a319dea5b71f1fca2564cd27b78431ecc15a9622` |
| `cases/real_world/meta_capacity.json` | `e9ee4feee125985b0fa42475b0eb6d04c71e452b15deee4e9baf40138ebbb860` |
| `cases/real_world/coreweave_deposit.json` | `cecb7da8605f7a54a93c4c6025c0942aebb297150233aa34740c91f94d37cdf4` |
| `protocols/scientific-validation-v1/apple.json` | `e1cd190d1c846b8838cf40b176e1d61f180af75f44be4640dc38a08081118eea` |
| `protocols/scientific-validation-v1/microsoft.json` | `3a2ca03a35786750da9732ef73f6fe53529856913db1bc2c55788dd91a36786a` |
| `protocols/scientific-validation-v1/prepare.py` | `7f6ca8178a89de4de936a705db5afdf5aba25c500b9ee6c9065a932786e40d21` |
| `tests/test_scientific_validation.py` | `40412cf670b5449f11dc6a906d14fd74a59e84f83b2e76061a7c3399a9ed4b0b` |
| `research/scientific-validation-v1-review.md` | `fce48a2246ad89c76f5941b8919f07b0ff2e509563032e86293f4b5c3ee94e3f` |
| `research/scientific-validation-v1-ground-truth-audit.md` | `e8262c20df64a9757dc4e43b1d3f80dc8c04601c4457d4e511da1832edc7ae53` |
| `research/scientific-validation-v1-reconciliation.md` | `6e6b26793bf68b4eff8dfd7f5ae917092ef11536989622815f2909e2d50ec9fe` |

SHA-256 of the reproducible preparation CLI's UTF-8 stdout (including its final
newline): `36e572fbf6650e82977b0d3292b15626fb3892ad64757d0717312ae90d5ce3e0`. Reproduce with
`.venv/bin/python protocols/scientific-validation-v1/prepare.py | shasum -a 256`.
It binds the exact 30 requests/order and per-case evidence hashes, without execution.
It is a review snapshot, not a claim that human-approved reference bytes are frozen.
