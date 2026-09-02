---
title: dg api alert-policy
type: index
triggers:
  - "managing alert policies in Dagster Plus (listing, syncing from YAML)"
---

# dg api alert-policy Reference

Commands for managing alert policies in Dagster Plus.

When the Dagster Plus MCP server is connected, prefer its alert tools — it covers more than the CLI, including reading a single policy, finding the policies that apply to a job, and notification history. See [general.md](../general.md) for how to choose and [sync.md](./sync.md) for the one behavioral difference: `dg api alert-policy sync` deletes policies missing from the file, while `create_or_update_alert_policy` does not.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [dg api alert-policy list](./list.md) — listing alert policies in Dagster Plus
- [dg api alert-policy sync](./sync.md) — syncing alert policies from YAML definition
<!-- END GENERATED INDEX -->
