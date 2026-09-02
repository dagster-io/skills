---
title: dg api run launch
triggers:
  - "materializing assets or launching jobs on a Dagster Plus deployment"
  - "remote asset materialization, remote job launch"
---

`dg api run launch` launches a run on a remote Dagster Plus deployment. Use this for materializing assets or launching jobs against your deployed environment. For local in-process execution during development, use [`dg launch`](../../launch.md) instead.

```bash
dg api run launch --location <LOCATION> --job <JOB_NAME>
dg api run launch --location <LOCATION> --asset-key <KEY> [--asset-key <KEY> ...]
```

- `--location` / `-l` (required) — code location name
- `--repository` / `-r` — repository name (default: `__repository__`, which is correct for most projects)
- `--job` / `-j` — name of the job to launch
- `--asset-key` — asset key to materialize. Repeatable. Use slash-separated syntax for prefixed keys (e.g. `my_prefix/my_asset`). The asset selection DSL (`group:`, `tag:`, `+upstream`) is not supported here — list explicit keys only. For DSL evaluation, use `dg launch` against a local project, or discover keys first with `dg api asset list`.
- `--partition` — single partition key. Partition ranges/backfills are not yet supported.
- `--tag` — tag to attach to the run as `key=value`. Repeatable.
- `--config-json` — JSON string of run config to use for the run
- `--wait` / `-w` — block until the run reaches a terminal status. Exits non-zero on `FAILURE` or `CANCELED`.
- `--interval` / `-i` — poll interval in seconds when `--wait` is set (default: 30)

At least one of `--job` or `--asset-key` must be provided.

## MCP equivalents

The MCP server splits this command into two tools. Prefer them when it is connected, and pick by what you are launching:

| Launching                             | CLI                     | MCP tool                                |
| ------------------------------------- | ----------------------- | --------------------------------------- |
| A job                                 | `--job`                 | `launch_job_run`                        |
| A job, narrowed to some of its assets | `--job` + `--asset-key` | `launch_job_run` with `asset_selection` |
| An ad hoc asset selection             | `--asset-key` only      | `launch_asset_run`                      |

`launch_asset_run` materializes assets that are not tied to a named job. It launches the implicit asset job under the hood, so all the assets must live in the same repository and code location.

Shared params, both tools: `repository_location_name` and `repository_name` (required, replacing `--location`/`--repository`), `deployment_name` (required), plus optional `run_config`, `tags`, and `partition`.

- `launch_job_run` additionally requires `job_name`, and takes an optional `asset_selection` to run a subset of that job's assets.
- `launch_asset_run` requires `asset_selection` with at least one key, and takes no `job_name`.

### Finding `repository_name` and `repository_location_name`

Both are required, and unlike the CLI's `--repository` there is no default to fall back on. Resolve them before calling:

- **Launching assets** — call `get_asset_location` (or `get_assets_locations` for several). It returns `repository_name` and `code_location_name`; pass that `code_location_name` as `repository_location_name`. The two names refer to the same thing.
- **Launching a job** — run [`dg api job list`](../job.md) and read the job's `repository_origin`, formatted `location@repository`. This discovery step is a CLI call even in an otherwise MCP-based workflow.

`list_code_locations` is not enough on its own: it returns location names without the repository name inside each location.

For `launch_asset_run`, confirm every key resolves to the same repository and location before calling — it launches one implicit asset job, so a mixed selection cannot be satisfied.

Differences from the CLI:

- `asset_selection` takes path segment lists (`[["my_prefix", "my_asset"]]`), not the slash-separated strings the CLI's `--asset-key` takes. Pass the segments unjoined.
- `tags` is a dict (`{"key": "value"}`) rather than the repeatable `--tag key=value`.
- `partition` is a single key, matching the CLI. Partition ranges and backfills are not supported by either.
- There is no `--wait`. Poll the returned run with `get_run` to await a terminal status.
- The asset selection DSL (`group:`, `tag:`, `+upstream`) is not supported here either — list explicit keys, discovering them first with `get_assets`, or use the CLI.
