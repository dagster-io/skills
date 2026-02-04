# Pythonic Integration

The Pythonic approach uses the `@dbt_assets` decorator to define dbt assets programmatically. This
provides maximum flexibility for complex customization scenarios.

## Overview

Key classes:

- **`@dbt_assets`**: Decorator that loads dbt models as Dagster assets from a manifest
- **`DbtCliResource`**: Resource for executing dbt CLI commands
- **`DbtProject`**: Represents a dbt project and manages manifest compilation
- **`DagsterDbtTranslator`**: Customizes how dbt nodes map to Dagster assets

## Basic Setup

```python
import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

# Define the dbt project
my_dbt_project = DbtProject(project_dir="path/to/dbt_project", target="dev")

# Create the dbt resource
dbt_resource = DbtCliResource(project_dir=my_dbt_project.project_dir)


# Define assets from dbt models
@dbt_assets(manifest=my_dbt_project.manifest_path)
def my_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


# Define definitions
defs = dg.Definitions(assets=[my_dbt_assets], resources={"dbt": dbt_resource})
```

## Manifest Management

The dbt manifest can be generated at runtime (development) or build time (production).

### Runtime Compilation (Development)

`DbtProject.prepare_if_dev()` automatically compiles the manifest during local development:

```python
my_dbt_project = DbtProject(project_dir="path/to/dbt_project")
my_dbt_project.prepare_if_dev()  # Runs dbt deps + dbt parse if needed
```

### Build-Time Compilation (Production)

For production deployments, precompile the manifest in CI/CD to avoid recompilation overhead. The
manifest at `DbtProject.manifest_path` (typically `target/manifest.json`) should be included in your
deployed package.

## Selecting Models

Use dbt selection syntax to filter which models are included:

```python
@dbt_assets(
    manifest=my_dbt_project.manifest_path,
    select="tag:daily",
    exclude="tag:deprecated",
)
def my_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
```

## Translation and Customization

### Using DagsterDbtTranslator

Create a custom translator by subclassing `DagsterDbtTranslator` and overriding `get_asset_spec()`:

```python
from collections.abc import Mapping
from typing import Any, Optional

import dagster as dg
from dagster_dbt import DagsterDbtTranslator, DbtProject, dbt_assets


class CustomDbtTranslator(DagsterDbtTranslator):
    def get_asset_spec(
        self,
        manifest: Mapping[str, Any],
        unique_id: str,
        project: Optional[DbtProject],
    ) -> dg.AssetSpec:
        base_spec = super().get_asset_spec(manifest, unique_id, project)
        dbt_props = self.get_resource_props(manifest, unique_id)

        return base_spec.merge_attributes(
            metadata={"model_name": dbt_props["name"]}, group_name="analytics"
        )


@dbt_assets(
    manifest=my_dbt_project.manifest_path,
    dagster_dbt_translator=CustomDbtTranslator(),
)
def my_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
```

The `get_asset_spec()` method is called once per dbt node and should return a complete `AssetSpec`
describing that node.

### dbt Meta Config

Define custom metadata in your dbt project files that can be consumed by your custom
`get_asset_spec()` implementation:

```yaml
models:
  - name: customers
    meta:
      custom_field: custom_value
```

Access this metadata via the manifest in your translator's `get_asset_spec()` method.

## Incremental Models and Partitioning

To partition incremental dbt models:

1. Define a `PartitionsDefinition`
2. Pass it to the `@dbt_assets` decorator
3. Access `context.partition_time_window` in the asset function
4. Pass partition-specific vars to the dbt CLI

```python
import json

import dagster as dg
from dagster_dbt import dbt_assets

daily_partitions = dg.DailyPartitionsDefinition(start_date="2023-01-01")


@dbt_assets(manifest=my_dbt_project.manifest_path, partitions_def=daily_partitions)
def my_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    time_window = context.partition_time_window

    dbt_vars = {
        "min_date": time_window.start.strftime("%Y-%m-%d"),
        "max_date": time_window.end.strftime("%Y-%m-%d"),
    }

    yield from dbt.cli(
        ["build", "--vars", json.dumps(dbt_vars)], context=context
    ).stream()
```

Reference these vars in your dbt SQL:

```sql
{{ config(materialized='incremental', unique_key='order_date') }}

select * from {{ ref('my_model') }}

{% if is_incremental() %}
where order_date >= '{{ var('min_date') }}' and order_date <= '{{ var('max_date') }}'
{% endif %}
```

For multiple partitions definitions, create separate `@dbt_assets` definitions and use
`select`/`exclude` to filter models for each.

## Metadata

Enable automatic metadata fetching by chaining methods on the event iterator:

```python
@dbt_assets(manifest=my_dbt_project.manifest_path)
def my_dbt_assets(context, dbt: DbtCliResource):
    yield from (
        dbt.cli(["build"], context=context)
        .stream()
        .fetch_row_counts()
        .fetch_column_metadata()
    )
```

- `fetch_row_counts()`: Fetch row counts for tables
- `fetch_column_metadata()`: Fetch column schema and lineage (extracted via sqlglot parsing)

Both metadata types are fetched in parallel during dbt execution.

## Asset Checks

See [Asset Checks](asset-checks.md) for details on how dbt tests are loaded as Dagster asset checks.

## Dependencies

See [Dependencies](dependencies.md) for details on how Dagster parses dbt project dependencies and
patterns for defining additional dependencies.

### Referencing dbt Models in Other Assets

Use `get_asset_key_for_model()` to get asset keys for dbt models:

```python
import dagster as dg
from dagster_dbt import get_asset_key_for_model


@dg.asset(deps=[get_asset_key_for_model([my_dbt_assets], "customers")])
def export_customers():
    # Use the customers model
    pass
```

## Scheduling

### dbt-Only Jobs

Use `build_schedule_from_dbt_selection()` for jobs that only materialize dbt assets:

```python
from dagster_dbt import build_schedule_from_dbt_selection

daily_dbt_schedule = build_schedule_from_dbt_selection(
    [my_dbt_assets],
    job_name="daily_dbt_models",
    cron_schedule="0 0 * * *",
    dbt_select="tag:daily",
)
```

### Mixed Jobs (dbt + Non-dbt Assets)

Use `build_dbt_asset_selection()` combined with `AssetSelection` for jobs with dbt and non-dbt
assets:

```python
import dagster as dg
from dagster_dbt import build_dbt_asset_selection

# Select dbt models and all downstream assets
dbt_models = build_dbt_asset_selection([my_dbt_assets], dbt_select="tag:daily")
all_assets = dbt_models.downstream(include_self=True)

daily_job = dg.define_asset_job(name="daily_pipeline", selection=all_assets)
daily_schedule = dg.ScheduleDefinition(job=daily_job, cron_schedule="0 0 * * *")
```

### Declarative Automation

Configure AutomationConditions via custom `get_asset_spec()` implementation in your translator:

```python
class AutomatedDbtTranslator(DagsterDbtTranslator):
    def get_asset_spec(self, manifest, unique_id, project) -> dg.AssetSpec:
        base_spec = super().get_asset_spec(manifest, unique_id, project)
        return base_spec.replace_attributes(
            automation_condition=dg.AutomationCondition.eager()
        )
```

## Runtime Configuration

Use Dagster's config system to provide runtime parameters:

```python
import dagster as dg
from dagster_dbt import dbt_assets


class DbtConfig(dg.Config):
    full_refresh: bool = False


@dbt_assets(manifest=my_dbt_project.manifest_path)
def my_dbt_assets(context, dbt: DbtCliResource, config: DbtConfig):
    args = ["build"]
    if config.full_refresh:
        args.append("--full-refresh")

    yield from dbt.cli(args, context=context).stream()
```

## dbt Cloud

For dbt Cloud projects, see [dbt Cloud Integration](dbt-cloud.md).
