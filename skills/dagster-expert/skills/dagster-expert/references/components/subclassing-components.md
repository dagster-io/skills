---
title: Subclassing Components
triggers:
  - "extending an existing component via subclassing"
  - "customize dagster integration component"
---

# Subclassing Components

When a [Dagster integration](../integrations/INDEX.md) already covers the external tool you're working with, it is almost always better to **subclass the existing component** instead of building from scratch. This preserves the core of the API interactions and metadata translation logic, while allowing you to customize the parts that differ for your use case.

## Common Override Points

### `get_asset_spec()` — Customize Asset Representation

Override to change asset keys, groups, metadata, kinds, or dependencies.

```python nocheckundefined
import dagster as dg
from dagster_fivetran import FivetranAccountComponent

class CustomFivetranComponent(FivetranAccountComponent):
    def get_asset_spec(self, data) -> dg.AssetSpec:
        spec = super().get_asset_spec(data)
        return spec.replace_attributes(
            group_name="warehouse_ingestion",
            kinds={"fivetran", "snowflake"},
        )
```

### `execute()` — Customize Execution Behavior

Override to add pre/post logic around the standard sync, or to filter which syncs run.

```python nocheckundefined
import dagster as dg
from dagster_fivetran import FivetranAccountComponent

class CustomFivetranComponent(FivetranAccountComponent):
    def execute(self, context: dg.AssetExecutionContext, resource):
        context.log.info("Starting custom pre-sync validation")
        # ... custom logic ...
        yield from super().execute(context, resource)
        context.log.info("Post-sync complete")
```

### (StateBackedComponent) `write_state_to_path()` — Customize State Persistence

For `StateBackedComponent` subclasses, override to transform or augment the persisted state. This is typically only necessary for mock / demo purposes, and should otherwise be avoided in most cases.

```python nocheckundefined
from pathlib import Path

class CustomComponent(ExistingStateBackedComponent):
    def write_state_to_path(self, state_path: Path) -> None:
        state = ... # note: you may need to inspect the parent class to determine the specific state format for `write_state_to_path()`
        state_path.write_text(dg.serialize_value(state))
```

### (StateBackedComponent) `build_defs_from_state()` — Customize Definition Construction

Override to change how persisted state is translated into Dagster definitions (e.g., adding sensors, extra assets, or resources). This is only necessary when:

- Fundamentally changing the existing definitions entirely (rare). Note that if you only want to change the runtime behavior of the existing definitions, you should just override `execute()`, and if you just want to change the metadata of the generated assets, you should just override `get_asset_spec()`.
- Adding additional definitions on top of the base definitions (shown below)

```python nocheckundefined
import dagster as dg

class CustomComponent(ExistingStateBackedComponent):
    def build_defs_from_state(self, context, state_path: Path) -> dg.Definitions:
        base_defs = super().build_defs_from_state(context, state_path)
        # Add a custom sensor alongside the base definitions
        return dg.Definitions(
            assets=base_defs.assets,
            sensors=[my_custom_sensor],
            resources=base_defs.resources,
        )
```
