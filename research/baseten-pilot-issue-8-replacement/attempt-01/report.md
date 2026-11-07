# Issue #8 replacement pilot outcome

**Stopped after the first request on November 7, 2026.** Baseten returned HTTP 403 for Boeing, condition A, with the error `please check the api-key you provided`. The authenticated model catalog had listed the replacement identifier with reasoning support. The completion rejection establishes an access failure for this request. It leaves the exact cause and live compatibility with the frozen parameters unresolved.

## Freeze and validation

The [replacement revision](../revision.md) was committed before inference as `2854d7757a92bddf7d8a498a73772473b00d84c5`. Its manifest SHA-256 is `ff09b07c0c886d52243b74e4053ec45b2a5828204f37f1357878240a34175388`. The offline plan SHA-256 is `587420ec385f4383123590f978be5404e6a89cfbcd3bc638913c0df811861c5d`. All 12 unique requests matched the original plan after normalizing the model identifier and top-level freeze digest. The model change from `meta-models/muse-spark-open-1026` to `meta-models/muse-spark-open` was the sole payload change. The original attempt and its audit trail remain at `12e4121`.

The user authorized the independent replacement run with a $1 estimated maximum. The catalog rates and completion budget yielded a conservative planning estimate of approximately $0.50 for 12 calls. The runner used the fresh private directory `/tmp/parallax-pilot-replacement-attempt-01`, with the original sequential transport and stopping rules.

## Execution and evaluation

| Case | A | B | C |
| --- | --- | --- | --- |
| Boeing | HTTP 403, no completion | Unattempted | Unattempted |
| Starbucks | Unattempted | Unattempted | Unattempted |
| Sempra | Unattempted | Unattempted | Unattempted |
| Sanofi / Blueprint | Unattempted | Unattempted | Unattempted |

One request was submitted at 16:10:38 UTC. Baseten supplied no usage counts or completion model identifier. Estimated inference cost is **$0**, assuming the rejected request was unbilled. Actual usage and charges are unverified. No retries or replacement requests were sent.

With zero completions, correctness, creditor usefulness, unsupported claims, omissions and regressions remain unevaluated. The attempt provides no evidence for or against any arm.

The [full plan](plan.json), [submitted request](01.request.json), [raw provider response](01.response) and [UTC status log](status.jsonl) are archived here. The archive was checked for the local credential before staging.
