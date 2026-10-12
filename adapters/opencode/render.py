"""Map portable instructions to OpenCode Markdown profiles."""
import textwrap


def render(agents, contract, host_instructions, config):
    mode = config["mode"]
    if mode not in {"primary", "subagent", "all"}:
        raise ValueError("Invalid OpenCode mode")
    files = {}
    for agent in agents:
        metadata = agent["metadata"]
        description = textwrap.fill(metadata["description"], width=78,
                                    initial_indent="  ", subsequent_indent="  ",
                                    break_long_words=False, break_on_hyphens=False)
        body = "\n\n".join([agent["instructions"].strip(), contract.strip(), host_instructions.strip()])
        files[f"agents/{metadata['id']}.md"] = (
            f"---\ndescription: >-\n{description}\nmode: {mode}\n---\n{body}\n"
        )
    return files
