---
description: Asset selection syntax for filtering by tag, group, kind, upstream, and downstream.
triggers:
  - "select, filter, tag, group, kind"
  - "upstream, downstream, asset selection syntax"
---

# Asset Selection Syntax

Reference for the asset selection syntax used by `dg list defs --assets` and `dg launch --assets`.

## Attributes

| Attribute | Syntax                             | Example                        |
| --------- | ---------------------------------- | ------------------------------ |
| `key`     | `key:<name>` or `<name>`           | `key:customers` or `customers` |
| `tag`     | `tag:<key>=<value>` or `tag:<key>` | `tag:priority=high`            |
| `owner`   | `owner:<value>`                    | `owner:team@company.com`       |
| `group`   | `group:<value>`                    | `group:sales_analytics`        |
| `kind`    | `kind:<value>`                     | `kind:dbt`                     |

**Wildcards:** `key:customer*`, `key:*_raw`, `*` (all assets)

## Operators

| Operator | Syntax        | Example                                           |
| -------- | ------------- | ------------------------------------------------- |
| AND      | `and` / `AND` | `tag:priority=high and kind:dbt`                  |
| OR       | `or` / `OR`   | `group:sales or group:marketing`                  |
| NOT      | `not` / `NOT` | `not kind:dbt`                                    |
| Grouping | `(expr)`      | `tag:priority=high and (kind:dbt or kind:python)` |

## Functions

| Function      | Description                          | Example                  |
| ------------- | ------------------------------------ | ------------------------ |
| `sinks(expr)` | Assets with no downstream dependents | `sinks(group:analytics)` |
| `roots(expr)` | Assets with no upstream dependencies | `roots(kind:dbt)`        |

## Traversals

| Syntax     | Description               | Example             |
| ---------- | ------------------------- | ------------------- |
| `+expr`    | All upstream dependencies | `+customers`        |
| `expr+`    | All downstream dependents | `customers+`        |
| `N+expr`   | N levels upstream         | `2+kind:dbt`        |
| `expr+N`   | N levels downstream       | `group:sales+1`     |
| `N+expr+M` | N up, M down              | `1+key:customers+2` |

## Examples

```bash
# Select by name
dg launch --assets customers
dg launch --assets "customer*"

# Select by metadata
dg launch --assets "tag:priority=high"
dg launch --assets "group:sales_analytics"
dg launch --assets "kind:dbt"
dg launch --assets "owner:team@company.com"

# Combine with operators
dg launch --assets "tag:priority=high and kind:dbt"
dg launch --assets "group:sales or group:marketing"
dg launch --assets "not kind:dbt"

# With traversals
dg launch --assets "+kind:dbt"            # all upstream of dbt assets
dg launch --assets "group:sales+"         # group:sales + all downstream
dg launch --assets "2+key:customers"      # customers + 2 levels upstream
dg launch --assets "kind:python+1"        # kind:python + 1 level downstream

# With functions
dg launch --assets "sinks(group:analytics)"  # terminal assets in group
dg launch --assets "roots(kind:dbt)"         # source dbt assets
```
