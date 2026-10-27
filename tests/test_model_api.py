from copy import deepcopy
from io import BytesIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from parallax.cli import load_case, main
from parallax.evaluate import run_evaluations
from parallax.model_api import ENDPOINT, MODEL, ModelAPIError, build_request, chat_completion


def completion(text="Unverified model analysis", finish_reason="stop"):
    return {
        "id": "mock-completion",
        "model": MODEL,
        "choices": [{"message": {"role": "assistant", "content": text}, "finish_reason": finish_reason}],
        "usage": {"total_tokens": 42},
    }


class ModelAPITests(unittest.TestCase):
    def setUp(self):
        self.case = load_case()

    def test_live_requests_exclude_answers_and_other_scenario(self):
        self.case["deterministic_reference"] = {"answer": "SECRET_REFERENCE"}
        self.case["scenarios"]["stress"]["assumption"] = "SECRET_CONCLUSION"
        self.case["perspectives"]["senior_unsecured_creditor"] = "SECRET_PERSPECTIVE_HINT"
        original = deepcopy(self.case)
        for perspective in ("equity_holder", "senior_unsecured_creditor"):
            for scenario in ("base", "stress"):
                request = build_request(self.case, perspective, scenario)
                serialized = json.dumps(request)
                for excluded in ("SECRET_", "deterministic_reference", "79.655172", "75.862069"):
                    self.assertNotIn(excluded, serialized)
                inputs = json.loads(request["messages"][1]["content"])
                self.assertEqual(inputs["perspective"], perspective)
                self.assertEqual(inputs["scenario"], scenario)
                self.assertNotIn("scenarios", inputs["evidence"])
                self.assertEqual(inputs["evidence"]["scenario"]["distributable_cash"], self.case["scenarios"][scenario]["distributable_cash"])
                self.assertEqual(inputs["evidence"]["reported_debt"], self.case["reported_debt"])
        self.assertEqual(self.case, original)

    @patch("parallax.model_api.urlopen")
    def test_documented_http_request_and_verbatim_response(self, urlopen):
        response = completion("Even an incorrect calculation must remain unchanged: 2+2=5.")
        urlopen.return_value.__enter__.return_value.read.return_value = json.dumps(response).encode()
        payload = build_request(self.case, "equity_holder", "base")
        self.assertEqual(chat_completion(payload, "test-secret"), response)
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, ENDPOINT)
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
        self.assertEqual(request.get_header("Content-type"), "application/json")
        self.assertEqual(json.loads(request.data), payload)
        self.assertNotIn("test-secret", request.data.decode())
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 60)

    @patch("parallax.model_api.urlopen")
    def test_http_connection_and_malformed_response_errors(self, urlopen):
        errors = (
            HTTPError(ENDPOINT, 401, "Unauthorized", {}, BytesIO(b"sensitive error body")),
            URLError("sensitive transport detail"),
            TimeoutError(),
        )
        for error in errors:
            urlopen.side_effect = error
            with self.assertRaises(ModelAPIError) as caught:
                chat_completion({}, "test-secret")
            self.assertNotIn("sensitive", str(caught.exception))
            self.assertNotIn("test-secret", str(caught.exception))
        urlopen.side_effect = None
        for body in (b"not json", b"{}", b'{"choices": []}', json.dumps(completion(None)).encode()):
            urlopen.return_value.__enter__.return_value.read.return_value = body
            with self.assertRaises(ModelAPIError):
                chat_completion({}, "test-secret")

    @patch.dict("os.environ", {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.model_api.urlopen")
    def test_four_calls_saved_separately_from_local_references(self, urlopen):
        responses = [completion(f"Original answer {index}") for index in range(4)]
        handles = []
        for response in responses:
            handle = Mock()
            handle.__enter__ = Mock(return_value=handle)
            handle.__exit__ = Mock(return_value=False)
            handle.read.return_value = json.dumps(response).encode()
            handles.append(handle)
        urlopen.side_effect = handles
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "responses.json"
            report = run_evaluations(self.case, path)
            saved = path.read_text()
            self.assertEqual(json.loads(saved), report)
            self.assertNotIn("test-secret", saved)
            self.assertEqual(urlopen.call_count, 4)
            self.assertEqual(len({item["task_id"] for item in report["evaluations"]}), 4)
            for index, item in enumerate(report["evaluations"]):
                self.assertEqual(item["status"], "completed")
                self.assertEqual(item["model_generated"], responses[index])
                self.assertFalse(item["deterministic_reference"]["sent_to_model"])
                self.assertNotIn("deterministic_reference", item["request"])
            with self.assertRaises(FileExistsError):
                run_evaluations(self.case, path)
            self.assertEqual(urlopen.call_count, 4)

    @patch.dict("os.environ", {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.evaluate.chat_completion")
    def test_failures_and_incomplete_answers_preserve_checkpoints(self, chat):
        def fail_after_checkpoint(*args):
            saved = json.loads(path.read_text())
            self.assertEqual(saved["evaluations"][0]["status"], "completed")
            self.assertEqual(saved["evaluations"][1]["status"], "in_progress")
            raise ModelAPIError("Meta Model API returned HTTP 429")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "responses.json"
            chat.side_effect = [completion(), fail_after_checkpoint, completion("Partial answer", "length"), completion()]
            # Mock side_effect lists return callables; use a dispatcher to execute the checkpoint check.
            outcomes = iter(chat.side_effect)
            def dispatch(*args):
                outcome = next(outcomes)
                return outcome(*args) if callable(outcome) else outcome
            chat.side_effect = dispatch
            report = run_evaluations(self.case, path)
            self.assertEqual([item["status"] for item in report["evaluations"]], ["completed", "error", "incomplete", "completed"])
            self.assertEqual(json.loads(path.read_text()), report)
            self.assertEqual(report["evaluations"][2]["model_generated"]["choices"][0]["message"]["content"], "Partial answer")

    @patch.dict("os.environ", {}, clear=True)
    @patch("parallax.evaluate.chat_completion")
    def test_missing_key_fails_before_output_or_network(self, chat):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "responses.json"
            with self.assertRaisesRegex(ModelAPIError, "MODEL_API_KEY"):
                run_evaluations(self.case, path)
            self.assertFalse(path.exists())
            chat.assert_not_called()

    @patch("parallax.evaluate.run_evaluations")
    def test_cli_evaluation_and_failure_exit(self, run):
        run.return_value = {"evaluations": [{"status": "completed"}] * 4}
        main(["--evaluate", "--output", "unused.json"])
        self.assertEqual(run.call_args.args[1], Path("unused.json"))
        run.return_value = {"evaluations": [{"status": "error"}] * 4}
        with self.assertRaises(SystemExit) as caught:
            main(["--evaluate", "--output", "unused.json"])
        self.assertEqual(caught.exception.code, 1)
        for args in (["--evaluate"], ["--evaluate", "--all", "--output", "unused.json"], ["--output", "unused.json"]):
            with self.assertRaises(SystemExit) as caught:
                main(args)
            self.assertEqual(caught.exception.code, 2)
