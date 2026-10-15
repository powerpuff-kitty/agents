#!/usr/bin/env python3
"""Check profile/command registration in a disposable persistent OpenCode server.

Requires an explicit executable and Git. Uses only this repository's exports,
never installs skills or invokes a model, and isolates host configuration.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request


def stage_export(export, project):
    export = Path(export).resolve()
    expected_agents = {}
    expected_commands = set()
    for kind in ("agents", "commands"):
        source = export / kind
        if source.is_symlink():
            raise ValueError("Linked export directory")
        for file in sorted(source.glob("*.md")):
            if file.is_symlink():
                raise ValueError("Linked export file")
            text = file.read_text(encoding="utf-8")
            if not text.startswith("---\n") or "\n---\n" not in text:
                raise ValueError("Missing export frontmatter: " + file.name)
            target = project / ".opencode" / kind / file.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
            if kind == "agents":
                expected_agents[file.stem] = text.split("\n---\n", 1)[1].strip()
            else:
                expected_commands.add(file.stem)
    if not expected_agents:
        raise ValueError("No agent profiles in export")
    return expected_agents, expected_commands


def check_registration(expected_agents, expected_commands, agents, commands):
    loaded_agents = {entry["id"]: entry for entry in agents}
    loaded_commands = {entry["name"]: entry for entry in commands}
    for name, body in expected_agents.items():
        if loaded_agents.get(name, {}).get("system", "").strip() != body:
            raise ValueError("Missing or altered agent prompt: " + name)
    missing = expected_commands - loaded_commands.keys()
    if missing:
        raise ValueError("Missing commands: " + ", ".join(sorted(missing)))


def probe(executable, export, expected_version=None):
    with tempfile.TemporaryDirectory(prefix="agents-native-host-") as raw:
        root = Path(raw).resolve()
        project = root / "project"
        project.mkdir()
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        expected_agents, expected_commands = stage_export(export, project)
        env = {k: v for k, v in os.environ.items() if k in
               ("PATH", "LANG", "LC_ALL", "SYSTEMROOT", "WINDIR", "TMPDIR")}
        for key, sub in (("HOME", "home"), ("XDG_CONFIG_HOME", "config"),
                         ("XDG_DATA_HOME", "data"), ("XDG_CACHE_HOME", "cache"),
                         ("XDG_STATE_HOME", "state")):
            directory = root / sub
            directory.mkdir()
            env[key] = str(directory)
        env["OPENCODE_CONFIG_CONTENT"] = '{"autoupdate":false}'
        env["OPENCODE_PASSWORD"] = secrets.token_hex(24)
        env["OPENCODE_USERNAME"] = "opencode"
        version = subprocess.check_output([executable, "--version"], text=True,
                                          env=env, timeout=30).strip()
        if expected_version and version != f"opencode v{expected_version}":
            raise ValueError("Unexpected OpenCode version")
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        server = subprocess.Popen(
            [executable, "serve", "--hostname", "127.0.0.1", "--port", str(port)],
            cwd=project, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        url = f"http://127.0.0.1:{port}"
        auth = base64.b64encode(("opencode:" + env["OPENCODE_PASSWORD"]).encode()).decode()
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

        def get(path):
            request = urllib.request.Request(url + path, headers={"Authorization": "Basic " + auth})
            with opener.open(request, timeout=2) as response:
                data = response.read(16_000_001)
            if len(data) > 16_000_000:
                raise ValueError("Host response exceeds probe bound")
            return json.loads(data)

        try:
            for _ in range(50):
                try:
                    api = get("/openapi.json")
                    break
                except (OSError, ValueError):
                    if server.poll() is not None:
                        raise ValueError("Isolated server exited")
                    time.sleep(.1)
            else:
                raise ValueError("Isolated server readiness timed out")

            def call(operation):
                paths = [path for path, methods in api["paths"].items()
                         if methods.get("get", {}).get("operationId") == operation]
                if len(paths) != 1:
                    raise ValueError("Missing or ambiguous API operation: " + operation)
                query = urllib.parse.urlencode({"location[directory]": str(project)})
                result = get(paths[0] + "?" + query)
                if result.get("location", {}).get("directory") != str(project):
                    raise ValueError("Host returned another location")
                return result["data"]

            # Plugins initialize asynchronously; poll the SAME server for IDs.
            for attempt in range(30):
                agents = call("agent.list")
                commands = call("command.list")
                if (set(expected_agents) <= {x["id"] for x in agents}
                        and expected_commands <= {x["name"] for x in commands}):
                    break
                time.sleep(.2)
            check_registration(expected_agents, expected_commands, agents, commands)
            return {"status": "passed", "host_version": version,
                    "agent_prompts": len(expected_agents), "team_commands": len(expected_commands),
                    "attempts": attempt + 1,
                    "agent_body_sha256": {name: hashlib.sha256(body.encode()).hexdigest()
                                          for name, body in expected_agents.items()},
                    "skill_installation": "not_performed", "model_execution": "not_run",
                    "scope": "temporary project, private persistent server, isolated home/configuration"}
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opencode", required=True)
    parser.add_argument("--agents-export", type=Path, required=True)
    parser.add_argument("--expected-version")
    args = parser.parse_args()
    print(json.dumps(probe(args.opencode, args.agents_export, args.expected_version), indent=2))
