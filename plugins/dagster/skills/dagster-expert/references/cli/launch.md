---
title: dg launch
triggers:
  - "materializing assets or executing jobs locally"
---

`dg launch` executes runs of assets or jobs **locally and in-process**. Useful for development. To launch a run on a remote Dagster Plus deployment, use the Dagster Plus MCP server's `launch_job_run` or `launch_asset_run` tool when it is connected, or [`dg api run launch`](./api/run/launch.md) otherwise.

```bash
dg launch --assets <selection>
dg launch --job <job_name>
```

See [Asset Selection Syntax](../asset-selection.md) for complete selection syntax.

## Partitions

```bash
dg launch --assets my_asset --partition 2024-01-15
dg launch --assets my_asset --partition-range "2024-01-01...2024-01-31"
```

**Note:** Use three dots (`...`) for inclusive ranges, not two dots.

## Configuration

```bash
# Inline JSON
dg launch --assets my_asset --config '{"limit": 100}'

# From file
dg launch --assets my_asset --config-file config.yaml
```
