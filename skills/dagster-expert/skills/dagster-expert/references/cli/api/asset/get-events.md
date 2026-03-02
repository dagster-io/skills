---
description: "dg api asset get-events: retrieve materialization and observation events for an asset from Dagster Plus."
triggers:
  - "asset events, materialization events, observation events"
  - "asset history, asset partitions, event log"
---

# dg api asset get-events - Asset Events

Get materialization and observation events for a specific asset from Dagster Plus. Requires authentication via `dg plus login` or `--api-token`.

```bash
dg api asset get-events <ASSET_KEY>
```

---

## Options

| Option                      | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| `--event-type <type>`       | Filter by event type (e.g. `ASSET_MATERIALIZATION`, `ASSET_OBSERVATION`) |
| `--limit <n>`               | Maximum number of events to return                                       |
| `--before <timestamp>`      | Return events before this timestamp                                      |
| `--partition <partition>`   | Filter events by partition key                                           |
| `--json`                    | Output in JSON format                                                    |
| `-d, --deployment <name>`   | Target a specific deployment                                             |
| `-o, --organization <name>` | Target a specific organization                                           |
| `--api-token <token>`       | Dagster Cloud API token (alternative to `dg plus login`)                 |
| `--view-graphql`            | Print GraphQL queries and responses to stderr for debugging              |

---

## Examples

```bash
# Get events for an asset
dg api asset get-events my_asset

# Filter to materialization events only
dg api asset get-events my_asset --event-type ASSET_MATERIALIZATION

# Filter to observation events only
dg api asset get-events my_asset --event-type ASSET_OBSERVATION

# Limit the number of results
dg api asset get-events my_asset --limit 20

# Filter by partition
dg api asset get-events my_asset --partition 2024-01-01

# Combine filters with JSON output
dg api asset get-events my_asset --event-type ASSET_MATERIALIZATION --partition 2024-01-01 --json

# Paginate by timestamp
dg api asset get-events my_asset --limit 100 --before <timestamp-from-previous>

# Target a specific deployment (typically unnecessary as `dg plus login` sets a default deployment)
dg api asset get-events my_asset --deployment prod
```

---

## See Also

- [get.md](get.md) - Get asset details
- [get-evaluations.md](get-evaluations.md) - Get automation condition evaluations for an asset
- [list.md](list.md) - List all assets
- [../../plus/login.md](../../plus/login.md) - Authenticate with Dagster Plus
