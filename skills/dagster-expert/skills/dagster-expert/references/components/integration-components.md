---
description: Integration component patterns including availability, config-file vs API-based types, subclassing, asset kinds, and troubleshooting.
triggers:
  - "integration component, component availability, which integrations have components"
  - "config-file vs API component, subclass component, override build_defs, override get_asset_spec, asset kinds"
---

# Integration Component Patterns

## Component Availability

Not all integration libraries have Component classes. This determines your workflow:

- **Has Component class** (dbt, Fivetran, Sling, Airbyte, PowerBI, Looker, Census, dlt): Use directly via `dg scaffold defs`, or subclass to customize behavior.
- **Resource only** (Snowflake, Slack, Datadog, AWS, etc.): Wrap the Resource in a custom component using the Resolvable pattern. See [resolvable-components](../resolvable-components.md).

| Integration | Component Class | Type |
|-------------|----------------|------|
| dbt | `DbtProjectComponent` | Configuration-file-based |
| Sling | `SlingReplicationCollectionComponent` | Configuration-file-based |
| dlt | `DltComponent` | Configuration-file-based |
| Fivetran | `FivetranAccountComponent` | API-based |
| Airbyte | `AirbyteComponent` | API-based |
| PowerBI | `PowerBIWorkspaceComponent` | API-based |
| Looker | `LookerComponent` | API-based |
| Census | `CensusComponent` | API-based |

**Check if an integration has Component classes:**

```bash
uv add dagster-<integration>
uv run dg list components
```

This lists all registered components in the project, including any from newly installed integration packages.

## Configuration-File vs API-Based

### Configuration-File-Based Components

Read from local files. Work out of the box without external credentials:

- `DbtProjectComponent` — Reads dbt project files (`dbt_project.yml`, SQL/Python models)
- `SlingReplicationCollectionComponent` — Reads replication YAML files
- `DltComponent` — Reads Python pipeline definitions

Use directly or subclass for custom behavior (custom asset specs, partitions, metadata). No credential mocking needed.

### API-Based Components

Call external services. Require credentials for production use:

- `FivetranAccountComponent` — Calls Fivetran API
- `PowerBIWorkspaceComponent` — Calls PowerBI API
- `LookerComponent` — Calls Looker API
- `AirbyteComponent` — Calls Airbyte API
- `CensusComponent` — Calls Census API

Subclass to add demo_mode for local development without credentials, or use directly with real credentials.

## Subclassing Integration Components

Override key methods to customize behavior:

### Choosing What to Override

| Method | When to Override |
|--------|-----------------|
| `build_defs()` | Modify definitions, add custom logic, implement demo mode |
| `get_asset_spec()` | Transform asset keys for downstream compatibility. See [asset-key-design](../asset-key-design.md) |
| `execute()` | Customize asset execution logic (legacy pattern) |
| `get_additional_scope()` | Add custom YAML templating functions |

### Dataclass-Based Subclassing (Most Common)

Most integration components use `@dataclass` with the `Resolvable` interface:

```python
from dataclasses import dataclass
import dagster as dg
from <integration_package> import <BaseComponentClass>

@dataclass
class Custom<ComponentName>(BaseComponentClass):
    """Customized component with additional behavior."""

    # New fields automatically appear in YAML schema via Resolvable
    custom_flag: bool = False

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        if self.custom_flag:
            # Custom logic here
            pass
        return super().build_defs(context)
```

**Key points:**

1. Use `@dataclass` decorator on your subclass
2. Fields with type annotations automatically become YAML schema fields
3. Use `field(default_factory=...)` for mutable defaults (lists, dicts)
4. All fields with defaults must come after fields without defaults

Check whether a component uses dataclass or Pydantic:

```bash
uv run python -c "from <package> import <Component>; import dataclasses; print(dataclasses.is_dataclass(<Component>))"
```

### Pydantic BaseModel Subclassing (Rare)

Some components use Pydantic BaseModel. Inherit from both the parent and `dg.Model`:

```python
import dagster as dg
from <integration_package> import <BaseComponentClass>

class Custom<ComponentName>(BaseComponentClass, dg.Model):
    custom_flag: bool = False

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        return super().build_defs(context)
```

### Custom Templating with get_additional_scope()

Add custom functions available in component YAML:

```python
from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any
import dagster as dg
from <integration_package> import <BaseComponentClass>

@dataclass
class Custom<ComponentName>(BaseComponentClass):
    @classmethod
    def get_additional_scope(cls) -> Mapping[str, Any]:
        def _custom_cron(cron_schedule: str) -> dg.AutomationCondition:
            return (
                dg.AutomationCondition.on_cron(cron_schedule)
                & ~dg.AutomationCondition.in_progress()
            )
        return {"custom_cron": _custom_cron}
```

### Component Instance YAML

Reference your subclass with its fully qualified Python path:

```yaml
type: <project_name>.defs.<instance_name>.component.Custom<ComponentName>

attributes:
  custom_flag: true
  # Parent class required fields
  <parent_field>: <value>
```

For API-based components with demo_mode, provide dummy values for required credential fields — they must be present for schema validation even when unused:

```yaml
type: my_project.defs.looker_dashboards.component.CustomLookerComponent

attributes:
  demo_mode: true
  looker_resource:
    base_url: "https://demo.looker.com"
    client_id: "demo_client_id"
    client_secret: "demo_client_secret"
```

## Asset Kinds by Integration

Always set `kinds` on assets to categorize by integration type. This enables filtering in the Dagster UI and makes the technology stack visible at a glance.

| Integration | Kind Value |
|------------|------------|
| dbt | `kinds={"dbt"}` |
| Fivetran | `kinds={"fivetran"}` |
| Sling | `kinds={"sling"}` |
| Airbyte | `kinds={"airbyte"}` |
| PowerBI | `kinds={"powerbi"}` |
| Looker | `kinds={"looker"}` |
| Census | `kinds={"census"}` |
| Snowflake | `kinds={"snowflake"}` |
| Python | `kinds={"python"}` |

Verify with `uv run dg list defs` — the "Kinds" column shows integration types.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Import errors | Install package: `uv add dagster-<integration>`. Hyphens in package names (`dagster-dbt`), underscores in imports (`dagster_dbt`). |
| Schema validation errors | Provide all required fields in YAML. Use dummy values for API-based components with demo_mode. |
| Type reference errors | Verify fully qualified type in `defs.yaml` matches your Python path. Ensure `component.py` is in the correct directory. |
| Component not found | Run `uv run dg list components`. Check package is installed and component class is importable. |
| Validation failures | Check `model_config = ConfigDict(extra="allow")` is set if using Pydantic subclass. |

## References

- [Asset Key Design](../asset-key-design.md) — Designing keys for multi-component pipelines
- [Resolvable Components](../resolvable-components.md) — Creating custom components from scratch
- [Subclassing Components Guide](https://docs.dagster.io/guides/build/components/creating-new-components/subclassing-components)
- [Integration Libraries](https://docs.dagster.io/integrations/libraries)
