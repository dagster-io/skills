---
description: "dg list defs: list and filter registered Dagster definitions."
triggers:
  - "list defs, list assets, show definitions"
  - "filter assets by tag, group, kind"
---

# dg list defs - List Definitions

List all registered Dagster definitions (assets, jobs, schedules, sensors, resources) in the current project.

```bash
dg list defs
```

---

## Options

| Option                     | Description                                                                    |
| -------------------------- | ------------------------------------------------------------------------------ |
| `--json`                   | Output as JSON instead of a table                                              |
| `-a, --assets <selection>` | Filter by asset selection (see [../asset-selection.md](../asset-selection.md)) |
| `-c, --columns <cols>`     | Columns to display (comma-separated or repeated flag)                          |
| `-p, --path <path>`        | Filter definitions by directory path                                           |
| `--target-path <path>`     | Directory containing `dg.toml` or `pyproject.toml` to load context from        |

**Available columns:** `key`, `group`, `deps`, `kinds`, `description`, `tags`, `cron`, `is_executable`

---

## Examples

```bash
# Custom columns
dg list defs --columns key,group,kinds
dg list defs -c key -c deps -c tags

# Filter assets by selection syntax
dg list defs --assets "tag:priority=high"
dg list defs --assets "group:sales"
dg list defs --assets "key_prefix:analytics"

# Filter by path
dg list defs --path ./defs/sales

# JSON output for scripting
dg list defs --json | jq '.assets[].key'
dg list defs --json | jq '.assets[] | select(.group == "sales")'
dg list defs --json | jq '.assets | length'
```

---

## See Also

- [../asset-selection.md](../asset-selection.md) - Asset selection syntax for `--assets`
- [../launch.md](../launch.md) - Launch assets discovered with `dg list defs`
