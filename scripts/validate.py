#!/usr/bin/env python3
"""Validate source/evaluation contracts and optionally actual host loading."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time

from build import ROOT, compile_profiles, load_agents, load_teams, select_catalog


def validate(opencode=None, packs=None, agent_ids=None, team_ids=None):
    agents, _ = load_agents()
    names = {agent["metadata"]["id"] for agent in agents}
    teams, _ = load_teams(agents)
    team_names = {team["metadata"]["id"] for team in teams}
    files = compile_profiles("opencode", packs, agent_ids, team_ids)
    cases = json.loads((ROOT / "evals/behavior-cases.json").read_text(encoding="utf-8"))
    if cases.get("format_version") != 1:
        raise ValueError("Unsupported evaluation format")
    ids = set()
    coverage = {name: 0 for name in names}
    team_coverage = {name: 0 for name in team_names}
    for case in cases["cases"]:
        if case["id"] in ids:
            raise ValueError(f"Duplicate evaluation case: {case['id']}")
        ids.add(case["id"])
        role = case["expected_agent"]
        if role not in names and role != "*":
            raise ValueError(f"Unknown evaluation role: {role}")
        if not all(case.get(field) for field in ("prompt", "fixture_requirements", "acceptance_criteria")):
            raise ValueError(f"Incomplete evaluation case: {case['id']}")
        if case.get("execution_status") != "not_run":
            raise ValueError("Case specifications must not claim observed model outcomes")
        if role != "*":
            coverage[role] += 1
        if "expected_team" in case:
            if case["expected_team"] not in team_names:
                raise ValueError(f"Unknown evaluation team: {case['expected_team']}")
            team_coverage[case["expected_team"]] += 1
    if any(count < 2 for count in coverage.values()):
        raise ValueError("Every role needs at least two role-specific acceptance scenarios")
    if any(count < 2 for count in team_coverage.values()):
        raise ValueError("Every team needs at least two acceptance scenarios")
    agents, teams, _, selected_packs = select_catalog(agents, teams, packs, agent_ids, team_ids)
    names = {a["metadata"]["id"] for a in agents}
    team_names = {t["metadata"]["id"] for t in teams}
    result = {"status": "passed", "packs": selected_packs, "validated_at_utc": datetime.now(timezone.utc).isoformat(),
              "agent_count": len(names), "scenario_count": len(ids),
              "team_count": len(team_names), "host_loading": "not_checked",
              "command_loading": "not_checked", "model_behavior": "not_run"}
    if opencode:
        result["opencode_executable"] = opencode
        result["opencode_version"] = subprocess.check_output([opencode, "--version"], text=True, timeout=30).strip()
        # Fresh locations can briefly return their initial agent set while the
        # service loads configuration. Retry missing IDs only; never hide drift.
        for attempt in range(3):
            output = subprocess.check_output([opencode, "debug", "agents"], text=True, timeout=30)
            loaded = {agent["id"]: agent for agent in json.loads(output)}
            if names <= loaded.keys() or attempt == 2:
                break
            time.sleep(0.25)
        for name in names:
            if name not in loaded:
                raise ValueError(f"Profile not loaded: {name}")
            front, body = files[f"agents/{name}.md"][4:].split("\n---\n", 1)
            config = json.loads((ROOT / "adapters/opencode/adapter.json").read_text(encoding="utf-8"))
            description = next(agent["metadata"]["description"] for agent in agents if agent["metadata"]["id"] == name)
            if loaded[name].get("system", "").strip() != body.strip():
                raise ValueError(f"Loaded prompt drift: {name}")
            mode = config.get("mode_overrides", {}).get(name, config["mode"])
            if loaded[name].get("mode") != mode or loaded[name].get("description") != description:
                raise ValueError(f"Loaded metadata drift: {name}")
        result["host_loading"] = "passed"
        for attempt in range(3):
            directory = str(Path.cwd().resolve())
            output = subprocess.check_output(
                [opencode, "api", "command.list", "--param", "location[directory]=" + directory],
                text=True, timeout=30)
            registry = json.loads(output)
            if registry.get("location", {}).get("directory") != directory:
                raise ValueError("Command registry returned a different project location")
            commands = {command["name"]: command for command in registry["data"]}
            if team_names <= commands.keys() or attempt == 2:
                break
            time.sleep(0.25)
        for team in teams:
            metadata = team["metadata"]
            if metadata["id"] not in commands:
                raise ValueError(f"Team command not loaded: {metadata['id']}")
            if commands[metadata["id"]].get("description") != metadata["description"]:
                raise ValueError(f"Team command metadata drift: {metadata['id']}")
        result["command_loading"] = "passed"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opencode", help="Explicit host executable; omit for source-only checks")
    parser.add_argument("--pack", action="append", help="Check selected pack outputs and loading; default: all packs")
    parser.add_argument("--agent", action="append", help="Check selected individual profiles")
    parser.add_argument("--team", action="append", help="Check selected teams and their profiles")
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.opencode, args.pack, args.agent, args.team), indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError, subprocess.SubprocessError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
