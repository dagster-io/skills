---
description: "dg list components: list available component types for scaffolding."
triggers:
  - "list components, available components, component types"
  - "what components can I scaffold"
---

# dg list components - Available Component Types

List all available Dagster component types in the current Python environment.

```bash
dg list components
```

---

## Options

| Option                 | Description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| `-p, --package <pkg>`  | Filter by package name                                                  |
| `--json`               | Output as JSON instead of a table                                       |
| `--target-path <path>` | Directory containing `dg.toml` or `pyproject.toml` to load context from |

---

## Examples

```bash
# List all component types
dg list components

# Filter by package
dg list components --package dagster
dg list components --package dagster_dbt

# JSON output
dg list components --json
```

## Workflow: Discover then Scaffold

```bash
# Find available components
dg list components --package dagster_dbt

# Scaffold the component
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt
```

---

## See Also

- [../scaffold/defs.md](../scaffold/defs.md) - Scaffold components with `dg scaffold defs`
