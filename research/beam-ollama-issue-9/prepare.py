"""Print the frozen Beam request grid without making network calls."""
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "skill-principle-pilot"
sys.path.insert(0, str(SOURCE))
from run import build_requests, encode


def build_grid():
    original = build_requests()
    return {
        "source_freeze_sha256": original["freeze_sha256"],
        "endpoint": "http://127.0.0.1:11434/api/chat",
        "timeout_seconds": original["timeout_seconds"],
        "requests": [
            {
                "case": item["case"],
                "arm": item["arm"],
                "payload": {
                    "model": "beam:cloud",
                    "stream": False,
                    "messages": item["payload"]["messages"],
                },
            }
            for item in original["requests"]
        ],
    }


def main():
    freeze = json.loads((ROOT / "freeze.json").read_bytes())
    if sha256((SOURCE / "freeze.json").read_bytes()).hexdigest() != freeze["source_freeze_sha256"]:
        raise SystemExit("Original freeze manifest changed")
    grid = encode(build_grid())
    if sha256(grid).hexdigest() != freeze["grid_sha256"]:
        raise SystemExit("Beam request grid changed")
    sys.stdout.buffer.write(grid)


if __name__ == "__main__":
    main()
