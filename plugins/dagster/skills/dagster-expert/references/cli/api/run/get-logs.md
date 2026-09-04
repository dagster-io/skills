---
title: dg api run get-logs
triggers:
  - "fetching stdout stderr compute logs for a run; downloading step output logs"
---

```bash
dg api run get-logs <RUN_ID>
```

- `--step-key` — filter to a specific step.
- `--link-only` — return download URLs instead of log content.
- `--max-bytes` — maximum bytes of log content per step.
- `--cursor` — cursor for paginating log content.
- `--json` — output in JSON format.

## Not the same as MCP `get_run_logs`

Despite the name, the MCP server's `get_run_logs` returns structured run events — the equivalent of [`dg api run get-events`](./get-events.md) — not the stdout/stderr compute logs this command fetches.
