"""Validate and execute the separately frozen Muse Spark Open revision."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "skill-principle-pilot"))
import run as original


def build_requests():
    manifest = (ROOT / "freeze.json").read_bytes()
    for name, digest in json.loads(manifest).items():
        if sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Replacement freeze mismatch: {name}")
    plan = original.build_requests()
    revision = json.loads((ROOT / "revision.json").read_bytes())
    plan["freeze_sha256"] = sha256(manifest).hexdigest()
    for request in plan["requests"]:
        request["payload"]["model"] = revision["model"]
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--offline", action="store_true")
    mode.add_argument("--execute-approved", type=Path, metavar="NEW_ATTEMPT_DIR")
    args = parser.parse_args()
    plan = build_requests()
    if args.offline:
        sys.stdout.buffer.write(original.encode(plan))
        return 0
    key = os.environ.get("BASETEN_API_KEY", "").strip()
    if not key:
        parser.error("Set BASETEN_API_KEY in the environment")
    opener = original.build_opener(original.NoRedirect())
    try:
        return 0 if original.execute(plan, args.execute_approved, key, opener.open) else 1
    except FileExistsError:
        parser.error("Attempt directory already exists")
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
