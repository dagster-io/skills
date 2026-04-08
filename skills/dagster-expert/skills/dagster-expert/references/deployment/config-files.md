---
title: Deployment Configuration Files
triggers:
  - "build.yaml, container_context.yaml, dagster_cloud.yaml"
  - "Dagster Plus deployment configuration"
  - "configuring Docker registry, container context, agent queue"
  - "Hybrid deployment files"
---

# Dagster+ Hybrid Deployment Configuration Files

Dagster+ Hybrid deployments use **three separate configuration files**, each with a distinct purpose. These are scaffolded by `dg plus deploy configure`.

## build.yaml

Defines Docker image build settings. Contains **only two fields**:

```yaml
# build.yaml
registry: 764506304434.dkr.ecr.us-east-1.amazonaws.com/my-image
directory: ./
```

- `registry` — Docker registry URL to push built images to
- `directory` — Path to the directory containing the Dockerfile (default: `.`)

**IMPORTANT:** `build.yaml` does NOT contain `location_name`, `code_source`, `container_context`, `agent_queue`, or other fields. Those belong in other files. The legacy `dagster_cloud.yaml` had all these fields in one file, but the modern `build.yaml` is a strict subset.

## container_context.yaml

Defines infrastructure-specific runtime configuration for code server and run containers. The schema depends on the agent platform (Kubernetes, ECS, or Docker).

All platforms support a top-level `env_vars` list. Platform-specific settings are nested under `k8s`, `ecs`, or `docker`:

```yaml
env_vars:
  - KEY=VALUE     # set a value
  - KEY           # pulled from agent environment
k8s:
  namespace: my-namespace
  env_secrets:
    - my-secret
```

Full schema per platform: see the Kubernetes, ECS, or Docker agent configuration reference in the Dagster docs.

## pyproject.toml [tool.dg.project]

Project metadata and deployment routing. Key deployment-related fields:

```toml
[tool.dg.project]
root_module = "my_project"              # REQUIRED
code_location_name = "my-project"       # defaults to directory name
agent_queue = "special-queue"           # routes to specific agent
image = "my-registry/my-image:latest"   # pre-built image (skips build)
```

If using `dg.toml`, these go under `[project]` instead.

## Workspace merging

In workspaces, both `build.yaml` and `container_context.yaml` can exist at workspace and project levels. Project-level settings override workspace-level settings. A common pattern:

- Workspace `build.yaml`: sets shared `registry`
- Project `build.yaml`: sets project-specific `directory`
- Workspace `container_context.yaml`: shared env vars / namespace
- Project `container_context.yaml`: project-specific resources

## Legacy dagster_cloud.yaml

Older deployments used a single `dagster_cloud.yaml` that combined all configuration into one file with a `locations` array. Each entry contained `location_name`, `code_source`, `build`, `container_context`, `agent_queue`, `image`, `working_directory`, and `executable_path`. This is still supported but new projects should use the three-file approach above.
