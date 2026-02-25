---
description: Integrating dbt Cloud projects into Dagster for cloud-based dbt orchestration.
triggers:
  - "dbt Cloud, cloud-based dbt"
  - "dbt Cloud integration"
---

# dbt Cloud Integration

The dagster-dbt library provides integration with dbt Cloud via the v2 API (recommended) for
projects hosted on dbt Cloud.

## When to Use

Use the dbt Cloud integration when:

- Your dbt project is hosted and run in dbt Cloud
- You want to trigger dbt Cloud jobs from Dagster
- You want to import dbt Cloud job metadata into Dagster as assets

For dbt Core projects (self-hosted), use the [Component-Based](component-based-integration.md) or
[Pythonic](pythonic-integration.md) integration instead.

## Key Components

- **`DbtCloudWorkspace`**: Resource for accessing a dbt Cloud workspace
- **`DbtCloudCredentials`**: Authentication credentials (account_id, token, access_url)
- **`dbt_cloud_assets`**: Decorator for defining assets from a dbt Cloud job
- **`load_dbt_cloud_asset_specs()`**: Load asset specs from dbt Cloud job
- **`build_dbt_cloud_polling_sensor()`**: Create a sensor that polls for dbt Cloud job completion

## Basic Setup

```python
import dagster as dg
from dagster_dbt import DbtCloudCredentials, DbtCloudWorkspace, dbt_cloud_assets

# Define credentials
dbt_cloud_credentials = DbtCloudCredentials(
    account_id=12345,
    token=dg.EnvVar("DBT_CLOUD_API_TOKEN"),
    access_url="https://cloud.getdbt.com",
)

# Define workspace resource
dbt_cloud = DbtCloudWorkspace(
    credentials=dbt_cloud_credentials,
    project_id=67890,
    environment_id=1,
)


# Define assets from dbt Cloud job
@dbt_cloud_assets(workspace=dbt_cloud)
def my_dbt_cloud_assets(context: dg.AssetExecutionContext):
    # Trigger the dbt Cloud job and wait for completion
    ...


defs = dg.Definitions(
    assets=[my_dbt_cloud_assets],
    resources={"dbt_cloud": dbt_cloud},
)
```

## Features

The dbt Cloud integration:

- Triggers dbt Cloud jobs from Dagster
- Imports dbt models as Dagster assets with proper lineage
- Syncs metadata from dbt Cloud job runs
- Supports polling sensors for external job triggers

For detailed usage, refer to the dagster-dbt dbt Cloud documentation.
