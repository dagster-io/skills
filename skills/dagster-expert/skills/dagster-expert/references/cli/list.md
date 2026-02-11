# dg list - Discovery and Inspection

Commands for discovering definitions, components, environment variables, and project structure.

## Subcommands

| Command                  | Description                                      |
| ------------------------ | ------------------------------------------------ |
| `dg list defs`           | List assets, jobs, schedules, sensors, resources |
| `dg list components`     | List available component types for scaffolding   |
| `dg list envs`           | List environment variables and deployment status |
| `dg list projects`       | List projects in workspace                       |
| `dg list component-tree` | Display component hierarchy                      |

---

## dg list defs

List all registered Dagster definitions.

```bash
dg list defs                              # All definitions
dg list defs --json                       # JSON output
dg list defs --assets "tag:priority=high" # Filter assets
dg list defs --columns key,group,kinds    # Custom columns
dg list defs --path ./defs/sales          # Specific path
```

**Options:**

| Option                     | Description                                                                |
| -------------------------- | -------------------------------------------------------------------------- |
| `--json`                   | Output as JSON                                                             |
| `-a, --assets <selection>` | Filter by asset selection (see [asset-selection.md](./asset-selection.md)) |
| `-c, --columns <cols>`     | Columns: `key`, `group`, `deps`, `kinds`, `description`, `tags`, `cron`    |
| `-p, --path <path>`        | Filter by directory path                                                   |

---

## dg list components

List available component types for scaffolding.

```bash
dg list components                        # All components
dg list components --json                 # JSON output
dg list components --package dagster_dbt  # Filter by package
```

**Options:**

| Option                | Description            |
| --------------------- | ---------------------- |
| `--json`              | Output as JSON         |
| `-p, --package <pkg>` | Filter by package name |

**Use with scaffold:**

```bash
dg list components --package dagster_dbt
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt
```

---

## dg list envs

List environment variables required by components.

```bash
dg list envs
```

Shows: variable name, whether set locally, which components use it. With Dagster Plus authentication, also shows deployment scope status (Dev/Branch/Full).

---

## dg list projects

List projects in workspace.

```bash
dg list projects
```

In workspace: outputs project paths. In standalone project: outputs `.`

---

## dg list component-tree

Display component hierarchy tree.

```bash
dg list component-tree
```

Shows visual tree of component instances in the project.

---

## JSON Output

Use `--json` for machine-readable output:

```bash
dg list defs --json | jq '.assets[].key'
dg list defs --json | jq '.assets[] | select(.group == "sales")'
dg list defs --json | jq '.assets | length'
```

## See Also

- [asset-selection.md](./asset-selection.md) - Asset selection syntax for `--assets`
- [scaffold.md](./scaffold.md) - Scaffold components discovered with `dg list components`
- [launch.md](./launch.md) - Launch assets discovered with `dg list defs`
