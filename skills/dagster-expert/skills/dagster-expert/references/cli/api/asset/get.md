---
description: "dg api asset get: retrieve details for a specific asset from Dagster Plus."
triggers:
  - "asset details, get asset, asset info"
  - "asset status, asset metadata"
---

# dg api asset get - Asset Details

Get details for a specific asset by asset key from Dagster Plus. Requires authentication via `dg plus login` or `--api-token`. Information about its current status may optionally be included, but is not included by default as it requires additional API calls.

```bash
dg api asset get <ASSET_KEY>
```

---

## Options

| Option                      | Description                                                 |
| --------------------------- | ----------------------------------------------------------- |
| `--status`                  | Include materialization status information                  |
| `--json`                    | Output in JSON format                                       |
| `-d, --deployment <name>`   | Target a specific deployment                                |
| `-o, --organization <name>` | Target a specific organization                              |
| `--api-token <token>`       | Dagster Cloud API token (alternative to `dg plus login`)    |
| `--view-graphql`            | Print GraphQL queries and responses to stderr for debugging |

---

## Examples

```bash
# Get details for an asset
dg api asset get my_asset

# Get details for a prefixed asset key
dg api asset get my_prefix/my_asset

# Include materialization status
dg api asset get my_asset --status

# Output as JSON
dg api asset get my_asset --json

# Target a specific deployment (typically unnecessary as `dg plus login` sets a default deployment)
dg api asset get my_asset --deployment prod
```

---

## See Also

- [list.md](list.md) - List all assets
- [get-evaluations.md](get-evaluations.md) - Get automation condition evaluations for an asset
- [get-events.md](get-events.md) - Get materialization and observation events for an asset
- [../../plus/login.md](../../plus/login.md) - Authenticate with Dagster Plus
