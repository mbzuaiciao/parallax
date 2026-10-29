"""One authorized exploratory execution of the frozen plan; no retries/resumption.

Uses existing request preparation, API client and atomic checkpoint helper.
Existing raw.json or plan.json prevents a second execution. Never run to score.
"""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import HTTPError
from urllib.request import build_opener, HTTPRedirectHandler

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from parallax import model_api as api
from parallax.benchmark import digest, write_new
from parallax.evaluate import save_report

HERE = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    if (HERE / "raw.json").exists() or (HERE / "plan.json").exists():
        raise SystemExit("Existing execution artifacts: do not retry or resume automatically")
    spec = importlib.util.spec_from_file_location("frozen_preparation", ROOT / "protocols/scientific-validation-v1/prepare.py")
    prepare = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prepare)
    plan = prepare.plan()
    readiness = (ROOT / "research/scientific-validation-v1-readiness.md").read_text()
    for name, expected in re.findall(r'^\| `([^`]+)` \| `([0-9a-f]{64})` \|$', readiness, re.M):
        if digest(ROOT / name) != expected:
            raise SystemExit(f"Readiness hash drift: {name}")
    plan_stdout = (json.dumps(plan, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    if hashlib.sha256(plan_stdout).hexdigest() not in readiness:
        raise SystemExit("Frozen preparation plan drift")
    refs_path = ROOT / "protocols/scientific-validation-v1/references.json"
    refs = json.loads(refs_path.read_text())
    assert len(refs["cases"]) == 5
    assert all(r["status"] == "provisional" and r["independent_verification"]["decision"] == "pending" for r in refs["cases"])
    assert api.MODEL == plan["requested_model_version"] == "muse-spark-1.3"
    assert api.ENDPOINT == plan["endpoint"] == "https://api.meta.ai/v1/chat/completions"
    assert len(plan["evaluations"]) == len({c["run_id"] for c in plan["evaluations"]}) == 30
    for cell in plan["evaluations"]:
        assert cell["request"]["model"] == api.MODEL
        assert cell["request"]["temperature"] == 0.7
        assert cell["request"]["max_completion_tokens"] == 8192
    auth_source = "process environment"
    if not os.environ.get("MODEL_API_KEY", "").strip():
        auth_source = "ignored local .env"
        for line in (ROOT / ".env").read_text().splitlines():
            if line.strip().startswith("MODEL_API_KEY="):
                os.environ["MODEL_API_KEY"] = line.split("=", 1)[1].strip().strip("\"'")
                break
    key = api.get_api_key()
    status = subprocess.check_output(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, text=True)
    write_new(HERE / "plan.json", plan)
    report = {
        "experiment": "scientific-validation-v1", "run_kind": "exploratory_pilot",
        "started_at_utc": now(), "finished_at_utc": None,
        "authorization": "User explicitly authorized exactly the existing 30-slot pilot with provisional AI-assisted references; this supersedes independent-human-approval gating for exploratory execution only, not certification or scoring rules.",
        "independent_external_human_certification": False,
        "reference_status": "all five provisional/pending; no reference edits",
        "reference_snapshot": refs, "protocol_snapshot": (ROOT / "protocols/scientific-validation-v1/protocol.md").read_text(),
        "git_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "working_tree_status_before_output_creation": status,
        "working_tree_status_before_task": "?? research/scientific-validation-v1-api-preflight.md\n",
        "working_tree_dirty": bool(status), "python_version": sys.version,
        "authentication_available": True, "authentication_source": auth_source,
        "requested_model": api.MODEL, "endpoint": api.ENDPOINT,
        "temperature": 0.7, "max_completion_tokens": 8192,
        "other_sampling_parameters": plan["other_sampling_parameters"],
        "schedule_seed": plan["schedule_seed"], "plan_sha256": digest(HERE / "plan.json"),
        "runner_sha256": digest(__file__), "source_versions": plan["source_versions"],
        "files_sha256": plan["files_sha256"],
        "preflight_report_sha256": digest(ROOT / "research/scientific-validation-v1-api-preflight.md"),
        "evaluations": deepcopy(plan["evaluations"]),
        "stopping_reason": None, "planned_slots": 30,
        "automatic_retries": 0, "redirects_followed": 0,
    }
    write_new(HERE / "raw.json", report)

    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = build_opener(NoRedirect())
    active = None

    def observed_open(request, timeout):
        # Only called once per slot by the existing non-retrying API client.
        active["http_attempts"] += 1
        try:
            response = opener.open(request, timeout=timeout)
            active["http_status"] = response.status
            return response
        except HTTPError as exc:
            active["http_status"] = exc.code
            raise

    api.urlopen = observed_open
    for index, item in enumerate(report["evaluations"], 1):
        active = item
        item.update(status="in_progress", submitted_at_utc=now(), http_status=None, http_attempts=0)
        save_report(HERE / "raw.json", report)
        print(f"Submitting {index}/30: {item['run_id']}", flush=True)
        response = None
        try:
            response = api.chat_completion(item["request"], key)
            item["status"] = "completed" if response["choices"][0]["finish_reason"] == "stop" else "incomplete"
        except api.ModelAPIError as exc:
            response = exc.response
            item.update(status="error", error=str(exc))
            if response and response.get("choices"):
                item["status"] = "incomplete" if response["choices"][0].get("finish_reason") != "stop" else "error"
        item["raw_provider_response"] = response
        if response:
            # Preserve the provider object without rewriting response text or reasoning.
            if key in json.dumps(response):
                item["raw_provider_response"] = None
                item.update(status="error", error="Credential unexpectedly present in response; body not persisted")
                report["stopping_reason"] = "Credential protection stop"
            else:
                item["provider_response_id"] = response.get("id")
                item["returned_model_version"] = response.get("model")
                item["usage"] = response.get("usage")
                choices = response.get("choices") or []
                item["finish_reason"] = choices[0].get("finish_reason") if choices else None
        item["finished_at_utc"] = now()
        if item.get("http_status") in (400, 401, 403, 429):
            report["stopping_reason"] = f"HTTP {item['http_status']}: parameter/authentication/quota check; no change or retry"
        if item.get("returned_model_version") not in (None, api.MODEL):
            report["stopping_reason"] = "Returned model differs from frozen requested model"
        save_report(HERE / "raw.json", report)
        print(f"Finished {index}/30: {item['status']}; HTTP {item.get('http_status')}; {item.get('finish_reason')}", flush=True)
        if report["stopping_reason"]:
            break
    report["finished_at_utc"] = now()
    report["attempted_slots"] = sum(c.get("http_attempts", 0) for c in report["evaluations"])
    report["protected_hashes_match_after_execution"] = all(digest(ROOT / p) == h for p, h in plan["files_sha256"].items()) and all(digest(ROOT / s["evidence_file"]) == s["sha256"] for s in plan["source_versions"].values())
    save_report(HERE / "raw.json", report)
    print(json.dumps({"attempted_slots": report["attempted_slots"], "stopping_reason": report["stopping_reason"], "hashes_unchanged": report["protected_hashes_match_after_execution"]}), flush=True)


if __name__ == "__main__":
    main()
