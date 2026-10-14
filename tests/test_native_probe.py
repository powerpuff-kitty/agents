"""Native verification must work without a Skills or CLI checkout."""
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import opencode_probe

spec = importlib.util.spec_from_file_location("fetch_opencode", ROOT / "scripts/fetch-opencode.py")
fetcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetcher)


class NativeProbeTests(unittest.TestCase):
    def test_stages_profiles_without_skills_and_rejects_prompt_drift(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            export, project = root / "export", root / "project"
            (export / "agents").mkdir(parents=True)
            (export / "commands").mkdir()
            (export / "agents/reviewer.md").write_text("---\nmode: all\n---\nReview the change.\n")
            (export / "commands/team-review.md").write_text("---\nagent: reviewer\n---\n$ARGUMENTS\n")
            agents, commands = opencode_probe.stage_export(export, project)
            self.assertFalse((project / ".opencode/skills").exists())
            loaded = [{"id": "reviewer", "system": "Review the change."}]
            opencode_probe.check_registration(agents, commands, loaded, [{"name": "team-review"}])
            with self.assertRaisesRegex(ValueError, "altered agent"):
                opencode_probe.check_registration(agents, commands, [{"id": "reviewer", "system": "Different"}], [{"name": "team-review"}])
            with self.assertRaisesRegex(ValueError, "Missing commands"):
                opencode_probe.check_registration(agents, commands, loaded, [])
            with self.assertRaisesRegex(ValueError, "Missing or altered"):
                opencode_probe.check_registration(agents, commands, [], [{"name": "team-review"}])

    def test_empty_export_is_not_a_successful_native_check(self):
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaisesRegex(ValueError, "No agent profiles"):
                opencode_probe.stage_export(Path(raw) / "missing", Path(raw) / "project")

    def test_corrupt_host_download_never_creates_executable(self):
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw) / "opencode"
            with patch.object(fetcher.urllib.request, "urlopen", return_value=io.BytesIO(b"corrupt archive")):
                with self.assertRaisesRegex(ValueError, "integrity mismatch"):
                    fetcher.fetch(output)
            self.assertFalse(output.exists())
