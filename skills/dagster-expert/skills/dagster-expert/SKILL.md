---
name: dagster-expert
description:
  Expert guidance for working with Dagster and the dg CLI. ALWAYS use before doing any task that requires
  knowledge specific to Dagster, or that references assets, materialization, components, data tools or data pipelines.
  Common tasks may include creating a new project, adding new definitions, understanding the current project structure, answering general questions about the codebase (finding asset, schedule, sensor, component or job definitions), debugging issues, or providing deep information about a specific Dagster concept.
---

## dg CLI

The `dg` CLI is the recommended way to programmatically interact with Dagster (adding definitions, launching runs, exploring project structure, etc.). It is installed as part of the `dagster-dg-cli` package. If a relevant CLI command for a given task exists, always attempt to use it.

ONLY explore the existing project structure if it is strictly necessary to accomplish the user's goal. In many cases, existing CLI tools will have sufficient understanding of the project structure, meaning listing and reading existing files is wasteful and unnecessary.

Almost all `dg` commands that return information have a `--json` flag that can be used to get the information in a machine-readable format. This should be preferred over the default table output unless you are directly showing the information to the user.

## UV Compatibility

Projects typically use `uv` for dependency management, and it is recommended to use it for `dg` commands if possible:

```bash
uv run dg list defs
uv run dg launch --assets my_asset
```

## Core Dagster Concepts

Brief definitions only (see reference files for detailed examples):

- **Asset**: Persistent object (table, file, model) produced by your pipeline
- **Component**: Reusable building block that generates definitions (assets, schedules, sensors, jobs, etc.) relevant to a particular domain.

## CRITICAL: Always Read Reference Files Before Answering

NEVER answer from memory or guess at CLI commands, APIs, or syntax. ALWAYS read the relevant reference file(s) from the Reference Index below before responding.

For every question, identify which reference file(s) are relevant using the index descriptions, read them, then answer based on what you read.

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
- [cli/asset-selection](./references/cli/asset-selection.md) — Asset selection syntax for filtering by tag, group, kind, upstream, and downstream. (select, filter, tag, group, kind; upstream, downstream, asset selection syntax)
- [cli/check](./references/cli/check.md) — dg check command: validate project configuration and definitions. (validate yaml, validate definitions, check, verify; validate project config; dg check)
- [cli/create-dagster](./references/cli/create-dagster.md) — Create a new Dagster project using the `uvx create-dagster` command. (create a new Dagster project; initial project setup)
- [cli/launch](./references/cli/launch.md) — dg launch command: materialize assets and execute jobs locally. (dg launch; execute locally)
- [cli/api/log](./references/cli/api/log.md) — dg api log get: retrieve and filter run logs from Dagster Plus. (run logs, get logs, debug run; filter logs by level, event type, step)
- [cli/list/component-tree](./references/cli/list/component-tree.md) — dg list component-tree: display component instance hierarchy. (component tree, component hierarchy)
- [cli/list/components](./references/cli/list/components.md) — dg list components: list available component types for scaffolding. (list components, available components, component types; what components can I scaffold)
- [cli/list/defs](./references/cli/list/defs.md) — dg list defs: list and filter registered Dagster definitions. (list defs, list assets, show definitions; filter assets by tag, group, kind)
- [cli/list/envs](./references/cli/list/envs.md) — dg list envs: list environment variables required by the project. (list env vars, environment variables, .env; what env vars are needed)
- [cli/list/projects](./references/cli/list/projects.md) — dg list projects: list projects in the current workspace. (list projects, workspace projects; find project path)
- [cli/plus/login](./references/cli/plus/login.md) — dg plus login: authenticate with Dagster Plus. (login, authenticate, dagster plus auth)
- [cli/plus/pull/env](./references/cli/plus/pull/env.md) — dg plus pull env: pull environment variables from Dagster Plus into a local .env file. (pull env, sync env vars, download env; local env vars; get env vars from dagster plus)
- [cli/scaffold/component](./references/cli/scaffold/component.md) — dg scaffold component: scaffold a custom reusable component type. (custom component, create component type; create reusable component)
- [cli/scaffold/defs](./references/cli/scaffold/defs.md) — dg scaffold defs: add new definitions to a project. (create asset, create schedule, create sensor; add component, scaffold component)
- [components/state-backed-components](./references/components/state-backed-components.md) — State-backed components pattern for Dagster. (state-backed component; component with state)
- [integrations](./references/integrations/INDEX.md) — Integration libraries index for 40+ tools and technologies (dbt, Fivetran, Snowflake, AWS, etc.). (integration, external tool, dagster-\*; dbt, fivetran, airbyte, snowflake, bigquery, sling, aws, gcp)
<!-- END GENERATED INDEX -->
