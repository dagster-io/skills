---
name: dagster-expert
description:
  Expert guidance for working with Dagster and the dg CLI. ALWAYS use before doing any task that requires
  knowledge specific to Dagster, or that references assets, materialization, components, data tools or data pipelines.
  Common tasks may include creating a new project, adding new definitions, understanding the current project structure, answering general questions about the codebase (finding asset, schedule, sensor, component or job definitions), debugging issues, or providing deep information about a specific Dagster concept.
---

## Project Exploration

ONLY explore the existing project structure if it is strictly necessary to accomplish the user's goal. In many cases, existing CLI tools will have sufficient understanding of the project structure, meaning listing and reading existing files is wasteful and unnecessary.

## Core Dagster Concepts

Brief definitions only (see reference files for detailed examples):

- **Asset**: Persistent object (table, file, model) produced by your pipeline
- **Job**: Selection of assets to execute together
- **Schedule**: Time-based automation using cron
- **Sensor**: Event-driven automation that watches for changes
- **Declarative Automation**: Modern automation where you set conditions on assets
- **Partition**: Logical division of data (by date, category)
- **Component**: Reusable, declarative building block (YAML-based)

## UV Compatibility

Projects typically use `uv` for dependency management:

```bash
uv run dg list defs
uv run dg launch --assets my_asset
```

## Reference Index

<!-- BEGIN GENERATED INDEX -->

- [asset-key-design](./references/asset-key-design.md) — Asset key design patterns for multi-component pipelines (e.g. Fivetran → dbt → Hightouch). (asset key design or naming; multi-component pipeline key alignment)
- [assets](./references/assets.md) — Asset patterns including dependencies, metadata, partitions, and multi-asset definitions. (asset definition or pattern; dependency, metadata, partition, multi-asset)
- [env-vars](./references/env-vars.md) — Environment variable configuration for Dagster projects across different environments. (environment variables, env, config; different environments, staging, production)
- [implementation-workflow](./references/implementation-workflow.md) — Complete workflow for building production-ready Dagster implementations. (implementation workflow or step-by-step guide; how to build a Dagster project from scratch)
- [project-structure](./references/project-structure.md) — Project structure patterns including code locations, definitions, and directory layout. (project structure, code location, definitions; directory layout, project organization)
- [resolvable-components](./references/resolvable-components.md) — Resolvable components pattern for creating custom Dagster components with auto-generated YAML schemas. (custom component, resolvable pattern; component YAML schema, dataclass fields)
- [automation/choosing-automation](./references/automation/choosing-automation.md) — Decision tree for choosing between schedules, sensors, and declarative automation. (which automation approach, schedule vs sensor vs declarative; set up automation, choose automation type)
- [automation/schedules](./references/automation/schedules.md) — Schedule-based automation using cron expressions and timezones. (schedule, cron, time-based automation; recurring execution, periodic run)
- [automation/declarative-automation](./references/automation/declarative-automation/INDEX.md) — Declarative automation using AutomationCondition for asset-centric condition-based orchestration. (declarative automation, AutomationCondition, conditions; eager, on_cron, on_missing, complex triggers)
- [automation/sensors/asset-sensors](./references/automation/sensors/asset-sensors.md) — Asset sensors that trigger on asset materialization events. (asset sensor, materialization trigger; react to asset update)
- [automation/sensors/basic-sensors](./references/automation/sensors/basic-sensors.md) — Basic sensor patterns for file watching and custom polling with cursors. (file sensor, custom polling, cursor; basic sensor, event-driven trigger)
- [automation/sensors/run-status-sensors](./references/automation/sensors/run-status-sensors.md) — Run status sensors that monitor run success, failure, and trigger actions. (run status sensor, success/failure monitoring; run completion trigger, alerting on run status)
- [cli/api](./references/cli/api.md) — dg api and dg plus commands: API access, Dagster Plus authentication, logs, and debugging. (logs, debug, troubleshoot run; deploy, plus, cloud, dg api)
- [cli/asset-selection](./references/cli/asset-selection.md) — Asset selection syntax for filtering by tag, group, kind, upstream, and downstream. (select, filter, tag, group, kind; upstream, downstream, asset selection syntax)
- [cli/check](./references/cli/check.md) — dg check command: validate project configuration and definitions. (validate, check, verify, test config; dg check)
- [cli/create-dagster](./references/cli/create-dagster.md) — Create a new Dagster project using the `uvx create-dagster` command. (create a new Dagster project; initial project setup)
- [cli/launch](./references/cli/launch.md) — dg launch command: materialize assets, execute jobs, and run backfills. (launch, run, materialize, execute, backfill; dg launch)
- [cli/list](./references/cli/list.md) — dg list command: discover and inspect definitions, assets, and components. (list, show, find, discover, what assets; dg list)
- [cli/scaffold](./references/cli/scaffold.md) — dg scaffold command: create assets, schedules, sensors, and integration components. (scaffold, generate, create asset/schedule/sensor; dg scaffold, new definition)
- [components/state-backed-components](./references/components/state-backed-components.md) — State-backed components pattern for Dagster. (state-backed component; component with state)
- [integrations](./references/integrations/INDEX.md) — Integration libraries index for 40+ tools and technologies (dbt, Fivetran, Snowflake, AWS, etc.). (integration, external tool, dagster-\*; dbt, fivetran, airbyte, snowflake, bigquery, sling, aws, gcp)
<!-- END GENERATED INDEX -->
