---
description: "dg api run list: list runs with filtering and pagination from Dagster Plus."
triggers:
  - "list runs, show runs, all runs"
  - "run history, browse runs, recent runs"
---

# dg api run list - List Runs

List runs from Dagster Plus with optional filtering and pagination. Requires authentication via `dg plus login` or `--api-token`.

```bash
dg api run list
```

---

## Options

| Option                      | Description                                                                                         |
| --------------------------- | --------------------------------------------------------------------------------------------------- |
| `--limit <n>`               | Number of runs to return (default: 50, max: 1000)                                                   |
| `--cursor <cursor>`         | Pagination cursor (run ID) for retrieving additional runs                                           |
| `--status <status>`         | Filter by run status: QUEUED, STARTING, STARTED, SUCCESS, FAILURE, CANCELING, CANCELED. Repeatable. |
| `--job <name>`              | Filter by job name                                                                                  |
| `--json`                    | Output in JSON format                                                                               |
| `-d, --deployment <name>`   | Target a specific deployment                                                                        |
| `-o, --organization <name>` | Target a specific organization                                                                      |
| `--api-token <token>`       | Dagster Cloud API token (alternative to `dg plus login`)                                            |
| `--view-graphql`            | Print GraphQL queries and responses to stderr for debugging                                         |

---

## Examples

```bash
# List recent runs (default limit: 50)
dg api run list

# Limit the number of results
dg api run list --limit 10

# Filter by status
dg api run list --status FAILURE

# Filter by multiple statuses
dg api run list --status FAILURE --status CANCELED

# Filter by job name
dg api run list --job my_daily_job

# Combine filters
dg api run list --status SUCCESS --job my_daily_job --limit 20

# Paginate through results
dg api run list --limit 100
dg api run list --limit 100 --cursor <run-id-from-previous>

# Output as JSON
dg api run list --json

# Target a specific deployment (typically unnecessary as `dg plus login` sets a default deployment)
dg api run list --deployment prod
```

---

## See Also

- [get-events.md](get-events.md) - Get logs/events for a specific run
- [../../plus/login.md](../../plus/login.md) - Authenticate with Dagster Plus
