---
title: dg api asset get
triggers:
  - "details about a specific asset"
---

```bash
dg api asset get <ASSET_KEY>
```

For prefixed asset keys, use slash-separated syntax: `dg api asset get my_prefix/my_asset`.

## MCP equivalent

`get_asset` — prefer it when the Dagster Plus MCP server is connected.

Params: `asset_key` (path segment list, e.g. `["my_prefix", "my_asset"]`), `deployment_name` (both required).

The response includes a `health` summary — `asset_health`, `materialization_status`, `freshness_status`, and `asset_checks_status` as bare status enums — plus `latest_materialization_timestamp` and `latest_failed_to_materialize_timestamp`. For the detail behind those statuses (failed run ID, partition and check counts, freshness lag), see [`dg api asset get-health`](./get-health.md).
