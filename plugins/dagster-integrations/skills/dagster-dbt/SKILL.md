---
name: dagster-dbt
description: Expert guidance for integrating dbt with Dagster, either through the CLI or using dbt Cloud. Use when users express an intent to integrate existing dbt projects with Dagster, or request assistance with the `dagster-dbt` integration.
---

# dagster-dbt Integration

The dagster-dbt integration represents dbt models as Dagster assets, enabling granular orchestration at the individual model level.

## Why Use This Integration

- Run and track individual dbt models, seeds, and snapshots as separate assets
- Schedule dbt models alongside other data tools (Python, Spark, etc.)
- Define dependencies between dbt models and other Dagster assets
- Use Dagster's UI to monitor dbt model runs, failures, and logs
- Leverage Dagster's asset selection syntax to run subsets of your dbt project

## Two Integration Approaches

### Component-Based (Recommended)

Configure dbt integration via YAML using `DbtProjectComponent`. This is a StateBackedComponent that automatically compiles and caches your dbt manifest.

- Minimal code, YAML-first configuration
- Supports both colocated and external Git-based dbt projects
- Automatic state management for manifest compilation
- See [Component-Based Integration](references/component-based-integration.md) for details

### Pythonic

Programmatic integration using the `@dbt_assets` decorator for full control over asset definitions.

- Maximum flexibility for complex customization
- Explicit Python code for all configuration
- Direct access to dbt CLI and manifest
- See [Pythonic Integration](references/pythonic-integration.md) for details

## dbt Cloud Integration

The integration also supports dbt Cloud projects via the v2 API. See [dbt Cloud Integration](references/dbt-cloud.md) for details.

## Key Concepts

- **dbt manifest**: Compiled representation of all dbt models, tests, sources, and relationships
- **Asset checks**: dbt tests are loaded as Dagster asset checks by default
- **State management**: For Component approach, see general [StateBackedComponents](../integrations-index/references/state-backed-components.md) pattern
- **Translation**: Customize how dbt nodes map to Dagster assets via `get_asset_spec()` method or YAML config

---

## Quick Reference

| If you're working on...                              | Check this reference                                                                      |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Setting up `DbtProjectComponent` in YAML            | [Component-Based Integration](references/component-based-integration.md)                  |
| Using `@dbt_assets` decorator                        | [Pythonic Integration](references/pythonic-integration.md)                                |
| Customizing asset metadata via YAML `translation:`   | [Component-Based Integration](references/component-based-integration.md#translation)      |
| Overriding `get_asset_spec()` method                 | Both integration references                                                               |
| Incremental models with partitions                   | [Component-Based](references/component-based-integration.md#incremental-models) / [Pythonic](references/pythonic-integration.md#incremental-models) |
| Managing dbt manifest compilation (dev vs prod)      | [Component-Based Integration](references/component-based-integration.md#state-management) |
| Enabling dbt tests as asset checks                   | [Asset Checks](references/asset-checks.md)                                                |
| Adding dependencies between dbt and Dagster assets   | [Dependencies](references/dependencies.md)                                                 |
| Fetching column metadata and row counts              | [Component-Based](references/component-based-integration.md#metadata) / [Pythonic](references/pythonic-integration.md#metadata) |
| Scheduling dbt models                                | [Component-Based](references/component-based-integration.md#scheduling) / [Pythonic](references/pythonic-integration.md#scheduling) |
| Using dbt Cloud instead of dbt Core                  | [dbt Cloud Integration](references/dbt-cloud.md)                                          |
| Understanding StateBackedComponent patterns          | [StateBackedComponents](../integrations-index/references/state-backed-components.md)      |

---
