"""Execute only the pre-frozen ten-slot v1B plan once. No retries or resume."""
from copy import deepcopy
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
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
PLAN = ROOT / "protocols/scientific-validation-v1b/plan.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    if (HERE / "raw.json").exists():
        raise SystemExit("Existing v1B run: no retry or automatic resumption")
    plan = json.loads(PLAN.read_text())
    spec = importlib.util.spec_from_file_location("v1b_preparation", PLAN.parent / "prepare.py")
    prepare = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prepare)
    assert plan == prepare.plan(), "Frozen v1B plan drift"
    assert len(plan["evaluations"]) == 10
    assert api.MODEL == plan["requested_model"] == "muse-spark-1.3"
    assert api.ENDPOINT == plan["endpoint"]
    for path, expected in {**plan["files_sha256"], **plan["historical_v1_files_sha256"]}.items():
        assert digest(ROOT / path) == expected, path
    source = "process environment"
    if not os.environ.get("MODEL_API_KEY", "").strip():
        source = "ignored local .env"
        for line in (ROOT / ".env").read_text().splitlines():
            if line.strip().startswith("MODEL_API_KEY="):
                os.environ["MODEL_API_KEY"] = line.split("=", 1)[1].strip().strip("\"'")
                break
    key = api.get_api_key()
    report = {"experiment": "scientific-validation-v1B", "started_at_utc": now(),
              "finished_at_utc": None, "planned_slots": 10, "attempted_slots": 0,
              "git_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "working_tree_status_before_run": subprocess.check_output(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT, text=True),
              "python_version": sys.version, "runner_sha256": digest(__file__),
              "plan_sha256": digest(PLAN), "plan_snapshot": plan,
              "authentication_available": True, "authentication_source": source,
              "reference_status": "all five provisional/pending; no external human certification",
              "evaluations": deepcopy(plan["evaluations"]),
              "automatic_retries": 0, "redirects_followed": 0, "stopping_reason": None}
    write_new(HERE / "raw.json", report)

    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = build_opener(NoRedirect())
    active = None

    def observed_open(request, timeout):
        active["http_attempts"] += 1
        assert request.data.decode() == active["wire_request_utf8"], "Wire request drift"
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
        item.update(status="in_progress", http_status=None, http_attempts=0, submitted_at_utc=now())
        save_report(HERE / "raw.json", report)
        print(f"Submitting {index}/10: {item['run_id']}", flush=True)
        response = None
        try:
            response = api.chat_completion(json.loads(item["wire_request_utf8"]), key)
            item["status"] = "completed" if response["choices"][0]["finish_reason"] == "stop" else "incomplete"
        except api.ModelAPIError as exc:
            response = exc.response
            item.update(status="error", error=str(exc))
            if response and response.get("choices") and response["choices"][0].get("finish_reason") != "stop":
                item["status"] = "incomplete"
        if response and key in json.dumps(response):
            response = None
            item.update(status="error", error="Credential unexpectedly present in response; body not persisted")
            report["stopping_reason"] = "Credential protection stop"
        item["raw_provider_response"] = response
        if response:
            item["provider_response_id"] = response.get("id")
            item["returned_model_version"] = response.get("model")
            item["usage"] = response.get("usage")
            choices = response.get("choices") or []
            item["finish_reason"] = choices[0].get("finish_reason") if choices else None
        item["finished_at_utc"] = now()
        if item.get("http_status") in (400, 401, 403, 429):
            report["stopping_reason"] = f"HTTP {item['http_status']}; settings/authentication/quota stop, no retry"
        if item.get("returned_model_version") not in (None, api.MODEL):
            report["stopping_reason"] = "Returned model drift"
        report["attempted_slots"] = sum(c.get("http_attempts", 0) for c in report["evaluations"])
        save_report(HERE / "raw.json", report)
        print(f"Finished {index}/10: {item['status']}; HTTP {item.get('http_status')}; {item.get('finish_reason')}", flush=True)
        if report["stopping_reason"]:
            break
    report["finished_at_utc"] = now()
    report["protected_hashes_match_after_execution"] = all(digest(ROOT / p) == h for p, h in {**plan["files_sha256"], **plan["historical_v1_files_sha256"]}.items()) and all(digest(ROOT / s["evidence_file"]) == s["sha256"] for s in plan["source_versions"].values())
    save_report(HERE / "raw.json", report)
    print(json.dumps({"attempted_slots": report["attempted_slots"], "stopping_reason": report["stopping_reason"], "protected_hashes_match": report["protected_hashes_match_after_execution"]}), flush=True)


if __name__ == "__main__":
    main()
