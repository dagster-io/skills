---
title: Asset Definition Properties
triggers:
  - "asset metadata, tags, owners, groups, key_prefix, code_version, AssetSpec properties"
---

# Asset Definition Properties

## Decorator Parameters

Applied once when the asset is defined:

```python
@dg.asset(
    description="Detailed description for the UI",
    group_name="analytics",
    key_prefix=["warehouse", "staging"],
    owners=["team:data-engineering", "user@example.com"],
    tags={"priority": "high", "pii": "true", "domain": "sales"},
    code_version="1.2.0",
)
def my_asset() -> None:
    pass
```

- **owners** — specify team (`team:name`) or individuals for accountability
- **tags** — primary organizational mechanism; use liberally for filtering and grouping (also used by asset selection and automation conditions)
- **code_version** — track when asset logic changes for lineage and debugging
- **description** — explain what the asset represents and its business purpose (docstring also works)
- **group_name** — visual organization in UI; use for data layers or domains
- **key_prefix** — generates the asset key as `AssetKey([*prefix, fn_name])`, e.g. `key_prefix=["warehouse", "raw"]` on a function named `orders` produces `AssetKey(["warehouse", "raw", "orders"])`. Use the `name` argument to override the function name portion (useful in factory patterns that produce many assets from one function).

## Setting Properties on AssetSpec

For `@multi_asset`, set the same properties on each `AssetSpec`:

```python nocheckundefined
@dg.multi_asset(
    specs=[
        dg.AssetSpec(
            "users",
            group_name="raw_data",
            owners=["team:data-engineering"],
            tags={"priority": "high"},
            description="Raw user records from API",
        ),
        dg.AssetSpec(
            "orders",
            group_name="raw_data",
            deps=["users"],
        ),
    ],
)
def load_data(): ...
```

`AssetSpec` accepts the same metadata parameters as `@dg.asset`: `description`, `group_name`, `owners`, `tags`, `kinds`, `deps`, `code_version`, `automation_condition`, `key_prefix`, and more.
