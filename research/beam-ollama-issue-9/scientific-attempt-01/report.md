# Beam reasoning-skill pilot results

On November 7, 2026, Beam completed all 12 frozen requests in order at commit `806d091`. Each case-condition pair was sent once. All responses returned HTTP 200, model `beam`, a nonempty assistant answer, token counts and a normal stop. The client spent 558.05 seconds in requests. No failures, retries or model substitutions occurred. [Preflight](preflight.json) · [Schedule](schedule.json) · [Raw request and response files](./) · [Status log](status.jsonl) · [Verification](verification.json)

Ollama 0.40.15 handled the requests on loopback and routed inference to Ollama Cloud. The identity check returned HTTP 200, the installed alias matched the smoke-test digest and route, and the public model card listed Beam. The prior human review of the unchanged references was recorded in the Issue #8 replacement revision. The user authorized a maximum estimated inference spend of USD 1 and allowed the account and model checks and usage estimate to substitute for an inaccessible quota balance.

The preflight allowance of 64,000 uncached input and 120,000 generated tokens yielded USD 0.056 at standard rates. Ollama reported 9,278 prompt tokens including 384 cached, and 55,747 generated tokens. Those counts imply approximately **USD 0.0234** at standard rates. Ollama advertised a free period through November 9, 2026 at 12:01 a.m. PST, so the expected charge was USD 0 if the promotion applied. Account charges and quota were not verified. Ollama did not separate thinking from visible output token usage or disclose an immutable serving revision. [Beam model card](https://ollama.com/library/beam:cloud) · [Ollama pricing](https://ollama.com/pricing)

## Case-level scoring

The assistant rated the visible text against the frozen evidence and references, using shuffled opaque IDs within each case. The assessment was saved and hashed before the arm map was opened. The same assistant administered the run, so these are preliminary judgments and the masking cannot rule out recognition from wording. [Masked answers](masked-review.json) · [Claim-level assessment](masked-assessment.md) · [Assessment digest](masked-assessment.sha256) · [Arm map](reveal-map.json)

| Case | Arm | Unsupported | Contradicted | F items covered | Creditor usefulness | Explicit excessive qualifications | Omissions |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| Boeing | A | 4 | 0 | 3/3 | Covered | 1 | None |
| Boeing | B | 2 | 0 | 3/3 | Covered | 1 | None |
| Boeing | C | 2 | 0 | 3/3 | Covered | 0 | None |
| Starbucks | A | 2 | 0 | 3/3 | Covered | 0 | None |
| Starbucks | B | 1 | 0 | 3/3 | Covered | 0 | None |
| Starbucks | C | 1 | 0 | 3/3 | Covered | 0 | None |
| Sempra | A | 2 | 0 | 3/3 | Covered | 1 | None |
| Sempra | B | 0 | 0 | 3/3 | Covered | 2 | None |
| Sempra | C | 0 | 0 | 3/3 | Covered | 2 | None |
| Sanofi | A | 0 | 0 | 3/3 | Covered | 0 | None |
| Sanofi | B | 0 | 0 | 2/3 | Covered | 2 | F2 partial. One CVR per eligible share omitted. |
| Sanofi | C | 4 | 0 | 2/3 | Covered | 0 | F2 partial. One CVR per eligible share omitted. |

The suppression checks found explicit qualifications that weakened supported facts elsewhere in the same answer. Every arm preserved Sempra's scheduled and reported payments, Sanofi's triggered tender cash, and the primary creditor mechanism in all four cases. Neither Sanofi omission removed the milestone triggers or dates.

## Within-case comparisons

| Case | B versus A | C versus B | C versus A |
| --- | --- | --- | --- |
| Boeing | Two fewer unsupported propositions. F coverage, U and excessive caution tied. | Same unsupported count, with one fewer excessive qualification. F coverage and U tied. | Two fewer unsupported propositions and one fewer excessive qualification. F coverage and U tied. |
| Starbucks | One fewer unsupported proposition. F coverage, U and excessive caution tied. | All scored dimensions tied. B gave a flawed rule about adding future starts, while C asserted that the exposure was incremental before establishing overlap. | One fewer unsupported proposition. F coverage, U and excessive caution tied. |
| Sempra | Two fewer unsupported propositions and one more excessive qualification. F coverage and U tied. | All scored dimensions tied, with different qualifications about the payment and obligation. | Two fewer unsupported propositions and one more excessive qualification. F coverage and U tied. |
| Sanofi | Unsupported claims and U tied. F coverage fell by one item and excessive qualifications rose by two. | Four more unsupported propositions and two fewer excessive qualifications. F coverage and U tied. | Four more unsupported propositions and one fewer F item covered. U and excessive caution tied. |

Contradicted claims were scored separately and tied at zero in every comparison. At Boeing, C removed the accounting caveat flagged for B, but it still inferred an incremental USD 1 million cash exposure and an unsupported net-exposure floor. At Sanofi, A preserved the one-CVR entitlement and avoided C's claims about the creditor's contractual promise, the ability to move cash within the group, Aventis control of development, and actual withholding.

The preregistered favorable pattern required an improvement against each comparator in unsupported or contradicted claims or suppression, with no case-level regressions against either comparator. **The observed pattern was mixed and did not meet that criterion.** C improved on A in unsupported-claim counts for three cases, but added excessive caution for Sempra and regressed on unsupported claims and factual coverage for Sanofi. Against B, C reduced excessive caution in Boeing and Sanofi, while adding unsupported claims in Sanofi.

These are observations from one answer per condition in each of four cases. Decoding variability, the additional prompt length, baseline overlap with the principle, and possible prior exposure to public filings limit attribution. The experiment does not establish a general improvement in reasoning, accuracy, or suppression, or isolate which example drove any difference. No further requests were sent after the frozen grid.
