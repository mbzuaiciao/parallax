# Parallax

Parallax evaluates how corporate financial obligations affect different stakeholders.
The original proof of concept prepares four financial-reasoning tasks from one
synthetic company: two investor perspectives across base and stress scenarios.
A second experiment compares non-recourse subsidiary debt with a parent-guaranteed
structure for the same two investors. Both experiments can submit four independent
requests to Meta Model API and save their unmodified responses for inspection.
The financial backend uses Python's standard library. The hackathon demo adds
Streamlit as its only direct dependency; its required dependencies are locked by uv.

The three real-world cases use **curated disclosure summaries**: manually selected
short quotations and factual paraphrases, rather than raw SEC filings. They test
financial interpretation of supplied summaries, not autonomous information extraction,
filing discovery or retrieval. Human/assistant preparation already selects and
organizes the relevant terms. Both neutral and guided experimental conditions are
preserved; even neutral prompts receive these curated summaries, and guided results
measure performance with explicit analytical instructions, not unaided capability.
CoreWeave is an on-balance-sheet comparison case, not an extra hidden debt layer.

The [post-audit correction record](docs/post-audit-corrections.md) documents primary
sources, corrected UI representations and unresolved accounting questions. Historical
case packs, reference answers, assessments and experiment results remain unchanged.

## React evidence workstation · Phase 1

The local React/TypeScript/Vite workstation covers NVIDIA, Meta, CoreWeave,
Apple and Microsoft using existing historical SEC source packs. It separates
disclosed evidence, provisional conditional interpretation and evidence limits.
The existing Streamlit application remains available and unchanged.

See [workstation development and validation](docs/workstation.md) for setup,
API routes, provenance, interface description and limitations.

## Launch the interactive workstation

From the repository root, launch saved-results mode without an API key:

```sh
uv sync --locked
uv run streamlit run streamlit_app.py --server.address 127.0.0.1
```

Open [localhost:8501](http://localhost:8501). Parallax operates as an issuer-centric financial analysis workstation inspired by Bloomberg Terminal workflows:

- **Issuer Workspace & Search:** A prominent command and search bar enables instant ticker and issuer lookup (`NVDA`, `META`, `CRWV`, `CEDAR`, `HARBOR`). Unsupported issuer queries (e.g. `AAPL`, `Tesla`) render a clear "Coverage Status: Not Covered" panel. Parallax does not fabricate coverage, balance sheets, ratings, or live pricing.
- **Persistent Context:** The active issuer, historical cutoff date, and investor perspective persist seamlessly across all analytical functions.
- **Issuer Overview:** Leads with reconstructed corporate obligations, distinguishing nominal accounting debt from contingent caps. Displays explicit unscorable metric notices (Debt/EBITDA leverage, default probability, expected loss, recovery rates) to prevent fabricated totals.
- **Financial Obligations:** Compact, audit-ready breakdown of reconstructed contracts, verified facts from the Wagner reference dataset, disclosed limitations, and primary SEC EDGAR accession links.
- **Capital Structure:** Claims-oriented hierarchy distinguishing obligors, guarantees, priorities, and investor economic exposure. Supports Common Equity and Senior Unsecured Creditor perspectives, with Secured Creditor, Subordinated Creditor, and CDS Participant perspectives cleanly marked as independent experiment data pending.
- **Scenario Analysis:** Dedicated Scenario Sandbox for deterministic synthetic benchmarks (Cedar Holdings subsidiary recourse pair and Harbor Components contingent guarantee), alongside real-world contractual activation sensitivity matrices.
- **AI Diagnostics:** Evaluates model reliability using the preregistered 12-cell prompt-guidance ablation (`guidance-ablation-v1`). Features side-by-side Guided vs. Neutral prompt comparisons, supported findings, omissions, verbatim unsupported conclusions, and on-demand inspection of original saved responses.

Synthetic figures are stipulated, conditional settlement outcomes, not market-value
losses or expected returns. The same cash pool is used in each guarantee comparison.
Cedar's group borrowing principal is distinct from the parent's own legal claims.
Real-world figures measure different things: NVIDIA's initial aggregate cap is
neither outstanding debt nor expected loss; Meta's up-to purchase commitment is not
an automatic loss; CoreWeave's dated carrying amount is already recognized financing,
not an additional off-balance-sheet debt layer. Do not add these figures into leverage.
The packs cannot determine issuer leverage ratios, equity valuations or creditor
recoveries. Secured, subordinated and CDS perspectives need further contractual inputs
and are not modeled.

The diagnostics lab displays **preliminary assistant-authored assessments**, not independent
blinded human ratings or correctness scores. Twelve completed ablation calls do not
mean twelve correct answers. Curated evidence, one sample per cell, imperfect masking
and assistant judgment limit inference. Research experiments, source packs, reference
annotations and historical outputs are unchanged by this interface redesign.

For optional live inference, configure `MODEL_API_KEY` in the ignored local `.env`
file as described below, then launch with uv loading it:

```sh
uv run --env-file .env streamlit run streamlit_app.py --server.address 127.0.0.1
```

Expand **Optional live analysis** on Capital Structure or AI Diagnostics. One click
sends exactly one request for the selected case, investor and scenario/structure or
prompt condition through the existing Meta client. References are excluded from
requests. Responses stay bound to that selection in the session; historical files
are never overwritten, and there are no automatic retries. Without a configured key,
the button is disabled; the entire saved-results demo remains usable. No keys are
entered in the page. This redesign makes no new live calls during verification.

The UI reuses the existing loaders, request builders, recorded assessments and API
client. No dependencies or research data were added. Streamlit AppTest verifies
issuer selection, unsupported issuer searches, persistent context across all 5 functions,
fixed-cash calculations, primary source links, keyless access to all saved combinations,
original-response access, planned perspective disclosures, and mocked single-selection live requests/errors. Run the complete suite with:

```sh
uv run python -m unittest discover -s tests -v
```

Redesign verification: all **55 tests pass**. A browser smoke
check confirmed the issuer workspace, 5-function navigation, investor switching,
unsupported query handling, and on-demand original model text. No new live inference was performed.

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

Beyond the single-page Streamlit demo, multi-agent orchestration, general
financial-data ingestion, benchmarking and deployment infrastructure remain
outside this proof of concept.

## Paired subsidiary-recourse experiment

The [paired case and reference answers](cases/subsidiary_pair.md) specify one parent
and its wholly owned subsidiary. Under subsidiary default, Case A has non-recourse
subsidiary debt; Case B adds an enforceable parent guarantee. All common facts are
stored once in [the input JSON](cases/subsidiary_pair.json), and tests check that
only `evidence.parent_guarantee` changes across paired prompt evidence. Each
structure is independently evaluated for parent equity and the parent senior
unsecured bondholder. The same no-default comparison in every prompt makes lost
subsidiary equity distributions measurable without implying parent debt liability.

```sh
uv sync --locked
uv run python -m parallax.paired --all
uv run --env-file .env python -m parallax.paired --evaluate --output results/subsidiary-pair-live.json
uv run python -m unittest discover -s tests -v
```

The preview contains four answer-free API payloads. Live output uses the same
separation of model-generated claims and local deterministic references as the
original evaluation. The paired module reuses the existing Meta client and atomic
checkpoint writer; no dependencies, models or generalized evaluation framework
were added. Existing Harbor commands and saved results remain unchanged. Use a new
output filename when repeating a live run.

The first paired run completed all four requests. See the
[unaltered responses](results/subsidiary-pair-live.json) and
[short manual evaluation](results/subsidiary-pair-review.md). Calculated outcomes
match the references across both structures and investor perspectives. The review
separates numerical, legal-structure and investor-perspective findings, including
a wording caveat and citation errors. All 22 tests pass.

## First real-world evaluation: NVIDIA PORTS

One historical financing arrangement from Alexander F. Wagner's
[*Leverage Beyond Debt: Evidence from the AI Build-Out (data)*](https://github.com/alex-wagner-research/leverage-beyond-debt)
(2026, v1.1) has been evaluated: NVIDIA's PORTS residual-value guaranties. The
[case documentation](cases/real_world/README.md) records the pinned dataset revision,
primary SEC disclosures, source preparation, annotation separation, attribution,
adaptations and [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.
The information cutoff is August 26, 2026, rather than a claim about current status.

```sh
uv run python -m parallax.real_world --preview
uv run --env-file .env python -m parallax.real_world --evaluate --output results/nvidia-ports-repeat.json
uv run python -m unittest discover -s tests -v
```

The command makes one request assessing both NVIDIA equity and senior unsecured
creditors using curated summaries prepared from SEC disclosures, rather than raw filings.
Wagner's coded conclusions are kept in a separate, attributed comparison file and
never sent to the model. The [unaltered live response](results/nvidia-ports-live.json)
and [manual evaluation](results/nvidia-ports-review.md) record broad agreement on
the contractual structure, supported investor-specific reasoning, an unsupported
fee inference, and legal-label/citation caveats. No quantitative risk ground truth
was invented. All 29 tests pass. Existing examples and UI are unchanged; this adds
no general ingestion, retrieval system, dependency or UI feature.

### Independent investor prompts on the same disclosure

The investor-conditional PORTS experiment reuses the exact existing source pack
and August 26, 2026 cutoff. It sends two separate conversations, changing only the
investor phrase in the developer instruction: NVIDIA equity investor or NVIDIA
senior unsecured creditor. All other instructions, evidence text and API parameters
are identical. Neither conversation sees the combined-perspective answer, research
annotations or review conclusions. Different outcomes are not required.

```sh
uv run python -m parallax.real_world --preview --investor-pair
uv run --env-file .env python -m parallax.real_world --evaluate --investor-pair --output results/nvidia-ports-investor-pair-repeat.json
```

Each live run makes exactly two requests without retries and saves the original
payloads and provider responses together, with the unchanged source-pack hash.
The new output path must not exist; failures/incomplete responses are checkpointed.
Omitting `--investor-pair` retains the original combined-perspective command.

The [two unaltered live responses](results/nvidia-ports-investor-pair-live.json)
and [comparative review](results/nvidia-ports-investor-pair-review.md) preserve the
contractual facts while documenting justified changes in investor priorities,
unsupported cost/accounting assumptions, missing information and citation errors.
The original combined result is unchanged. All 33 tests pass, including exact
evidence equality and a check that only the investor phrase changes between prompts.

## Small real-world benchmark registry

The lightweight registry now supports **three arrangements**: the existing NVIDIA
PORTS guaranties, Meta's contingent cloud-capacity purchase and CoreWeave's refundable
capacity deposit reclassified as debt. Streamlit is unchanged. See the
[method, case provenance and limitations](docs/benchmark.md),
[human-review Markdown template](docs/review-template.md), and
[pilot findings](results/benchmark-review.md).

```sh
uv sync --locked
uv run python -m parallax.benchmark list
uv run python -m parallax.benchmark preview nvidia-ports --perspective equity_holder
uv run python -m parallax.benchmark preview meta-capacity
uv run --env-file .env python -m parallax.benchmark run meta-capacity --output results/meta-new-run.json
uv run --env-file .env python -m parallax.benchmark run coreweave-deposit --output results/coreweave-new-run.json
uv run python -m parallax.benchmark assess-template meta-capacity --run results/meta-new-run.json --output assessments/meta-new-review.json
uv run python -m parallax.benchmark summary assessments/meta-capacity.json assessments/coreweave-deposit.json
uv run python -m unittest discover -s tests -v
```

Listing, previews and review commands work without a key. Each `run` attempts two
independent investor requests, changing only the investor instruction; failures and
incomplete outputs remain recorded. Output paths must be new. Exact requests and
provider responses, source versions/hashes, Git/working-draft metadata and times
are saved. NVIDIA's existing commands, prompts and results remain compatible.

Primary evidence, reference facts and Wagner research annotations are separate
files. Only the curated primary-disclosure summaries enter prompts. Automated checks cover bytes, protocol
structure, completion statuses and recognized catalog identifiers; they do **not**
grade narrative extraction, citation support, legal reasoning or economic judgment.
Recorded assessments are explicitly assistant drafts awaiting human review.
Missing/unscorable fields are explicit; no artificial accuracy scores are assigned.
The [generated comparison](results/benchmark-comparison.md) is reproducible from
the two assessment JSON files; it summarizes recorded verdicts, not automatic truth.

Four new live requests completed successfully. Core extraction mostly preserves
source facts, with cost/benefit, classification and settlement-reasoning concerns
documented in the pilot review. No quantitative loss/recovery ground truth, new
dependencies, retrieval or ingestion infrastructure were added. Dataset attribution
is Alexander F. Wagner, *Leverage Beyond Debt: Evidence from the AI Build-Out (data)*,
2026 v1.1, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); pinned provenance,
adaptation notices and the unchanged license/disclaimer are linked in the method.
All **41 tests pass**, including legacy NVIDIA/Streamlit regressions and the new
registry, evidence-isolation, checkpointing and assessment-rendering checks.

## Preregistered prompt-guidance ablation

The [separate preregistered protocol](protocols/guidance-ablation-v1.md) and
[machine-readable snapshot](protocols/guidance-ablation-v1.json) define a new
3-case × 2-investor × 2-condition matrix, one sample per cell. Guided requests are
exactly the existing investor-specific prompts. Neutral replaces only the developer
instruction with a short standardized analysis request; evidence, cutoffs, model
and API parameters are unchanged. Historical guided responses are supplementary,
not substitutes for the twelve new calls.

```sh
uv run python -m parallax.ablation plan
uv run --env-file .env python -m parallax.ablation run --protocol protocols/guidance-ablation-v1.json --output results/ablation-new-run.json
uv run python -m parallax.ablation blind --run results/ablation-new-run.json --directory reviews/new-package --mapping results/new-condition-map.json
uv run python -m parallax.ablation reveal --directory reviews/new-package --assessment assessments/new-recorded-review.json --mapping results/new-condition-map.json --output results/new-revealed-review.json
```

All output paths must be new. `run` checks committed protocol/narrative bytes,
request hashes and source versions before any call, checkpoints every attempt,
and never retries automatically. Each run makes twelve calls at the default single
sample count. `--samples` supports future repetitions, but a different count needs
a new matching committed preregistration; no extra repetitions belong to this pilot.
`preregister --narrative PATH --output PATH` creates the JSON snapshot for a new
protocol before it is committed. Preview/planning/review commands need no key.

Give a future reviewer **only** the generated review directory. It contains shuffled
original answer text, anonymized arm labels, company/investor context, evidence,
reference facts and a blank assessment template. Keep raw runs, prompts, protocol,
mapping, historical answers and outcome reports outside that reviewer's materials.
The private controller mapping records its random seed separately. Copy and fill
the JSON template, recording all category rationales and case/arm consistency
assessments before `reveal`; the gate cannot prove actual reviewer blinding.

The source packs are curated and already contain explanatory cues. This ablation
tests developer-guidance removal conditional on those packs, not unaided SEC-filing
extraction. Assistant-written preliminary assessments are not independent blinded
human ratings. No aggregate accuracy percentage or statistical significance is
warranted by one sample per condition. Streamlit, prior evidence/results and
dependencies remain unchanged.

The first ablation run is complete: **12/12 new responses**, one per cell, no retries.
See the [preliminary assistant comparison](results/guidance-ablation-v1-preliminary-review.md),
[unchanged request/provider records](results/guidance-ablation-v1-live.json),
[anonymized reviewer package](reviews/guidance-ablation-v1/review.md) and
[recorded assistant assessments](assessments/guidance-ablation-v1-preliminary.json).
The reveal file binds the assessment bytes to the package and separate mapping;
it is researcher material, not part of the masked review package. All **47 tests
pass**. Basic mechanism extraction survived neutral prompting; unsupported creditor
priority/funding inferences appear more sensitive to guidance in this single sample.
Guided answers still contain overconfidence and an unsupported profit-share offset.
These are preliminary qualitative observations, not independent human ratings or
statistical findings.
