# Scientific validation v1 — Muse Spark API preflight

Date: October 29, 2026. Git revision: `870a683cf1aaed6d54424a6b444f32eccd2bd9ec`.
Scope: one harmless connectivity request, zero scientific experiment responses.
No AGENTS.md was found in the repository or inspected ancestor directories.
Final compatibility follow-up: official model-specific configuration examples now
support the planned 8192-token budget on a documentation basis; see the final
section. **No additional live request was made.** Total live preflight requests: one.

## Model, endpoint and authentication

- Intended model: `muse-spark-1.3`.
- Endpoint: `POST https://api.meta.ai/v1/chat/completions`; existing `parallax/model_api.py` configuration.
- Authentication available from the ignored local .env file, sent as a bearer credential
  only to the intended endpoint. No credential value or authorization header is
  printed, persisted in this report, or committed.
- No alternate model, endpoint or backend was requested. Returned identifier is
  recorded below; an identifier alone does not establish an immutable backend.

## Initial preflight: exactly one live request

The bounded probe used the protocol's temperature but a deliberately smaller
128-token output budget. It contained no financial evidence or reference answers.
No tools, conversation history, reasoning-effort override, or other sampling
parameters were sent. No automatic retries, redirect following, model-list call,
validation call or second model call was made. The existing client's one-shot,
60-second urllib transport pattern was used directly to capture HTTP status;
production integration code was not changed.

Request body (credentials are not part of this JSON):

```json
{
  "model": "muse-spark-1.3",
  "temperature": 0.7,
  "max_completion_tokens": 128,
  "messages": [
    {
      "role": "developer",
      "content": "Reply with exactly OK."
    },
    {
      "role": "user",
      "content": "Reply OK."
    }
  ]
}
```

Result: **HTTP success**. HTTP 200 acceptance: **true**;
returned model matches requested identifier: **true**.
Only the following allowlisted response metadata, numeric usage and short answer
were retained. Raw response bodies, reasoning text and headers were not saved.
A null field means unavailable, not zero usage or a successful response.

```json
{
  "live_request_attempts": 1,
  "automatic_retries": 0,
  "redirects_followed": 0,
  "http_status": 200,
  "returned_model": "muse-spark-1.3",
  "provider_response_id": "chatcmpl-01a18849-bfae-777a-a80a-10a5a74a06e0",
  "finish_reason": "length",
  "usage": {
    "completion_tokens": 128,
    "prompt_tokens": 20,
    "total_tokens": 148,
    "completion_tokens_details": {
      "reasoning_tokens": 126
    },
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  },
  "answer": null,
  "error_category": null,
  "elapsed_seconds": 1.127,
  "started_at_utc": "2026-10-29T15:31:23.813124+00:00",
  "finished_at_utc": "2026-10-29T15:31:24.940958+00:00"
}
```

This establishes endpoint/authentication access and acceptance of the requested
model, temperature 0.7 and 128-token cap for this attempt, **not a usable text
completion**. The response exhausted its budget (`finish_reason=length`), reported
126 reasoning tokens out of 128 completion tokens, and returned no visible answer.
Parallax's existing `chat_completion()` text validator would reject this response
as having no valid text completion. No retry was made to obtain an “OK” answer.

## Confirmed versus unverified settings

| Setting | Documentation and probe evidence | Conclusion |
| --- | --- | --- |
| `muse-spark-1.3`, Chat Completions | [Meta model catalog](https://dev.meta.ai/docs/models) lists this model; the probe returned HTTP 200 and the same model identifier. | Endpoint access/model identity confirmed for this attempt; no usable text completion or immutable backend identity established. |
| `temperature=0.7` | [Official parameter guide](https://dev.meta.ai/docs/protocols/chat-completions) permits 0–2. The probe explicitly sent 0.7. | Accepted without rejection; this does not prove the sampling distribution or that a value was internally honored. |
| `max_completion_tokens=128` | [Request schema](https://dev.meta.ai/docs/api-reference/chat-completions/schemas) defines an integer bound including visible and reasoning tokens. | Accepted at 128; budget exhausted with no visible answer. |
| Planned `max_completion_tokens=8192` | Initial pages checked did not specify a model-specific maximum. The final follow-up below located official Chat Completions configuration examples listing a model-specific output limit of 131072. | **Supported by provider documentation**, with the scope/limitations below. Runtime acceptance at 8192 and actual generation of 8192 tokens remain untested. |
| Other settings | Omitted identically to the protocol: top_p, stream, n, seed, reasoning_effort. Guide documents top_p=1, stream=false, n=1, seed=null; reasoning is model-set. | Defaults documented; effective reasoning effort and immutable backend version not measured. |

Documentation was inspected without authentication to the model API. No explicit
non-generating request validator was located in those pages; no speculative endpoint
or token-limit probe was invoked. The absence of such a mechanism in this search
is not proof the provider offers none. Third-party backends were not used as
validation of Meta's direct API limits.

Relevant documented restrictions: only n=1 is supported; reasoning tokens consume
the completion budget; unsupported parameters may be rejected; the provider
recommends temperature 1.0, while the protocol intentionally retains 0.7. A short
probe does not establish quota for 30 calls, batch reliability, future availability,
financial reasoning quality, or response length at the planned budget.

## Initial experiment decision and preservation

The following was the initial decision before the additional documentation check;
its output-limit uncertainty is updated by the final section below.

**The 30-response experiment cannot proceed on this record alone.** The 8192-token
setting remains unverified; obtain explicit provider documentation or an authorized
non-generating validation mechanism before clearing that readiness gap. A small
request is not evidence for the larger output limit. Further API requests are not
authorized by this preflight and none were attempted.

All five reference records remain provisional and still require explicit human
approval and the protocol's reference-freeze procedure. No scoring rubric,
experimental condition, source fixture, historical result or production code was
changed. Protocol/reference hashes unchanged during preflight: **true**.
The probe is outside the 30 planned observations and cannot replace one of them.
Independent ground-truth approval and separate experiment authorization remain
required, even if the connectivity probe succeeded.

Only this report was added. No repository code changed, so offline tests were not
rerun under the requested code-change-only rule. No commits or pushes were made.

## Final API compatibility check — October 29, 2026

Re-read the protocol and this initial preflight. No AGENTS.md was present in the
repository or inspected ancestor directories. The intended model, endpoint,
temperature 0.7 and completion-token budget 8192 are unchanged.

### Newly located official model-specific evidence

Meta's [coding-agent guide](https://dev.meta.ai/docs/coding-agents), under
“Set up OpenCode → Configuration → Chat Completions adapter (fallback),” specifies
`muse-spark-1.3`, base URL `https://api.meta.ai/v1`, and a model output limit of
**131072**, separately from context capacity. The adapter is explicitly identified
as Chat Completions. Meta's [GitHub-agent cookbook](https://dev.meta.ai/docs/cookbook/github-agent),
section 2 configuration, independently shows the same model/output setting for
direct Meta Model API access over that transport. Its relevant configuration is:

```json
"muse-spark-1.3": {
  "name": "Muse Spark",
  "limit": { "context": 1048576, "output": 131072 }
}
```

These are first-party integration examples, not a measured server response or a
separate formal account-specific limit contract. They provide explicit
model-specific documentary support for an output budget above 8192. Combined with
the [Chat Completions request schema](https://dev.meta.ai/docs/api-reference/chat-completions/schemas),
which defines `max_completion_tokens` as the integer bound on reasoning plus visible
output, this supports **documented compatibility** of the planned 8192 setting.
The conclusion uses the stated output limit, not the larger context window or
the initial 128-token probe. No OpenCode installation or backend substitution was
made; only the official documentation was read.

### Additional request and empirical limits

No additional live request was necessary under the documentation-first instruction.
For this follow-up, HTTP status, termination reason, visible output, returned model
identifier and token usage are **not applicable: no request sent**. The initial
probe's recorded HTTP 200 / model `muse-spark-1.3` / `length` / null visible answer /
148 total tokens remain the only runtime observations. No retries, benchmark
prompts, non-generating API calls or other model calls were made.

Documented capacity, parameter acceptance and demonstrated generation are distinct:

- Documentation supports the planned 8192-token budget within the published
  configuration limit; this resolves the earlier absence of model-specific evidence.
- Runtime acceptance of `max_completion_tokens=8192` for this account was **not
  tested**. No claim of HTTP acceptance at that value is made.
- Actual generation of 8192 completion tokens, or 8192 **visible** tokens, was
  **not demonstrated**. Even a successful one-word response at that setting would
  establish parameter acceptance only. Reasoning shares the completion budget.

### Updated decision

The output-budget compatibility gap is resolved **at the provider-documentation
level**, with runtime acceptance and sustained generation still untested. No further
paid check is performed or required by this documentation-first task. This does not
authorize the experiment or guarantee account quotas, complete answers, default
reasoning effort, immutable backend identity, or reliability across 30 requests.

All five references remain provisional; human approval, the reference freeze and
separate authorization to run the scientific experiment are still required. The
protocol, references, scoring rules, fixtures and experimental conditions were not
modified. Only this preflight report was updated. No code changes, test reruns,
commits or pushes were made.
