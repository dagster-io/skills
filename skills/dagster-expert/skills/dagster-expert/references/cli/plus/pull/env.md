---
description: "dg plus pull env: pull environment variables from Dagster Plus into a local .env file."
triggers:
  - "pull env, sync env vars, download env"
  - "local env vars"
  - "get env vars from dagster plus"
---

# dg plus pull env - Pull Environment Variables

Pull environment variables from Dagster Plus and save them to a local `.env` file. Requires authentication via `dg plus login`.

```bash
dg plus pull env
```

---

## Options

| Option                 | Description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| `--target-path <path>` | Directory containing `dg.toml` or `pyproject.toml` to load context from |

---

## Examples

```bash
# Pull env vars into .env
dg plus pull env

# Pull for a specific project in a workspace
dg plus pull env --target-path ./projects/analytics
```

## Workflow

```bash
dg plus login               # Authenticate first
dg list envs                # See what variables are expected
dg plus pull env            # Pull values from Dagster Plus
dg list envs                # Verify variables are now set
```

---

## See Also

- [../login.md](../login.md) - Authenticate with Dagster Plus (required before pull)
- [../../list/envs.md](../../list/envs.md) - List environment variables and their status
