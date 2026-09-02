---
title: Dagster Plus insights metrics
triggers:
  - "Dagster credits, compute or warehouse cost, and usage metrics for an asset, job, or deployment"
  - "execution time, materialization counts, row counts, or cost trends over a time window"
---

Insights metrics are reporting data about cost and usage — Dagster credits, execution time, materialization counts, row counts, and warehouse cost metrics — aggregated over a time window.

These are only available through the **Dagster Plus MCP server**. There is no `dg api` counterpart, so they cannot be reached when the server is not connected. See [general.md](./general.md) for how to tell whether it is.

## Discover, then report

The tools are split by scope. Metric availability varies by deployment, so discover which metrics exist for a scope before reporting on them.

| Scope      | Discover metric types          | Report metrics           |
| ---------- | ------------------------------ | ------------------------ |
| Asset      | `list_asset_metric_types`      | `get_asset_metrics`      |
| Job        | `list_job_metric_types`        | `get_job_metrics`        |
| Deployment | `list_deployment_metric_types` | `get_deployment_metrics` |

`get_asset_selection_metrics` reports metrics **aggregated across** an asset selection as a single series, where `get_asset_metrics` breaks the same window down **per asset**. Use it for "what did this whole pipeline cost", and `get_asset_metrics` for "which of these assets cost the most".

## Params

Every tool requires `deployment_name`.

The reporting tools require `metric_name` — a metric key such as `__dagster_dagster_credits`, taken from the matching `list_*_metric_types` call — plus `after` and `before` as **Unix timestamps** (floats). There is no named time-range or relative-window parameter; compute the two timestamps for the window you want.

Optional, with defaults:

- `granularity` — `HOURLY`, `DAILY` (default), `WEEKLY`, `MONTHLY`
- `aggregation_function` — `SUM` (default), `AVERAGE`, `P75`, `P90`, `P95`, `P99`, `LATEST`, `MAX`, `MIN`
- `limit` — default 20, max 100 entities
- `sort_targets` / `sort_directions` — `NAME`, `CODE_LOCATION_NAME`, `PCT_CHANGE`, `AGGREGATION_VALUE`, paired with `ASCENDING` or `DESCENDING`. Sorting by `PCT_CHANGE` descending is how you find what grew most over the window.

`limit` and the sort params apply to the three per-entity tools only. `get_asset_selection_metrics` returns one aggregated series, so it has nothing to rank or truncate.

Scoping differs by tool:

- **Asset-scoped** tools take `asset_keys` as path segment lists (`[["warehouse", "orders"]]`), or an `asset_selection` string. Unlike the launch tools, `asset_selection` here accepts the selection DSL (`group:`, `tag:`, `+upstream`).
- **Job-scoped** tools take `jobs` as dicts with `job_name`, `repository_name`, and `code_location_name` keys.
- The `list_*_metric_types` tools take the same scoping params plus optional `after`/`before` to narrow discovery to a window.
