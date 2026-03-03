---
description: "dg api asset get-evaluations: retrieve automation condition evaluation records for an asset from Dagster Plus."
triggers:
  - "declarative automation, automation condition history"
  - "declarative automation, automation condition debugging"
---

# dg api asset get-evaluations

```bash
dg api asset get-evaluations <ASSET_KEY>
```

## General

Retrieve automation condition evaluation records for a specific asset from Dagster Plus.

For shared flags (`--json`, `--response-schema`, `--deployment`, `--organization`, `--api-token`, `--view-graphql`), see [general.md](../general.md).

## --limit

Maximum number of evaluation records to return.

## --cursor

Pagination cursor for retrieving additional records.

## --include-nodes

Include individual evaluation nodes in the response. Warning: this produces dense output with the full tree of conditions evaluated for each record. Only use when processing a small number of records.
