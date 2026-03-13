---
title: dg scaffold component
triggers:
  - "creating a custom reusable component type"
---

Scaffold a new custom Dagster component type class. Must be run inside a Dagster project directory. The scaffold is placed in `<project_name>.components.<name>`.

Use `dg scaffold component` when the component will be used multiple times. For one-off components, use `dg scaffold defs inline-component` instead, which places the component class definition directly under `defs/` alongside its `defs.yaml`:

```bash
dg scaffold defs inline-component
```

```bash
dg scaffold component <class-name>
```

`--model / --no-model` — whether the generated class inherits from `dagster.components.Model` (default: `--model`).

## Inspecting Components

To inspect an existing component type's description, scaffold parameters, or `defs.yaml` schema, use [`dg utils inspect-component`](../utils/inspect-component.md).
