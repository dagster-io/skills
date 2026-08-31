---
title: dg api code-location
type: index
triggers:
  - "managing code locations in Dagster Plus (add, delete, list, inspect)"
---

# dg api code-location Reference

Commands for managing code locations in a Dagster Plus deployment.

When the Dagster Plus MCP server is connected, prefer `list_code_locations` over `dg api code-location list`. See [general.md](../general.md) for how to choose.

To find which code location defines a given **asset**, use the MCP server's `get_asset_location` or `get_assets_locations` instead; those answer a different question and have no CLI counterpart.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [dg api code-location add](./add.md) — adding or updating a code location in Dagster Plus
- [dg api code-location delete](./delete.md) — deleting a code location from Dagster Plus
- [dg api code-location get](./get.md) — details about a specific code location
- [dg api code-location list](./list.md) — listing code locations in Dagster Plus
<!-- END GENERATED INDEX -->
