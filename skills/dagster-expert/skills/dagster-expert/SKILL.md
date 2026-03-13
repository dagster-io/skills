---
name: dagster-expert
description:
  Expert guidance for working with Dagster and the dg CLI. ALWAYS use before doing any task that requires
  knowledge specific to Dagster, or that references assets, materialization, components, data tools or data pipelines.
  Common tasks may include creating a new project, adding new definitions, understanding the current project structure, answering general questions about the codebase (finding asset, schedule, sensor, component or job definitions), debugging issues, or providing deep information about a specific Dagster concept.
---

## Core Dagster Concepts

Brief definitions only (see reference files for detailed examples):

- **Asset**: Persistent object (table, file, model) produced by your pipeline
- **Component**: Reusable building block that generates definitions (assets, schedules, sensors, jobs, etc.) relevant to a particular domain.

## Integration Workflow

When integrating with ANY external tool or service, read the [Integration libraries index](./references/integrations/INDEX.md). This contains information about which integration libraries exist, and references on how to create new custom integrations for tools that do not have a published library.

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

## CRITICAL: Always Read Reference Files Before Answering

NEVER answer from memory or guess at CLI commands, APIs, or syntax. ALWAYS read the relevant reference file(s) from the Reference Index below before responding.

For every question, identify which reference file(s) are relevant using the index descriptions, read them, then answer based on what you read.

## Reference Index

<!-- BEGIN GENERATED INDEX -->

- [Asset Patterns](./references/assets.md) — defining assets, dependencies, metadata, partitions, or multi-asset definitions
- [Environment Variables](./references/env-vars.md) — configuring environment variables across different environments
- [Choosing an Automation Approach](./references/automation/choosing-automation.md) — deciding between schedules, sensors, and declarative automation
- [Schedules](./references/automation/schedules.md) — time-based automation with cron expressions
- [Declarative Automation](./references/automation/declarative-automation/INDEX.md) — asset-centric condition-based automation using AutomationCondition
- [Asset Sensors](./references/automation/sensors/asset-sensors.md) — triggering on asset materialization events
- [Basic Sensors](./references/automation/sensors/basic-sensors.md) — event-driven automation with file watching or custom polling
- [Run Status Sensors](./references/automation/sensors/run-status-sensors.md) — reacting to run success, failure, or other status changes
- [Asset Selection Syntax](./references/cli/asset-selection.md) — filtering assets by tag, group, kind, upstream, or downstream
- [dg check](./references/cli/check.md) — validating project configuration or definitions
- [create-dagster](./references/cli/create-dagster.md) — creating a new Dagster project from scratch
- [dg dev](./references/cli/dev.md) — starting a local Dagster development instance
- [dg launch](./references/cli/launch.md) — materializing assets or executing jobs locally
- [dg list components](./references/cli/list-components.md) — seeing available component types for scaffolding
- [dg list defs](./references/cli/list-defs.md) — listing or filtering registered definitions
- [Dagster Plus API](./references/cli/api/INDEX.md) — dg api, programmatically querying or managing Dagster Plus resources (assets, runs, deployments, code locations, schedules, sensors, secrets, etc.)
- [dg list](./references/cli/list/INDEX.md) — exploring project structure (component tree, environment variables, workspace projects)
- [Dagster Plus CLI](./references/cli/plus/INDEX.md) — dg plus, Dagster Plus authentication, configuration, and deployment; logging in, setting config, creating API tokens, deploying code, pulling env vars, managing dbt manifests
- [dg scaffold component](./references/cli/scaffold/component.md) — creating a custom reusable component type
- [dg scaffold defs](./references/cli/scaffold/defs.md) — adding new definitions (assets, schedules, sensors, components) to a project
- [dg utilities](./references/cli/utils/INDEX.md) — dg utils, inspecting component types, viewing integrations, refreshing state-backed component cache
- [Creating Components](./references/components/creating-components.md) — building a new custom component from scratch
- [Designing Component Integrations](./references/components/designing-component-integrations.md) — designing a component that wraps an external service or tool; custom integrations
- [Resolved Framework](./references/components/resolved-framework.md) — defining custom YAML schema types using Resolver, Model, or Resolvable
- [Subclassing Components](./references/components/subclassing-components.md) — extending an existing component via subclassing; customize dagster integration component
- [Template Variables](./references/components/template-variables.md) — using Jinja2 template variables in component YAML (env, dg, context, or custom scopes)
- [Creating State-Backed Components](./references/components/state-backed/creating.md) — building a component that fetches and caches external state
- [Using State-Backed Components](./references/components/state-backed/using.md) — managing state-backed components in production, CI/CD, or refreshing state
- [Integration libraries index for 40+ tools and technologies (dbt, Fivetran, Snowflake, AWS, etc.).](./references/integrations/INDEX.md) — integration, external tool, dagster-\*; dbt, fivetran, airbyte, snowflake, bigquery, sling, aws, gcp
<!-- END GENERATED INDEX -->
