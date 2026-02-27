---
description: "dg scaffold component: scaffold a custom reusable component type."
triggers:
  - "custom component, create component type"
  - "create reusable component"
---

# dg scaffold component - Custom Component Type

Scaffold a new custom Dagster component type class. Must be run inside a Dagster project directory. The scaffold is placed in `<project_name>.lib.<name>`.

This should be used when the new component is expected to be used multiple times within the same project. If the component is expected to be used only once, it is recommended to use `dg scaffold defs inline-component` instead, which will add the component definition directly to the relevant folder underneath the `defs/` directory. See the [dg scaffold defs](./defs.md) reference for more details.

```bash
dg scaffold component <class-name>
```

---

## Options

| Option                 | Description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| `--model / --no-model` | Whether the generated class inherits from `dagster.components.Model`    |
| `--target-path <path>` | Directory containing `dg.toml` or `pyproject.toml` to load context from |

---

## Examples

```bash
# Scaffold a component type with a Model base class (default)
dg scaffold component MyCustomSource

# Scaffold without Model inheritance
dg scaffold component MyCustomSource --no-model
```

## Generated Structure

```
src/<project_name>/lib/
└── my_custom_source.py     # Component class definition
```

The component type will then be available via `dg list components` and can be instantiated with `dg scaffold defs`.

---

## See Also

- [./defs.md](./defs.md) - Scaffold instances of component types
- [../list/components.md](../list/components.md) - Verify your component appears after scaffolding
