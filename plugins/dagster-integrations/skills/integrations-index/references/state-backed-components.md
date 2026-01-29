# StateBackedComponents

StateBackedComponents are Dagster components that depend on external state (compiled artifacts, API responses, etc.) that must be fetched and cached before building Dagster definitions.

## How They Work

StateBackedComponents implement a two-phase lifecycle:
1. **`write_state_to_path(state_path)`** - Fetches state from external sources and writes it to disk
2. **`build_defs_from_state(context, state_path)`** - Builds Dagster definitions from the cached state

Common examples: `DbtProjectComponent` (compiles dbt manifests), `TableauComponent` (syncs dashboards), `FivetranAccountComponent` (syncs connectors).

## State Management: Dev vs Prod

### Development Mode
- State automatically refreshes on code location reload by default
- Controlled by `refresh_if_dev` configuration (defaults to `true`)
- Ensures developers see latest external metadata

### Production Mode
- State refresh handled via `dg utils refresh-defs-state` command in CI/CD
- For Dagster+, use `dg plus deploy refresh-defs-state`
- Command exits with error code on failure to prevent deployment with stale state

## Management Types

**LOCAL_FILESYSTEM**: State stored in `.local_defs_state/` directory. Refreshed before building deployment images. Best for Docker/container deployments.

**VERSIONED_STATE_STORAGE**: State stored in cloud storage (S3/GCS/Azure). Refreshed anytime without rebuilding code. Best for production environments needing frequent state updates without redeployment.

Neither approach is universally recommended—choose based on your deployment constraints and how frequently external state changes.
