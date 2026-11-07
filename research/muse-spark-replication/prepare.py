"""Verify and print the Muse request grid offline."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BEAM = ROOT / "research" / "beam-ollama-issue-9"
ARCHIVE = BEAM / "scientific-attempt-01"
MAX_COMPLETION_TOKENS = 8192

sys.path.insert(0, str(ROOT))
from parallax.model_api import ENDPOINT, MODEL


def build_grid():
    # The Beam CLI verifies the historical source files and its frozen grid digest.
    beam = json.loads(subprocess.check_output([sys.executable, str(BEAM / "prepare.py")]))
    schedule = [{"case": item["case"], "arm": item["arm"]} for item in beam["requests"]]
    if schedule != json.loads((ARCHIVE / "schedule.json").read_bytes()):
        raise ValueError("Frozen schedule differs from the executed Beam schedule")

    requests = []
    for index, item in enumerate(beam["requests"], start=1):
        archived = json.loads((ARCHIVE / f"{index:02d}.request.json").read_bytes())
        if item["payload"] != archived:
            raise ValueError(f"Frozen Beam payload differs from archived request {index}")
        requests.append({
            "case": item["case"],
            "arm": item["arm"],
            "payload": {
                "model": MODEL,
                "stream": False,
                "max_completion_tokens": MAX_COMPLETION_TOKENS,
                "messages": archived["messages"],
            },
        })

    return {
        "source_freeze_sha256": beam["source_freeze_sha256"],
        "endpoint": ENDPOINT,
        "method": "POST",
        "requests": requests,
    }


if __name__ == "__main__":
    print(json.dumps(build_grid(), ensure_ascii=False, indent=2))
