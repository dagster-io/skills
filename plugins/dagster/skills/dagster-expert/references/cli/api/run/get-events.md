---
title: dg api run get-events
triggers:
  - "debugging a run by reading its logs; filtering run events by level or step"
---

```bash
dg api run get-events <RUN_ID>
```

- `--level` — filter by log level: DEBUG, INFO, WARNING, ERROR, CRITICAL. Repeatable.
- `--event-type` — filter by event type (e.g. `STEP_FAILURE`, `RUN_START`). Repeatable.
- `--step` — filter by step key. Supports partial matching — `--step my_asset` will match step keys containing that substring. Repeatable.
- `--limit` — maximum number of events to return.
- `--cursor` — pagination cursor for retrieving more events.

## MCP equivalent

`get_run_logs` — prefer it when the Dagster Plus MCP server is connected. Despite the name, it returns this command's structured run events, not the compute logs from `dg api run get-logs`.

Params: `run_id`, `deployment_name` (required), `limit` (max 100), `cursor`.

It has no equivalent of `--level`, `--event-type`, or `--step`. Filter the returned events yourself, or use the CLI when server-side filtering matters for a high-volume run.
