---
title: dg api asset get-evaluations
triggers:
  - "automation condition evaluation history for an asset"
---

```bash
dg api asset get-evaluations <ASSET_KEY>
```

`--include-nodes` — includes individual evaluation nodes in the response. Warning: this produces dense output with the full tree of conditions evaluated for each record. Only use when processing a small number of records.
