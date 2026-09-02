---
title: dg scaffold defs
triggers:
  - "adding new definitions (assets, schedules, sensors, components) to a project"
---

`dg scaffold defs` is the preferred way to add new definitions to the project. It automatically ensures new code is added to the correct location.

## Python Definition Objects

Scaffolds a single `.py` file at the specified path (relative to `defs/`). ALWAYS include the `.py` extension.

```bash
dg scaffold defs dagster.asset assets/my_asset.py
dg scaffold defs dagster.schedule schedules/daily.py
dg scaffold defs dagster.sensor sensors/watcher.py
```

## Component Types

Scaffold a component directory with `defs.yaml`. Additional arguments can be provided via flags or `--json-params`.

**Important**: After scaffolding a custom component with `dg scaffold component`, run `dg list components` to get the exact registered type path. The path includes the file module name — e.g. `my_project.components.my_component.MyComponent`, not `my_project.components.MyComponent`.

```bash
dg scaffold defs some_lib.SomeComponent my_component

# With flags
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt --project-dir dbt_project

# With JSON params
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt --json-params '{"project_dir": "dbt_project"}'
```

## Inline Components

For one-off components, use `inline-component` to place the component class definition directly under `defs/` alongside its `defs.yaml`. Use `dg scaffold component` instead if you expect to reuse it.

```bash
dg scaffold defs inline-component
```

## Important: Always run `dg list defs` to confirm the definitions were scaffolded correctly

## Inspecting Components Before Scaffolding

To inspect a component's scaffold parameters or `defs.yaml` schema before scaffolding, use [`dg utils inspect-component`](../utils/inspect-component.md).
