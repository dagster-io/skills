---
title: Using State-Backed Components
triggers:
  - "managing state-backed components in production, CI/CD, or refreshing state"
---

# Using State-Backed Components

## What Are State-Backed Components

State-backed components produce Dagster definitions that depend on external systems (BI tools, ETL platforms, compiled artifacts). Instead of calling external APIs on every code server load, they split definition-building into two steps:

1. **`write_state_to_path`** — fetches external state and persists it locally (expensive, runs on refresh)
2. **`build_defs_from_state`** — builds definitions from persisted state (cheap, runs on every load)

The framework controls when refresh happens based on the configured management strategy.

## State Management Strategies

| Strategy                       | Storage                                         | Refresh Mechanism                                            | Best For                                           |
| ------------------------------ | ----------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| `LOCAL_FILESYSTEM`             | `.local_defs_state/` in project dir             | `dg utils refresh-defs-state` in CI before building artifact | Most deployments                                   |
| `VERSIONED_STATE_STORAGE`      | Cloud storage (S3 on Dagster+, or S3/GCS/Azure) | `dg utils refresh-defs-state` or independent of deploys      | Dagster+ (automatic); decoupling state from builds |
| `LEGACY_CODE_SERVER_SNAPSHOTS` | In-memory                                       | Auto-refresh on every code server load                       | Not recommended; changing in 1.13.0                |

### LOCAL_FILESYSTEM

State is written to `.local_defs_state/` inside your project directory. This directory is auto-gitignored but must be included in your deployment artifact (Docker image, PEX).

```
my_project/
├── my_project/
│   ├── defs/
│   └── ...
├── .local_defs_state/
│   ├── DbtProjectComponent[my_dbt_project]/
│   └── FivetranAccountComponent/
├── pyproject.toml
└── .gitignore          # includes .local_defs_state/
```

### VERSIONED_STATE_STORAGE

State is stored in cloud storage with UUID-based versioning. Enables state updates without rebuilding deployment artifacts.

#### Dagster+ (automatic)

On Dagster+, `VERSIONED_STATE_STORAGE` works automatically with no user configuration. Dagster+ uploads and downloads state to an S3 bucket managed by Dagster Labs. Simply set `management_type: VERSIONED_STATE_STORAGE` on your component and Dagster+ handles the rest.

#### OSS / self-hosted (manual configuration)

For OSS or self-hosted deployments, you must configure `dagster.yaml` with a storage backend:

```yaml
# dagster.yaml (OSS / self-hosted only — not needed on Dagster+)
defs_state_storage:
  module: dagster._core.storage.defs_state.blob_storage_state_storage
  class: UPathDefsStateStorage
  config:
    base_path: s3://my-bucket/dagster/defs-state # or gs:// or az://
```

### LEGACY_CODE_SERVER_SNAPSHOTS

In-memory state that auto-refreshes on every code server load. This is the current default for backwards compatibility but is **not recommended**. The default will change in version 1.13.0. Explicitly set `management_type` to `LOCAL_FILESYSTEM` or `VERSIONED_STATE_STORAGE` instead.

### State Storage Availability

All code location loads and run processes require access to the configured `DefsStateStorage`, as state is downloaded in all of these cases. The configured storage must be high-availability.

## Configuring State-Backed Components

Each state-backed component accepts a `defs_state` field in its YAML configuration:

```yaml
type: dagster_fivetran.FivetranAccountComponent

attributes:
  account: ...
  defs_state:
    management_type: LOCAL_FILESYSTEM
    refresh_if_dev: false
```

| Field             | Type                                                                              | Default                        | Description                                                                               |
| ----------------- | --------------------------------------------------------------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------- |
| `management_type` | `LOCAL_FILESYSTEM` \| `VERSIONED_STATE_STORAGE` \| `LEGACY_CODE_SERVER_SNAPSHOTS` | Component-specific             | Storage strategy for state                                                                |
| `key`             | string                                                                            | Auto-generated from class name | Unique identifier for this component's state                                              |
| `refresh_if_dev`  | boolean                                                                           | `true`                         | Auto-refresh state during `dagster dev`. Set `false` to reduce API calls during local dev |

### Dev mode auto-refresh

When `refresh_if_dev: true` (the default), running `dagster dev` or using the `dg` CLI automatically refreshes state on startup. Set to `false` when:

- External API rate limits are a concern
- You want faster local iteration with previously-cached state
- The external system is unavailable in your dev environment

### Viewing state in the Dagster UI

Navigate to **Deployment → [your code location] → Defs state** to see registered state keys, last update timestamps, and version identifiers.

## Defs State Keys

Keys uniquely identify a component's state within a deployment. Default format: `ClassName` or `ClassName[discriminator]`.

- **Auto-generated:** Most components use `self.__class__.__name__` as the default key
- **Discriminator:** Used when multiple instances of the same component exist (e.g., `DbtProjectComponent[analytics]`, `DbtProjectComponent[marketing]`)
- **Custom override:** Set `key` in the YAML `defs_state` block to use a custom key
- **Shared keys:** Two components sharing a key will share the same state — use this intentionally or not at all

## CI/CD State Refresh

Before deploying, refresh state for all state-backed components:

```bash
uv run dg utils refresh-defs-state
```

This fetches current state from all external systems and persists it according to each component's configured strategy.

### LOCAL_FILESYSTEM deployments

Run `dg utils refresh-defs-state` **before** building your Docker image or PEX artifact. The `.local_defs_state/` directory must be included when copying project files into the image.

### VERSIONED_STATE_STORAGE deployments

Ensure the CI environment has:

- `DAGSTER_HOME` pointing to a directory containing `dagster.yaml` with `defs_state_storage` configured
- Cloud storage credentials (AWS, GCS, or Azure) available in the environment

### Dagster+ deployments

Use the Dagster+ variant of the refresh command:

```bash
uv run dg plus deploy refresh-defs-state
```

Or scaffold a complete CI/CD workflow with state refresh included:

```bash
uv run dg scaffold github-actions
```

### Programmatic State Refresh (Without Redeploying)

A component can produce a job that calls `self.refresh_state(project_root)`, decoupling state refresh from the deploy cycle entirely. This job can be triggered via manual runs, schedules, sensors, or the GraphQL API.

```python nocheckundefined
import asyncio
import dagster as dg


class MyApiComponent(dg.StateBackedComponent, dg.Model, dg.Resolvable):
    api_url: str

    # ... defs_state_config, write_state_to_path, build_defs_from_state ...

    def build_defs_from_state(
        self, context: dg.ComponentLoadContext, state_path: Path | None
    ) -> dg.Definitions:
        assets = ...  # build assets from state
        op_name = f"refresh_state_{hash(self.defs_state_config.key) % 10**8}"

        @dg.op(name=op_name)
        def refresh_my_api_state():
            asyncio.run(self.refresh_state(context.project_root))

        @dg.job(name="refresh_my_api_component_state")
        def refresh_job():
            refresh_my_api_state()

        return dg.Definitions(assets=assets, jobs=[refresh_job])
```

After the job runs, the new state is persisted. On Dagster+, use "Refresh definitions state" in the UI or the `refreshDefsState` GraphQL mutation to pick up the new versions (see below). On OSS, the next code location reload automatically uses the latest state.

## Code Location Reloads and Versioned State

How state updates become visible depends on the deployment model:

- **Dagster+**: Each code location load is pinned to specific defs state versions. A normal code location reload does **not** automatically pick up new state versions. To pull in the latest versions, use the "Refresh definitions state" option in the code location dropdown menu in the Dagster UI, or call the `refreshDefsState` GraphQL mutation:

```graphql
mutation RefreshDefsStateMutation($locationName: String!) {
  refreshDefsState(locationName: $locationName) {
    ... on WorkspaceEntry {
      locationName
    }
    ... on RefreshDefsStateError {
      message
    }
  }
}
```

- **OSS / self-hosted**: There is no version pinning. Every code location reload reads the latest state from the configured storage backend. State updates are visible immediately after reload.

This distinction matters when using programmatic refresh or CI/CD pipelines that update state independently of deploys — on Dagster+, you must explicitly request the new versions; on OSS, a reload is sufficient.

## Common State-Backed Components

- **Tableau** — `dagster_tableau.TableauComponent`
- **Looker** — `dagster_looker.LookerComponent`
- **Sigma** — `dagster_sigma.SigmaComponent`
- **Power BI** — `dagster_powerbi.PowerBIWorkspaceComponent`
- **Fivetran** — `dagster_fivetran.FivetranAccountComponent`
- **Airbyte** — `dagster_airbyte.AirbyteWorkspaceComponent`
- **dbt** — `dagster_dbt.DbtProjectComponent`
- **Omni** — `dagster_omni.OmniComponent`
