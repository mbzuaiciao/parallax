# Muse Spark replication of the Beam reasoning-skill pilot

## Compatibility result

On November 7, 2026, Parallax's existing Meta client sent one non-streaming synthetic POST with system and user messages to Meta's Model API. The client used the nonempty `MODEL_API_KEY` from Parallax's ignored, untracked `.env`, with a 60-second socket timeout. Meta reported `muse-spark-1.3` and returned the expected `PURPLE` with finish reason `stop` in 2.816 seconds. Usage was 40 input tokens (zero cached) and 301 completion tokens (including 290 reasoning tokens), for 341 total. There were zero errors, redirects, retries, fallbacks, or scientific calls. The [smoke record](smoke.json) contains the request body and returned JSON.

## Beam findings

The hypothesis was that adding a failure-derived principle and two applicability examples (C) would improve creditor analysis relative to the Parallax baseline (A) and the baseline plus the principle alone (B). The preregistered criterion required improvement against each comparator without case-level regressions. [Frozen hypothesis and scoring](../skill-principle-pilot/protocol.md#preregistered-scoring-checklist) · [Draft PR #7](https://github.com/mbzuaiciao/parallax/pull/7)

Beam completed all 12 cells. C produced fewer unsupported claims than A on Boeing, Starbucks, and Sempra, but added excessive caution on Sempra. C had more unsupported claims and lower factual coverage than A on Sanofi. Compared with B, C reduced excessive caution on Boeing and Sanofi, while adding unsupported claims on Sanofi. Creditor usefulness was covered throughout, and all contradicted-claim counts were zero. The mixed pattern missed the favorable criterion. [Beam report and artifacts](../beam-ollama-issue-9/scientific-attempt-01/report.md) · [Draft PR #10](https://github.com/mbzuaiciao/parallax/pull/10)

A separate, context-isolated AI adjudicator independently reviewed the same three Sanofi answers with blinded condition labels and locked its scores before reveal. It corroborated C's unsupported-claim regression against both comparators, its coverage loss against A, and its lower excessive caution than B. It counted five unsupported claims in C instead of four by separating the remitter assignment from actual withholding. [Sanofi re-adjudication](../sanofi-re-adjudication-issue-11/report.md) · [Draft PR #12](https://github.com/mbzuaiciao/parallax/pull/12)

One answer per cell leaves decoding variability unresolved. The prompts differ in length, the baseline overlaps with the principle, and prior exposure to public filings is possible. The original reviewer also administered the run. The second AI review covers one case and had no human adjudication. Provider defaults and serving revisions can differ across Beam and Muse, so the comparison measures the pattern under each model and serving configuration.

## Offline Muse grid

From the repository root:

```sh
python3 research/muse-spark-replication/prepare.py > /tmp/parallax-muse-grid.json
```

The builder runs the frozen Beam preparation offline, which checks the original source hashes, then verifies the schedule and each complete Beam payload against the executed archive. The Muse grid retains the exact system and user messages, the four cases (Boeing, Starbucks, Sempra, and Sanofi), and the three conditions in the same order. Case and arm identifiers remain outside the POST bodies. The reference answers and scoring rules stay separate from model inputs. All 12 unique case/arm pairs and identical user messages across each case's arms were checked. [Offline verification](verification.json) · [Frozen evidence](../skill-principle-pilot/cases/) · [References](../skill-principle-pilot/references.md)

The grid selects Meta's standard `muse-spark-1.3`, disables streaming, and sets an 8,192-token completion cap, matching the synthetic request and the existing Meta client's default payload cap. Beam's experiment omitted an explicit cap. The Muse cap includes reasoning and visible tokens, so it can affect completion relative to Beam. Sampling and reasoning settings use provider defaults in every cell. [Meta Chat Completions schema](https://dev.meta.ai/docs/api-reference/chat-completions/schemas)

## Cost and execution gate

The grid contains 31,989 message characters. Using Beam's observed 9,278 input and 55,747 generated tokens as a planning proxy, the 12 Muse requests would cost about **USD 0.25** at Meta's standard rates of USD 1.25 per million uncached input and USD 4.25 per million output tokens. An allowance of 12,000 input tokens and all 98,304 available completion tokens gives a **USD 0.43** budget scenario before any cache savings. Muse's tokenizer and reasoning usage can differ. Account quota, credits, actual billing, and behavior on the full scientific packets remain unverified. [Meta pricing](https://dev.meta.ai/docs/pricing-rate-limits)

The grid is ready for offline review. **Zero of the 12 scientific calls were sent.** Live execution requires separate authorization. For an authorized run, preserve the fixed order and masking procedure, archive exact requests and returned responses in a fresh attempt directory, and stop on any provider or transport error, malformed or empty output, missing model or usage, changed model ID, or non-`stop` finish. Score only the visible assistant text under the frozen checklist.

## Completed scientific run

The separately authorized run completed all 12 frozen calls once at `c920458`. The preparation above records the state before that authorization. See the [execution and preliminary scoring report](scientific-attempt-01/report.md) for the archive, within-Muse comparisons, and comparison with Beam.
