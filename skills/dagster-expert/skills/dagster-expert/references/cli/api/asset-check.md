---
title: dg api asset-check
triggers:
  - "querying asset checks or asset check execution history in Dagster Plus"
---

# dg api asset-check Reference

Commands for querying asset checks in a Dagster Plus deployment.

## dg api asset-check list

```bash
dg api asset-check list --asset-key <ASSET_KEY>
```

- `--asset-key` (required) — slash-separated asset key (e.g. `my/asset`)

## dg api asset-check get-executions

```bash
dg api asset-check get-executions --asset-key <ASSET_KEY> --check-name <CHECK_NAME>
```

- `--asset-key` (required) — slash-separated asset key (e.g. `my/asset`)
- `--check-name` (required) — name of the asset check
- `--limit` — max results (default: 25)
- `--cursor` — pagination cursor
