# Prototype Dagster Implementation

You are helping a developer prototype a new Dagster implementation following best practices. The implementation requirements and working directory have been provided:
$ARGUMENTS

## Overview

This command guides you through building production-ready Dagster code with:
- Best practices from `dagster-conventions` skill
- Appropriate integrations from `dagster-integrations` skill
- Validation and testing at every step
- Components and Pythonic assets as appropriate

## Workflow

### Step 1: Understand Requirements & Plan

1. **Analyze the requirements** to determine:
   - What assets need to be created
   - What integrations are needed
   - Whether to use Components or Pythonic assets (or both)
   - Testing strategy

2. **Reference available integrations**:
   ```bash
   uv run dg docs integrations --json
   ```

   Also consult the `dagster-integrations` skill for finding appropriate integrations for the use case.

3. **Review current project structure**:
   ```bash
   uv run dg list defs
   uv run dg list components
   ```

### Step 2: Choose Implementation Approach

**Use Components when**:
- Implementing common patterns (dbt, Fivetran, Airbyte, dlt, Sling)
- Need declarative YAML configuration
- Want reusability across projects
- Building standardized data pipelines

**Use Pythonic Assets when**:
- Custom business logic required
- Complex transformations
- One-off implementations
- Need fine-grained control

**Use Both**:
- Mix Components for standard patterns (e.g., dbt transformations)
- Use Pythonic assets for custom logic
- Merge definitions as shown in `dagster-conventions`

### Step 3: Implement with Best Practices

#### For Component-Based Implementation

1. **Scaffold the component** (if creating custom):
   ```bash
   uv run dg scaffold component ComponentName
   ```

2. **Create component definitions**:
   ```bash
   uv run dg scaffold defs my_module.components.ComponentName my_component
   ```

3. **Configure in YAML** (`defs/<component_name>.yaml`):
   - Set all required parameters
   - Use `demo_mode: false` for production, `demo_mode: true` for local testing
   - Reference environment variables appropriately

4. **Validate the component loads**:
   ```bash
   uv run dg check defs
   uv run dg list defs
   ```

#### For Pythonic Asset Implementation

1. **Scaffold asset file**:
   ```bash
   uv run dg scaffold defs dagster.asset assets/<domain_name>.py
   ```

2. **Implement assets following conventions**:
   - Use `@dg.asset` decorator with metadata (group_name, owners, tags, kinds)
   - Define clear dependencies via function parameters
   - Use `ConfigurableResource` for external services
   - Add type hints and docstrings
   - Keep assets focused and composable

3. **Example asset structure**:
   ```python
   import dagster as dg
   from my_project.resources import MyDatabaseResource

   @dg.asset(
       group_name="analytics",
       owners=["team:data-engineering"],
       tags={"priority": "high", "domain": "sales"},
       kinds={"snowflake", "python"},
       description="Cleaned and deduplicated customer data",
   )
   def customers(database: MyDatabaseResource) -> None:
       """Load and clean customer data from source database."""
       # Implementation here
       pass

   @dg.asset(
       group_name="analytics",
       owners=["team:data-engineering"],
       tags={"priority": "high", "domain": "sales"},
       kinds={"snowflake", "python"},
   )
   def customer_metrics(customers) -> None:
       """Calculate aggregated customer metrics."""
       # Implementation here
       pass
   ```

4. **Create resources** (`resources.py`):
   ```python
   from dagster import ConfigurableResource, EnvVar

   class MyDatabaseResource(ConfigurableResource):
       connection_string: str = EnvVar("DATABASE_URL")

       def query(self, sql: str) -> list:
           # Implementation
           pass
   ```

5. **Register in definitions** (`definitions.py`):
   ```python
   from dagster import Definitions
   from dagster_dg import load_defs
   from my_project.defs.assets import customers, customer_metrics
   from my_project.defs.resources import MyDatabaseResource

   # Load component definitions
   component_defs = load_defs()

   # Define pythonic assets
   pythonic_defs = Definitions(
       assets=[customers, customer_metrics],
       resources={"database": MyDatabaseResource()},
   )

   # Merge together
   defs = Definitions.merge(component_defs, pythonic_defs)
   ```

### Step 4: Add Automation

Choose the appropriate automation pattern based on requirements:

#### Declarative Automation (Recommended)

```python
from dagster import AutomationCondition

@dg.asset(
    automation_condition=AutomationCondition.on_missing()
    | AutomationCondition.on_cron("0 9 * * *")
)
def automated_asset() -> None:
    pass
```

#### Traditional Schedules

```bash
uv run dg scaffold defs dagster.schedule schedules.py
```

```python
import dagster as dg

my_schedule = dg.ScheduleDefinition(
    job=my_job,
    cron_schedule="0 0 * * *",  # Daily at midnight
)
```

#### Sensors (Event-Driven)

```bash
uv run dg scaffold defs dagster.sensor sensors.py
```

### Step 5: Implement Testing

**Always include tests** following `dagster-conventions` testing patterns:

1. **Create test file** (`tests/test_<asset_name>.py`):
   ```python
   import dagster as dg
   from my_project.defs.assets import customers, customer_metrics
   from unittest.mock import Mock

   def test_customers_asset():
       """Test customers asset logic directly."""
       # Mock dependencies
       mock_database = Mock()
       mock_database.query.return_value = [{"id": 1, "name": "Test"}]

       # Test with dg.materialize
       result = dg.materialize(
           assets=[customers],
           resources={"database": mock_database},
       )

       assert result.success

   def test_customer_metrics_dependency():
       """Test customer_metrics depends on customers."""
       result = dg.materialize(
           assets=[customers, customer_metrics],
           resources={"database": Mock()},
       )

       assert result.success
       assert result.output_for_node("customer_metrics") is not None
   ```

2. **Add asset checks** for data quality:
   ```python
   @dg.asset_check(asset=customers)
   def customers_not_empty(customers):
       """Validate that customers table has data."""
       return dg.AssetCheckResult(
           passed=len(customers) > 0,
           metadata={"row_count": len(customers)},
       )
   ```

3. **Run tests**:
   ```bash
   pytest tests/
   ```

### Step 6: Validate Complete Implementation

Run comprehensive validation checks:

1. **Validate definitions load**:
   ```bash
   uv run dg check defs
   ```

2. **List all definitions** to verify assets are registered:
   ```bash
   uv run dg list defs
   ```

3. **Check components** (if using Components):
   ```bash
   uv run dg list components
   ```

4. **Test asset materialization** in dev mode:
   ```bash
   uv run dg launch --assets <asset_name>
   ```

5. **Run the test suite**:
   ```bash
   pytest tests/ -v
   ```

### Step 7: Documentation & Next Steps

1. **Document the implementation**:
   - Add clear docstrings to all assets
   - Document any custom components
   - Note any environment variables required
   - Explain the data flow

2. **Recommend next steps**:
   - Deploy to staging environment
   - Set up monitoring and alerting
   - Configure production resources
   - Enable automation conditions or schedules

## Key Principles

Throughout implementation, follow these principles from `dagster-conventions`:

- **Think in Assets**: Focus on *what* to produce, not *how* to execute
- **Environment Separation**: Use `ConfigurableResource` and `EnvVar` for configuration
- **Testing First**: Write tests alongside assets
- **Clear Naming**: Use nouns for assets (`customers`, not `load_customers`)
- **Proper Dependencies**: Use function parameters for asset dependencies
- **Metadata Rich**: Add owners, tags, groups, kinds to assets
- **Avoid Over-Engineering**: Keep it simple, don't add unnecessary abstractions

## Reference Documentation

Always cross-reference these resources:

- **Dagster API Reference**: https://docs.dagster.io/llms.txt for titles and descriptions
- **Full API Details**: https://docs.dagster.io/llms-full.txt for complete API information
- **Component Creation**: https://docs.dagster.io/guides/build/components/creating-new-components/creating-and-registering-a-component
- **Component Customization**: https://docs.dagster.io/guides/build/components/creating-new-components/component-customization

## Example Complete Implementation

For reference, here's a complete example structure:

```
my_project/
├── src/
│   └── my_project/
│       ├── definitions.py         # Merge components + pythonic definitions
│       ├── defs/
│       │   ├── assets/
│       │   │   ├── __init__.py
│       │   │   └── analytics.py   # Pythonic assets
│       │   ├── resources.py       # Custom resources
│       │   ├── schedules.py       # (Optional) schedules
│       │   └── my_component.yaml  # Component configurations
│       └── components/            # (Optional) custom components
└── tests/
    ├── test_analytics.py          # Asset tests
    └── test_resources.py          # Resource tests
```

## Validation Checklist

Before considering the prototype complete, ensure:

- [ ] All definitions load successfully (`dg check defs`)
- [ ] Assets appear in `dg list defs` output
- [ ] Tests pass (`pytest tests/`)
- [ ] At least one asset can be materialized (`dg launch --assets <name>`)
- [ ] Resources use environment variables appropriately
- [ ] Assets have proper metadata (owners, tags, groups, kinds)
- [ ] Dependencies are correctly defined
- [ ] Documentation is clear and complete
- [ ] Appropriate integrations from `dagster-integrations` are used
- [ ] Best practices from `dagster-conventions` are followed
