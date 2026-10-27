"""Minimal Meta chat-completions client and answer-free prompt construction."""

from copy import deepcopy
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .cli import PERSPECTIVES, SCENARIOS


ENDPOINT = "https://api.meta.ai/v1/chat/completions"
MODEL = "muse-spark-1.3"


class ModelAPIError(RuntimeError):
    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response


def build_request(case, perspective, scenario):
    """Allowlist contractual inputs; never consume prepare_task or its answers."""
    if perspective not in PERSPECTIVES or scenario not in SCENARIOS:
        raise ValueError("Unknown perspective or scenario")
    evidence = {key: deepcopy(case[key]) for key in (
        "case_id", "company", "provenance", "currency", "amount_unit",
        "valuation_date", "settlement_date", "reported_debt",
        "contingent_guarantee", "assumptions", "reference_facts",
    )}
    # Scenario prose includes a precomputed shortfall. Send only raw scenario inputs.
    evidence["scenario"] = {
        key: case["scenarios"][scenario][key] for key in (
            "distributable_cash", "distributor_default", "covered_debt_due", "lender_recoveries",
        )
    }
    return {
        "model": MODEL,
        "max_completion_tokens": 8192,
        "messages": [
            {
                "role": "developer",
                "content": (
                    "Analyze the supplied synthetic company from the selected investor's "
                    "perspective in the selected economic scenario. Identify relevant "
                    "obligations and explain their economic consequences for that investor. "
                    "Show the necessary calculations, units, denominators and settlement "
                    "cash flows. Also consider the same scenario without the guarantee. "
                    "Disclose uncertainties and missing information. Use only the supplied "
                    "facts and contractual assumptions; cite evidence field paths or "
                    "reference fact IDs. Do not invent external company facts. Provide "
                    "a concise analysis with calculations and limitations."
                ),
            },
            {
                "role": "user",
                "content": json.dumps({
                    "perspective": perspective,
                    "investor": ("Holder of the company's common equity" if perspective == "equity_holder"
                                 else "Holder of the company's entire senior unsecured bond"),
                    "scenario": scenario,
                    "evidence": evidence,
                }, sort_keys=True),
            },
        ],
    }


def get_api_key():
    key = os.environ.get("MODEL_API_KEY", "").strip()
    if not key or key == "replace-with-your-meta-model-api-key":
        raise ModelAPIError("Set MODEL_API_KEY before running live evaluations")
    return key


def chat_completion(payload, api_key):
    """Single non-streaming request, no retries; preserve the provider response."""
    request = Request(
        ENDPOINT,
        data=json.dumps(payload, allow_nan=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            raw = response.read()
    except HTTPError as exc:
        # Do not log request headers or arbitrary server error bodies containing credentials.
        exc.close()
        raise ModelAPIError(f"Meta Model API returned HTTP {exc.code}") from None
    except (URLError, TimeoutError, OSError):
        raise ModelAPIError("Meta Model API connection failed or timed out") from None
    try:
        result = json.loads(raw)
    except (ValueError, UnicodeError):
        raise ModelAPIError("Meta Model API returned invalid JSON") from None
    try:
        choice = result["choices"][0]
        content = choice["message"]["content"]
        finish_reason = choice["finish_reason"]
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Missing text")
        if not isinstance(finish_reason, str):
            raise ValueError("Missing finish reason")
    except (KeyError, IndexError, TypeError, ValueError):
        raise ModelAPIError("Meta Model API response has no valid text completion", result) from None
    return result
