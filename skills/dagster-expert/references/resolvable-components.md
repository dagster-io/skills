# Resolvable Components Pattern

## Overview

The Resolvable pattern is a modern approach to creating custom Dagster components that automatically generates YAML schemas from Python dataclass fields. This eliminates boilerplate and ensures YAML configurations stay in sync with component code.

## Basic Pattern

Use `@dataclass` with `Resolvable` to create components with automatic YAML schema generation:

```python
from dataclasses import dataclass, field
import dagster as dg
from dagster.components import Component, ComponentLoadContext, Resolvable

@dataclass
class CustomETLComponent(Component, Resolvable):
    """Custom ETL component with auto-generated YAML schema.

    All dataclass fields automatically become YAML-configurable via Resolvable.
    """

    # Required fields (no defaults)
    source_table: str
    destination_table: str
    transformation_sql: str

    # Optional fields with defaults
    enable_logging: bool = True
    batch_size: int = 1000

    # Collections use field(default_factory=...)
    custom_tags: list[str] = field(default_factory=list)

    def build_defs(self, context: ComponentLoadContext) -> dg.Definitions:
        """Build asset definitions for this component."""

        @dg.asset(
            key=dg.AssetKey([self.destination_table]),
            kinds={"postgres", "python"},
            tags={tag: "true" for tag in self.custom_tags},
        )
        def etl_asset(context: dg.AssetExecutionContext):
            if self.enable_logging:
                context.log.info(f"Processing {self.source_table} → {self.destination_table}")

            # ETL implementation
            # 1. Query source table
            # 2. Apply transformation_sql
            # 3. Load to destination table
            pass

        return dg.Definitions(assets=[etl_asset])
```

## Corresponding YAML Configuration

```yaml
# defs/my_etl/defs.yaml
type: my_project.components.CustomETLComponent

attributes:
  source_table: "raw_orders"
  destination_table: "processed_orders"
  transformation_sql: "SELECT * FROM raw_orders WHERE status = 'complete'"
  enable_logging: true
  batch_size: 5000
  custom_tags: ["finance", "daily"]
```

## Key Benefits

1. **Automatic YAML schema** - Fields generate YAML schema via `Resolvable`
2. **Type validation** - Type hints provide automatic validation
3. **Optional fields** - Default values make fields optional in YAML
4. **No boilerplate** - No manual schema definition needed
5. **Standard pattern** - Used by most Dagster integration components

## Field Types and Patterns

### Required vs Optional Fields

```python
@dataclass
class MyComponent(Component, Resolvable):
    # Required field - no default value
    required_field: str

    # Optional field - has default value
    optional_field: str = "default_value"
```

### Collections (Lists, Dicts)

Use `field(default_factory=...)` for mutable defaults:

```python
@dataclass
class MyComponent(Component, Resolvable):
    # List field
    tags: list[str] = field(default_factory=list)

    # Dict field
    config: dict[str, str] = field(default_factory=dict)
```

### Nested Configuration

```python
from typing import Optional

@dataclass
class ConnectionConfig:
    host: str
    port: int
    database: str

@dataclass
class MyComponent(Component, Resolvable):
    connection: ConnectionConfig
    backup_connection: Optional[ConnectionConfig] = None
```

## When to Use This Pattern

### Use Resolvable Components When

- Building reusable, configurable patterns
- Need declarative YAML configuration
- Creating organization-specific standards
- Multiple similar implementations with different configs

### Use Regular Pythonic Assets When

- One-off custom logic
- Complex transformation logic
- Fine-grained execution control
- Pattern is used only once

## Complete Example with Asset Selection Scheduling

```python
from dataclasses import dataclass
import dagster as dg
from dagster.components import Component, ComponentLoadContext, Resolvable

@dataclass
class ScheduledJobComponent(Component, Resolvable):
    """Component for scheduling assets using flexible selection syntax."""

    job_name: str
    cron_schedule: str
    asset_selection: str  # Selection string using tags, groups, kinds, etc.

    def build_defs(self, context: ComponentLoadContext) -> dg.Definitions:
        """Build a scheduled job with flexible asset selection."""

        job = dg.define_asset_job(
            name=self.job_name,
            selection=self.asset_selection,
        )

        schedule = dg.ScheduleDefinition(
            job=job,
            cron_schedule=self.cron_schedule,
        )

        return dg.Definitions(schedules=[schedule], jobs=[job])
```

**YAML Configuration:**

```yaml
# Daily finance job - selects by tags
type: my_project.components.ScheduledJobComponent
attributes:
  job_name: "daily_finance_job"
  cron_schedule: "0 6 * * *"
  asset_selection: "tag:schedule=daily and tag:domain=finance"
```

## Best Practices

1. **Type hints are mandatory** - Required for schema generation
2. **Use `field(default_factory=...)` for collections** - Avoid mutable defaults
3. **Document with docstrings** - Explain component purpose and fields
4. **Always include `kinds`** - Add to asset definitions for filtering
5. **Keep components focused** - Single responsibility per component

## References

- [Component Creation Guide](https://docs.dagster.io/guides/build/components/creating-new-components/creating-and-registering-a-component)
- [Component Customization](https://docs.dagster.io/guides/build/components/creating-new-components/component-customization)
- [Project Structure Reference](./project-structure.md) - Where components fit in project layout
