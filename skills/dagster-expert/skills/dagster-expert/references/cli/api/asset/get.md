---
description: "dg api asset get: retrieve details for a specific asset from Dagster Plus."
triggers:
  - "asset details, get asset, asset info"
  - "asset status, asset metadata"
---

# dg api asset get

```bash
dg api asset get <ASSET_KEY>
```

## General

Retrieve details for a specific asset by asset key from Dagster Plus. For prefixed asset keys, use slash-separated syntax: `dg api asset get my_prefix/my_asset`.

For shared flags (`--json`, `--response-schema`, `--deployment`, `--organization`, `--api-token`, `--view-graphql`), see [general.md](../general.md).

## --status

Include materialization status information. Not included by default as it requires additional API calls.
