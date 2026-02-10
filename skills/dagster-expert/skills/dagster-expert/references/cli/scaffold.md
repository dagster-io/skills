# dg scaffold - Create Definitions

Scaffold Dagster definitions including Python objects (assets, schedules, sensors) and integration components.

**ALWAYS use `dg scaffold` for new definitions.** Do not manually create definition files.

> ⚠️ **PATHS ARE RELATIVE TO defs/ DIRECTORY, not project root**
>
> - ✅ CORRECT: `dg scaffold defs dagster.asset assets/my_asset.py`
> - ❌ WRONG: `dg scaffold defs dagster.asset src/project/defs/assets/my_asset.py`

## Recommended Directory Structure

```
defs/
├── assets/
│   ├── customers.py
│   └── sales/
│       └── revenue.py
├── schedules/
│   └── daily_refresh.py
└── sensors/
    └── file_watcher.py
```

## Python Objects

```bash
dg scaffold defs dagster.asset <path>.py
dg scaffold defs dagster.schedule <path>.py
dg scaffold defs dagster.sensor <path>.py
```

**Examples:**

```bash
# Asset
dg scaffold defs dagster.asset assets/customers.py
dg scaffold defs dagster.asset assets/sales/revenue.py

# Schedule
dg scaffold defs dagster.schedule schedules/daily_refresh.py

# Sensor
dg scaffold defs dagster.sensor sensors/file_watcher.py
```

---

## Integration Components

```bash
dg scaffold defs <component_type> <name> [--json-params '{...}']
```

**Examples:**

```bash
# dbt
dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt --json-params '{
  "project_dir": "dbt_project"
}'

# Sling
dg scaffold defs dagster_sling.SlingReplicationComponent my_sling --json-params '{
  "replication_config": "replication.yaml"
}'
```

**Find available components:**

```bash
dg list components
dg list components --package dagster_dbt
```

**For integration-specific configuration and parameters, use the dagster-integrations skill.**

---

## Custom Components

```bash
# Reusable component type
dg scaffold component MyComponentType
```

Creates a new component class that can be instantiated multiple times via YAML.

---

## Validation Checklist

After scaffolding, always run:

```bash
dg check defs && dg list defs
```

This verifies:

- Definition syntax is valid
- All imports resolve correctly
- Definition appears in the registry

---

## Generated Structure

**Python objects:** Single `.py` file at specified path.

**Integration components:** Directory with `defs.yaml`:

```
defs/
└── my_dbt/
    └── defs.yaml
```

---

## See Also

- [list.md](./list.md) - Discover component types with `dg list components`
- [check.md](./check.md) - Validate definitions after scaffolding
- [launch.md](./launch.md) - Test scaffolded assets
- **dagster-integrations skill** - Integration-specific configuration and parameters
