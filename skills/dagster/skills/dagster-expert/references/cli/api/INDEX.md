---
title: Dagster Plus API
type: index
triggers:
  - "dg api or the Dagster Plus MCP server, programmatically querying or managing Dagster Plus resources (assets, runs, deployments, code locations, schedules, sensors, secrets, issues, alert policies, etc.)"
  - "Dagster credits, compute or warehouse cost, usage, and other insights metrics for an asset, job, or deployment"
  - "retrying or re-executing a failed run or backfill; terminating a run"
---

# Dagster Plus API Reference

Dagster Plus resources are reachable two ways: the **Dagster Plus MCP server** and the **`dg api` CLI**. Prefer the MCP server whenever it is connected and covers the operation; use `dg api` otherwise. Reference files name their MCP equivalent where one exists, and are CLI-only where none does.

One area runs the other way: [insights metrics](./insights.md) — cost, credits, and usage reporting — exist only on the MCP server.

**Important**: Always read [general.md](./general.md) first before using any `dg api` subcommand. It covers how to choose between MCP and the CLI, plus shared flags (`--json`, `--response-schema`, `--deployment`, `--view-graphql`) and best practices.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [dg api asset-check](./asset-check.md) — querying asset checks or asset check execution history in Dagster Plus
- [dg api: General](./general.md) — always read before using any dg api subcommand; choosing between the Dagster Plus MCP server and the dg api CLI
- [Dagster Plus insights metrics](./insights.md) — Dagster credits, compute or warehouse cost, and usage metrics for an asset, job, or deployment; execution time, materialization counts, row counts, or cost trends over a time window
- [dg api job](./job.md) — listing or inspecting jobs in Dagster Plus
- [dg api agent](./agent/INDEX.md) — listing or inspecting Dagster Plus agents
- [dg api alert-policy](./alert-policy/INDEX.md) — managing alert policies in Dagster Plus (listing, syncing from YAML)
- [dg api artifact](./artifact/INDEX.md) — uploading or downloading artifacts in Dagster Plus
- [dg api asset](./asset/INDEX.md) — querying information about assets in Dagster Plus (metadata, events, DA evaluations, health status, etc.)
- [dg api code-location](./code-location/INDEX.md) — managing code locations in Dagster Plus (add, delete, list, inspect)
- [dg api deployment](./deployment/INDEX.md) — managing Dagster Plus deployments (create, delete, list, settings)
- [dg api issue](./issue/INDEX.md) — listing Dagster Plus Issues, fetching a specifc Dagster Plus Issue
- [dg api organization](./organization/INDEX.md) — managing Dagster Plus organization settings and SAML/SSO configuration
- [dg api run](./run/INDEX.md) — run operations, run details, run events, run logs; listing runs, getting run info, fetching run events, compute logs; re-executing or retrying a failed run or backfill, from failure or from scratch; terminating or canceling an in-flight run
- [dg api schedule](./schedule/INDEX.md) — schedule operations, schedule details, schedule ticks; listing schedules, getting schedule info, schedule tick history
- [dg api secret](./secret/INDEX.md) — listing or inspecting secrets in a Dagster Plus deployment
- [dg api sensor](./sensor/INDEX.md) — sensor operations, sensor details, sensor ticks; listing sensors, getting sensor info, sensor tick history
<!-- END GENERATED INDEX -->
