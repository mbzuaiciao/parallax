"""Single-case Baseten A/B test. Requires independently sourced SEC excerpts.

Input JSON: {"excerpts":[{"source":"SEC filing URL","locator":"Item/Note","text":"verbatim passage"}]}
Run: BASETEN_API_KEY=... python experiments/disney_hulu_baseten_ab.py --evidence evidence.json --output result.json
"""
import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

URL = "https://inference.baseten.co/v1/chat/completions"
MODEL = "meta-models/muse-spark-open-1026"
QUESTION = (
    "Using only these excerpts, analyze Disney's contractual obligations related to Hulu. "
    "Explain payment conditions, timing, consequences for common equity and senior "
    "unsecured creditors, and what cannot be concluded. Cite excerpt IDs; do not invent facts."
)
PROMPTS = {
    "baseline": "Analyze SEC disclosure evidence accurately. Cite excerpt IDs and note uncertainty.",
    "parallax": (
        "Construct an obligation map: obligor, beneficiary, amount/formula, trigger, "
        "timing, recourse, evidence IDs, and unknowns. Separate disclosed facts, "
        "conditional interpretation, and unsupported conclusions. Then analyze "
        "equity-holder versus senior unsecured creditor exposure. Do not assume "
        "that a contractual commitment is recognized debt or double-count amounts."
    ),
}


def load_excerpts(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    excerpts = data.get("excerpts")
    if not isinstance(excerpts, list) or not excerpts:
        raise ValueError("Evidence must have a nonempty 'excerpts' list")
    result = []
    for i, excerpt in enumerate(excerpts, 1):
        if not isinstance(excerpt, dict) or any(
            not isinstance(excerpt.get(k), str) or not excerpt[k].strip()
            for k in ("source", "locator", "text")
        ):
            raise ValueError(f"Excerpt {i} requires source, locator and text")
        result.append({**{k: excerpt[k] for k in ("source", "locator", "text")}, "id": f"E{i}"})
    return result


def run_call(key, condition, excerpts):
    payload = {
        "model": MODEL,
        "max_completion_tokens": 4096,
        "messages": [
            {"role": "system", "content": PROMPTS[condition]},
            {"role": "user", "content": QUESTION + "\n\n" + json.dumps(excerpts)},
        ],
    }
    request = Request(
        URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=120) as response:
            result = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Baseten HTTP {exc.code} on {condition}") from None
    except (URLError, TimeoutError, OSError):
        raise RuntimeError(f"Baseten connection failed on {condition}") from None
    try:
        content = result["choices"][0]["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            raise ValueError
    except (KeyError, IndexError, TypeError, ValueError):
        return {"request": payload, "raw_response": result, "error": "Empty/invalid completion"}
    return {"request": payload, "raw_response": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    excerpts = load_excerpts(args.evidence)
    key = os.environ.get("BASETEN_API_KEY", "").strip()
    if not key:
        parser.error("Set BASETEN_API_KEY; no live call has been made")
    if args.output.exists():
        parser.error("Output already exists; choose another path to avoid overwriting results")
    record = {"model": MODEL, "evidence": excerpts, "results": {}}
    for condition in ("baseline", "parallax"):
        try:
            record["results"][condition] = run_call(key, condition, excerpts)
        except RuntimeError as exc:
            record["results"][condition] = {"error": str(exc)}
            args.output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            raise SystemExit(str(exc))
        args.output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Raw responses saved to {args.output}")
    print("Next: independently adjudicate factual accuracy and unsupported inferences.")


if __name__ == "__main__":
    main()
