"""Behavioral contracts for building and installing profiles, without model calls."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build
import validate as validator

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
            self.assertEqual(len(json.loads(result.stdout)["changed"]), 14)
            self.assertFalse((Path(temporary) / "commands").exists())

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
            self.assertEqual(len(files), 10)
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

    def test_team_commands_select_parent_coordinator_and_include_scope(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "opencode"
            result = run("build.py", "--adapter", "opencode", "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            commands = list((output / "commands").glob("*.md"))
            self.assertEqual(len(commands), 4)
            for command in commands:
                front, body = command.read_text()[4:].split("\n---\n", 1)
                self.assertIn("agent: team-lead", front.splitlines())
                self.assertIn("subagent: false", front.splitlines())
                self.assertEqual(body.count("$ARGUMENTS"), 1)
                self.assertNotIn("!`", body)
                self.assertIn("Maximum active independent assignments: 3", body)
            lead_front = (output / "agents/team-lead.md").read_text().split("\n---\n", 1)[0]
            self.assertIn("mode: primary", lead_front.splitlines())
            specialist_front = (output / "agents/designer.md").read_text().split("\n---\n", 1)[0]
            self.assertIn("mode: all", specialist_front.splitlines())

    def test_command_conflicts_preflight_before_any_agent_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            agents, commands = base / "agents", base / "commands"
            commands.mkdir()
            conflict = commands / "team-audit.md"
            conflict.write_text("My personal audit command.\n")
            result = run("install.py", "--target", agents)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(agents.exists())
            self.assertEqual(conflict.read_text(), "My personal audit command.\n")
            result = run("install.py", "--target", agents, "--replace")
            self.assertEqual(result.returncode, 0, result.stderr)
            backup = Path(json.loads(result.stdout)["backups"]["commands"])
            self.assertEqual((backup / "team-audit.md").read_text(), "My personal audit command.\n")
            conflict.write_text("User edit to the managed command.\n")
            result = run("install.py", "--target", agents)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(conflict.read_text(), "User edit to the managed command.\n")

    def test_agent_only_install_does_not_create_commands(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            result = run("install.py", "--target", base / "profiles", "--agents-only")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(result.stdout)["changed"]), 10)
            self.assertFalse((base / "commands").exists())

    def test_nested_profile_and_command_destinations_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            agents = Path(temporary) / "agents"
            result = run("install.py", "--target", agents,
                         "--commands-target", agents / "commands")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(agents.exists())

    def test_team_references_and_writer_constraints_are_validated(self):
        agents, _ = build.load_agents()
        original = json.loads((ROOT / "teams/team-feature.json").read_text())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "teams").mkdir()
            path = root / "teams/team-feature.json"
            unknown = json.loads(json.dumps(original))
            unknown["stages"][0]["assignments"][0]["agent"] = "missing-agent"
            path.write_text(json.dumps(unknown))
            with patch.object(build, "ROOT", root), self.assertRaisesRegex(ValueError, "Unknown or recursive"):
                build.load_teams(agents)
            wrong_mode = json.loads(json.dumps(original))
            wrong_mode["mode"] = "review"
            path.write_text(json.dumps(wrong_mode))
            with patch.object(build, "ROOT", root), self.assertRaisesRegex(ValueError, "Writing requires delivery"):
                build.load_teams(agents)
            two_writers = json.loads(json.dumps(original))
            two_writers["stages"][1]["assignments"].append(two_writers["stages"][1]["assignments"][0])
            path.write_text(json.dumps(two_writers))
            with patch.object(build, "ROOT", root), self.assertRaisesRegex(ValueError, "one owner"):
                build.load_teams(agents)

    def test_portable_team_briefs_have_no_host_macros(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "portable"
            result = run("build.py", "--adapter", "portable", "--output", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            teams = list((output / "teams").glob("*.md"))
            self.assertEqual(len(teams), 4)
            for team in teams:
                body = team.read_text()
                self.assertNotIn("OpenCode", body)
                self.assertNotIn("$ARGUMENTS", body)
                self.assertNotIn("subagent: false", body)
                self.assertIn("Completion evidence", body)

    def test_command_validation_queries_current_project_and_rejects_other_location(self):
        agents, _ = build.load_agents()
        teams, _ = build.load_teams(agents)
        profiles = build.compile_profiles("opencode")
        config = json.loads((ROOT / "adapters/opencode/adapter.json").read_text())
        host_agents = []
        for agent in agents:
            metadata = agent["metadata"]
            body = profiles[f"agents/{metadata['id']}.md"][4:].split("\n---\n", 1)[1]
            host_agents.append({"id": metadata["id"], "description": metadata["description"],
                                "mode": config.get("mode_overrides", {}).get(metadata["id"], config["mode"]),
                                "system": body})
        current = str(Path.cwd().resolve())

        def response(command, **kwargs):
            if command[1:] == ["--version"]:
                return "opencode v2.0.27"
            if command[1:] == ["debug", "agents"]:
                return json.dumps(host_agents)
            self.assertEqual(command[1:], ["api", "command.list", "--param", "location[directory]=" + current])
            return json.dumps({"location": {"directory": current},
                               "data": [{"name": t["metadata"]["id"], "description": t["metadata"]["description"]} for t in teams]})

        with patch.object(validator.subprocess, "check_output", side_effect=response):
            self.assertEqual(validator.validate("fixture-host")["command_loading"], "passed")

        def wrong_location(command, **kwargs):
            result = response(command, **kwargs)
            if "command.list" in command:
                decoded = json.loads(result)
                decoded["location"]["directory"] = "/another/project"
                return json.dumps(decoded)
            return result

        with patch.object(validator.subprocess, "check_output", side_effect=wrong_location):
            with self.assertRaisesRegex(ValueError, "different project location"):
                validator.validate("fixture-host")


if __name__ == "__main__":
    unittest.main()
