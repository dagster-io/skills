---
title: Template Variables
triggers:
  - "using Jinja2 template variables in component YAML (env, dg, context, or custom scopes)"
---

# Template Variables

## Overview

Dagster component YAML files support Jinja2 expressions with `{{ expression }}` syntax. Any Resolvable field can accept template strings because the generated schema unions every non-`str` field type with `str`.

Templates are often resolved at component load time, but some contexts resolve independently. For example, post-processing templates (`post_processing.assets[].attributes`) are resolved once per asset, with the current asset available as a template variable.

## Built-in Scopes

### env — Environment Variables

Access environment variables directly or with a fallback default:

```yaml
attributes:
  connection_string: "{{ env.DATABASE_URL }}"
  api_key: "{{ env('API_KEY', 'dev-key-fallback') }}"
```

`{{ env.MY_VAR }}` returns the value or `None` if unset. `{{ env('MY_VAR', 'default') }}` raises an error if unset and no default is provided.

### dg — Dagster Objects

Instantiate Dagster objects directly in YAML:

```yaml
attributes:
  automation_condition: "{{ dg.AutomationCondition.eager() }}"
  partitions_def: "{{ dg.DailyPartitionsDefinition(start_date='2024-01-01') }}"
```

Available objects: `AutomationCondition`, `FreshnessPolicy`, `DailyPartitionsDefinition`, `WeeklyPartitionsDefinition`, `MonthlyPartitionsDefinition`, `HourlyPartitionsDefinition`, `StaticPartitionsDefinition`, `TimeWindowPartitionsDefinition`.

### datetime — Python datetime

```yaml
attributes:
  lookback: "{{ datetime.timedelta(days=7) }}"
  start: "{{ datetime.datetime(2024, 1, 1) }}"
```

Available: `datetime` and `timedelta`.

### context — Component Load Context

Access project information and load other components:

```yaml
attributes:
  root: "{{ context.project_root }}"
  other_component: "{{ context.load_component('other/path') }}"
  sub_defs: "{{ context.build_defs('submodule') }}"
```

### asset — Current Asset (Post-Processing Only)

Available inside `post_processing.assets[].attributes` blocks. The template is resolved independently per matching asset, with `asset` bound to the current `AssetSpec`:

```yaml
post_processing:
  assets:
    - target: "*"
      attributes:
        tags:
          source_group: "{{ asset.group_name }}"
        metadata:
          key_path: "{{ asset.key }}"
```

Available attributes include `key`, `tags`, `group_name`, `metadata`, `kinds`, and all other `AssetSpec` fields.

## Custom Template Variables

### Module-Level Template Vars

Create a `template_vars.py` file and reference it in `defs.yaml`:

```yaml
# defs.yaml
template_vars_module: template_vars.py
```

```python
# template_vars.py
import dagster as dg


@dg.template_var
def team_prefix():
    """Static value — no parameters."""
    return "analytics"


@dg.template_var
def project_name(context: dg.ComponentLoadContext):
    """Context-aware — receives the load context."""
    return context.path.parent.name
```

Template var functions have one of two signatures:

- `() -> Any` — zero parameters, returns a static value
- `(context: ComponentLoadContext) -> Any` — receives the component load context

### Component Static Methods

Define `@template_var` as static methods on a Component class. These are auto-discovered without needing `template_vars_module`:

```python
class MyComponent(dg.Component, dg.Resolvable, dg.Model):
    asset_key: dg.ResolvedAssetKey

    @staticmethod
    @dg.template_var
    def default_group():
        return "ingestion"

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions: ...
```

```yaml
type: my_project.components.MyComponent

attributes:
  asset_key: "{{ default_group }}/my_asset"
```

### User-Defined Functions (UDFs)

Template vars can return callables, which are then invoked with arguments in templates:

```python
# template_vars.py
import dagster as dg


@dg.template_var
def prefixed_key():
    def _make_key(table_name: str) -> str:
        return f"analytics/raw/{table_name}"

    return _make_key
```

```yaml
attributes:
  asset_key: "{{ prefixed_key('orders') }}"
```

## References

- [Resolved Framework](./resolved-framework.md)
