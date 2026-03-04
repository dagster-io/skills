---
description: "dg api run get-events: retrieve and filter run logs/events from Dagster Plus."
triggers:
  - "run logs, get logs, debug run"
  - "filter logs by level, event type, step"
---

# dg api run get-events

```bash
dg api run get-events <RUN_ID>
```

## General

Retrieve logs/events for a specific run from Dagster Plus.

For shared flags (`--json`, `--response-schema`, `--deployment`, `--organization`, `--api-token`, `--view-graphql`), see [general.md](../general.md).

## --level

Filter by log level: DEBUG, INFO, WARNING, ERROR, CRITICAL. Repeatable.

## --event-type

Filter by event type (e.g. `STEP_FAILURE`, `RUN_START`). Repeatable.

## --step

Filter by step key. Supports partial matching — `--step my_asset` will match step keys containing that substring. Repeatable.

## --limit

Maximum number of log entries to return.

## --cursor

Pagination cursor for retrieving additional logs.
