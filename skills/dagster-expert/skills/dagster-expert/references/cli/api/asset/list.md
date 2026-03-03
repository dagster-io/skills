---
description: "dg api asset list: list assets with pagination from Dagster Plus."
triggers:
  - "list assets, show assets, all assets"
  - "asset inventory, browse assets"
---

# dg api asset list

```bash
dg api asset list
```

## General

List assets from Dagster Plus with pagination support.

For shared flags (`--json`, `--response-schema`, `--deployment`, `--organization`, `--api-token`, `--view-graphql`), see [general.md](../general.md).

## --limit

Maximum number of assets to return.

## --cursor

Pagination cursor for retrieving additional assets.

## --status

Include detailed status information in the response.
