---
title: dg plus deploy
triggers:
  - "ad-hoc deployment to Dagster Plus"
---

Deploy code to Dagster Plus. This command is typically invoked automatically by CI pipelines created via `dg plus deploy configure`, but can be run manually for ad-hoc deployments.

```bash
dg plus deploy
```

In most cases, prefer using `dg plus deploy configure` to set up automated CI/CD deployments rather than running this command directly.
