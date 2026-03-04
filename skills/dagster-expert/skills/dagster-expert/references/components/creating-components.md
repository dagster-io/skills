---
description: Guide for creating custom Dagster components.
triggers:
  - "create component, new component, custom component"
---

# Creating Custom Components

Components are the primary unit of reuse in Dagster projects. A component is a Python class that maps YAML configuration to Dagster definitions via the [Resolved framework](./resolved-framework.md). The core method is `build_defs()`, which returns a `dg.Definitions` object.

## Scaffolding

Use the CLI to generate boilerplate for a new component:

```bash
dg scaffold component MyComponent
```

This creates the class file and registers it. Verify it appears in the component list, and note its full path (e.g. `my_project.lib.my_component.MyComponent`) for future scaffolding:

```bash
dg list components
```

## Component Structure

A component inherits from `dg.Component` and `dg.Resolvable`, plus a base class for field definitions.

See [Resolved Framework](./resolved-framework.md#nested-resolution) for details on how to structure your component fields.

ALWAYS use the built-in resolved types for asset-related fields instead of raw strings or dicts:

- **`dg.ResolvedAssetKey`** — for a single asset key (accepts `"a/b/c"` string in YAML)
- **`dg.ResolvedAssetSpec`** — for a full asset spec (accepts structured mapping in YAML)
- **`dg.ResolvedAssetCheckSpec`** — for asset check specs

These handle YAML-to-Python resolution automatically.

## Building Definitions

`build_defs()` returns `dg.Definitions` — this is the primary concern of a component.

Prefer `@dg.multi_asset(specs=[...])` even for a single asset. This lets you pass `AssetSpec` objects directly via `specs=` instead of mapping all spec subfields to individual `@dg.asset()` kwargs:

```python
import dagster as dg


class MyComponent(dg.Component, dg.Resolvable, dg.Model):
    spec: dg.ResolvedAssetSpec
    query: str

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        spec = self.spec

        @dg.multi_asset(specs=[spec])
        def my_asset(ctx: dg.AssetExecutionContext):
            ctx.log.info(f"Running query: {self.query}")
            # ... materialize the asset ...

        return dg.Definitions(assets=[my_asset])
```

Corresponding YAML:

```yaml
type: my_project.components.MyComponent

attributes:
  spec:
    key: my_database/my_schema/orders
    group_name: ingestion
    kinds:
      - sql
  query: "SELECT * FROM orders"
```

## Expensive Operations

If building definitions requires expensive work — querying a database, hitting an API, cloning a repo, compiling artifacts — ALWAYS use [StateBackedComponent](./state-backed/creating.md). It separates state-fetching from definition-building so that code server loads remain efficient.

```python
# Use StateBackedComponent instead of Component when external state is involved
class MyApiComponent(dg.StateBackedComponent, dg.Model, dg.Resolvable):
    ...
```

See [State-Backed Components](./state-backed/creating.md) for full implementation details.

## References

- [Resolved Framework](./resolved-framework.md)
- [Template Variables](./template-variables.md)
- [State-Backed Components](./state-backed/creating.md)
- [`dg scaffold component`](../cli/scaffold/component.md)
- [`dg list components`](../cli/list/components.md)
