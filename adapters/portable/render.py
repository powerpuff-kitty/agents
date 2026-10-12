"""Export complete neutral instructions without host configuration."""


def render(agents, contract, host_instructions, config):
    files = {}
    for agent in agents:
        metadata = agent["metadata"]
        files[f"agents/{metadata['id']}.md"] = "\n\n".join([
            "# " + metadata["title"], metadata["description"],
            agent["instructions"].strip(), contract.strip()
        ]) + "\n"
    return files
