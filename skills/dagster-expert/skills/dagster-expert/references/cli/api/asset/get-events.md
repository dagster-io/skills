---
description: "dg api asset get-events: retrieve materialization and observation events for an asset from Dagster Plus."
triggers:
  - "asset events, materialization events, observation events"
  - "asset history, asset partitions, event log"
---

# dg api asset get-events

```bash
dg api asset get-events <ASSET_KEY>
```

## General

Retrieve materialization and observation events for a specific asset from Dagster Plus.

For shared flags (`--json`, `--response-schema`, `--deployment`, `--organization`, `--api-token`, `--view-graphql`), see [general.md](../general.md).

## --event-type

Filter by event type (e.g. `ASSET_MATERIALIZATION`, `ASSET_OBSERVATION`).

## --limit

Maximum number of events to return.

## --before

Return events before this timestamp. Use with `--limit` to paginate through results chronologically.

## --partition

Filter events by partition key.
