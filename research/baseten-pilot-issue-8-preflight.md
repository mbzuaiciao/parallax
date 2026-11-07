# Issue #8 Baseten pilot preflight

**November 7, 2026. Stopped before inference.** The available Baseten credit, expiration, applicability to this model, and exact-alias pricing could not be verified in the account billing UI. The prior billing API request returned HTTP 403. Chrome access was denied during this preflight. The previously authenticated model catalog listed the historical alias, which establishes catalog visibility. The approximately $100 expiring November 9 is user-reported. [Issue #8](https://github.com/mbzuaiciao/parallax/issues/8), [draft PR #7](https://github.com/mbzuaiciao/parallax/pull/7), [Baseten billing dashboard documentation](https://www.baseten.co/resources/changelog/model-usage-dashboard-and-invoice-history/)

## SEC evidence recheck

The assistant rechecked the four frozen packets against primary disclosures. Human sign-off on the frozen references remains pending. No material correction was identified in this preflight.

| Case | Source check |
| --- | --- |
| Boeing | Note 15 distinguishes the $15 million maximum potential payments from the $14 million carrying amount at December 31, 2024. Payment depends on specified nonperformance, and the guarantees expire through 2036. The blank recourse cell leaves recoveries unresolved. [Form 10-K](https://www.sec.gov/Archives/edgar/data/12927/000001292725000015/ba-20241231.htm) |
| Starbucks | The $11,942.3 million schedule less $1,707.6 million imputed interest reconciles to the $10,234.7 million carrying amount. Fiscal 2024 cash paid and commitments for leases yet to commence are distinct disclosures. [Form 10-K](https://www.sec.gov/Archives/edgar/data/829224/000082922424000057/sbux-20240929.htm) |
| Sempra | SDG&E’s Note 8 describes the March 26, 2007 separate City settlement and its scheduled $8.5 million payment on April 25. A later paragraph independently states that payment occurred on April 25. These are the obligation at signing and the subsequently reported fulfillment of the same obligation. The new payment replaced the earlier $12 million installment schedule for the City. Entity-level allocation remains unspecified in the packet. [SDG&E Form 10-Q](https://www.sec.gov/Archives/edgar/data/86521/000008652107000055/sdge2qtr07.htm) |
| Sanofi / Blueprint | The closing disclosure and merger agreement support the accepted tender and $129 per share payable promptly within one business day of acceptance. The CVR contract separately supports the Aventis deposit role and the $2 and $4 milestones and deadlines. The packet scopes out non-tendered shares and post-acceptance disbursements. [Form 8-K](https://www.sec.gov/Archives/edgar/data/1597264/000119312525160804/d909980d8k.htm), [merger agreement](https://www.sec.gov/Archives/edgar/data/1597264/000110465925055143/tm2516831d1_ex2-1.htm), [CVR agreement](https://www.sec.gov/Archives/edgar/data/1597264/000119312525160804/d909980dex991.htm) |

## Audit trail and outcome

- Frozen commit `7319fa3338f173d3db5982fcff55acdc7eb1691a`. Freeze manifest SHA-256 `b71cc0494ccbd99e7c4bfd836574f1ee98cefc5137a32b870d1a91492edac0b7`. Frozen files match the commit.
- Offline plan SHA-256 `3505a46b13a3a8c5caac079fea2e7f1043b081e9cde0ecb57fe31a1f27e39e17`. Verified 12 unique case/arm pairs, identical within-case question and evidence, exact system-prompt deltas, fixed settings, and model inputs built only from the specified prompts and source packets.
- Actual inference requests **0 of 12**. Input tokens **0**, output tokens **0**, estimated inference cost **$0**. All 12 cells are unattempted. The principle, examples, excess caution and regressions remain unevaluated.
- Planning estimate remains **$0.08–$0.17** at public Muse Spark Open family rates, or about **$0.43** at the full completion budget under the protocol's input-token assumption. This is a planning estimate. Exact-alias pricing and an approved hard budget are pending. No live attempt directory was created. [Baseten pricing](https://www.baseten.co/pricing/)

Before execution, record human sign-off, account credit confirmation and exact-alias pricing, the approved hard budget, and a fresh private output directory as required by Issue #8.
