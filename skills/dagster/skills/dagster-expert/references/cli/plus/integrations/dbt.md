---
title: dg plus integrations dbt
triggers:
  - "managing dbt manifests with Dagster Plus"
  - "downloading dbt manifest for dbt --defer or slim CI"
---

Commands for managing dbt integrations with Dagster Plus.

## `dg plus integrations dbt manage-manifest`

Automatically manage dbt manifest uploads and downloads based on deployment context. Used to enable dbt's `--defer` flag (slim CI) by providing a production state manifest. In branch deployments, downloads the prod manifest. In the source deployment (default: "prod"), uploads the manifest. Requires a `dg plus deploy` session (`DAGSTER_BUILD_STATEDIR`).

## `dg plus integrations dbt download-manifest`

Download a dbt manifest from Dagster Plus for local development. Does not require a deploy session. Use `--components` to discover DbtProject instances from a dg project, or `--file` to point at a Python file containing DbtProject definitions. Use `--output` to override the download destination (cannot be used with multiple projects).
