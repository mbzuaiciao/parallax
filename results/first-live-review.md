# First live evaluation: manual review

Run date: October 27, 2026 (America/Los_Angeles).
Model: `muse-spark-1.3`. Endpoint: Meta chat completions.
Artifact: [first-live.json](first-live.json).

All four evaluations completed with finish reason `stop`; none required retries.
The saved provider responses are unchanged. This review is human-readable analysis
of those responses, separate from both model-generated claims and the deterministic
references. It is not an automated score or evidence of performance on other cases.

## Numerical comparison

All payments below are USD millions. Expected stress figures are rounded to six
decimal places; the model generally reports two decimal places.

| Investor / scenario | Deterministic reference | Model result | Assessment |
| --- | --- | --- | --- |
| Equity / base | Bond 105; guarantee 0; equity 45; bond recovery 100% | Bond 105; guarantee 0; equity 45; bond recovery 100% | Matches |
| Equity / stress | Bond 79.655172; guarantee 30.344828; equity 0; bond recovery 75.862069% | Bond 79.66; guarantee 30.34; equity 0; bond recovery 75.86% | Matches at reported precision |
| Senior unsecured creditor / base | Bond 105; guarantee 0; equity 45; bond recovery 100% | Bond 105; guarantee 0; equity 45; bond recovery 100% | Matches |
| Senior unsecured creditor / stress | Bond 79.655172; guarantee 30.344828; equity 0; bond recovery 75.862069% | Bond 79.66; guarantee 30.34; equity 0; bond recovery 75.86% | Matches at reported precision |

Both stress answers derive the 40 guarantee claim from 50 due minus 10 lender
recoveries, combine it with the 105 bond claim, and distribute the 110 pool
proportionally across total claims of 145. They distinguish the guarantee's
contractual claim from its actual cash payment. Both base answers correctly leave
the untriggered guarantee at zero.

All four answers also give the correct same-cash-pool counterfactual without the
guarantee: base bond 105 and equity 45; stress bond 105 and equity 5. The equity
answers emphasize the residual and stress wipeout; the creditor answers emphasize
full contractual payment in base and dilution/recovery shortfall in stress. All
acknowledge absent probabilities, discount rates and purchase prices. No material
arithmetic or settlement-allocation errors were observed in this run.

## Observed issues

The **creditor/base** answer says: “Cash cushion = 150 - 105 = 45.0 before equity
impaired and before bond impaired.” This conflates the two investors' protection.
The 45 residual absorbs reductions in cash before the bond suffers a shortfall;
equity's residual itself declines immediately as cash falls below 150. The model's
cash-flow calculations are correct, but this qualitative statement is imprecise.
The original wording remains in the saved response.

Several answers cite `evidence.investor` and `evidence.perspective`, although those
fields are at the top level of the user-message JSON (`investor` and `perspective`).
The base answers also describe `evidence.scenario` as the label `base` even though
the label is top-level `scenario` and `evidence.scenario` contains the input object.
These are citation/path errors, not numerical financial errors.

## Verification and limits

- `.env` is ignored by Git and is not tracked. uv loaded the key from that file;
  the key was never printed or placed in the report.
- Saved requests contain no `deterministic_reference`; local references explicitly
  record `sent_to_model: false`. Live prompts contain contractual distribution
  rules needed to solve the case, but no calculated reference answers.
- All 16 deterministic and mocked tests pass using
  `uv run python -m unittest discover -s tests -v`.
- This is one response per investor/scenario combination on one synthetic case.
  The correct outputs here do not establish repeatability or broader financial
  reasoning quality. No response was automatically corrected or resubmitted.
