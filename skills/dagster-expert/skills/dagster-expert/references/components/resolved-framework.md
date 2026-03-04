---
description: Resolved framework for auto-generating YAML schemas from Python classes using Resolver, Model, and Resolvable.
triggers:
  - "Custom component, component YAML schema"
  - "ResolvedAssetKey, ResolvedAssetSpec"
---

# Resolved Framework

## Overview

The Resolved framework lets you write Pythonic classes that auto-generate YAML schemas with Jinja2 templating support. When a component field needs a non-primitive type (like `AssetKey`, `datetime`, or a custom object), you use `Annotated` with a `Resolver` to define how raw YAML values become Python objects.

Key classes (all importable via `import dagster as dg`):

- **Resolvable** — mixin that enables YAML-to-Python resolution on any class
- **Model** — pydantic `BaseModel` with `extra="forbid"`, recommended for component attributes
- **Resolver** — metadata annotation that defines how a field is resolved from YAML

## Choosing a Base Class

Both `dg.Model` and `@dataclass` are fully supported. Either works well for most components.

**Model (pydantic)** extends pydantic's `BaseModel` with `extra="forbid"`. Benefits:

- Catches typos in YAML early (unknown fields are rejected)
- `Field()` metadata (descriptions, examples, defaults) propagates into the generated YAML schema, improving IDE autocompletion
- More powerful subclassing capabilities (subclasses can add new required fields)

**Dataclass** (`@dataclass`) is a lighter-weight alternative. Use `field(default_factory=...)` for mutable defaults. Dataclasses don't support `Field()` metadata propagation and have the standard Python limitation where subclasses cannot add required fields after optional ones.

**Plain class with annotated `__init__`** is supported for highly specific use cases, but is not recommended for standard use. The framework inspects the `__init__` signature to derive fields.

## Nested Resolution

The Resolved framework supports nesed resolution of classes, making it possible to simultaneously maintain complex python-native classes alongside automatically-generated YAML schemas.

There are a few options for nesting resoltion, depending on the specific use case.

## Nested Resolvable Classes

Any class — not just components — can inherit `dg.Resolvable` + `dg.Model` to get automatic YAML resolution including Jinja2 template support. This is the **preferred approach for structured config objects** like connection configs, database configs, etc.

```python
import dagster as dg


class ConnectionConfig(dg.Model, dg.Resolvable):
    token: str
    hostname: str


class MyComponent(dg.Component, dg.Resolvable, dg.Model):
    connection: ConnectionConfig  # auto-resolved, templates supported
    assets: list[dg.ResolvedAssetSpec]

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions: ...
```

Corresponding YAML — Jinja2 templates work inside nested Resolvable objects:

```yaml
type: my_project.components.my_component.MyComponent

attributes:
  connection:
    token: "{{ env.TOKEN }}"
    hostname: "api.example.com"
  assets:
    - key: my_data/api_results
```

### `Annotated` + `Resolver`

If your value contains a type that is not possible to natively represent in YAML, you can define a custom `Resolver` to handle this translation, and then use `Annotated` to create a new type alias that associates the custom resolver with the target python type.

```python
from typing import Annotated, TypeAlias
from datetime import datetime
import dagster as dg


def resolve_datetime(context: dg.ResolutionContext, raw: str) -> datetime:
    resolved = context.resolve_value(raw, as_type=str)  # process templates first
    return datetime.fromisoformat(resolved)

ResolvedDatetime: TypeAlias = Annotated[datetime, dg.Resolver(resolve_datetime, model_field_type=str)]

class MyComponent(dg.Component, dg.Resolvable, dg.Model):
    # In YAML this field accepts a string; at load time it becomes a datetime
    start_date: ResolvedDatetime

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions: ...
```

### `*Args` Classes

Sometimes, the target python type is a class that you cannot change the base class of (e.g. a third-party library class), but you still want to be able to resolve it from YAML.

In these cases, you can create a separate class that inherits from `dg.Resolvable` + `dg.Model` and mirrors the target python class's constructor signature.

```python
from typing import Annotated, TypeAlias

# ... defined elsewhere ...
class SomeLibraryClass:

    def __init__(self, name: str, age: int): ...

class SomeLibraryClassArgs(dg.Resolvable, dg.Model):
    name: str
    age: int

def resolve_some_library_class(context: dg.ResolutionContext, model) -> SomeLibraryClass:
    # `model` will be an instance of SomeLibraryClassArgs.model()
    # this step will ensure all jinja templates are resolved (and handle any nested resolution)
    args = SomeLibraryClassArgs.resolve_from_model(context, model)
    # once the arguments are fully resolved, we can instantiate the target class using the resolved arguments
    return SomeLibraryClass(**args.model_dump())

ResolvedSomeLibraryClass: TypeAlias = Annotated[SomeLibraryClass, dg.Resolver(resolve_some_library_class, model_field_type=SomeLibraryClassArgs.model())]

class MyComponent(dg.Component, dg.Resolvable, dg.Model):
    some_library_class: ResolvedSomeLibraryClass

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions: ...
```

## Resolver Types

**`Resolver(fn)`** — custom resolution function. The function receives `(context: ResolutionContext, raw_value)` and returns the resolved Python object. String values are template-resolved before the function is called (controlled by `inject_before_resolve`, default `True`).

**`Resolver.default()`** — standard recursive resolution. Resolves templates in the value and any nested Resolvable objects. Use this when the default behavior is sufficient but you want to add `description` or `examples` metadata:

```python
from typing import Annotated

name: Annotated[
    str | None,
    dg.Resolver.default(
        description="Human-readable name of the asset.",
        examples=["my_asset"],
    ),
] = None
```

**`Resolver.passthrough()`** — returns the raw value without template processing or nested resolution. Use for fields that should receive the literal YAML value. This can be useful in cases where you intend to process jinja templates _after_ the component has been loaded.

**`Resolver.from_model(fn)`** — the function receives the entire parent model instead of just the field value. Use when resolution depends on multiple fields together.

`Injected[T]` is a shorthand for `Annotated[T, Resolver.default(model_field_type=str)]` — the field accepts a string in YAML (for template injection) and resolves to type `T`.

## Built-in Type Aliases

**`dg.ResolvedAssetKey`** accepts a string like `"my_database/my_schema/my_table"` in YAML and resolves to an `AssetKey`. Template strings are resolved before parsing.

**`dg.ResolvedAssetSpec`** accepts a structured mapping in YAML (with fields like `key`, `deps`, `group_name`, `tags`, `kinds`, `automation_condition`, `partitions_def`) and resolves to an `AssetSpec`.

**`dg.ResolvedAssetCheckSpec`** accepts a structured mapping and resolves to an `AssetCheckSpec`.

## How Schema Generation Works

When you define a Resolvable class, the framework auto-generates a pydantic model for YAML validation:

1. Each field's type and `Resolver` metadata are inspected
2. If `model_field_type` is set on the Resolver, that type is used in the schema instead of the Python type
3. All non-`str` fields become `field_type | str` in the schema, allowing any field to accept a Jinja2 template string
4. `description` and `examples` from the Resolver propagate into the generated schema, appearing in IDE autocompletion during YAML editing

## References

- [Template Variables](./template-variables.md)
