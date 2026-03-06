---
description: Designing component integrations for external services and tools.
triggers:
  - "component integration, external service, modeling concepts"
  - "creating component integrations"
---

# Designing Component Integrations

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

## Pattern: Observation via Sensors

For components that need to monitor external tool events without orchestrating them, a component's `build_defs` would include a sensor definition (adding this sensor could be controlled via a boolean flag on the component):

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
