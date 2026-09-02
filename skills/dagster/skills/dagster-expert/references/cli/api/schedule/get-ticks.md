---
title: dg api schedule get-ticks
triggers:
  - "viewing schedule tick history; checking schedule evaluation results and failures"
---

```bash
dg api schedule get-ticks <SCHEDULE_NAME>
```

- `--status` — filter by tick status: STARTED, SKIPPED, SUCCESS, FAILURE. Repeatable.
- `--limit` — maximum number of ticks to return (default: 25).
- `--cursor` — pagination cursor.
- `--before` — filter ticks before this Unix timestamp.
- `--after` — filter ticks after this Unix timestamp.
- `--json` — output in JSON format.
