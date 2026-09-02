---
title: dg api run
type: index
triggers:
  - "run operations, run details, run events, run logs"
  - "listing runs, getting run info, fetching run events, compute logs"
  - "re-executing or retrying a failed run or backfill, from failure or from scratch"
  - "terminating or canceling an in-flight run"
---

# Run API Commands

Commands for interacting with Dagster runs via `dg api run`.

When the Dagster Plus MCP server is connected, prefer its tools for the commands it covers. See [general.md](../general.md) for how to choose.

| Command                         | MCP tool                             |
| ------------------------------- | ------------------------------------ |
| [`list`](./list.md)             | `list_runs`                          |
| [`get`](./get.md)               | `get_run`                            |
| [`get-events`](./get-events.md) | `get_run_logs`                       |
| [`launch`](./launch.md)         | `launch_job_run`, `launch_asset_run` |

`get_run_logs` maps to `get-events`, not to [`get-logs`](./get-logs.md) — despite its name it returns structured run events rather than compute logs.

The MCP server also offers run actions with no CLI counterpart. All three require `deployment_name`.

- `rerun_run` — re-execute a run. Params: `run_id` (required), `strategy`, `use_parent_run_tags` (default `true`), `extra_tags`.
- `rerun_backfill` — re-execute a backfill. Params: `backfill_id` (required), then the same as `rerun_run`.
- `terminate_run` — terminate an in-flight run. Params: `run_id` (required).

`strategy` is `FROM_FAILURE` (default), `ALL_STEPS`, or `FROM_ASSET_FAILURE`. Retrying only the failed portion of a run or backfill is the `FROM_FAILURE` default; pass `ALL_STEPS` to re-execute everything.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [dg api run get-events](./get-events.md) — debugging a run by reading its logs; filtering run events by level or step
- [dg api run get-logs](./get-logs.md) — fetching stdout stderr compute logs for a run; downloading step output logs
- [dg api run get](./get.md) — details about a specific run
- [dg api run launch](./launch.md) — materializing assets or launching jobs on a Dagster Plus deployment; remote asset materialization, remote job launch
- [dg api run list](./list.md) — listing or filtering runs
<!-- END GENERATED INDEX -->
