---
description: "dg scaffold defs: add new definitions to a project."
triggers:
  - "create asset, create schedule, create sensor"
  - "add component, scaffold component"
---

# dg scaffold defs - Scaffoldable Types

`dg scaffold defs` is the preferred way to add new definitions to the project. It automatically ensures that new code is added to the correct location within the project.

After scaffolding new definitions, it is recommended to run `dg list defs` to verify that the new definitions appear in the project.

---

## Python Definition Objects

A variety of dagster definition objects can be scaffolded using `dg scaffold defs`. These will create a single `.py` file at the specified path (relative to `defs/`). ALWAYS include the `.py` extension when scaffolding.

```bash
dg scaffold defs dagster.asset assets/my_asset.py
dg scaffold defs dagster.schedule schedules/daily.py
dg scaffold defs dagster.sensor sensors/watcher.py
```

---

## Component Types

Scaffold a component directory with `defs.yaml` (default). Use `--format` to choose YAML or Python configuration. YAML configuration should be preferred by default.

Each component type has a corresponding subcommand that accept provide additional arguments. When scaffolding a component from a dagster-provided library (see [../../integrations/INDEX.md](../../integrations/INDEX.md)), consult the reference documentation for recommended arguments. Otherwise, you can run `--help` to see the available options.

Additional arguments can be provided either via flags directly, or using `--json-params` to provide a JSON object.

```bash
dg scaffold defs some_lib.SomeComponent my_component

# With flags
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt --project-dir dbt_project

# With JSON params (integration components)
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt --json-params '{
  "project_dir": "dbt_project"
}'
```

---

## Inline Components

In cases where a component is expected to be used only once, it is recommended to use `dg scaffold defs inline-component` instead, which will add the component definition directly to the relevant folder underneath the `defs/` directory. This is simpler for people examining the code as the `defs.yaml` file will be co-located with the definition of the component class.

If you expect to use the component multiple times, it is recommended to use `dg scaffold component` instead.

```bash
dg scaffold defs inline-component
```

---

## See Also

- [../list/components.md](../list/components.md) - Discover available component types
- [../list/defs.md](../list/defs.md) - List definitions in the project
- [../check.md](../check.md) - Validate definitions after scaffolding
