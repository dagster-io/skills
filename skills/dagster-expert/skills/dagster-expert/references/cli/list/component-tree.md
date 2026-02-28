---
description: "dg list component-tree: display component instance hierarchy."
triggers:
  - "component tree, component hierarchy"
---

# dg list component-tree - Component Hierarchy

Display a visual tree of component instances in the project.

```bash
dg list component-tree
```

---

## Options

| Option                 | Description                                                             |
| ---------------------- | ----------------------------------------------------------------------- |
| `--output-file <path>` | Write tree to a file instead of stdout                                  |
| `--target-path <path>` | Directory containing `dg.toml` or `pyproject.toml` to load context from |

---

## Examples

```bash
# Display tree in terminal
dg list component-tree

# Save tree to file
dg list component-tree --output-file tree.txt
```

---

## See Also

- [./components.md](./components.md) - List available component types
