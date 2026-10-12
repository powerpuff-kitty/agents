"""Export complete neutral instructions without host configuration."""


def render(agents, teams, contract, host_instructions, config):
    files = {}
    for agent in agents:
        metadata = agent["metadata"]
        files[f"agents/{metadata['id']}.md"] = "\n\n".join([
            "# " + metadata["title"], metadata["description"],
            agent["instructions"].strip(), contract.strip()
        ]) + "\n"
    for team in teams:
        files[f"teams/{team['metadata']['id']}.md"] = team["instructions"] + (
            "\n\nProvide the coordinator and applicable specialist instruction bundles to the host. "
            "These briefs do not themselves create named agents or independent model sessions.\n"
        )
    return files
