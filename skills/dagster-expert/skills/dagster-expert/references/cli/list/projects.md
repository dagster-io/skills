---
description: "dg list projects: list projects in the current workspace."
triggers:
  - "list projects, workspace projects"
  - "find project path"
---

# dg list projects - Workspace Projects

List projects in the current workspace, or emit the current project directory for a standalone project.

```bash
dg list projects
```

---

## Options

| Option                 | Description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| `--target-path <path>` | Directory containing `dg.toml` or `pyproject.toml` to load context from |

---

## Examples

```bash
# List all projects in workspace
dg list projects

# Standalone project (outputs ".")
dg list projects
```

In a workspace, outputs the path to each project. In a standalone project, outputs `.`.

---

## See Also

- [./defs.md](./defs.md) - List definitions in a project
