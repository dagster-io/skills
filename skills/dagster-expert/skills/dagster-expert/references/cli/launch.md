# dg launch - Materialize Assets

Materialize Dagster assets or execute jobs.

## Basic Usage

```bash
dg launch --assets <selection>
dg launch --job <job_name>
```

**Examples:**

```bash
# Single asset
dg launch --assets customers

# Multiple assets
dg launch --assets customers,orders,products

# All assets
dg launch --assets "*"

# By metadata
dg launch --assets "tag:priority=high"
dg launch --assets "group:analytics"
dg launch --assets "kind:dbt"

# Combined selection
dg launch --assets "tag:schedule=daily and kind:dbt"

# With traversals (upstream/downstream)
dg launch --assets "+customers"      # All upstream + customers
dg launch --assets "customers+"      # Customers + all downstream
dg launch --assets "+2 customers"    # 2 levels upstream + customers

# Execute job
dg launch --job daily_job
```

See [asset-selection.md](./asset-selection.md) for complete selection syntax.

---

## Partitions

```bash
# Single partition
dg launch --assets my_asset --partition 2024-01-15

# Partition range (backfill) - use three dots
dg launch --assets my_asset --partition-range "2024-01-01...2024-01-31"

# Static partitions
dg launch --assets regional_asset --partition us-west
```

**Note:** Use three dots (`...`) for inclusive ranges, not two dots.

---

## Configuration

```bash
# Inline JSON
dg launch --assets my_asset --config '{"limit": 100}'

# From file
dg launch --assets my_asset --config-file config.yaml
```

---

## Options

| Option                      | Description                            |
| --------------------------- | -------------------------------------- |
| `--assets <selection>`      | Asset selection string                 |
| `--job <name>`              | Job name to execute                    |
| `--partition <key>`         | Single partition key                   |
| `--partition-range <range>` | Partition range (inclusive, use `...`) |
| `--config <json>`           | Inline JSON configuration              |
| `--config-file <path>`      | Configuration file path                |

---

## Preview Before Launch

```bash
# Verify what will be launched
dg list defs --assets "tag:priority=high and kind:dbt"

# Then launch
dg launch --assets "tag:priority=high and kind:dbt"
```

---

## See Also

- [asset-selection.md](./asset-selection.md) - Complete selection syntax including traversals and functions
- [list.md](./list.md) - Preview assets before launching
