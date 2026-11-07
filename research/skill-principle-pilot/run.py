"""Build the frozen request grid offline, or execute once after approval."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
from http.client import HTTPException
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "experiments"))
from disney_hulu_baseten_ab import MODEL, PROMPTS, URL, load_excerpts


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def load(path):
    return json.loads(path.read_bytes())


def now():
    return datetime.now(timezone.utc).isoformat()


def build_requests():
    manifest_bytes = (ROOT / "freeze.json").read_bytes()
    for name, digest in json.loads(manifest_bytes).items():
        if sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Frozen file changed: {name}")

    design = load(ROOT / "design.json")
    if design["endpoint"] != URL or design["settings"]["model"] != MODEL:
        raise ValueError("Provider endpoint or historical model changed")
    schedule = design["schedule"]
    expected = {(case, arm) for case in ("01", "02", "03", "04") for arm in "ABC"}
    if len(schedule) != 12 or {tuple(pair) for pair in schedule} != expected:
        raise ValueError("Expected one request for every case and arm")

    original = PROMPTS["parallax"]
    sentence = design["scope_sentence"]
    if original.count(sentence) != 1:
        raise ValueError("Historical Parallax prompt has changed")
    baseline = original.replace(sentence, "")
    principle = baseline + "\n\n" + design["principle"]
    prompts = {
        "A": baseline,
        "B": principle,
        "C": principle + "\n\n" + design["positive_example"] + "\n\n" + design["boundary_example"],
    }
    requests = []
    for case_id, arm in schedule:
        path = ROOT / "cases" / f"{case_id}.json"
        case = load(path)
        question = design["question"].format(
            issuer=case["issuer"], scope=case["scope"], as_of=case["as_of"]
        )
        evidence = encode(load_excerpts(path)).decode()
        requests.append({
            "case": case_id,
            "arm": arm,
            "payload": {
                **design["settings"],
                "messages": [
                    {"role": "system", "content": prompts[arm]},
                    {"role": "user", "content": question + "\n\n" + evidence},
                ],
            },
        })
    return {
        "freeze_sha256": sha256(manifest_bytes).hexdigest(),
        "endpoint": URL,
        "timeout_seconds": design["timeout_seconds"],
        "requests": requests,
    }


def append_status(attempt, event):
    with (attempt / "status.jsonl").open("ab") as log:
        log.write((json.dumps(event, ensure_ascii=False) + "\n").encode())
        log.flush()
        os.fsync(log.fileno())


def completion_metadata(raw):
    try:
        response = json.loads(raw)
        choice, = response["choices"]
        content = choice["message"]["content"]
        finish = choice["finish_reason"]
        model = response["model"]
        usage = response["usage"]
        valid = (
            finish == "stop"
            and isinstance(content, str) and bool(content.strip())
            and isinstance(model, str) and bool(model.strip())
            and all(type(usage[name]) is int and usage[name] >= 0
                    for name in ("prompt_tokens", "completion_tokens", "total_tokens"))
        )
    except (ValueError, KeyError, TypeError, IndexError):
        return {"status": "invalid_completion"}
    return {
        "status": "complete" if valid else "invalid_completion",
        "finish_reason": finish,
        "reported_model": model,
        "usage": usage,
    }


def execute(plan, attempt, key, open_request):
    # mkdir is exclusive even if two processes choose the same path.
    attempt.mkdir(mode=0o700)
    (attempt / "plan.json").write_bytes(encode(plan))
    append_status(attempt, {"status": "started", "at": now()})
    reported_model = None
    for index, item in enumerate(plan["requests"], 1):
        payload = item["payload"]
        data = encode(payload)
        (attempt / f"{index:02d}.request.json").write_bytes(data)
        fields = {"index": index, "case": item["case"], "arm": item["arm"],
                  "requested_model": payload["model"]}
        request = Request(plan["endpoint"], data=data, method="POST", headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        })
        append_status(attempt, {**fields, "status": "sending", "at": now()})
        try:
            try:
                response = open_request(request, timeout=plan["timeout_seconds"])
            except HTTPError as error:
                response = error
            with response, (attempt / f"{index:02d}.response").open("xb") as raw_file:
                # Preserve bytes verbatim, including HTTP error bodies.
                http_status = response.code
                while chunk := response.read1(64 * 1024):
                    raw_file.write(chunk)
            if http_status == 200:
                metadata = completion_metadata((attempt / f"{index:02d}.response").read_bytes())
            else:
                metadata = {"status": "provider_error"}
            metadata["http_status"] = http_status
        except (OSError, HTTPException) as error:
            metadata = {"status": "transport_or_io_error", "error_type": type(error).__name__}
        except KeyboardInterrupt:
            append_status(attempt, {**fields, "status": "interrupted", "at": now()})
            raise
        if metadata["status"] == "complete":
            if reported_model is None:
                reported_model = metadata["reported_model"]
            elif reported_model != metadata["reported_model"]:
                metadata["status"] = "reported_model_changed"
        append_status(attempt, {**fields, **metadata, "at": now()})
        if metadata["status"] != "complete":
            append_status(attempt, {"status": "stopped", "at": now(), "index": index})
            return False
    append_status(attempt, {"status": "finished", "at": now(), "requests_completed": 12})
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--offline", action="store_true", help="print all 12 payloads without network access")
    mode.add_argument("--execute-approved", metavar="NEW_ATTEMPT_DIR", type=Path)
    args = parser.parse_args()
    try:
        plan = build_requests()
    except (OSError, ValueError, KeyError) as error:
        parser.error(str(error))
    if args.offline:
        sys.stdout.buffer.write(encode(plan))
        return 0
    key = os.environ.get("BASETEN_API_KEY", "").strip()
    if not key:
        parser.error("Set BASETEN_API_KEY in the environment")
    try:
        return 0 if execute(plan, args.execute_approved, key, build_opener(NoRedirect()).open) else 1
    except FileExistsError:
        parser.error("Attempt path already exists. Inspect existing artifacts before any further authorization.")
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
