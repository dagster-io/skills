---
title: dg api alert-policy sync
triggers:
  - "syncing alert policies from YAML definition"
---

Sync alert policies from a YAML definition file. This will create, update, or remove alert policies to match the definition file.

```bash
dg api alert-policy sync <FILE>
```

- `<FILE>` — path to a YAML file defining the desired alert policies
