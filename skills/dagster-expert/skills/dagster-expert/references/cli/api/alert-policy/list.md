---
title: dg api alert-policy list
triggers:
  - "listing alert policies in Dagster Plus"
---

List alert policies for a deployment.

```bash
dg api alert-policy list
```

## MCP equivalent

`list_alert_policies` — prefer it when the Dagster Plus MCP server is connected.

Params: `deployment_name` (required).

The MCP server has additional functionality, with no CLI counterpart for any of these:

- `get_alert_policy` — fetch one policy by ID
- `get_alert_policies_for_job` — policies currently applying to a job
- `get_alert_policy_notifications` — notification history for a policy
- `get_run_alert_notifications` — alerts that fired for a given run
- `delete_alert_policy` — delete one policy by name
