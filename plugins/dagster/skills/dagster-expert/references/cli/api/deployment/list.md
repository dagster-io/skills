---
title: dg api deployment list
triggers:
  - "listing deployments in Dagster Plus"
---

```bash
dg api deployment list
```

## MCP equivalent

`list_deployments` — prefer it when the Dagster Plus MCP server is connected.

Params: `deployment_type` (`"production"` or `"branch"`), `limit` (max 100, branch deployments only).

Because most other MCP tools require a `deployment_name`, this is usually the first call in an MCP-based workflow.
