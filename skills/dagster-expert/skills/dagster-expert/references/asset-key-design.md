# Asset Key Design for Multi-Component Pipelines

## Overview

When building multi-component pipelines (e.g., Fivetran → dbt → Hightouch), asset keys must be designed so downstream components can reference them naturally. This eliminates per-asset configuration and makes pipelines maintainable.

## Core Principle: Upstream Defines, Downstream Consumes

The upstream component should generate asset keys that downstream components naturally expect. This "configure once, apply to all" approach prevents configuration burden downstream.

## Common Downstream Integration Patterns

### Pattern 1: Keys for dbt Consumption

Use **flat, 2-level keys** like `["source_name", "table"]`:

```python
# GOOD: Flat 2-level keys
["fivetran_raw", "customers"]  # dbt: source('fivetran_raw', 'customers')
["api_data", "orders"]          # dbt: source('api_data', 'orders')

# AVOID: Deeply nested keys
["fivetran", "raw", "production", "customers"]  # Requires extra dbt config
```

**Why flat keys?** dbt sources expect 2-level structure:

```yaml
# sources.yml - works naturally with flat keys
sources:
  - name: fivetran_raw
    tables:
      - name: customers # Matches ["fivetran_raw", "customers"]
      - name: orders # Matches ["fivetran_raw", "orders"]
```

### Pattern 2: Keys for Custom Dagster Assets

Match the key structure those assets expect in their `deps`:

```python
# Upstream component creates:
["raw", "customers"]

# Downstream asset references naturally:
@dg.asset(deps=[dg.AssetKey(["raw", "customers"])])
def processed_customers(): ...
```

### Pattern 3: Keys for Reverse ETL Tools (Census, Hightouch)

Use simple model names from dbt (typically single-level keys):

```python
# dbt creates from model file names:
["customer_lifetime_value"]
["monthly_revenue_by_region"]

# Reverse ETL tools reference by model name directly
```

## Asset Key Anti-Patterns

### ❌ Too Deeply Nested

```python
["company", "team", "project", "environment", "schema", "table"]
# Hard for downstream to reference, requires complex mapping
```

### ❌ Inconsistent Structure

```python
["raw", "customers"]                    # 2 levels
["processed", "finance", "revenue"]     # 3 levels
# Confusing for consumers, unpredictable references
```

### ❌ Generic Names

```python
["data", "table1"]
["output", "result"]
# Not clear what system they're from, conflicts likely
```

### ✅ Good Patterns

```python
["source_system", "entity"]    # ["fivetran_raw", "customers"]
["integration", "object"]      # ["salesforce", "accounts"]
["stage", "table"]             # ["staging", "orders"]
```

## Verifying Asset Key Alignment

After implementing your components, verify dependencies are correct:

```bash
# Check that asset keys and dependencies align
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

**What to verify:**

- ✅ Downstream assets list upstream assets in their `deps` array
- ✅ No missing dependencies (especially dbt models depending on sources)
- ✅ Keys are simple and descriptive (typically 2 levels)
- ✅ No duplicate keys with different structures

**Common issues:**

- **dbt models not depending on sources**: SQL must use `{{ source('source_name', 'table') }}`
- **Nested keys don't match dbt expectations**: Consider flattening (see advanced pattern below)
- **Reverse ETL can't find models**: Use simple model names that match dbt output

## Advanced: Override get_asset_spec() for Key Transformation

When subclassing existing integration components (like Fivetran, Sling), you can override `get_asset_spec()` to transform asset keys for better downstream compatibility.

### When to Use This Pattern

- Subclassing integration components that generate nested keys
- Need to flatten keys for dbt compatibility
- Want to apply consistent key structure across all assets from a component
- "Configure once, apply to all" - one override affects all generated assets

### Example: Flatten Fivetran Keys for dbt

**Problem:** Fivetran creates `["fivetran", "connector_id", "schema", "table"]` but dbt expects `["fivetran_raw", "table"]`.

**Solution:**

```python
from dagster_fivetran import FivetranAccountComponent
from dagster_fivetran.translator import FivetranConnectorTableProps
import dagster as dg

class CustomFivetranComponent(FivetranAccountComponent):
    """Fivetran component with flattened asset keys for dbt compatibility."""

    def get_asset_spec(self, props: FivetranConnectorTableProps) -> dg.AssetSpec:
        """Override to flatten asset keys for easier dbt integration."""
        base_spec = super().get_asset_spec(props)
        original_key = base_spec.key.path

        # Flatten nested key: ["fivetran", "connector", "schema", "table"]
        # becomes: ["fivetran_raw", "table"]
        table_name = original_key[-1]  # Get the last element (table name)
        flattened_key = dg.AssetKey(["fivetran_raw", table_name])

        return base_spec.replace_attributes(key=flattened_key)
```

**Result:** dbt sources work naturally without extra configuration:

```yaml
# sources.yml - no meta.dagster needed!
sources:
  - name: fivetran_raw
    tables:
      - name: customers # Matches ["fivetran_raw", "customers"]
      - name: orders # Matches ["fivetran_raw", "orders"]
```

### When NOT to Override

- Using component directly (not subclassing) → Can't override
- Default keys already work for your pipeline → Keep it simple
- Only one or two assets need different keys → Configure individually instead

### Other Use Cases

- **Sling**: Flatten `["sling", "replication_name", "stream"]` → `["raw", "stream"]`
- **Custom components**: Apply consistent prefixing or namespacing
- **Multi-environment**: Add environment suffix like `_staging` or `_prod`

## Common Multi-Component Scenarios

### Scenario 1: Fivetran → dbt → Reverse ETL

```python
# Fivetran component (override get_asset_spec)
["fivetran_raw", "customers"]  # Flat 2-level

# dbt models automatically depend via source()
["customer_lifetime_value"]    # Single-level from model name

# Reverse ETL references dbt model name
"customer_lifetime_value"
```

### Scenario 2: Sling → Custom Dagster → dbt

```python
# Sling component
["raw", "orders"]              # Flat 2-level

# Custom Dagster asset
@dg.asset(
    key=dg.AssetKey(["staging", "orders_cleaned"]),
    deps=[dg.AssetKey(["raw", "orders"])]
)
def orders_cleaned(): ...

# dbt models
["analytics", "order_metrics"]
```

### Scenario 3: API Ingestion → Multiple dbt Projects

```python
# API ingestion component
["api", "salesforce_accounts"]
["api", "hubspot_contacts"]

# Project 1: Sales dbt
source('api', 'salesforce_accounts')

# Project 2: Marketing dbt
source('api', 'hubspot_contacts')
```

## Validation Checklist

Before deploying multi-component pipelines:

- [ ] Run `dg list defs --json` dependency check (command above)
- [ ] Verify downstream assets show upstream in `deps` array
- [ ] Check dbt models use `{{ source('...') }}` references
- [ ] Confirm asset keys are 2-level structure for dbt consumption
- [ ] Test materialization across component boundaries
- [ ] No duplicate asset keys with different structures

## Troubleshooting Common Issues

| Issue                               | Cause                                 | Fix                                                |
| ----------------------------------- | ------------------------------------- | -------------------------------------------------- |
| dbt models missing dependencies     | SQL doesn't use `{{ source('...') }}` | Add source references in SQL                       |
| Asset keys don't match expectations | Default component keys too nested     | Override `get_asset_spec()` to flatten             |
| Reverse ETL missing deps            | Model names don't match               | Use simple model names or configure explicitly     |
| Duplicate keys                      | Key collision                         | Check key generation logic, ensure unique prefixes |

## References

- [Asset Patterns Reference](./assets.md) - General asset patterns
- [Implementation Workflow](./implementation-workflow.md) - Using this in complete workflows
- [Component Customization](https://docs.dagster.io/guides/build/components/creating-new-components/component-customization)
