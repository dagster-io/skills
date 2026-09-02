---
title: Advanced Asset Patterns
triggers:
  - "@multi_asset, @graph_asset, @graph_multi_asset, or asset factories"
  - "MaterializeResult, dynamic metadata, MetadataValue types"
---

# Advanced Asset Patterns

## @multi_asset

Use when a single computation produces multiple assets. Define outputs with `specs=[...]` using `AssetSpec`, and yield `MaterializeResult` for each asset.

```python nocheckundefined
@dg.multi_asset(
    specs=[dg.AssetSpec("users"), dg.AssetSpec("orders", deps=["users"])],
)
def load_data():
    users_df = fetch_users()
    yield dg.MaterializeResult(asset_key="users", metadata={"row_count": len(users_df)})

    # orders depend on user data for enrichment
    orders_df = fetch_orders(users_df)
    yield dg.MaterializeResult(asset_key="orders", metadata={"row_count": len(orders_df)})
```

When to use:

- One computation produces multiple related assets
- Assets share expensive setup or have computational dependencies on each other

**Subsettability:** By default, all assets in a `@multi_asset` are materialized together. To allow materializing a subset, set `can_subset=True` on the decorator and `skippable=True` on individual `AssetSpec`s. Use `context.op_execution_context.selected_asset_keys` to check which assets were requested.

**Static metadata on specs:** `AssetSpec` accepts the same metadata parameters as `@dg.asset` — `description`, `group_name`, `owners`, `tags`, `kinds`, `deps`, `code_version`, `automation_condition`, etc. See [Asset Definition Properties](./definition-metadata.md) for details on each parameter.

## MaterializeResult

`MaterializeResult` records dynamic metadata each time an asset materializes. Use it as a return type for `@dg.asset` or yield it in `@multi_asset`.

```python
@dg.asset
def my_asset() -> dg.MaterializeResult:
    data = [...]
    return dg.MaterializeResult(
        metadata={
            "row_count": dg.MetadataValue.int(len(data)),
            "last_updated": dg.MetadataValue.text(str(datetime.now())),
            "sample_data": dg.MetadataValue.json(data[:5]),
        }
    )
```

`MaterializeResult[T]` can also carry a value (like `Output[T]`), making it the preferred return type for greenfield code:

```python
@dg.asset
def my_asset() -> dg.MaterializeResult[dict]:
    data = {"key": "value"}
    return dg.MaterializeResult(value=data, metadata={"size": len(data)})
```

### MetadataValue Types

- `MetadataValue.int(n)` — integer values (row counts)
- `MetadataValue.float(n)` — float values (percentages)
- `MetadataValue.text(s)` — short text values
- `MetadataValue.json(obj)` — JSON-serializable objects
- `MetadataValue.md(s)` — markdown text
- `MetadataValue.url(s)` — clickable URLs
- `MetadataValue.path(s)` — file paths
- `MetadataValue.table(records)` — tabular data

## @graph_asset

Compose multiple `@op`s into a single asset. Each op is independently retriable — if the last step fails, you can retry without re-running earlier steps.

```python
@dg.op
def fetch_data() -> dict:
    return {"raw": [1, 2, 3]}


@dg.op
def transform_data(data: dict) -> dict:
    return {"processed": [x * 2 for x in data["raw"]]}


@dg.graph_asset
def complex_asset():
    raw = fetch_data()
    return transform_data(raw)
```

When to use:

- Single asset requires multiple distinct steps
- You want independent retriability for each step
- Steps are reusable across multiple assets

## @graph_multi_asset

Combine `@graph_asset` and `@multi_asset` — compose ops into a pipeline that produces multiple assets.

```python nocheckundefined
@dg.graph_multi_asset(
    outs={
        "users": dg.AssetOut(),
        "orders": dg.AssetOut(),
    }
)
def etl_pipeline():
    raw_data = extract_from_api()
    cleaned = clean_data(raw_data)
    return {"users": extract_users(cleaned), "orders": extract_orders(cleaned)}
```

When to use:

- Multiple assets require shared complex multi-step logic
- Steps are expensive and should be shared
- Better encapsulation than separate assets with `deps=`
