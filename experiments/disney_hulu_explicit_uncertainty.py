"""Issue #3: one request derived from the saved historical Parallax request.

Run: uv run --env-file .env python experiments/disney_hulu_explicit_uncertainty.py
No retries; an existing output (including a failed attempt) prevents another call.
"""
import copy
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from disney_hulu_baseten_ab import URL, load_excerpts

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "results/disney-hulu-baseten-ab-20261105-low-8192.json"
EVIDENCE = ROOT / "research/disney-hulu-baseten-evidence.json"
OUTPUT = ROOT / "results/disney-hulu-baseten-explicit-uncertainty-20261105.json"
APPEND = (
    "When the supplied evidence does not establish an obligation's amount, payment "
    "trigger, timing, recourse, accounting treatment, or stakeholder consequence, "
    "explicitly mark that information as unknown. Do not infer missing information "
    "merely to complete the structure. Label conditional economic interpretations "
    "as inferences and state their assumptions."
)


def main():
    history = json.loads(HISTORY.read_text())
    original = history["results"]["parallax"]["request"]
    excerpts = load_excerpts(EVIDENCE)
    assert len(excerpts) == 7 and excerpts == history["evidence"]
    assert original["messages"][1]["content"].endswith(json.dumps(excerpts))
    assert original["model"] == "meta-models/muse-spark-open-1026"
    assert original["reasoning_effort"] == "low"
    assert original["max_completion_tokens"] == 8192
    payload = copy.deepcopy(original)
    payload["messages"][0]["content"] += "\n\n" + APPEND
    key = os.environ.get("BASETEN_API_KEY", "").strip()
    if not key:
        raise SystemExit("Missing BASETEN_API_KEY; no request made")
    record = {
        "condition": "parallax_explicit_uncertainty",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "historical_comparator": str(HISTORY.relative_to(ROOT)),
        "input_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (HISTORY, EVIDENCE)},
        "appended_instruction": APPEND,
        "request": payload,
        "status": "attempt_reserved",
    }
    # Reserve before any network activity. Never overwrite or retry an attempt.
    with OUTPUT.open("x", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
        f.write("\n")
    try:
        request = Request(URL, data=json.dumps(payload).encode(), method="POST",
                          headers={"Authorization": f"Bearer {key}",
                                   "Content-Type": "application/json"})
        with urlopen(request, timeout=120) as response:
            raw = json.load(response)
        record["raw_response"] = raw
        choice = raw["choices"][0]
        content = choice["message"]["content"]
        record["status"] = ("complete" if choice["finish_reason"] == "stop"
                            and isinstance(content, str) and content.strip() else "failed_completion")
    except HTTPError as exc:
        record.update(status="failed", error=f"HTTP {exc.code}; no retry")
    except Exception as exc:
        # Avoid provider error bodies or exception messages containing credentials.
        record.update(status="failed", error=f"{type(exc).__name__}; no retry")
    record["finished_at"] = datetime.now(timezone.utc).isoformat()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"{record['status']}: {OUTPUT}")


if __name__ == "__main__":
    main()
