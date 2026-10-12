"""Map portable instructions to OpenCode Markdown profiles."""
import textwrap


def render(agents, teams, contract, host_instructions, config):
    modes = config.get("mode_overrides", {})
    names = {agent["metadata"]["id"] for agent in agents}
    if set(modes) - names or any(mode not in {"primary", "subagent", "all"}
                                  for mode in [config["mode"], *modes.values()]):
        raise ValueError("Invalid OpenCode mode")
    files = {}
    for agent in agents:
        metadata = agent["metadata"]
        mode = modes.get(metadata["id"], config["mode"])
        description = textwrap.fill(metadata["description"], width=78,
                                    initial_indent="  ", subsequent_indent="  ",
                                    break_long_words=False, break_on_hyphens=False)
        body = "\n\n".join([agent["instructions"].strip(), contract.strip(), host_instructions.strip()])
        files[f"agents/{metadata['id']}.md"] = (
            f"---\ndescription: >-\n{description}\nmode: {mode}\n---\n{body}\n"
        )
    for team in teams:
        metadata = team["metadata"]
        description = textwrap.fill(metadata["description"], width=78,
                                    initial_indent="  ", subsequent_indent="  ",
                                    break_long_words=False, break_on_hyphens=False)
        # Keep the coordinator in the current session; specialists are its children.
        body = team["instructions"] + "\n\n## Requested scope\n\n$ARGUMENTS\n\n"
        body += "Use an unambiguous current task when this argument is empty; otherwise ask only for the missing critical scope.\n"
        files[f"commands/{metadata['id']}.md"] = (
            f"---\ndescription: >-\n{description}\nagent: {metadata['coordinator']}\n"
            f"subagent: false\n---\n{body}"
        )
    return files
