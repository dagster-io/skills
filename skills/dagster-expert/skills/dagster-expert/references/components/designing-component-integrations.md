---
title: Designing Component Integrations
triggers:
  - "designing a component that wraps an external service or tool"
  - "custom integrations"
---

# Designing Component Integrations

## When to Use This Guide

This guide applies whenever you need to integrate with an external tool — whether or not a published `dagster-*` library exists. If no library exists, you should **always** create a custom component rather than writing raw `@dg.asset` or `@dg.sensor` definitions. See [Integration Workflow](../integrations/INDEX.md#custom-integration-workflow-no-library-exists) for the scaffolding steps.

## Three Levels of Integration

When designing a component integration, first determine how Dagster should interact with the external tool. There are three levels:

- **Definition-only**: Dagster understands assets defined in an external tool and their dependencies. Example: `OmniComponent` maps Omni dashboards to Dagster assets.
- **Observing**: Definition-only plus Dagster monitors for events via sensors, emitting `AssetObservation` or `AssetMaterialization` events. (Aspirational — no clean component example yet.)
- **Orchestrating**: Definition-only plus Dagster can trigger execution. Example: `FivetranAccountComponent` kicks off Fivetran syncs.

If it is necessary to fetch data from APIs in order to understand the _definitions_ of the assets, then [State-Backed Components](./state-backed/creating.md) should always be used. If creating the definitions does NOT require fetching data (e.g. tool configuration is checked into the git repository), then a regular `Component` should be used, regardless of if executing the asset requires external API calls or not.

## Pattern: External Data Class

Create a data class representing the raw data (for a specific asset) from the external tool's API. This is the "props" type that flows through translation and into `get_asset_spec`.

```python
from dagster_shared.record import record

@record
class MyConnectorTableProps:
    """Raw data from the external tool for a single asset."""
    connector_id: str
    table_name: str
    schema_name: str
    sync_enabled: bool
```

## Pattern: Translation Field

Translation allows YAML users to customize asset properties without subclassing. Use `TranslationFnResolver` with an `Annotated` type:

```python nocheck
from typing import Annotated
from dagster.components.utils.translation import TranslationFn, TranslationFnResolver

class MyServiceComponent(dg.Component, dg.Model, dg.Resolvable):
    translation: (
        Annotated[
            TranslationFn[MyConnectorTableProps],
            TranslationFnResolver(
                template_vars_for_translation_fn=lambda data: {
                    "table_name": data.table_name,
                    "schema_name": data.schema_name,
                }
            ),
        ]
        | None
    ) = None
```

`TranslationFn` is a type alias for `Callable[[AssetSpec, T], AssetSpec]`. The `template_vars_for_translation_fn` callback exposes fields as Jinja template variables for YAML users. The variable `spec` is always available automatically.

Corresponding YAML usage:

```yaml
component_type: my_service
params:
  translation:
    key: "my_prefix/{{ schema_name }}/{{ table_name }}"
    group: "{{ schema_name }}"
```

## Pattern: `get_asset_spec` Method

A public method that converts external data into a Dagster `AssetSpec`. It should provide sensible defaults (name → key, extract tags, set `kinds`, add metadata) and be designed for subclass override.

```python nocheckundefined
import dagster as dg

class MyServiceComponent(dg.Component, dg.Resolvable, dg.Model):
  translation: ...

  def get_asset_spec(self, data: MyConnectorTableProps) -> dg.AssetSpec:
      """Generates an AssetSpec for a given connector table."""
      base_spec = dg.AssetSpec(
          key=dg.AssetKey([data.schema_name, data.table_name]),
          metadata={"connector_id": data.connector_id},
          kinds={"myservice"},
      )
      if self.translation:
          return self.translation(base_spec, data)
      return base_spec
```

Subclasses can override to customize defaults:

```python nocheckundefined
class CustomComponent(MyServiceComponent):
    def get_asset_spec(self, data: MyConnectorTableProps) -> dg.AssetSpec:
        spec = super().get_asset_spec(data)
        return spec.replace_attributes(group_name="my_group")
```

## Pattern: Credentials and Secrets

Component fields should accept credential **values** directly (e.g. `api_key: str`), not environment variable names (e.g. `api_key_env_var: str`). YAML users provide secrets via the Jinja `{{ env.VAR }}` syntax, which is resolved at component load time. The component code then uses the resolved value directly.

```python
class MyServiceComponent(dg.Component, dg.Model, dg.Resolvable):
    api_secret: str
```

```yaml
type: my_project.components.my_service_component.MyServiceComponent

attributes:
  api_secret: "{{ env.MY_SERVICE_API_SECRET }}"
```

See [Template Variables](./template-variables.md) for more information.

## Pattern: `execute()` Method

A public method for triggering external tool execution. Designed for subclass override.

```python nocheckundefined
def execute(
    self, context: dg.AssetExecutionContext, resource: MyServiceWorkspace
) -> Iterable[dg.AssetMaterialization | dg.MaterializeResult]:
    """Executes a sync for the selected connector."""
    yield from resource.sync_and_poll(context=context)
```

The component wires `execute` into a `@multi_asset`:

```python
def _build_multi_asset(self, connector_id, asset_specs, resource):
    @dg.multi_asset(name=connector_id, specs=asset_specs)
    def _assets(context: dg.AssetExecutionContext):
        yield from self.execute(context=context, resource=resource)

    return _assets
```

## Pattern: Subsettable Multi-Assets

When the external tool supports executing an arbitrary subset of the assets defined in a single component instance, add `can_subset=True` to `@dg.multi_asset()` and use `context.selected_asset_keys` to determine which assets to execute.

**When to use**: The external tool lets you select which assets to execute independently (e.g. dbt lets you select any subset of models to build).

**When NOT to use**: The external tool executes all assets atomically (e.g. a Fivetran connector sync runs all tables together — no per-table control).

**Key changes**:

1. Add `can_subset=True` to the `@dg.multi_asset()` decorator in the `_build_multi_asset` helper
2. Mark each `AssetSpec` with `skippable=True` so Dagster knows individual assets can be skipped when subsetting
3. Pass `context` through to `execute()`:

```python
def _build_multi_asset(self, connector_id, asset_specs, resource):
    @dg.multi_asset(name=connector_id, specs=asset_specs, can_subset=True)
    def _assets(context: dg.AssetExecutionContext):
        yield from self.execute(context=context, resource=resource)

    return _assets
```

The `execute()` method can then use `context.selected_asset_keys` to only process the requested subset:

```python nocheckundefined
def execute(
    self, context: dg.AssetExecutionContext, resource: MyServiceWorkspace
) -> Iterable[dg.MaterializeResult]:
    for key in context.selected_asset_keys:
        yield from resource.sync_asset(key, context=context)
```

## Pattern: Observation via Sensors

For components that need to monitor external tool events without orchestrating them, a component's `build_defs` should include a sensor definition (adding this sensor could be controlled via a boolean flag on the component).

**Important**: Sensors for observing an external tool MUST be bundled inside the component's `build_defs()` method — do NOT create separate standalone `@dg.sensor` definition files for the same tool. The component should be the single source of truth for all definitions related to an integration, including sensors. This keeps observe vs. orchestrate mode toggling in one place (the component's YAML config).

```python
def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
    asset_specs = [self.get_asset_spec(d) for d in []]

    @dg.sensor(name="my_service_sensor")
    def _sensor(context: dg.SensorEvaluationContext):
        new_events = self._poll_for_events(context)
        for event in new_events:
            context.instance.report_runless_asset_event(
              dg.AssetObservation(asset_key=self.get_asset_spec(event).key)
            )


    return dg.Definitions(assets=asset_specs, sensors=[_sensor] if self.enable_sensor else None)
```

## Cross-Component Dependencies

Components in the same code location can reference each other's assets by key — Dagster resolves all `deps` references across all components at load time. A downstream component only needs to know the **asset key** of an upstream asset, not where or how it's defined.

```python nocheckundefined
# In a Census reverse ETL component — depends on dbt-produced marts
dg.AssetSpec(
    key=dg.AssetKey(["census", "salesforce_sync"]),
    deps=[dg.AssetKey(["snowflake", "marts", "mart_customers"])],  # produced by DbtProjectComponent
)
```

The `DbtProjectComponent` (or `FivetranAccountComponent`, etc.) is solely responsible for producing its own asset specs. Downstream components just reference the keys via `deps=`. There is no need to pre-define or duplicate asset specs for the dependency graph to connect.
