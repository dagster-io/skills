---
description: Step-by-step guide for scaffolding a new dbt component in a Dagster project.
triggers:
  - "scaffold dbt, create dbt component"
  - "new dbt project in Dagster, set up dbt"
---

# Scaffolding a dbt Component

This guide covers the end-to-end process of creating a new `DbtProjectComponent` in a Dagster project.
For configuration and customization of an existing component, see
[Component-Based Integration](component-based-integration.md).

## Prerequisites

Ensure `dagster-dbt` is installed in the project:

```bash
uv add dagster-dbt
```

## Scaffold the Component

### Colocated dbt Project

If the dbt project lives inside the Dagster repository:

```bash
dg scaffold defs dagster_dbt.DbtProjectComponent <component name> --project-path <path to dbt project>
```

### Remote Git Repository

If the dbt project lives in a separate git repository:

```bash
dg scaffold defs dagster_dbt.DbtProjectComponent <component name> --git-url <git url> --project-path <repo-relative path to dbt project, default '.'>
```

## Install the Adapter Library (Required)

dbt requires a database-specific adapter library to compile the project manifest. **Without it,
`dbt parse` will fail and no assets will be loaded.**

1. Check the `profiles.yml` file in the dbt project for the adapter type (look for the `type:` field
   under the target configuration).
2. If the adapter type is not clear from `profiles.yml`, ask the user which database they are
   targeting.
3. Install the adapter:

```bash
uv add dbt-<adapter>
```

Common adapters:

| Adapter    | Package         |
| ---------- | --------------- |
| DuckDB     | `dbt-duckdb`    |
| Snowflake  | `dbt-snowflake` |
| BigQuery   | `dbt-bigquery`  |
| PostgreSQL | `dbt-postgres`  |
| Redshift   | `dbt-redshift`  |

## Verify

Run `dg list defs` to confirm the manifest compiled and assets are visible:

```bash
dg list defs
```

If this returns no definitions, check that:

- The adapter library is installed
- The dbt project path is correct
- `profiles.yml` is properly configured
