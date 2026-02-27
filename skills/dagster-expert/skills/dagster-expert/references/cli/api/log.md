---
description: "dg api log get: retrieve and filter run logs from Dagster Plus."
triggers:
  - "run logs, get logs, debug run"
  - "filter logs by level, event type, step"
---

# dg api log get - Run Log Retrieval

Retrieve logs for a specific run from Dagster Plus. Requires authentication via `dg plus login` or `--api-token`.

```bash
dg api log get <run-id>
```

---

## Options

| Option                      | Description                                                             |
| --------------------------- | ----------------------------------------------------------------------- |
| `--level <level>`           | Filter by log level: DEBUG, INFO, WARNING, ERROR, CRITICAL. Repeatable. |
| `--event-type <type>`       | Filter by event type (e.g. STEP_FAILURE, RUN_START). Repeatable.        |
| `--step <key>`              | Filter by step key (partial matching). Repeatable.                      |
| `--limit <n>`               | Maximum number of log entries to return                                 |
| `--cursor <cursor>`         | Pagination cursor for retrieving additional logs                        |
| `--json`                    | Output in JSON format                                                   |
| `-d, --deployment <name>`   | Target a specific deployment                                            |
| `-o, --organization <name>` | Target a specific organization                                          |
| `--api-token <token>`       | Dagster Cloud API token (alternative to `dg plus login`)                |
| `--view-graphql`            | Print GraphQL queries and responses to stderr for debugging             |

---

## Examples

```bash
# Get all logs for a run
dg api log get 8a7b6c5d-1234-5678-9abc-def012345678

# Filter to errors only
dg api log get <run-id> --level ERROR

# Filter to errors and warnings
dg api log get <run-id> --level ERROR --level WARNING

# Filter by event type
dg api log get <run-id> --event-type STEP_FAILURE

# Filter by step
dg api log get <run-id> --step my_asset

# Combine filters with JSON output
dg api log get <run-id> --level ERROR --step my_asset --json

# Paginate through large log sets
dg api log get <run-id> --limit 100
dg api log get <run-id> --limit 100 --cursor <cursor-from-previous>

# Target a specific deployment (typically unnecessary as `dg plus login` sets a default deployment)
dg api log get <run-id> --deployment prod
```

---

## See Also

- [../launch.md](../launch.md) - Launch assets (returns run ID for log retrieval)
- [../plus/login.md](../plus/login.md) - Authenticate with Dagster Plus
