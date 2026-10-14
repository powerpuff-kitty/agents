"""Behavioral contracts for building and installing profiles, without model calls."""
import json
from pathlib import Path
import shutil
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
            self.assertEqual(len(json.loads(result.stdout)["changed"]), 57)
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
            self.assertEqual(len(files), 35)
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
            self.assertEqual(len(commands), 20)
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
            self.assertEqual(len(json.loads(result.stdout)["changed"]), 36)
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
            with patch.object(build, "ROOT", root), self.assertRaisesRegex(ValueError, "Writing requires delivery or adaptive"):
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
            self.assertEqual(len(teams), 20)
            for team in teams:
                body = team.read_text()
                self.assertNotIn("OpenCode", body)
                self.assertNotIn("$ARGUMENTS", body)
                self.assertNotIn("subagent: false", body)
                self.assertIn("Completion evidence", body)

    def test_adaptive_team_mutations_are_conditional_and_review_actions_rejected(self):
        agents, _ = build.load_agents()
        original = json.loads((ROOT / "teams/team.json").read_text())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "teams").mkdir()
            path = root / "teams/team.json"
            path.write_text(json.dumps(original))
            with patch.object(build, "ROOT", root):
                teams, _ = build.load_teams(agents)
            self.assertIn("candidate roster", teams[0]["instructions"])
            self.assertIn("user's actual request and existing authorization", teams[0]["instructions"])
            for index, stage in enumerate(original["stages"]):
                if stage["execution"] not in {"exclusive-write", "serial-action"}:
                    continue
                with self.subTest(stage=stage["id"]):
                    invalid = json.loads(json.dumps(original))
                    invalid["stages"][index]["assignments"][0]["when"] = " ALWAYS "
                    path.write_text(json.dumps(invalid))
                    with patch.object(build, "ROOT", root), self.assertRaisesRegex(ValueError, "task authorization condition"):
                        build.load_teams(agents)
            invalid = json.loads(json.dumps(original))
            invalid["mode"] = "review"
            invalid["stages"] = [original["stages"][-1]]
            path.write_text(json.dumps(invalid))
            with patch.object(build, "ROOT", root), self.assertRaisesRegex(ValueError, "Actions require delivery or adaptive"):
                build.load_teams(agents)
            invalid = json.loads(json.dumps(original))
            invalid["stages"][-1]["assignments"][0]["agent"] = original["coordinator"]
            path.write_text(json.dumps(invalid))
            with patch.object(build, "ROOT", root), self.assertRaisesRegex(ValueError, "Unknown or recursive"):
                build.load_teams(agents)

    def test_general_routing_and_research_evidence_dependencies(self):
        agents, _ = build.load_agents()
        teams, _ = build.load_teams(agents)
        metadata = {team["metadata"]["id"]: team["metadata"] for team in teams}
        general = metadata["team"]
        candidates = {a["agent"] for stage in general["stages"] for a in stage["assignments"]}
        self.assertEqual(candidates, {a["metadata"]["id"] for a in agents} - {"team-lead"})
        self.assertTrue(all(a["when"] != "always" for stage in general["stages"] for a in stage["assignments"]))
        research = metadata["team-research"]
        self.assertEqual(research["mode"], "review")
        self.assertEqual(research["stages"][0]["execution"], "serial-review")
        self.assertEqual([a["agent"] for a in research["stages"][0]["assignments"]], ["researcher"])
        self.assertEqual(research["stages"][1]["assignments"][0]["agent"], "evidence-validator")
        self.assertTrue(all(stage["execution"] in {"serial-review", "parallel-review"} for stage in research["stages"]))

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

    def test_pack_selection_resolves_dependencies_and_filters_candidates(self):
        for requested, agent_count, team_count in ((["core"], 16, 8), (["science-data"], 19, 10),
                                                  (["product-growth"], 27, 15), (["game-3d"], 22, 12),
                                                  (["product-growth", "game-3d"], 30, 17),
                                                  (["finance"], 22, 11),
                                                  (["product-growth", "game-3d", "finance"], 33, 18),
                                                  (["crypto"], 23, 12), (["forecasting"], 20, 11),
                                                  (["crypto", "forecasting"], 24, 13),
                                                  (["product-growth", "game-3d", "crypto", "forecasting"], 35, 20)):
            with self.subTest(packs=requested):
                files = build.compile_profiles("portable", requested)
                manifest = json.loads(files["build-manifest.json"])
                self.assertEqual(len(manifest["agents"]), agent_count)
                self.assertEqual(len(manifest["teams"]), team_count)
                self.assertIn("core", manifest["packs"])
                agents, _ = build.load_agents()
                teams, _ = build.load_teams(agents)
                selected, workflows, _, _ = build.select_catalog(agents, teams, requested)
                names = {a["metadata"]["id"] for a in selected}
                for team in workflows:
                    self.assertTrue({a["agent"] for stage in team["metadata"]["stages"]
                                     for a in stage["assignments"]} <= names)
        core = build.compile_profiles("opencode", ["core"])
        self.assertNotIn("Agent: geo-specialist", core["commands/team.md"])
        self.assertNotIn("commands/team-geo.md", core)
        self.assertNotIn("commands/team-finance.md", core)
        self.assertNotIn("commands/team-crypto-review.md", core)
        self.assertNotIn("commands/team-forecast.md", core)
        self.assertNotIn("Agent: financial-analyst", core["commands/team.md"])
        full = build.compile_profiles("opencode")
        self.assertIn("Agent: geo-specialist", full["commands/team.md"])
        self.assertIn("commands/team-geo.md", full)
        self.assertIn("commands/team-finance.md", full)
        self.assertIn("commands/team-crypto-review.md", full)
        self.assertIn("commands/team-forecast.md", full)
        self.assertIn("Agent: financial-analyst", full["commands/team.md"])

    def test_pack_graph_rejects_cycles_unknowns_missing_dependencies_and_ownership(self):
        agents, _ = build.load_agents()
        teams, _ = build.load_teams(agents)
        for kind, expected in (("cycle", "dependency cycle"), ("unknown", "Unknown pack dependency"),
                               ("duplicate", "multiply owned"), ("unowned", "cover every"),
                               ("missing", "cannot resolve team")):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                shutil.copytree(ROOT / "packs", root / "packs")
                path = root / "packs" / ("product-growth.json" if kind == "missing" else "core.json")
                value = json.loads(path.read_text())
                if kind == "cycle":
                    value["requires"] = ["science-data"]
                elif kind == "unknown":
                    value["requires"] = ["missing-pack"]
                elif kind == "duplicate":
                    value["agents"].append("scientist")
                elif kind == "unowned":
                    value["agents"].remove("designer")
                else:
                    value["requires"] = ["core"]
                path.write_text(json.dumps(value))
                with patch.object(build, "ROOT", root), self.assertRaisesRegex(ValueError, expected):
                    build.load_packs(agents, teams)

    def test_partial_install_preserves_other_packs_and_rejects_unknown_pack_before_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "agents"
            invalid = run("install.py", "--target", target, "--pack", "unknown-pack")
            self.assertNotEqual(invalid.returncode, 0)
            self.assertFalse(target.exists())
            first = run("install.py", "--target", target, "--pack", "core")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(len(json.loads(first.stdout)["changed"]), 26)
            self.assertFalse((target / "scientist.md").exists())
            more = run("install.py", "--target", target, "--pack", "game-3d")
            self.assertEqual(more.returncode, 0, more.stderr)
            asset = target / "artist-3d.md"
            before = asset.read_bytes(), asset.stat().st_mtime_ns
            narrower = run("install.py", "--target", target, "--pack", "core")
            self.assertEqual(narrower.returncode, 0, narrower.stderr)
            self.assertEqual((asset.read_bytes(), asset.stat().st_mtime_ns), before)
            self.assertTrue((base / "commands/team-3d.md").exists())
            again = run("install.py", "--target", target, "--pack", "core")
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(json.loads(again.stdout)["changed"], [])

    def test_ux_workflow_filters_optional_roles_and_orders_dependent_checks(self):
        agents, _ = build.load_agents()
        teams, _ = build.load_teams(agents)
        selected, workflows, _, _ = build.select_catalog(agents, teams, ["core"])
        ux = next(t["metadata"] for t in workflows if t["metadata"]["id"] == "team-ux")
        members = {a["agent"] for stage in ux["stages"] for a in stage["assignments"]}
        self.assertTrue({"ux-designer", "usability-auditor", "accessibility-specialist"} <= members)
        self.assertFalse({"user-researcher", "data-analyst", "copywriter"} & members)
        self.assertNotIn("user-evidence", [s["id"] for s in ux["stages"]])
        full = next(t["metadata"] for t in teams if t["metadata"]["id"] == "team-ux")
        stages = {stage["id"]: index for index, stage in enumerate(full["stages"])}
        self.assertLess(stages["user-evidence"], stages["journey"])
        self.assertLess(stages["journey"], stages["ui-copy-and-access"])
        self.assertLess(stages["ui-copy-and-access"], stages["implement"])
        self.assertLess(stages["implement"], stages["independent-checks"])
        writer = full["stages"][stages["implement"]]
        self.assertEqual(writer["execution"], "exclusive-write")
        self.assertEqual(len(writer["assignments"]), 1)
        self.assertNotEqual(writer["assignments"][0]["when"], "always")
        checks = full["stages"][stages["independent-checks"]]
        self.assertNotIn("ux-designer", {a["agent"] for a in checks["assignments"]})
        self.assertIn("usability-auditor", {a["agent"] for a in checks["assignments"]})

    def test_iteration_gates_follow_current_checks_and_precede_dependent_actions(self):
        agents, _ = build.load_agents()
        teams, _ = build.load_teams(agents)
        _, selected, _, _ = build.select_catalog(agents, teams, ["core"])
        workflows = {t["metadata"]["id"]: t["metadata"] for t in selected}
        iteration = workflows["team-iteration"]
        members = {a["agent"] for stage in iteration["stages"] for a in stage["assignments"]}
        self.assertIn("iteration-reviewer", members)
        self.assertNotIn("product-manager", members)
        self.assertNotIn("serial-action", {stage["execution"] for stage in iteration["stages"]})
        indices = {stage["id"]: n for n, stage in enumerate(iteration["stages"])}
        self.assertLess(indices["scope-and-done"], indices["remediate"])
        self.assertLess(indices["remediate"], indices["specialist-checks"])
        self.assertLess(indices["specialist-checks"], indices["artifact-evidence"])
        self.assertLess(indices["artifact-evidence"], indices["readiness-verdict"])
        writer = iteration["stages"][indices["remediate"]]
        self.assertEqual(writer["execution"], "exclusive-write")
        self.assertEqual(len(writer["assignments"]), 1)
        self.assertNotEqual(writer["assignments"][0]["when"], "always")
        feature = workflows["team-feature"]
        self.assertTrue(any(a["agent"] == "iteration-reviewer" and a["when"] == "always"
                            for a in feature["stages"][0]["assignments"]))
        feature_order = {stage["id"]: n for n, stage in enumerate(feature["stages"])}
        self.assertLess(feature_order["implement"], feature_order["verify"])
        self.assertLess(feature_order["verify"], feature_order["artifact-evidence"])
        self.assertLess(feature_order["artifact-evidence"], feature_order["iteration-readiness"])
        general_order = {stage["id"]: n for n, stage in enumerate(workflows["team"]["stages"])}
        self.assertLess(general_order["verify"], general_order["iteration-readiness"])
        self.assertLess(general_order["iteration-readiness"], general_order["requested-actions"])

    def test_pack_builds_have_separate_default_destinations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(build, "ROOT", root), patch.object(build, "compile_profiles", return_value={"test.md": "body"}):
                full = build.build("portable")
                partial = build.build("portable", packs=["core"])
                self.assertNotEqual(full, partial)
                self.assertEqual(partial.name, "portable-core")


if __name__ == "__main__":
    unittest.main()
