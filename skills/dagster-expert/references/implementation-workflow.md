# Dagster Implementation Workflow

Complete workflow for building production-ready Dagster implementations following best practices.

## Overview

This guide walks through implementing Dagster projects from requirements to production, covering:

- Component vs Pythonic asset selection
- Multi-asset pipeline patterns
- Automation strategies
- Testing patterns
- Validation workflows

Use this workflow when building new Dagster features or prototyping complete data pipelines.

---

## Step 1: Understand Requirements & Plan

### Analyze Requirements

Determine:

- What assets need to be created
- What integrations are needed (see dagster-integrations skill)
- Whether to use Components or Pythonic assets (or both)
- Testing strategy
- Automation requirements

### Review Current Project Structure

Use [dg CLI commands](./cli/list.md):

```bash
dg list defs
dg list components
```

### Reference Available Integrations

```bash
dg docs integrations --json
```

Consult the dagster-integrations skill for finding appropriate integrations.

---

## Step 2: Choose Implementation Approach

### Use Components When

- Implementing common patterns (dbt, Fivetran, Airbyte, dlt, Sling)
- Need declarative YAML configuration
- Want reusability across projects
- Building standardized data pipelines
- **For dbt**: Use remote Git repository configuration to avoid cloning projects locally

### Use Pythonic Assets When

- Custom business logic required
- Complex transformations
- One-off implementations
- Need fine-grained control

### Use Both

- Mix Components for standard patterns (e.g., dbt transformations)
- Use Pythonic assets for custom logic
- Merge definitions as shown in [project-structure reference](./project-structure.md)

---

## Step 3: Implement with Best Practices

### Component-Based Implementation

#### 1. Scaffold the Component

For custom components (not using built-in integrations):

```bash
dg scaffold component ComponentName
```

See [CLI scaffold reference](./cli/scaffold.md) for full scaffolding details.

#### 2. Create Component Definitions

```bash
dg scaffold defs my_module.components.ComponentName my_component
```

#### 3. Configure in YAML

Create `defs/<component_name>/defs.yaml`:

- Set all required parameters
- Reference environment variables appropriately (see [env-vars reference](./env-vars.md))
- Configure component-specific settings
- **For dbt components**: Prefer `repo_url` + `repo_relative_path` over `project_dir`

#### 4. Validate Component Loads

```bash
dg check defs
dg list defs
```

#### 5. Use Modern Component Pattern

When creating custom components, use the Resolvable pattern for automatic YAML schema generation. See [Resolvable Components reference](./resolvable-components.md) for complete details.

**Quick example:**

```python
from dataclasses import dataclass
import dagster as dg
from dagster.components import Component, ComponentLoadContext, Resolvable

@dataclass
class CustomETLComponent(Component, Resolvable):
    """All dataclass fields automatically become YAML-configurable."""
    source_table: str
    destination_table: str
    enable_logging: bool = True

    def build_defs(self, context: ComponentLoadContext) -> dg.Definitions:
        @dg.asset(
            key=dg.AssetKey([self.destination_table]),
            kinds={"postgres", "python"},
        )
        def etl_asset(context: dg.AssetExecutionContext):
            # Implementation
            pass
        return dg.Definitions(assets=[etl_asset])
```

### Pythonic Asset Implementation

#### 1. Scaffold Asset File

```bash
dg scaffold defs dagster.asset assets/<domain_name>.py
```

#### 2. Implement Assets Following Conventions

- Use `@dg.asset` decorator with metadata (group_name, owners, tags, kinds)
- Define clear dependencies via function parameters
- Use `ConfigurableResource` for external services
- Add type hints and docstrings
- Keep assets focused and composable

#### 3. Example Multi-Asset Chain

Realistic 3-5 asset pipeline demonstrating key patterns:

```python
import dagster as dg
from my_project.resources import DatabaseResource, S3Resource
import pandas as pd

# Asset 1: Raw data ingestion
@dg.asset(
    group_name="sales_analytics",
    owners=["team:data-engineering"],
    tags={"priority": "high", "domain": "sales", "schedule": "daily"},
    kinds={"s3", "python"},  # ALWAYS include kinds
    description="Raw customer orders extracted from operational database",
)
def raw_customer_orders(database: DatabaseResource) -> pd.DataFrame:
    """Extract raw customer orders from operational DB."""
    query = "SELECT * FROM orders WHERE created_at >= CURRENT_DATE - INTERVAL '1 day'"
    return database.query(query)

# Asset 2: Data cleaning/transformation
@dg.asset(
    group_name="sales_analytics",
    owners=["team:data-engineering"],
    tags={"priority": "high", "domain": "sales", "schedule": "daily"},
    kinds={"python"},
    description="Cleaned orders with validation and deduplication",
)
def cleaned_orders(raw_customer_orders: pd.DataFrame) -> pd.DataFrame:
    """Clean and deduplicate order data."""
    df = raw_customer_orders.drop_duplicates(subset=["order_id"])
    df = df.dropna(subset=["order_id", "customer_id", "amount"])
    df["amount"] = df["amount"].astype(float)
    df["created_at"] = pd.to_datetime(df["created_at"])
    return df

# Asset 3: Business logic/aggregation
@dg.asset(
    group_name="sales_analytics",
    owners=["team:data-engineering"],
    tags={"priority": "high", "domain": "sales", "schedule": "daily"},
    kinds={"python"},
    description="Customer lifetime value aggregated by customer",
)
def customer_lifetime_value(cleaned_orders: pd.DataFrame) -> pd.DataFrame:
    """Calculate customer lifetime value metrics."""
    clv = cleaned_orders.groupby("customer_id").agg({
        "amount": "sum",
        "order_id": "count",
        "created_at": ["min", "max"]
    }).reset_index()
    clv.columns = ["customer_id", "total_revenue", "order_count", "first_order", "last_order"]
    clv["avg_order_value"] = clv["total_revenue"] / clv["order_count"]
    return clv

# Asset 4: Enrichment with external data
@dg.asset(
    group_name="sales_analytics",
    owners=["team:data-engineering"],
    tags={"priority": "high", "domain": "sales", "schedule": "daily"},
    kinds={"python", "snowflake"},
    description="CLV enriched with customer demographic data",
)
def enriched_customer_metrics(
    customer_lifetime_value: pd.DataFrame,
    database: DatabaseResource
) -> pd.DataFrame:
    """Enrich CLV metrics with customer demographic data."""
    customers = database.query("SELECT customer_id, segment, region FROM customers")
    enriched = customer_lifetime_value.merge(customers, on="customer_id", how="left")
    return enriched

# Asset 5: Output/export for downstream consumption
@dg.asset(
    group_name="sales_analytics",
    owners=["team:data-engineering"],
    tags={"priority": "high", "domain": "sales", "schedule": "daily"},
    kinds={"s3", "python"},
    description="Customer metrics exported to S3 for BI tools",
)
def customer_metrics_export(
    enriched_customer_metrics: pd.DataFrame,
    s3: S3Resource
) -> None:
    """Export enriched metrics to S3 for Tableau/Looker consumption."""
    s3.write_parquet(
        enriched_customer_metrics,
        bucket="analytics-exports",
        key="customer_metrics/latest.parquet"
    )
```

**Key patterns demonstrated:**

- **Clear asset chain**: raw → cleaned → aggregated → enriched → exported
- **Always include `kinds`**: Helps with filtering and organization
- **Dependencies via parameters**: Each asset lists its dependencies as function parameters
- **Descriptive names**: Nouns that describe the data output, not the action
- **Consistent metadata**: Same group, owners, tags across related assets
- **Type hints**: Specify return types for better IDE support and validation

#### 4. Create Resources

```python
# resources.py
from dagster import ConfigurableResource, EnvVar

class MyDatabaseResource(ConfigurableResource):
    connection_string: str = EnvVar("DATABASE_URL")

    def query(self, sql: str) -> list:
        # Implementation
        pass
```

See [env-vars reference](./env-vars.md) for environment variable patterns.

#### 5. Register in Definitions

```python
# definitions.py
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

---

## Critical: Design Asset Keys for Multi-Component Pipelines

When building multi-component pipelines (e.g., Fivetran → dbt → Hightouch), asset keys must be designed so downstream components can reference them naturally.

**For complete guidance**, see the [Asset Key Design reference](./asset-key-design.md).

**Quick summary:**

- Use flat 2-level keys for dbt consumption: `["fivetran_raw", "customers"]`
- Match expected key structure of downstream components
- Override `get_asset_spec()` when subclassing integration components
- Verify with `dg list defs --json` dependency check

---

## Step 4: Add Automation

Choose the appropriate automation pattern based on requirements:

### Declarative Automation (Recommended)

```python
from dagster import AutomationCondition

@dg.asset(
    automation_condition=AutomationCondition.on_missing()
    | AutomationCondition.on_cron("0 9 * * *")
)
def automated_asset() -> None:
    pass
```

### Traditional Schedules

```bash
dg scaffold defs dagster.schedule schedules.py
```

```python
import dagster as dg

my_schedule = dg.ScheduleDefinition(
    job=my_job,
    cron_schedule="0 0 * * *",  # Daily at midnight
)
```

### Asset Selection-Based Scheduling (Recommended for Scale)

For larger projects, use asset selection syntax instead of hardcoded asset keys. See [Resolvable Components reference](./resolvable-components.md) for a complete example.

**Quick example:**

```yaml
# Daily finance job - selects by tags
type: my_project.components.ScheduledJobComponent
attributes:
  job_name: "daily_finance_job"
  cron_schedule: "0 6 * * *"
  asset_selection: "tag:schedule=daily and tag:domain=finance"
```

**Benefits:**

- No hardcoded asset keys → easier maintenance
- Automatically includes new assets matching criteria
- Self-documenting selection string
- Scales to hundreds of assets

### Sensors (Event-Driven)

```bash
dg scaffold defs dagster.sensor sensors.py
```

---

## Step 5: Implement Testing

**Always include tests** following testing best practices:

### 1. Create Test File

```python
# tests/test_<asset_name>.py
import dagster as dg
from my_project.defs.assets import customers, customer_metrics
from unittest.mock import Mock

def test_customers_asset():
    """Test customers asset logic directly."""
    mock_database = Mock()
    mock_database.query.return_value = [{"id": 1, "name": "Test"}]

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

### 2. Add Asset Checks

```python
@dg.asset_check(asset=customers)
def customers_not_empty(customers):
    """Validate that customers table has data."""
    return dg.AssetCheckResult(
        passed=len(customers) > 0,
        metadata={"row_count": len(customers)},
    )
```

### 3. Run Tests

```bash
pytest tests/
```

---

## Step 6: Validate Complete Implementation

Run comprehensive validation checks:

### 1. Validate Definitions Load

```bash
dg check defs
```

### 2. List All Definitions

```bash
dg list defs
```

### 3. Check Components

If using Components:

```bash
dg list components
```

### 4. Test Asset Materialization

Use [dg launch command](./cli/launch.md):

```bash
dg launch --assets <asset_name>
```

### 5. Run Test Suite

```bash
pytest tests/ -v
```

### 6. Verify Asset Key Alignment and Dependencies

This is CRITICAL for multi-component pipelines. See [Asset Key Design reference](./asset-key-design.md) for complete verification guidance.

**Quick check:**

```bash
dg list defs --json | python -c "
import sys, json
data = json.load(sys.stdin)
assets = data.get('assets', [])
print('Asset Dependencies:\n')
for asset in assets:
    key = asset.get('key', 'unknown')
    deps = asset.get('deps', [])
    if deps:
        print(f'{key}')
        for dep in deps:
            print(f'  ← {dep}')
    else:
        print(f'{key} (no dependencies)')
    print()
"
```

---

## Step 7: Documentation & Next Steps

### Document the Implementation

- Add clear docstrings to all assets
- Document any custom components
- Note any environment variables required (see [env-vars reference](./env-vars.md))
- Explain the data flow

### Recommend Next Steps

- Deploy to staging environment
- Set up monitoring and alerting
- Configure production resources
- Enable automation conditions or schedules

---

## Key Principles

Throughout implementation, follow these principles:

- **Think in Assets**: Focus on _what_ to produce, not _how_ to execute
- **Environment Separation**: Use `ConfigurableResource` and `EnvVar` for configuration
- **Testing First**: Write tests alongside assets
- **Clear Naming**: Use nouns for assets (`customers`, not `load_customers`)
- **Proper Dependencies**: Use function parameters for asset dependencies
- **Metadata Rich**: Add owners, tags, groups, kinds to assets
- **Avoid Over-Engineering**: Keep it simple, don't add unnecessary abstractions

---

## Validation Checklist

Before considering the implementation complete, ensure:

### Core Functionality

- [ ] All definitions load successfully (`dg check defs`)
- [ ] Assets appear in `dg list defs` output
- [ ] Tests pass (`pytest tests/`)
- [ ] At least one asset can be materialized (`dg launch --assets <name>`)

### Asset Quality

- [ ] All assets include `kinds` parameter (e.g., `kinds={"python", "snowflake"}`)
- [ ] Assets have proper metadata (owners, tags, groups)
- [ ] Asset names are descriptive nouns (data outputs, not actions)
- [ ] Resources use environment variables appropriately (`EnvVar`)

### Multi-Component Integration

If using multiple components:

- [ ] Asset keys designed for downstream integration
- [ ] Dependencies verified (see [Asset Key Design reference](./asset-key-design.md))
- [ ] Downstream assets list upstream assets in their `deps` array
- [ ] Asset keys are flat 2-level structure when consumed by dbt
- [ ] No missing dependencies between components

### Components

If using custom components:

- [ ] Dataclass pattern with `@dataclass` + `Resolvable` (see [Resolvable Components reference](./resolvable-components.md))
- [ ] All asset examples include `kinds` parameter

### Automation

If using automation:

- [ ] Schedules/jobs use asset selection syntax (not hardcoded keys) for scalability
- [ ] Selection patterns tested

### Documentation

- [ ] Documentation is clear and complete
- [ ] Appropriate integrations referenced
- [ ] Best practices followed

---

## Related References

- [Asset Patterns Reference](./assets.md) - Detailed asset pattern documentation
- [Project Structure Reference](./project-structure.md) - Project organization patterns
- [Asset Key Design Reference](./asset-key-design.md) - Multi-component pipeline key design
- [Resolvable Components Reference](./resolvable-components.md) - Modern component pattern
- [Environment Variables Reference](./env-vars.md) - Environment configuration
- [CLI Reference](./cli/) - CLI commands for scaffolding, launching, and validation
- dagster-integrations skill - Finding and using integration components

---

## Reference Documentation

Always cross-reference these resources:

- **Dagster API Reference**: https://docs.dagster.io/llms.txt for titles and descriptions
- **Full API Details**: https://docs.dagster.io/llms-full.txt for complete API information
- **Component Creation**: https://docs.dagster.io/guides/build/components/creating-new-components/creating-and-registering-a-component
- **Component Customization**: https://docs.dagster.io/guides/build/components/creating-new-components/component-customization
