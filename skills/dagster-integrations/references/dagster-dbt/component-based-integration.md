# Component-Based Integration

The Component-based approach uses `DbtProjectComponent` to define dbt assets via YAML configuration.
This is the recommended approach for new projects.

## Overview

`DbtProjectComponent` is a StateBackedComponent that automatically compiles and caches your dbt
project's manifest. See
[StateBackedComponents](../../integrations-index/references/state-backed-components.md) for general
state management patterns.

### dbt-Specific State Management

**What state is managed**: The dbt `manifest.json` file, which contains all dbt models, tests,
sources, and their relationships.

**How it's compiled**: Runs `dbt parse` (and `dbt deps` if needed) to generate the manifest.

**Configuration**: Use `prepare_if_dev` setting to control whether manifest is recompiled during
local development (defaults to `true`).

In CI/CD, use `dg utils refresh-defs-state` or `dg plus deploy refresh-defs-state` to compile the
manifest before deployment.

## Project Setup

### Colocated Projects

Provide a local path to a dbt project within your Dagster repository:

```yaml
type: dagster_dbt.DbtProjectComponent
attributes:
  project: "{{ context.project_root }}/dbt_project"
```

Scaffold this with the following command:

```bash
dg scaffold defs dagster_dbt.DbtProjectComponent <component name> --project-path <path to dbt project>
```

### Remote Git Repositories

Provide a Git URL and path to the dbt project within the repository:

```yaml
type: dagster_dbt.DbtProjectComponent
attributes:
  project:
    repo_url: https://github.com/org/dbt-project.git
    repo_relative_path: path/to/dbt
```

During `dg utils refresh-defs-state`, the component automatically clones the repository and compiles
the manifest.

Scaffold this with the following command:

```bash
dg scaffold defs dagster_dbt.DbtProjectComponent <component name> --git-url <git url> --project-path <repo-relative path to dbt project, default '.'>
```

### Important: Adapter Libraries

Most dbt projects will use an adapter library to connect to the specific database technology being used. This adapter library will be in a `dbt-<database>` (e.g. `dbt-snowflake`, `dbt-bigquery`, `dbt-duckdb`) package, which you should add to the project. For `uv`-based projects, this can be done with `uv add dbt-<database>`.

You can determine which database technology to use by:

- Asking the user
- Looking at the profiles.yml file in the dbt project and scanning for which database(s) it uses
- Attempting to execute the dagster code without the adapter library installed and seeing which errors are thrown

## Basic Configuration

### Selecting Models

Use dbt selection syntax to filter which models are included:

```yaml
attributes:
  select: "tag:daily"
  exclude: "tag:deprecated"
```

### CLI Arguments

Customize the dbt command executed for asset materialization:

```yaml
attributes:
  cli_args:
    - build
    - --full-refresh
```

CLI args support template variables for dynamic values based on execution context.

## Translation and Customization

### Simple Customization: YAML Translation Block

For basic metadata customization, use the `translation` block:

```yaml
attributes:
  translation:
    group_name: analytics
    description: "dbt model {{ node.name }}"
```

Template variables have access to the dbt node properties.

### Advanced Customization: Subclassing

For complex customization, create a subclass and override `get_asset_spec()`:

```python
from collections.abc import Mapping
from typing import Any, Optional

import dagster as dg
from dagster_dbt import DbtProject, DbtProjectComponent


class CustomDbtComponent(DbtProjectComponent):
    def get_asset_spec(
        self,
        manifest: Mapping[str, Any],
        unique_id: str,
        project: Optional[DbtProject],
    ) -> dg.AssetSpec:
        base_spec = super().get_asset_spec(manifest, unique_id, project)
        dbt_props = self.get_resource_props(manifest, unique_id)

        return base_spec.merge_attributes(metadata={"model_name": dbt_props["name"]})
```

Then use your custom component in `defs.yaml`:

```yaml
type: my_project.lib.custom_dbt_component.CustomDbtComponent
```

### dbt Meta Config

Define custom metadata in your dbt project files that can be consumed by your custom
`get_asset_spec()` implementation:

```yaml
models:
  - name: customers
    meta:
      custom_field: custom_value
```

This metadata is accessible via the manifest in your translator code.

## Incremental Models and Partitioning

To partition incremental dbt models:

1. Define a partitions definition as a template variable
2. Apply it to assets via `post_processing`
3. Pass partition-specific vars through `cli_args`

```yaml
template_vars_module: .template_vars

attributes:
  cli_args:
    - build
    - --vars:
      min_date: "{{ context.partition_time_window.start.strftime('%Y-%m-%d') }}"
      max_date: "{{ context.partition_time_window.end.strftime('%Y-%m-%d') }}"

post_processing:
  assets:
    - target: "*"
      attributes:
        partitions_def: "{{ my_partitions_def }}"
```

The `context.partition_time_window` variable is available in `cli_args` during execution. Dagster
automatically converts the vars dict to JSON format for dbt CLI.

For multiple partitions definitions, create separate `DbtProjectComponent` instances and use
`select` to filter models for each.

## Metadata

Enable automatic metadata fetching during materialization:

```yaml
attributes:
  include_metadata:
    - row_count
    - column_metadata
```

- `row_count`: Fetch row counts for tables
- `column_metadata`: Fetch column schema and lineage (extracted via sqlglot parsing)

Both metadata types are fetched in parallel during dbt execution.

## Asset Checks

See [Asset Checks](asset-checks.md) for details on how dbt tests are loaded as Dagster asset checks.

## Dependencies

See [Dependencies](dependencies.md) for details on how Dagster parses dbt project dependencies and
patterns for defining additional dependencies.

### Referencing dbt Models in Other Components

Use the `asset_key_for_model` method to reference dbt models from other components:

```yaml
type: dagster.PythonScriptComponent
attributes:
  script_path: export_customers.py
  dependencies:
    - "{{ context.load_component('dbt_component').asset_key_for_model('customers') }}"
```

## Scheduling

Use standard Dagster scheduling approaches with asset selections:

```python
import dagster as dg

daily_dbt_job = dg.define_asset_job(
    name="daily_dbt_models",
    selection=dg.AssetSelection.groups("analytics"),
)

daily_schedule = dg.ScheduleDefinition(
    job=daily_dbt_job,
    cron_schedule="0 0 * * *",
)
```

For declarative automation, configure AutomationConditions via custom `get_asset_spec()`
implementation.

## Runtime Configuration

Override the `execute()` method to customize execution behavior:

```python
from collections.abc import Iterator

import dagster as dg
from dagster_dbt import DbtCliResource, DbtProjectComponent


class ConfigurableDbtComponent(DbtProjectComponent):
    @property
    def op_config_schema(self) -> type[dg.Config]:
        class DbtConfig(dg.Config):
            full_refresh: bool = False

        return DbtConfig

    def execute(
        self, context: dg.AssetExecutionContext, dbt: DbtCliResource
    ) -> Iterator:
        if context.op_config.get("full_refresh"):
            args = ["build", "--full-refresh"]
        else:
            args = self.get_cli_args(context)

        yield from dbt.cli(args, context=context).stream()
```

Define `op_config_schema` property to specify available config options.

## dbt Cloud

For dbt Cloud projects, see [dbt Cloud Integration](dbt-cloud.md).
