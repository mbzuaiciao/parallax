# Parallax

Parallax evaluates how corporate financial obligations affect different stakeholders.
This proof of concept prepares four financial-reasoning tasks from one synthetic
company: two investor perspectives across base and stress scenarios. It can also
submit all four to Meta Model API and save their unmodified responses for inspection.
It uses Python's standard library with no third-party runtime or test dependencies.

## Run

Use Python 3.10 or later and [uv](https://docs.astral.sh/uv/). From the repository root:

```sh
uv sync --locked
uv run python -m parallax --all > /tmp/parallax-tasks.json
uv run python -m parallax --perspective equity_holder --scenario base
uv run python -m parallax --perspective equity_holder --scenario stress
uv run python -m parallax --perspective senior_unsecured_creditor --scenario base
uv run python -m parallax --perspective senior_unsecured_creditor --scenario stress
uv run python -m unittest discover -s tests -v
```

`pyproject.toml` defines the project and `uv.lock` records its dependency resolution.
`uv sync` creates `.venv`; `--locked` verifies the committed lockfile. The project
runs directly from the existing source tree (`package = false`), without a build
backend or installed console script. Use `uv run` for execution and tests.

`--all` emits a JSON array in the order shown above; each individual command emits
the corresponding JSON object. These offline commands are stable across repeated runs: no runtime
timestamps, random values, API keys or network dependencies. `--case PATH` optionally
loads a local copy of the same case schema; the bundled path is resolved relative
to the module. This is a single-case implementation, not a general contract engine:
calculations assume the one-year term and payment rules below. Changing those rules
in prose requires changing the calculation code too.

## The case

`cases/harbor.json` is the complete evidence record. Harbor Components and its
counterparty are fictional. **Every company figure, contract term and scenario is
a synthetic assumption**, not a financial fact about an actual issuer. All amounts
are USD millions; the valuation date is December 31, 2026 and settlement is
December 31, 2027.

Harbor reports 100 of borrowings: one senior unsecured bullet bond with a 5% annual
simple coupon. Principal and the single year's coupon are due together at settlement,
so its contractual claim is 105. There are no interim payments, collateral,
amortization, acceleration, covenants or default penalties.

Harbor also guarantees a distributor's debt, with a total cap of 40 including
interest and fees. Distributor default at settlement immediately creates a claim
equal to covered debt due less lender recoveries, floored at zero and capped at 40.
Without default the claim is zero. The guarantee expires after settlement. A
triggered claim shares the same rank and settlement time as the bond principal and
coupon. Harbor receives no reimbursement, collateral or subrogation proceeds.

The reported borrowings number is not the total economic exposure. No accounting
carrying amount for the guarantee is supplied: a contingent payment trigger does
not establish whether or how a guarantee must be recognized under an accounting
standard. The case makes no GAAP or IFRS recognition claim.

## Assumptions and verifiable background

The terminal cash pool is after operating costs, taxes and administration expenses,
but before either modeled claim is paid. There are no other claims or distributions.
If cash is insufficient, bond and guarantee claims share it proportionally;
common equity receives only the positive remainder and cannot be negative. This
is a stipulated settlement mechanism, not a simulation of actual bankruptcy law.
The cash pool is neither a reported asset balance nor a market enterprise valuation.
Scenario probabilities, discount rates and security purchase prices are absent.

In base, the cash pool is 150 and the distributor does not default. In stress, cash
falls to 110 and the distributor defaults with 50 due and 10 recovered by its lender.
The joint stress is assumed, not estimated. These are conditional cash outcomes,
not forecasts, expected losses, present values or investment returns.

The independently verifiable background facts are that a corporate bond promises
interest and repayment of principal, and that bondholders have priority over
shareholders in bankruptcy. See the SEC's
[What Are Corporate Bonds?](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/what-are),
sections “What is a corporate bond?” and “What happens if a company goes into
bankruptcy?”. Verified October 27, 2026. The JSON records these facts with stable
IDs, URLs, verification dates and scope limits. The source does not establish this
case's amounts, guarantee terms or equal ranking; those are explicitly synthetic.

## Reference calculations and economic distinctions

Let `D = 100 × (1 + 0.05) = 105`, `G` be the triggered guarantee claim, and `A`
the terminal cash pool. Set `r = min(1, A / (D + G))`. Bond cash is `D × r`,
guarantee cash is `G × r`, and equity cash is `max(0, A - D - G)`.
These formulas use claims before rounding and distribute one common cash pool;
they do not subtract the guarantee first and then allocate it again.

| Quantity (USD millions unless marked) | Base | Stress |
| --- | ---: | ---: |
| Cash available | 150 | 110 |
| Reported debt principal | 100 | 100 |
| Bond principal plus coupon claim | 105 | 105 |
| Triggered guarantee claim | 0 | 40 |
| Total contractual claims | 105 | 145 |
| Bond cash payment | 105 | 79.655172 |
| Guarantee cash payment | 0 | 30.344828 |
| Bond payment shortfall | 0 | 25.344828 |
| Bond claim recovery (%) | 100 | 75.862069 |
| Common equity residual | 45 | 0 |

The stress bond recovery is independently checkable as `110 × 105 / 145`; the
guarantee receives `110 × 40 / 145`. The 40 guarantee is a contractual claim, not
40 of actual cash paid. Recovery uses principal **plus coupon** as its denominator.
Amounts and percentages are emitted as decimal strings rounded half-even to six
decimal places; independently rounded outputs may have small summation differences.

The equity holder cares about the residual: base leaves 45 and stress wipes it
out. The senior unsecured creditor has capped contractual upside at 105 and suffers
a stress shortfall because the equally ranked guarantee dilutes recovery. With the
same stress cash of 110 **and no guarantee**, the bond would receive all 105 and
equity would receive 5. This counterfactual isolates the guarantee's effect from
the separate decline in cash. In base, removing the untriggered guarantee changes
neither stakeholder's payment.

## Offline task format and tests

Each task contains a stable ID, selected perspective and scenario, instructions,
contract terms, assumptions, cited background facts, the selected scenario's
evidence, deterministic reference values and a requested structured response shape.
The model is asked to explain the investor-specific economics, cite case field
paths or fact IDs, distinguish claims from payments and identify limitations.
Reference arithmetic is visible to the model; this is task preparation, not a
hidden-answer benchmark. Both perspectives receive the same scenario arithmetic.

The unittest suite checks independent repeated loading, invalid inputs, the base
waterfall, stress recovery against exact rational calculations, cash conservation,
guarantee triggering/capping/recovery netting, evidence preservation and all four
CLI tasks. It compares repeated output and each individual task byte for byte.

## Live Meta Model API evaluation

The integration follows Meta's [Chat Completions documentation](https://dev.meta.ai/docs/protocols/chat-completions)
and [key setup guide](https://dev.meta.ai/docs/quickstart), checked October 27, 2026.
It sends `POST https://api.meta.ai/v1/chat/completions` using bearer authentication,
model `muse-spark-1.3`, and `developer` and `user` messages. It uses `urllib` rather
than adding an SDK dependency. Temperature and reasoning effort use provider
defaults; `max_completion_tokens` is 8192. Each call has a 60-second socket timeout.

Create a key in the [Meta Model API dashboard](https://dev.meta.ai/), then configure
`MODEL_API_KEY` in your environment. Alternatively, copy `.env.example` to `.env`,
replace its placeholder locally, and let uv load it:

```sh
uv sync --locked
cp .env.example .env
# Edit .env locally to set MODEL_API_KEY; do not put credentials in source files.
uv run --env-file .env python -m parallax --evaluate --output results/first-live.json
```

If `MODEL_API_KEY` is already exported in the current shell, omit `--env-file .env`.
The application reads only the environment variable; uv handles loading an optional
environment file. `.env` and related local environment files are ignored by Git.

`--evaluate` submits the same four combinations in the offline command order. It
cannot be combined with `--all`, `--perspective` or `--scenario`; `--output` is
required. It refuses to overwrite an existing report, so choose a new filename
for another live run. Live responses need not be reproducible; the exact submitted
request and provider response are saved for inspection.

Live prompts are constructed separately from offline tasks. They contain contractual
inputs, settlement rules, cited background facts, the selected investor identity,
and only the selected scenario's raw inputs. They exclude deterministic reference
values, precomputed scenario prose, and perspective descriptions that suggest the
expected conclusion. They ask the model to identify obligations, explain their
economic consequences, show calculations, consider the guarantee counterfactual,
and disclose uncertainty. The contractual distribution rules remain in the prompt
because they are facts needed to solve the case. The offline `--all` format still
includes visible reference arithmetic and **must not be used as the live prompt**.

The JSON report stores each evaluation's:

- `request`: the exact model payload, without authentication headers or keys.
- `model_generated`: the unmodified provider JSON, including model text under
  `choices[0].message.content`, finish reason, and any usage and model metadata.
- `deterministic_reference`: separately labeled local arithmetic with
  `sent_to_model: false`. These values are never part of the submitted payload.
- `status`: `pending`, `in_progress`, `completed`, `incomplete` or `error`; errors
  have a separate message. A non-`stop` finish reason is marked incomplete.

The runner checkpoints the report before calls and after every response, continues
through API failures, and returns a nonzero exit status unless all four complete.
There are no automatic retries: a timeout may occur after a request reached Meta;
rerunning can incur another charge. HTTP errors, connection failures, invalid JSON
and malformed completions are handled without logging authentication headers.
Structured malformed provider JSON is retained where available. A process interrupted
mid-call leaves the last checkpoint with that entry marked `in_progress`.

Model text is saved unchanged as a JSON string; no model JSON response schema or
automatic financial scoring is enforced. Inspect the four answers alongside the
local references above, noting errors separately without rewriting the answers.
Mocked tests cover prompt isolation, HTTP request and response handling, key
preflight, response preservation, four-call persistence, failure checkpoints,
incomplete outputs and CLI exit behavior. Tests never require a live key.

The first live evaluation completed on October 27, 2026: all four requests returned
`muse-spark-1.3` responses with finish reason `stop`. Exact requests, unmodified
responses and separate local references are saved in
[`results/first-live.json`](results/first-live.json). The
[manual review](results/first-live-review.md) records the numerical comparison and
one imprecise statement about equity's cash cushion. No model answers were corrected.

Web UI, multi-agent orchestration, general financial-data ingestion and benchmarking
infrastructure are intentionally outside this proof of concept.
