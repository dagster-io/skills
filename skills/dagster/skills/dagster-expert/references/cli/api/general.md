---
title: "dg api: General"
triggers:
  - "always read before using any dg api subcommand"
  - "choosing between the Dagster Plus MCP server and the dg api CLI"
---

# Choosing between the MCP server and `dg api`

Dagster Plus exposes the same resources two ways: the **Dagster Plus MCP server** and the **`dg api` CLI**. When both can do the job, prefer the MCP server — it returns structured data directly, needs no shell or `dg plus login`, and avoids parsing CLI output.

Decide once, at the start of the task:

1. **Check whether the MCP server is connected** by looking for its tools in your available tool list. Do not shell out to test for it. Clients namespace MCP tools under a server name the user chose, so match on the trailing tool name rather than an exact string — `list_deployments` may appear as `mcp__dagster__list_deployments` or similar. Look for the distinctive names (`list_deployments`, `get_assets`, `launch_asset_run`, `get_alert_policies_as_document`) rather than generic ones like `get_run` or `list_runs`, which another server could also define.
2. **If those tools are present**, use them for every operation they cover. Each `dg api` reference file names its MCP counterpart under an "MCP equivalent" heading.
3. **If they are absent**, use the `dg api` commands documented here.

**A reference file with no "MCP equivalent" section is CLI-only**, meaning the server exposes no tool for that command. Absence is the signal; there are no explicit "no equivalent" notes to look for.

## Falling back to the CLI

Falling back is expected, not a failure. The server covers most read paths but leaves real gaps — compute logs, server-side event filtering, fetching a single Issue, asset events and evaluations, schedules, sensors, and secrets among them. Use the CLI whenever the operation you need has no tool, even in the middle of an otherwise MCP-based task.

What to avoid is switching paths for the *same* call: do not launch a run through MCP and then launch it again through the CLI, or page through one result set alternating between them.

When you do fall back, keep both paths pointed at the same place:

- **Pass `--deployment <name>` explicitly**, using the same `deployment_name` you gave the MCP tools. Otherwise the CLI targets whatever `dg plus login` configured, which may be a different deployment.
- **Watch for an organization mismatch.** The MCP server is bound to one organization by its own credentials and exposes no tool reporting which one. If `list_deployments` and `dg api deployment list` disagree, they are pointed at different organizations — say so rather than merging the two sets of results.

## When an MCP tool fails

- **Authentication or authorization errors** mean the server's session is not valid for the request. Return to the user to ask if they want to execute the equivalent `dg api` command if one exists; otherwise tell the user the Dagster Plus MCP server needs to be reconnected.
- **Entitlement errors** ("not available for your organization") mean the feature is disabled for that organization, not that the call was malformed. The CLI reaches the same backend and will fail identically, so report it rather than retrying there.

## Using the MCP tools

- Nearly every tool takes a required `deployment_name`. Call `list_deployments` first if you don't already know it.
- Asset keys are passed as **path segment lists** (`["warehouse", "orders"]`), not the slash-separated strings the CLI uses (`warehouse/orders`).
- Paginated tools (`list_runs`, `get_assets`, `get_run_logs`) return a cursor; pass it back to fetch the next page.

## Using the `dg api` CLI

All `dg api` subcommands support `--json`, `--response-schema`, `--deployment`, `--organization`, `--api-token`, and `--view-graphql`.

- `--response-schema` — prints the JSON schema for the command's response and exits. Run this before writing any parsing logic to get exact field names, types, and valid enum values.
- `--view-graphql` — prints GraphQL queries and responses to stderr, useful for debugging.

### Tips

For complex debugging/analysis workflows, ALWAYS use `--json` to get machine-readable output. Pipe into `jq` (recommended) or other tools for further processing.

Flags like `--deployment`/`--organization`/`--api-token` are typically not needed when authenticated via `dg plus login`. The exception is falling back from the MCP server mid-task: pass `--deployment` explicitly there, since the login default and the deployment you were querying through MCP need not be the same.
