---
name: dg
description: Skill that enables interaction with Dagster projects (creating new projects, adding new definitions (assets, schedules, sensors, components) to existing projects, listing definitions, launching compute, viewing logs, and troubleshooting). Used whenever users have requests related to creating, understanding, or manipulating Dagster projects.
---

# Dagster CLI (dg) Skill

This skill is a thin wrapper around more complex and detailed reference documents. It helps guide users through workflows that require using the Dagster CLI (`dg`).

## Workflow Decision Tree

Depending on the user's request, choose the appropriate reference file or skill:

- Setting up a new project?
  - Single project (default): [`references/create-project.md`](references/create-project.md)
  - Multiple projects in the same repo: [`references/create-workspace.md`](./references/create-workspace.md)
- Creating new definitions within existing projects? [`references/scaffold.md`](./references/scaffold.md)
- Integrating with an external tool? [`/dagster-integrations` skill](../dagster-integrations/SKILL.md)
- Understanding the project structure? [`references/list.md`](references/list.md). Handles:
  - All definitions (assets, jobs, schedules, sensors, components)
  - Available component types
  - Environment variables
  - Projects in the workspace
- Launching assets or jobs? [`references/launch.md`](references/launch.md)
- Viewing logs or output? [`references/logs.md`](references/logs.md)
- Debugging failed runs or issues? [`references/troubleshoot.md`](references/troubleshoot.md)

These reference files contain detailed instructions specific to the given workflow. If it is unclear which reference file to use, ask the user to clarify their request.

Note that some requests may require multiple reference files in order to complete.

## `uv`-compatible projects

When projects are created with `create-dagster`, the standard project structure is created with a `pyproject.toml` file that contains the project dependencies, and it is encouraged to use `uv` to manage the project dependencies.

If the project is compatible with `uv`, it is encouraged to use this tool to invoke all `dg` commands against the project, e.g. instead of `dg list defs` being executed in a specific virtual environment, use `uv run dg list defs`.
