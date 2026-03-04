---
description: "dg api run list: list runs with filtering and pagination from Dagster Plus."
triggers:
  - "list runs, show runs, all runs"
  - "run history, browse runs, recent runs"
---

# dg api run list

```bash
dg api run list
```

## General

List runs from Dagster Plus with optional filtering and pagination. `--status` is repeatable to filter by multiple statuses (e.g. `--status FAILURE --status CANCELED`).

For shared flags (`--json`, `--response-schema`, `--deployment`, `--organization`, `--api-token`, `--view-graphql`), see [general.md](../general.md).

## --limit

Number of runs to return (default: 50, max: 1000).

## --cursor

Pagination cursor (run ID) for retrieving additional runs.

## --status

Filter by run status: QUEUED, STARTING, STARTED, SUCCESS, FAILURE, CANCELING, CANCELED. Repeatable.

## --job

Filter by job name.
