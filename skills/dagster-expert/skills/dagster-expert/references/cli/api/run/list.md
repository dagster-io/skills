---
title: dg api run list
triggers:
  - "listing or filtering runs"
---

```bash
dg api run list
```

- `--status` — filter by run status: QUEUED, STARTING, STARTED, SUCCESS, FAILURE, CANCELING, CANCELED. Repeatable (e.g. `--status FAILURE --status CANCELED`).
- `--job` — filter by job name

## MCP equivalent

`list_runs` — prefer it when the Dagster Plus MCP server is connected.

Params: `deployment_name` (required), `status`, `job_name`, `limit` (max 100), `cursor`.

`status` accepts a single value, unlike the repeatable `--status` flag. To filter on several statuses, call the tool once per status or use the CLI.
