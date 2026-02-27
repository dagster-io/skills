---
description: "dg launch command: materialize assets and execute jobs locally."
triggers:
  - "dg launch"
  - "execute locally"
---

# dg launch

The `dg launch` command can be used to execute runs of assets or jobs LOCALLY, and in-process. This can be useful in development workflows, but will NOT execute runs on a remote Dagster deployment.

## Basic Usage

```bash
dg launch --assets <selection>
dg launch --job <job_name>
```

See [asset-selection.md](./asset-selection.md) for complete selection syntax.

---

## Partitions

For partitioned assets, the `--partition` option can be used to specify a single partition key to execute, or a range of partition keys if the asset has a BackfillPolicy that supports executing multiple partition keys at once.

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

The `--config` option can be used to provide inline JSON configuration for the run.

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
