---
description: "dg list envs: list environment variables required by the project."
triggers:
  - "list env vars, environment variables, .env"
  - "what env vars are needed"
---

# dg list envs - Environment Variables

List environment variables from the `.env` file of the current project. Shows variable name, whether it is set locally, and which components use it.

```bash
dg list envs
```

With Dagster Plus authentication (`dg plus login`), also shows deployment scope status (Dev/Branch/Full).

---

## Options

| Option                 | Description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| `--target-path <path>` | Directory containing `dg.toml` or `pyproject.toml` to load context from |

---

## Examples

```bash
# List all required env vars
dg list envs

# Check a specific project in a workspace
dg list envs --target-path ./projects/analytics
```

## Workflow: Sync from Dagster Plus

```bash
dg plus login
dg list envs                # See what's set and what's missing
dg plus pull env            # Pull values from Dagster Plus into .env
```

---

## See Also

- [../plus/login.md](../plus/login.md) - Authenticate to see deployment scope status
- [../plus/pull/env.md](../plus/pull/env.md) - Pull env vars from Dagster Plus
