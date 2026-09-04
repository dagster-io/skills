---
title: Asset Selection Syntax
triggers:
  - "filtering assets by tag, group, kind, upstream, or downstream"
  - "AssetSelection in Python, UI search bar, or CLI"
---

Assets can be selected two ways:

- **String-based selection syntax** — works identically in the UI search bar, `dg` CLI (`--assets`), and `dg.AssetSelection.from_coercible()` in Python
- **`AssetSelection` in Python** — programmatic API with set operations (`|`, `&`, `-`), traversals, and methods not available in string syntax

## String-Based Selection Syntax

### Attributes

- `key:<name>` or just `<name>` — select by asset key (e.g. `customers`)
- `tag:<key>=<value>` or `tag:<key>` — select by tag (e.g. `tag:priority=high`)
- `owner:<value>` — select by owner (e.g. `owner:team@company.com`)
- `group:<value>` — select by group (e.g. `group:sales_analytics`)
- `kind:<value>` — select by kind (e.g. `kind:dbt`)
- `code_location:<value>` — select by code location (e.g. `code_location:my_project`)
- `status:<value>` — select by materialization status
- `column:<value>` — select by column name (assets with table schema metadata)
- `table_name:<value>` — select by table name
- `column_tag:<key>=<value>` or `column_tag:<key>` — select by column-level tag
- `changed_in_branch:<value>` — select assets changed in a git branch (Dagster Plus)

**Wildcards:** `key:customer*`, `key:*_raw`, `*` (all assets)

### Operators

- `and` / `AND` — e.g. `tag:priority=high and kind:dbt`
- `or` / `OR` — e.g. `group:sales or group:marketing`
- `not` / `NOT` — e.g. `not kind:dbt`
- `(expr)` — grouping, e.g. `tag:priority=high and (kind:dbt or kind:python)`

### Functions

- `sinks(expr)` — assets with no downstream dependents (e.g. `sinks(group:analytics)`)
- `roots(expr)` — assets with no upstream dependencies (e.g. `roots(kind:dbt)`)

### Traversals

- `+expr` — all upstream dependencies (e.g. `+customers`)
- `expr+` — all downstream dependents (e.g. `customers+`)
- `N+expr` — N levels upstream (e.g. `2+kind:dbt`)
- `expr+N` — N levels downstream (e.g. `group:sales+1`)
- `N+expr+M` — N up, M down (e.g. `1+key:customers+2`)

### Examples

Selection strings (work identically in UI, CLI, and Python):

```
# By metadata
tag:priority=high and kind:dbt
group:sales or group:marketing
not kind:dbt
owner:team@company.com

# With traversals
+kind:dbt                        # all upstream of dbt assets
group:sales+                     # group:sales + all downstream
2+key:customers                  # customers + 2 levels upstream

# With functions
sinks(group:analytics)           # terminal assets in group
roots(kind:dbt)                  # source dbt assets
```

Using in the CLI:

```bash
dg launch --assets "tag:priority=high and kind:dbt"
dg list defs --assets "group:sales"
```

Using in Python (via `from_coercible`):

```python
sel = dg.AssetSelection.from_coercible("tag:priority=high and kind:dbt")
```

---

## Python API

### Parsing Selection Strings

`dg.AssetSelection.from_coercible()` converts a selection string (or other coercible types) into an `AssetSelection` object. It accepts:

- A selection string (parsed using the same grammar as the UI and CLI)
- An existing `AssetSelection` instance (returned as-is)
- A sequence of strings (each parsed and unioned together)
- A sequence of `AssetsDefinition` or `AssetKey` objects

```python
# Parse a selection string
sel = dg.AssetSelection.from_coercible("tag:priority=high and kind:dbt")

# Pass to APIs that expect AssetSelection
job = dg.define_asset_job("my_job", selection=sel)
```

### Basic Selection

```python
# Select specific assets
dg.AssetSelection.assets("asset_a", "asset_b", "asset_c")

# Select all assets
dg.AssetSelection.all()

# Select by group
dg.AssetSelection.groups("analytics", "raw_data")

# Select by tag
dg.AssetSelection.tag("priority", "high")
```

### Dependency-Based Selection

```python
# Select asset and all upstream dependencies
dg.AssetSelection.assets("final_report").upstream()

# Select asset and all downstream dependencies
dg.AssetSelection.assets("raw_data").downstream()

# Select asset and immediate upstream only
dg.AssetSelection.assets("final_report").upstream(depth=1)
```

### Combining Selections

```python
selection_a = dg.AssetSelection.assets("a")
selection_b = dg.AssetSelection.assets("b")

# Union: assets in A OR B
selection_a | selection_b

# Intersection: assets in A AND B
selection_a & selection_b

# Difference: assets in A but not in B
selection_a - selection_b

# Example: All analytics assets except one
dg.AssetSelection.groups("analytics") - dg.AssetSelection.assets("excluded_asset")
```

### Using in Jobs

```python
analytics_job = dg.define_asset_job(
    name="analytics_job",
    selection=dg.AssetSelection.groups("analytics").downstream(),
)
```

---

## Python-Only Methods

These methods are only available via the Python API and have no string syntax equivalent:

- `dg.AssetSelection.key_prefixes(["warehouse", "staging"])` — select by key prefix (`key:prefix*` in string syntax is a partial alternative)
- `dg.AssetSelection.key_substring("customer")` — select by substring match on asset key
- `selection.required_multi_asset_neighbors()` — include co-selected assets in non-subsettable multi-asset definitions
- `selection.materializable()` — filter to only materializable (non-observable, non-external) assets
- `selection.upstream_source_assets()` — select external/source assets that are upstream parents
- `selection.without_checks()` — remove asset checks from a selection
- `dg.AssetSelection.checks_for_assets("my_asset")` — select asset checks targeting specific assets
- `dg.AssetSelection.checks(my_check_key)` — select specific asset checks by key
- `dg.AssetSelection.all_asset_checks()` — select all asset checks
