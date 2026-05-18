---
title: dg api job
triggers:
  - "listing or inspecting jobs in Dagster Plus"
---

# dg api job Reference

Commands for querying jobs in a Dagster Plus deployment.

## dg api job list

```bash
dg api job list
```

Lists all jobs in the deployment.

## dg api job get

```bash
dg api job get <JOB_NAME>
```

Returns details for a specific job in the deployment.

## Launching jobs

To launch a job on a deployed Dagster Plus environment, see [`dg api run launch`](./run/launch.md). For local in-process execution during development, see [`dg launch`](../launch.md).
