import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from parallax import ablation as a
from parallax import benchmark as b
from parallax.model_api import ModelAPIError


NARRATIVE = b.ROOT / "protocols/guidance-ablation-v1.md"


def response(text="Test answer", finish="stop"):
    return {"choices": [{"message": {"content": text}, "finish_reason": finish}], "usage": {"total_tokens": 99}}


class AblationTests(unittest.TestCase):
    def test_twelve_cells_preserve_guided_prompts_and_every_noninstruction_byte(self):
        cells = a.matrix()
        self.assertEqual(len(cells), 12)
        self.assertEqual(len({item["cell_id"] for item in cells}), 12)
        for case in a.CASES:
            for investor in b.INVESTORS:
                guided = a.request_for(case, investor, "guided")
                neutral = a.request_for(case, investor, "neutral")
                self.assertEqual(guided, b.request_for(case, investor))
                self.assertEqual(guided["messages"][1], neutral["messages"][1])
                neutral_text = neutral["messages"][0]["content"]
                for prohibited in ("contingent", "double counting", "ranking", "cap", "expected loss"):
                    self.assertNotIn(prohibited, neutral_text.lower())
                neutral["messages"][0]["content"] = guided["messages"][0]["content"]
                self.assertEqual(guided, neutral)
        with self.assertRaises(ValueError):
            a.request_for("nvidia-ports", "equity_holder", "unknown")

    def test_schedule_replays_and_supports_future_samples_without_executing_them(self):
        self.assertEqual(a.matrix(), a.matrix())
        future = a.matrix(samples=2)
        self.assertEqual(len(future), 24)
        self.assertEqual({item["sample"] for item in future}, {1, 2})
        with self.assertRaises(ValueError):
            a.matrix(samples=0)

    def test_protocol_pins_requests_evidence_and_sample_count(self):
        with tempfile.TemporaryDirectory(dir=b.ROOT) as directory:
            path = Path(directory) / "protocol.json"
            protocol = a.preregistration(NARRATIVE)
            b.write_new(path, protocol)
            with patch("parallax.ablation.require_committed"):
                self.assertEqual(a.validate_protocol(path, 1), protocol)
                with self.assertRaisesRegex(ValueError, "Sample count"):
                    a.validate_protocol(path, 2)
                protocol["cells"][0]["developer_instruction"] += " drift"
                path.write_text(json.dumps(protocol))
                with self.assertRaisesRegex(ValueError, "Protocol drift"):
                    a.validate_protocol(path, 1)
            with self.assertRaises(subprocess.CalledProcessError):
                a.require_committed(path)

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch("parallax.ablation.require_committed")
    @patch("parallax.ablation.chat_completion")
    def test_twelve_independent_calls_retain_failures_incompletes_and_checkpoint(self, chat, committed):
        chat.side_effect = [ModelAPIError("HTTP 429"), response("Partial", "length")] + [response(str(i)) for i in range(10)]
        with tempfile.TemporaryDirectory(dir=b.ROOT) as directory:
            protocol = Path(directory) / "protocol.json"
            output = Path(directory) / "run.json"
            b.write_new(protocol, a.preregistration(NARRATIVE))
            run = a.run(protocol, output)
            self.assertEqual(chat.call_count, 12)
            self.assertEqual([item["status"] for item in run["evaluations"][:2]], ["error", "incomplete"])
            self.assertEqual(b.read_json(output), run)
            self.assertNotIn("test-secret", output.read_text())
            for index, item in enumerate(run["evaluations"]):
                self.assertEqual(chat.call_args_list[index].args, (item["request"], "test-secret"))
                self.assertEqual(len(item["request"]["messages"]), 2)
            with self.assertRaises(FileExistsError):
                a.run(protocol, output)
            self.assertEqual(chat.call_count, 12)

    def mock_run(self, path):
        cells = a.matrix()
        run = {"ablation_schema_version": 1, "protocol_snapshot": a.preregistration(NARRATIVE),
               "evaluations": [{**item, "status": "completed", "model_generated": response(f"Original text {index}")}
                               for index, item in enumerate(cells)]}
        b.write_new(path, run)
        return run

    def test_blind_package_randomizes_and_separates_prompt_mapping_and_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            run_path = directory / "run.json"
            run = self.mock_run(run_path)
            review, mapping = directory / "review", directory / "map.json"
            package = a.blind_package(run_path, review, mapping, seed=77)
            text = (review / "review.json").read_text()
            for hidden in ('"condition":', '"request":', '"usage":', '"submitted_at":', '"run_file":'):
                self.assertNotIn(hidden, text)
            self.assertEqual(len(package["answers"]), 12)
            self.assertEqual({item["arm"] for item in package["answers"]}, {"Arm X", "Arm Y"})
            assignments = b.read_json(mapping)["assignments"]
            self.assertNotEqual([assignments[item["review_id"]]["cell_id"] for item in package["answers"]],
                                [item["cell_id"] for item in run["evaluations"]])
            source_text = {item["cell_id"]: a.response_text(item) for item in run["evaluations"]}
            for item in package["answers"]:
                self.assertEqual(item["answer"], source_text[assignments[item["review_id"]]["cell_id"]])
            again = a.blind_package(run_path, directory / "review-again", directory / "map-again.json", seed=77)
            self.assertEqual(package, again)
            with self.assertRaises(FileExistsError):
                a.blind_package(run_path, review, mapping)
            with self.assertRaises(ValueError):
                a.blind_package(run_path, directory / "unsafe", directory / "unsafe/map.json")

    def test_reveal_requires_recorded_rationales_and_binds_assessment_before_unmasking(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            run_path = directory / "run.json"
            self.mock_run(run_path)
            review, mapping = directory / "review", directory / "map.json"
            a.blind_package(run_path, review, mapping, seed=77)
            assessment = b.read_json(review / "assessment-template.json")
            assessed, revealed = directory / "assessed.json", directory / "revealed.json"
            b.write_new(assessed, assessment)
            with self.assertRaises(ValueError):
                a.reveal(review, assessed, mapping, revealed)
            assessment.update(reviewer="Synthetic unit-test reviewer", review_type="assistant_not_blinded")
            records = list(assessment["pair_consistency"])
            for item in assessment["answers"]:
                for group in ("objective", "judgment"):
                    records += list(item[group].values())
            for record in records:
                record.update(status="unscorable", notes="Unit test only; not a financial judgment")
            assessed.write_text(json.dumps(assessment))
            result = a.reveal(review, assessed, mapping, revealed)
            self.assertEqual(result["assessment_sha256"], b.digest(assessed))
            self.assertEqual({item["condition"] for item in result["answers"]}, {"guided", "neutral"})
            self.assertEqual(len(result["answers"]), 12)
            with self.assertRaises(FileExistsError):
                a.reveal(review, assessed, mapping, revealed)
