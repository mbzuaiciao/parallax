# Issue #8 pilot execution report

**Stopped on November 7, 2026 after one request.** Baseten returned HTTP 400 for case 01, condition A. Its error body reported that model version `wpgy40e` was deactivated and had to be activated before predictions. The runner stopped immediately under the frozen protocol.

## Preflight and configuration

The user confirmed $100 in Baseten credit expiring November 9, 2026 and authorized a maximum estimated inference cost of $1. Credit balance, expiry and exact-alias billing rates are treated as independently unverified for execution accounting. The user confirmed the references had been checked. The SEC recheck identified no substantive discrepancy, including the distinction between Sempra's March 26 payment obligation and the reported April 25 fulfillment. The public Muse Spark Open rates gave a conservative preflight estimate of approximately $0.50 for all 12 calls. [Preflight report](../baseten-pilot-issue-8-preflight.md), [Baseten pricing](https://www.baseten.co/pricing/)

The runner and inputs matched frozen commit `7319fa3338f173d3db5982fcff55acdc7eb1691a`. The manifest digest was `b71cc0494ccbd99e7c4bfd836574f1ee98cefc5137a32b870d1a91492edac0b7`. Offline generation reproduced the 12-request plan byte for byte. Execution used a fresh private directory at `/tmp/parallax-pilot-attempt-01`. The requested model was `meta-models/muse-spark-open-1026`, with low reasoning effort and an 8,192-token completion cap.

## Request and usage record

| Case | A | B | C |
| --- | --- | --- | --- |
| 01 Boeing | HTTP 400, no completion | Unattempted | Unattempted |
| 02 Starbucks | Unattempted | Unattempted | Unattempted |
| 03 Sempra | Unattempted | Unattempted | Unattempted |
| 04 Sanofi / Blueprint | Unattempted | Unattempted | Unattempted |

One POST was sent at 16:07:23 UTC. There were zero completed responses and 11 unattempted requests. Baseten returned no token usage and no completion model identifier. Estimated inference cost is **$0**, assuming the rejected request was unbilled. Actual charges and token usage are unverified.

The archived files preserve the [full request plan](plan.json), [exact submitted body](01.request.json), [raw provider response](01.response), and [UTC status events](status.jsonl). Authentication headers were excluded by the runner. The archive was checked against the local credential before staging.

## Evaluation

All three comparisons remain unevaluated. With no answer text, this attempt provides no evidence about whether the principle or examples improved reasoning, suppressed useful conclusions, or introduced errors. The provider response establishes that the requested version was deactivated at the time of the attempt. The pilot stopped without retries, replacement requests, or a change to the frozen model.
