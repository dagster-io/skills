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

## MCP equivalent

When the Dagster Plus MCP server is connected, use `get_alert_policies_as_document` to read the current policies as an editable config document, then `create_or_update_alert_policy` to write it back. Both take `deployment_name` (required); the write takes a `document`.

The semantics differ, so choose deliberately:

- `dg api alert-policy sync` is a full reconcile against a file — it also **deletes** any policy absent from that file.
- `create_or_update_alert_policy` only creates or updates what the document names, leaving everything else alone. Delete explicitly with `delete_alert_policy` (by policy name).

Prefer the MCP tools for targeted edits. Use the CLI when you want a file to be the single source of truth for the whole deployment.
