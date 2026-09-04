---
title: dg api issue
type: index
triggers:
  - "listing Dagster Plus Issues, fetching a specifc Dagster Plus Issue"
---

# dg api issue Reference

Commands for interacting with Dagster Plus Issues.

A Dagster Plus Issue is a record of a problem within the Users' Dagster deployment like you would find in an issue tracking tool. Issues have the following fields: ID, title, description, status, createdBy, links to related Runs and Assets, and additional context about the Issue, including any previous conversations about the problem.

Some organizations do not have access to Dagster Plus Issues. If you get an Unauthorized error indicating that Issues are not available, inform the user that Issues are not enabled for their organization.

## MCP equivalents

Prefer these tools when the Dagster Plus MCP server is connected. Every tool requires `deployment_name` in addition to the params listed.

| Command                    | MCP tool                 | Params                                                                                 |
| -------------------------- | ------------------------ | -------------------------------------------------------------------------------------- |
| `dg api issue list`        | `list_issues`            | `statuses`, `created_after`, `created_before`, `limit` (default 10, max 100), `cursor` |
| `dg api issue create`      | `create_issue`           | `title`, `description` (both required), `status`, `run_id`, `asset_key`                |
| `dg api issue update`      | `update_issue`           | `issue_id` (required), `status`, `title`, `description`, `context`                     |
| `dg api issue add-link`    | `add_link_to_issue`      | `issue_id` (required), `run_id`, `asset_key`                                           |
| `dg api issue remove-link` | `remove_link_from_issue` | `issue_id` (required), `run_id`, `asset_key`                                           |

The params look like the flags documented below but are shaped differently in five places:

- **Asset keys** are path segment lists (`["my", "asset"]`), not slash-separated strings.
- **`statuses` is a single list** (`["OPEN", "TRIAGE"]`), not a repeatable `--status` flag.
- **`created_after` and `created_before` are Unix timestamps** (floats), not the `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS` dates the CLI parses. Convert before calling.
- **`run_id` on the link tools must be a UUID string.**
- **`create_issue` can attach an origin at creation.** Passing `run_id` or `asset_key` links that run or asset as part of the same call — the CLI cannot, and needs `create` followed by `add-link`.

The guidance below on how to write a title, a description, and appended context applies to the MCP tools as well.

## Get a specific Dagster Plus Issue

```bash
dg api issue get <ID>
```

- `<ID>` — the ID of the Issue to get

## List Issues for a deployment.

```bash
dg api issue list
```

Issues can be filtered by:

- Status: `--status` - options are `OPEN`, `CLOSED`, `TRIAGE`, `CANCELED`. Multiple `--status` filters can be specified
- Created before: `--created-before` - filter to Issues created before this date
- Created after: `--created-after` - filter to Issues created after this date

The response will contain a list of `limit` Issues in chronologically descending order. To fetch the next page of Issues, use the ID of the oldest Issue as the cursor.

## Create a Dagster Plus Issue

```bash
dg api issue create --title <title> --description <description> --status <status>
```

- `<title>` - The title should be short and clearly state the problem to fix so that the reader quickly understands the cause of the problem. Do not mention specific run ids or other downstream impacts.
- `<description>` - The description should be a total of 2-4 bullet points that outline the root cause of the problem and next steps.
- `--status` (optional) - updates the status of the Issue. One of `OPEN`, `CLOSED`, `TRIAGE`, `CANCELED`

## Update a Dagster Plus Issue

```bash
dg api issue update <ID>
```

- `<ID>` - The ID of the Issue to update
- `--status` (optional) - updates the status of the Issue. One of `OPEN`, `CLOSED`, `TRIAGE`, `CANCELED`
- `--title` (optional) - updates the title of the Issue
- `--description` (optional) - updates the description of the Issue
- `--context` (optional) - replaces the additional context stored about this Issue. If you want to append to the current context, fetch the Issue first, append to the context string with the new information, then call the `update` command with the resulting context.

## Link a run or asset to an Issue

```bash
dg api issue add-link <ID>
```

- `<ID>` - The ID of the Issue
- `--run-id` (optional) - The run id of the run to link to the Issue
- `--asset-key` (optional) - The asset key of the asset to link to the Issue. The asset key should be slash-separated (e.g. `my/asset`)

## Remove a linked run or asset from an Issue

```bash
dg api issue remove-link <ID>
```

- `<ID>` - The ID of the Issue
- `--run-id` (optional) - The run id of the run to remove from the Issue
- `--asset-key` (optional) - The asset key of the asset to remove from to the Issue. The asset key should be slash-separated (e.g. `my/asset`)

<!-- BEGIN GENERATED INDEX -->


<!-- END GENERATED INDEX -->
