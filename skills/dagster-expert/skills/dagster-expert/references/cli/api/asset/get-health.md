---
title: dg api asset get-health
triggers:
  - "getting asset health or runtime status"
---

Get asset health and runtime status information.

```bash
dg api asset get-health <ASSET_KEY>
```

For prefixed asset keys, use slash-separated syntax: `dg api asset get-health my_prefix/my_asset`.

## Partial MCP equivalent

The MCP server's `get_asset` returns the same four status enums (`asset_health`, `materialization_status`, `freshness_status`, `asset_checks_status`) inside its `health` field, and is enough when you only need the status itself.

Params: `asset_key` (path segment list, e.g. `["my_prefix", "my_asset"]`), `deployment_name` (both required).

The `dg api asset get-health` command additionally returns the evidence behind each status, none of which the MCP server exposes:

- `health_metadata` — failing run ID, failed/missing/total partition counts, failed/warning/total check counts, last materialized timestamp
- `latest_materialization` — timestamp, run ID, and partition
- `freshness_info` — current lag, minutes late, maximum lag, cron schedule
- `checks_status` — check status with its counts

Use the `dg` command whenever you need to explain *why* an asset is degraded, not just that it is.
