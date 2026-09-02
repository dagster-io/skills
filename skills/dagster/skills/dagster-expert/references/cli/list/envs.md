---
title: dg list envs
triggers:
  - "seeing which environment variables the project requires"
---

List environment variables from the `.env` file of the current project. Shows variable name, whether it is set locally, and which components use it.

```bash
dg list envs
```

With Dagster Plus authentication (`dg plus login`), also shows deployment scope status (Dev/Branch/Full).
