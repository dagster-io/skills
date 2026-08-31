---
title: dg api asset
type: index
triggers:
  - "querying information about assets in Dagster Plus (metadata, events, DA evaluations, health status, etc.)"
---

# dg api asset Reference

Commands for querying information about assets in a Dagster Plus deployment.

> To **materialize** an asset on a deployed Dagster Plus environment, use the MCP server's `launch_asset_run` tool when it is connected, or [`dg api run launch`](../run/launch.md) otherwise. For local in-process materialization, see [`dg launch`](../../launch.md).

When the Dagster Plus MCP server is connected, prefer its tools for the operations it covers: `get_assets` (list) and `get_asset` (metadata plus a coarse health summary). `get_asset` fully replaces [`get`](./get.md), but only partially replaces [`get-health`](./get-health.md) — it reports each health status without the partition counts, check counts, or freshness lag behind it. See [general.md](../general.md) for how to choose. Note that MCP tools take asset keys as path segment lists (`["my_prefix", "my_asset"]`), not slash-separated strings.

The MCP server also resolves an asset's code location, which no `dg api asset` command does:

- `get_asset_location` — code location and repository for one asset
- `get_assets_locations` — the same for a list of assets

These answer "which code location defines this asset", and are distinct from [`dg api code-location`](../code-location/INDEX.md), which manages code locations themselves.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [dg api asset get-evaluations](./get-evaluations.md) — automation condition evaluation history for an asset
- [dg api asset get-events](./get-events.md) — materialization or observation event history for an asset
- [dg api asset get-health](./get-health.md) — getting asset health or runtime status
- [dg api asset get-partition-status](./get-partition-status.md) — partition materialization status or stats for an asset
- [dg api asset get](./get.md) — details about a specific asset
- [dg api asset list](./list.md) — querying which assets exist in a deployment
<!-- END GENERATED INDEX -->
