---
title: dg api asset list
triggers:
  - "querying which assets exist in a deployment"
---

```bash
dg api asset list
```

- `--limit` / `--cursor` — pagination support (default 50, max 1000)

There is no way to filter by asset key prefix from the CLI.

## MCP equivalent

`get_assets` — prefer it when the Dagster Plus MCP server is connected.

Params: `deployment_name` (required), `prefix` (path segment list, e.g. `["warehouse"]`), `limit` (default 25, max 100), `cursor`.

Both return the same per-asset shape, including the coarse `health` summary described in [`get`](./get.md). One difference:

- `prefix` filters by asset key prefix, which the CLI cannot do. Prefer the MCP tool when narrowing to a subtree.
