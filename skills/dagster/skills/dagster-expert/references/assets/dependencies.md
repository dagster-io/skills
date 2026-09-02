---
title: Asset Dependencies
triggers:
  - "asset dependencies, parameter-based deps, deps= external dependencies"
---

# Asset Dependencies

## Parameter-Based Dependencies

When an asset depends on another Dagster-managed asset, add it as a function parameter. Dagster uses an **IOManager** to load the upstream asset's output into memory and pass it as a Python object.

```python
@dg.asset
def upstream_asset() -> dict:
    return {"data": [1, 2, 3]}


@dg.asset
def downstream_asset(upstream_asset: dict) -> list:
    # upstream_asset is loaded into memory via IOManager
    return upstream_asset["data"]
```

- Parameter name must match the upstream asset's function name (or asset key)
- Dagster automatically materializes upstream first, then loads and passes the output
- Creates a visible dependency edge in the asset graph
- Use when you want Dagster to manage data transfer between assets

## `deps=` Dependencies

Use `deps=` to declare a data dependency for **lineage and scheduling purposes only**. The asset function does NOT receive the upstream data. Either the function itself handles data access (e.g. reading from a database directly), or some external process ensures the data is available.

```python
@dg.asset(deps=["external_table", "raw_file"])
def processed_data() -> None:
    # No upstream values passed in — read from sources directly
    pass
```

- Declares ordering and lineage without coupling data transfer
- Use when the upstream asset doesn't return a value, is external, or data is managed outside Dagster's IOManager system
- The dependency still affects scheduling: Dagster knows `processed_data` should run after `external_table`

## Mixed Dependencies

Combine both patterns when an asset has some IOManager-managed inputs and some loose data dependencies:

```python
@dg.asset(deps=["raw_file"])
def enriched_data(reference_table: dict) -> dict:
    # reference_table: loaded via IOManager (parameter-based)
    # raw_file: declared dependency only, read manually
    return {"enriched": reference_table}
```
