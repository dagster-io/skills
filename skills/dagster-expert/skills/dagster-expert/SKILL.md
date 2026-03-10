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
- [dg api: General](./references/cli/api/general.md) — always read before using any dg api subcommand
- [dg api agent get](./references/cli/api/agent/get.md) — details about a specific Dagster Plus agent
- [dg api agent list](./references/cli/api/agent/list.md) — listing agents in Dagster Plus
- [dg api alert-policy list](./references/cli/api/alert-policy/list.md) — listing alert policies in Dagster Plus
- [dg api alert-policy sync](./references/cli/api/alert-policy/sync.md) — syncing alert policies from YAML definition
- [dg api artifact download](./references/cli/api/artifact/download.md) — downloading an artifact from Dagster Plus
- [dg api artifact upload](./references/cli/api/artifact/upload.md) — uploading an artifact to Dagster Plus
- [dg api asset get-evaluations](./references/cli/api/asset/get-evaluations.md) — automation condition evaluation history for an asset
- [dg api asset get-events](./references/cli/api/asset/get-events.md) — materialization or observation event history for an asset
- [dg api asset get-health](./references/cli/api/asset/get-health.md) — getting asset health or runtime status
- [dg api asset get](./references/cli/api/asset/get.md) — details about a specific asset
- [dg api asset list](./references/cli/api/asset/list.md) — querying which assets exist in a deployment
- [dg api code-location add](./references/cli/api/code-location/add.md) — adding or updating a code location in Dagster Plus
- [dg api code-location delete](./references/cli/api/code-location/delete.md) — deleting a code location from Dagster Plus
- [dg api code-location get](./references/cli/api/code-location/get.md) — details about a specific code location
- [dg api code-location list](./references/cli/api/code-location/list.md) — listing code locations in Dagster Plus
- [dg api deployment delete](./references/cli/api/deployment/delete.md) — deleting a deployment from Dagster Plus
- [dg api deployment get](./references/cli/api/deployment/get.md) — details about a specific deployment
- [dg api deployment list](./references/cli/api/deployment/list.md) — listing deployments in Dagster Plus
- [dg api deployment settings-get](./references/cli/api/deployment/settings-get.md) — getting deployment-level settings in Dagster Plus
- [dg api deployment settings-set](./references/cli/api/deployment/settings-set.md) — setting deployment settings in Dagster Plus
- [dg api organization saml-remove](./references/cli/api/organization/saml-remove.md) — removing SAML metadata from Dagster Plus
- [dg api organization saml-upload](./references/cli/api/organization/saml-upload.md) — uploading SAML metadata for SSO in Dagster Plus
- [dg api organization settings-get](./references/cli/api/organization/settings-get.md) — getting organization-level settings in Dagster Plus
- [dg api organization settings-set](./references/cli/api/organization/settings-set.md) — setting organization settings in Dagster Plus
- [dg api run get-events](./references/cli/api/run/get-events.md) — debugging a run by reading its logs; filtering run events by level or step
- [dg api run get](./references/cli/api/run/get.md) — details about a specific run
- [dg api run list](./references/cli/api/run/list.md) — listing or filtering runs
- [dg api schedule get](./references/cli/api/schedule/get.md) — details about a specific schedule
- [dg api schedule list](./references/cli/api/schedule/list.md) — listing schedules in Dagster Plus
- [dg api secret get](./references/cli/api/secret/get.md) — details about a specific secret
- [dg api secret list](./references/cli/api/secret/list.md) — listing secrets in Dagster Plus
- [dg api sensor get](./references/cli/api/sensor/get.md) — details about a specific sensor
- [dg api sensor list](./references/cli/api/sensor/list.md) — listing sensors in Dagster Plus
- [dg list component-tree](./references/cli/list/component-tree.md) — viewing the component instance hierarchy
- [dg list components](./references/cli/list/components.md) — seeing available component types for scaffolding
- [dg list defs](./references/cli/list/defs.md) — listing or filtering registered definitions
- [dg list envs](./references/cli/list/envs.md) — seeing which environment variables the project requires
- [dg list projects](./references/cli/list/projects.md) — listing projects in the current workspace
- [dg plus login](./references/cli/plus/login.md) — authenticating with Dagster Plus
- [dg plus config set](./references/cli/plus/config/set.md) — set Dagster Plus CLI configuration values
- [dg plus config view](./references/cli/plus/config/view.md) — view current Dagster Plus CLI configuration
- [dg plus create ci-api-token](./references/cli/plus/create/ci-api-token.md) — creating a CI/CD API token for Dagster Plus
- [dg plus deploy configure](./references/cli/plus/deploy/configure.md) — Deploying to Dagster Plus, Github Actions, GitLab CI; CI/CD configuration
- [dg plus deploy](./references/cli/plus/deploy/deploy.md) — ad-hoc deployment to Dagster Plus
- [dg plus integrations dbt manage-manifest](./references/cli/plus/integrations/dbt-manage-manifest.md) — auto-managing dbt manifest uploads to Dagster Plus
- [dg plus pull env](./references/cli/plus/pull/env.md) — pulling environment variables from Dagster Plus into a local .env file
- [dg scaffold component](./references/cli/scaffold/component.md) — creating a custom reusable component type
- [dg scaffold defs](./references/cli/scaffold/defs.md) — adding new definitions (assets, schedules, sensors, components) to a project
- [dg utils inspect-component](./references/cli/utils/inspect-component.md) — inspecting a component type's description, schema, or examples
- [dg utils integrations](./references/cli/utils/integrations.md) — viewing the integration index
- [dg utils refresh-defs-state](./references/cli/utils/refresh-defs-state.md) — refreshing cached state for state-backed components
- [Creating Components](./references/components/creating-components.md) — building a new custom component from scratch
- [Designing Component Integrations](./references/components/designing-component-integrations.md) — designing a component that wraps an external service or tool
- [Resolved Framework](./references/components/resolved-framework.md) — defining custom YAML schema types using Resolver, Model, or Resolvable
- [Subclassing Components](./references/components/subclassing-components.md) — extending an existing component via subclassing
- [Template Variables](./references/components/template-variables.md) — using Jinja2 template variables in component YAML (env, dg, context, or custom scopes)
- [Creating State-Backed Components](./references/components/state-backed/creating.md) — building a component that fetches and caches external state
- [Using State-Backed Components](./references/components/state-backed/using.md) — managing state-backed components in production, CI/CD, or refreshing state
- [Integration libraries index for 40+ tools and technologies (dbt, Fivetran, Snowflake, AWS, etc.).](./references/integrations/INDEX.md) — integration, external tool, dagster-\*; dbt, fivetran, airbyte, snowflake, bigquery, sling, aws, gcp
<!-- END GENERATED INDEX -->
