---
description: "dg api asset list: list assets with pagination from Dagster Plus."
triggers:
  - "list assets, show assets, all assets"
  - "asset inventory, browse assets"
---

# dg api asset list - List Assets

List assets from Dagster Plus with pagination support. Requires authentication via `dg plus login` or `--api-token`.

```bash
dg api asset list
```

---

## Options

| Option                      | Description                                                 |
| --------------------------- | ----------------------------------------------------------- |
| `--limit <n>`               | Maximum number of assets to return                          |
| `--cursor <cursor>`         | Pagination cursor for retrieving additional assets          |
| `--status`                  | Include detailed status information in the response         |
| `--json`                    | Output in JSON format                                       |
| `-d, --deployment <name>`   | Target a specific deployment                                |
| `-o, --organization <name>` | Target a specific organization                              |
| `--api-token <token>`       | Dagster Cloud API token (alternative to `dg plus login`)    |
| `--view-graphql`            | Print GraphQL queries and responses to stderr for debugging |

---

## Examples

```bash
# List all assets
dg api asset list

# Limit the number of results
dg api asset list --limit 50

# Include status information
dg api asset list --status

# Paginate through results
dg api asset list --limit 100
dg api asset list --limit 100 --cursor <cursor-from-previous>

# Output as JSON
dg api asset list --json

# Target a specific deployment (typically unnecessary as `dg plus login` sets a default deployment)
dg api asset list --deployment prod
```

---

## See Also

- [get.md](get.md) - Get details for a specific asset
- [get-evaluations.md](get-evaluations.md) - Get automation condition evaluations for an asset
- [get-events.md](get-events.md) - Get materialization and observation events for an asset
- [../../plus/login.md](../../plus/login.md) - Authenticate with Dagster Plus
