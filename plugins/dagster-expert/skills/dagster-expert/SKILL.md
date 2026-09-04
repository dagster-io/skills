---
name: dagster-expert
description:
  Use for any task involving Dagster, the dg CLI, assets, materialization, components, data tools or data
  pipelines, matching the situations the Dagster skill handles. This is the deprecated dagster-expert
  plugin. It carries no Dagster guidance and exists only to tell the user to move to the dagster plugin.
---

## This plugin has been replaced

The user is running the deprecated `dagster-expert` plugin. It no longer carries the Dagster skill — that now ships in the `dagster` plugin.

Do not answer the user's Dagster question from memory. Tell them to run:

```
/plugin install dagster@dagster

/plugin uninstall dagster-expert
```
if they are in a Claude code session. If they are in a Cursor session, instruct them to uninstall the current Dagster plugin and re-install it.

Both commands matter. Installing `dagster` without uninstalling `dagster-expert` leaves two plugins providing a skill named `dagster-expert`, and this deprecated one may be chosen instead of the real one. If the user reaches this notice after already installing `dagster`, that is what has happened — have them uninstall `dagster-expert` and retry.

Nothing else changes: the skill keeps the name `dagster-expert` and is still invoked as `/dagster-expert`.
