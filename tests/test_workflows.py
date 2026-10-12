"""Behavioral contracts for building and installing profiles, without model calls."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run(script, *arguments):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / script), *map(str, arguments)],
                          text=True, capture_output=True)


class WorkflowTests(unittest.TestCase):
    def test_deterministic_exports_and_drift_detection(self):
        for adapter in ("portable", "opencode"):
            with self.subTest(adapter=adapter), tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / "output"
                self.assertEqual(run("build.py", "--adapter", adapter, "--output", output).returncode, 0)
                before = {str(p.relative_to(output)): p.read_bytes() for p in output.rglob("*") if p.is_file()}
                self.assertEqual(run("build.py", "--adapter", adapter, "--output", output).returncode, 0)
                after = {str(p.relative_to(output)): p.read_bytes() for p in output.rglob("*") if p.is_file()}
                self.assertEqual(before, after)
                self.assertEqual(run("build.py", "--adapter", adapter, "--output", output, "--check").returncode, 0)
                profile = output / "agents/designer.md"
                profile.write_text(profile.read_text() + "\nLocal drift.\n")
                self.assertNotEqual(run("build.py", "--adapter", adapter, "--output", output, "--check").returncode, 0)

    def test_dry_run_does_not_create_target(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "profiles"
            result = run("install.py", "--target", target, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(target.exists())
            self.assertEqual(len(json.loads(result.stdout)["changed"]), 9)

    def test_install_preserves_other_profiles_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "profiles"
            target.mkdir()
            unrelated = target / "personal-agent.md"
            unrelated.write_text("Personal instructions.\n")
            first = run("install.py", "--target", target)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in target.iterdir()}
            second = run("install.py", "--target", target)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(json.loads(second.stdout)["changed"], [])
            after = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in target.iterdir()}
            self.assertEqual(before, after)
            self.assertEqual(unrelated.read_text(), "Personal instructions.\n")

    def test_conflict_refusal_and_explicit_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "profiles"
            target.mkdir()
            existing = target / "designer.md"
            existing.write_text("Unmanaged local instructions.\n")
            result = run("install.py", "--target", target)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(existing.read_text(), "Unmanaged local instructions.\n")
            self.assertFalse((target / "feature-developer.md").exists())
            result = run("install.py", "--target", target, "--replace")
            self.assertEqual(result.returncode, 0, result.stderr)
            backup = Path(json.loads(result.stdout)["backup"])
            self.assertEqual((backup / "designer.md").read_text(), "Unmanaged local instructions.\n")
            existing.write_text("Managed profile with user edit.\n")
            edited = run("install.py", "--target", target)
            self.assertNotEqual(edited.returncode, 0)
            self.assertEqual(existing.read_text(), "Managed profile with user edit.\n")

    def test_symlink_collision_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "profiles"
            target.mkdir()
            outside = base / "user.md"
            outside.write_text("User content.\n")
            (target / "designer.md").symlink_to(outside)
            result = run("install.py", "--target", target, "--replace")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(outside.read_text(), "User content.\n")

    def test_portable_bundles_are_complete_and_host_neutral(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "portable"
            result = run("build.py", "--adapter", "portable", "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            files = list((output / "agents").glob("*.md"))
            self.assertEqual(len(files), 9)
            for path in files:
                body = path.read_text()
                self.assertEqual(body.count("## Operating contract"), 1)
                self.assertNotIn("OpenCode", body)
                self.assertNotIn("mode: all", body)

    def test_build_does_not_follow_output_directory_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            output = base / "output"
            output.mkdir()
            outside = base / "outside"
            outside.mkdir()
            (output / "agents").symlink_to(outside, target_is_directory=True)
            result = run("build.py", "--output", output)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(outside.iterdir()), [])

    def test_invalid_management_state_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "profiles"
            target.mkdir()
            state = target / ".agents-managed.json"
            state.write_text(json.dumps({"schema_version": 1, "tool": "opencode", "files": []}))
            result = run("install.py", "--target", target)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(target.iterdir()), [state])

    def test_opencode_folding_preserves_routing_description(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "opencode"
            result = run("build.py", "--adapter", "opencode", "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            for profile in (output / "agents").glob("*.md"):
                metadata = json.loads((ROOT / "agents" / profile.stem / "agent.json").read_text())
                front = profile.read_text().split("\n---\n", 1)[0]
                folded = front.split("description: >-\n", 1)[1].split("\nmode:", 1)[0]
                self.assertEqual(" ".join(line.strip() for line in folded.splitlines()), metadata["description"])


if __name__ == "__main__":
    unittest.main()
