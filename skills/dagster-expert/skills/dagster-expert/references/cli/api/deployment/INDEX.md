---
title: dg api deployment
type: index
triggers:
  - "managing Dagster Plus deployments (create, delete, list, settings)"
---

# dg api deployment Reference

Commands for managing Dagster Plus deployments and their settings.

When the Dagster Plus MCP server is connected, prefer `list_deployments` over `dg api deployment list` and `get_deployment_info` over `dg api deployment get`. See [general.md](../general.md) for how to choose. Since most MCP tools require a `deployment_name`, `list_deployments` is usually the first call in an MCP workflow.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [dg api deployment delete](./delete.md) — deleting a deployment from Dagster Plus
- [dg api deployment get](./get.md) — details about a specific deployment
- [dg api deployment list](./list.md) — listing deployments in Dagster Plus
- [dg api deployment settings-get](./settings-get.md) — getting deployment-level settings in Dagster Plus
- [dg api deployment settings-set](./settings-set.md) — setting deployment settings in Dagster Plus
<!-- END GENERATED INDEX -->
