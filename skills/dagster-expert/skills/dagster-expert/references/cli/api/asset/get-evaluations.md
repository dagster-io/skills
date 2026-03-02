---
description: "dg api asset get-evaluations: retrieve automation condition evaluation records for an asset from Dagster Plus."
triggers:
  - "declarative automation, automation condition history"
  - "declarative automation, automation condition debugging"
---

# dg api asset get-evaluations - Automation Condition Evaluations

Get automation condition evaluation records for a specific asset from Dagster Plus. Requires authentication via `dg plus login` or `--api-token`. Returns a list of evaluation records for the asset.

```bash
dg api asset get-evaluations <ASSET_KEY>
```

## Detailed debugging information

Each evaluation record contains detailed information about the tree of conditions that were evaluated to produce the final result. This information is dense and should only be included when a small number of records are being processed to avoid overly-large text responses.

---

## Options

| Option                      | Description                                                 |
| --------------------------- | ----------------------------------------------------------- |
| `--limit <n>`               | Maximum number of evaluation records to return              |
| `--cursor <cursor>`         | Pagination cursor for retrieving additional records         |
| `--include-nodes`           | Include individual evaluation nodes in the response         |
| `--json`                    | Output in JSON format                                       |
| `-d, --deployment <name>`   | Target a specific deployment                                |
| `-o, --organization <name>` | Target a specific organization                              |
| `--api-token <token>`       | Dagster Cloud API token (alternative to `dg plus login`)    |
| `--view-graphql`            | Print GraphQL queries and responses to stderr for debugging |

---

## Examples

```bash
# Get evaluations for an asset
dg api asset get-evaluations my_asset

# Limit the number of results
dg api asset get-evaluations my_asset --limit 10

# Include detailed evaluation nodes
dg api asset get-evaluations my_asset --include-nodes

# Paginate through results
dg api asset get-evaluations my_asset --limit 50
dg api asset get-evaluations my_asset --limit 50 --cursor <cursor-from-previous>

# Output as JSON
dg api asset get-evaluations my_asset --json

# Target a specific deployment (typically unnecessary as `dg plus login` sets a default deployment)
dg api asset get-evaluations my_asset --deployment prod
```

---

## See Also

- [get.md](get.md) - Get asset details
- [get-events.md](get-events.md) - Get materialization and observation events for an asset
- [list.md](list.md) - List all assets
- [../../plus/login.md](../../plus/login.md) - Authenticate with Dagster Plus
