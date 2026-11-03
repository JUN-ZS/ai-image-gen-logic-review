import hashlib
import tempfile
import unittest
from pathlib import Path

from bubble_break.prompt_trial_planner import TRIAL_BY_ID, build_trial_plan, main


def evidence_for(trial_id):
    trial = TRIAL_BY_ID[trial_id]
    items = []
    for arm in ("control", "treatment"):
        for index in range(trial["replicates_per_arm"]):
            digest = hashlib.sha256(f"{trial_id}:{arm}:{index}".encode()).hexdigest()
            items.append({
                "arm": arm,
                "artifact_sha256": digest,
                "artifact_kind": "reviewed_test_fixture",
                "review_receipt": {"artifact_sha256": digest, "verdict": "PASS" if index < 2 else "FAIL"}
            })
    return {"trial_id": trial_id, "evidence": items}


class TestPromptTrialPlanner(unittest.TestCase):
    def test_default_plan_covers_image_formula_teaching_and_video_formula(self):
        result = build_trial_plan()
        self.assertEqual(result["plan_status"], "PLAN_READY")
        self.assertEqual(
            [x["trial_id"] for x in result["next_trials"]],
            ["IMG-FORMULA-01", "IMG-TEACH-01", "VIDEO-FORMULA-01"]
        )
        self.assertEqual(
            {x["family"] for x in result["next_trials"]},
            {"image_formula", "image_teaching", "video_formula"}
        )
        self.assertTrue(result["plan_only"])
        self.assertFalse(result["external_generation_called"])

    def test_invalid_or_sha_mismatched_receipts_do_not_skip_trial(self):
        entry = evidence_for("IMG-FORMULA-01")
        entry["evidence"][0]["review_receipt"]["artifact_sha256"] = "0" * 64
        result = build_trial_plan({"reviewed_trials": [entry]})
        self.assertEqual(result["next_trials"][0]["trial_id"], "IMG-FORMULA-01")
        self.assertTrue(any("SHA-mismatched" in item for item in result["ignored_history"]))

    def test_valid_evidence_for_three_initial_trials_unlocks_followups(self):
        history = {"reviewed_trials": [
            evidence_for("IMG-FORMULA-01"),
            evidence_for("IMG-TEACH-01"),
            evidence_for("VIDEO-FORMULA-01")
        ]}
        result = build_trial_plan(history, limit=3)
        self.assertEqual(
            [x["trial_id"] for x in result["next_trials"]],
            ["VIDEO-CONTINUITY-02", "VIDEO-CAUSALITY-03", "IMG-CAMERA-02"]
        )

    def test_video_filter_does_not_schedule_image_trials(self):
        result = build_trial_plan(family="video", limit=10)
        self.assertTrue(result["next_trials"])
        self.assertTrue(all(x["family"].startswith("video_") for x in result["next_trials"]))
        self.assertEqual(result["next_trials"][0]["trial_id"], "VIDEO-FORMULA-01")

    def test_cli_writes_control_treatment_cards(self):
        with tempfile.TemporaryDirectory() as tmp:
            import sys
            old_argv = sys.argv
            try:
                sys.argv = ["prompt_trial_planner.py", "--outdir", tmp, "--limit", "3"]
                self.assertEqual(main(), 0)
            finally:
                sys.argv = old_argv
            self.assertTrue((Path(tmp) / "trial_plan.json").is_file())
            self.assertTrue((Path(tmp) / "trial_cards" / "IMG-FORMULA-01.control.txt").is_file())
            self.assertTrue((Path(tmp) / "trial_cards" / "IMG-TEACH-01.treatment.txt").is_file())
            card = (Path(tmp) / "trial_cards" / "VIDEO-FORMULA-01.md").read_text(encoding="utf-8")
            self.assertIn("five-state prompt formula", card.lower())
