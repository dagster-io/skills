---
title: dg api asset get-events
triggers:
  - "materialization or observation event history for an asset"
---

```bash
dg api asset get-events <ASSET_KEY>
```

- `--event-type` — filter by event type (e.g. `ASSET_MATERIALIZATION`, `ASSET_OBSERVATION`)
- `--partition` — filter events by partition key
- `--before` — return events before this timestamp; use with `--limit` to paginate chronologically
