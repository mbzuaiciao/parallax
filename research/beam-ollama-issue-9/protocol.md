# Beam via Ollama Cloud

[Issue #9](https://github.com/mbzuaiciao/parallax/issues/9) prepares a separate Beam experiment based on the pilot frozen at `7319fa3` in [draft PR #7](https://github.com/mbzuaiciao/parallax/pull/7). The two Baseten attempts under [Issue #8](https://github.com/mbzuaiciao/parallax/issues/8) ended with zero completed scientific responses.

## Compatibility smoke test

On November 7, 2026, Ollama 0.40.15 was started temporarily on loopback with cloud enabled. The installed `beam:cloud` alias routed to `beam` at `https://ollama.com`. The client connected locally and inference ran remotely. The [model metadata](smoke-attempt-01/model-metadata.json) records the local alias digest, advertised 1,048,576-token context, and capabilities. The reported identifier `beam` and the local digest do not identify an immutable serving revision.

The [smoke plan](smoke-attempt-01/plan.json) and [exact request body](smoke-attempt-01/request.json) were hashed and checked offline before sending. The request used system and user messages about an unrelated fictional lantern. It used a 120-second wall-clock deadline, one non-streaming POST, no redirects and no retries. The compatibility gate required HTTP 200, a completed assistant response with stop reason `stop`, a reported model ID, and visible content equal to `GREEN` after trimming. [Ollama chat API](https://docs.ollama.com/api/chat)

The request passed all checks in **1.017 seconds** client elapsed time. Ollama reported `beam`, a total duration of 688,298,169 ns, 102 prompt tokens (0 cached) and 57 generated tokens. The response contains both visible content and a separate thinking field. It does not break out reasoning tokens, provide per-stage timing, or report billed usage. The provider's response timestamp is roughly 2.4 seconds later than the client's receipt timestamp, so elapsed time uses the client's monotonic clock. [Raw response](smoke-attempt-01/response.json) · [Client timestamps and HTTP status](smoke-attempt-01/status.jsonl)

Ollama advertised Beam as free through November 9, 2026 at 12:01 a.m. PST, with listed rates of USD 0.125 per million input tokens, USD 0.015 per million cached input tokens and USD 0.40 per million output tokens. Actual billing, account credits and remaining quota were unavailable from the local API. [Beam model card](https://ollama.com/library/beam:cloud) · [Ollama pricing](https://ollama.com/pricing)

## Frozen offline grid

The [Beam freeze](freeze.json) pins the [historical freeze](../skill-principle-pilot/freeze.json) and the exact serialized grid. It reuses the historical builder, which verifies its frozen inputs. The four cases remain Boeing credit guarantees, Starbucks operating leases, Sempra's City settlement, and Sanofi's Blueprint tender/CVR. Arms remain A (Parallax baseline), B (plus principle), and C (plus principle and both examples), in the original order. The [reference judgments](../skill-principle-pilot/references.md), [scoring rules and hypothesis](../skill-principle-pilot/protocol.md#preregistered-scoring-checklist), and human review and masking procedure carry over verbatim. Score only the visible assistant content.

From the repository root, generate the grid offline:

```sh
python3 research/beam-ollama-issue-9/prepare.py > /tmp/parallax-beam-grid.json
```

The grid uses `POST /api/chat` on loopback, `beam:cloud`, `stream: false`, and a 120-second client deadline as in the smoke test. Both message roles and all message text are unchanged. Case and arm labels are local metadata outside each POST payload. The smoke and grid omit sampling, seed, reasoning and output-limit overrides, leaving Beam's serving defaults uniform across arms. In particular, the Baseten `reasoning_effort=low` and 8,192-token cap are omitted. Effective sampling defaults, usable context and output limits for the scientific packets, and accounting for thinking tokens remain unverified. The smoke test exercised role formatting and the response envelope on a short prompt.

Offline checks verified all 12 unique case/arm pairs in frozen order, exact equality of every model-facing message to the historical payload, and byte-for-byte equality of each case's user message across its arms. The user message was independently reconstructed from the frozen question template and the packet's source, locator and evidence text with excerpt IDs. The system messages preserve the frozen baseline and exact B/C additions. This confines the model input to the intended prompt, question and evidence. The reference and rubric documents enter only through hash verification. All 75 repository Python tests passed with loopback-only networking and the Ollama port blocked.

**Basic compatibility passed and the offline grid is ready.** Scientific execution requires separate explicit authorization. At that point, confirm the reference review, cloud budget and quota, and recheck the service and alias metadata. Use the fixed schedule, one request per cell, and a fresh attempt directory with exact requests, raw responses and status logs. Preserve the original stop-on-error rule for transport or provider errors, malformed, incomplete or empty answers, missing model or token counts, changed reported model, or non-stop termination. Do not retry or substitute models. Record `prompt_eval_count` and `eval_count` as Ollama counts. **This attempt stopped after one smoke request. Zero of the 12 scientific requests were sent.**
