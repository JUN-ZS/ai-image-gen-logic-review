from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from bubble_break.runner import CommandRerunProvider


class CommandRerunProviderTests(unittest.TestCase):
    def test_provider_receives_locked_request_and_returns_actual_candidate_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            provider_script = root / "fake_provider.py"
            provider_script.write_text(
                "import json, os\n"
                "from pathlib import Path\n"
                "request = json.loads(Path(os.environ['BUBBLE_BREAK_REQUEST_JSON']).read_text(encoding='utf-8'))\n"
                "response_path = Path(os.environ['BUBBLE_BREAK_RESPONSE_JSON'])\n"
                "candidate_path = response_path.parent / 'candidate_fake.png'\n"
                "candidate_path.write_bytes(b'provider-test-fixture-not-a-real-image')\n"
                "response_path.write_text(json.dumps({'candidates':[{'path':str(candidate_path),'evidence':{'stage':request['stage']}}]}), encoding='utf-8')\n",
                encoding="utf-8",
            )
            outdir = root / "attempts"
            provider = CommandRerunProvider([sys.executable, str(provider_script)], timeout_seconds=30)
            batch = provider("CAL_PRE_FAR", 0, None, ["contact surface unclear"], outdir)

            self.assertEqual(len(batch), 1)
            candidate_path, evidence = batch[0]
            self.assertTrue(candidate_path.is_file())
            self.assertEqual(evidence["stage"], "PRE_FAR")

            request_files = list(outdir.glob("request_*.json"))
            self.assertEqual(len(request_files), 1)
            request = json.loads(request_files[0].read_text(encoding="utf-8"))
            self.assertEqual(request["protocol"], "BUBBLE_BREAK_IMAGE_PROVIDER_REQUEST_V1")
            self.assertIn("diagnostic_experiment", request)
            self.assertIn("stage_prompt", request)
            self.assertIn("actual raster files", request["hard_rule"])
            self.assertTrue(request["diagnostic_experiment"]["action_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
