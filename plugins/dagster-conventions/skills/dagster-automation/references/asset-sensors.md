# Asset Sensors

Asset sensors monitor asset materializations and trigger actions when specific assets are
materialized.

## Basic Asset Sensor

The `@asset_sensor` decorator monitors a specific asset:

```python
import dagster as dg

@dg.asset_sensor(asset_key=dg.AssetKey("daily_sales_data"), job=downstream_job)
def sales_data_sensor(context: dg.SensorEvaluationContext, asset_event: dg.EventLogEntry):
    yield dg.RunRequest(run_key=context.cursor)
```

## When Triggered

Asset sensors trigger when the monitored asset is materialized, providing access to the
materialization event.

## Cross-Job Dependencies

Asset sensors enable dependencies across different jobs:

```python
# Asset in job A
@dg.asset
def upstream_asset():
    ...

# Sensor monitors upstream_asset and triggers job B
@dg.asset_sensor(asset_key=dg.AssetKey("upstream_asset"), job=job_b)
def cross_job_sensor(context, asset_event):
    return dg.RunRequest()
```

## Cross-Code Location Dependencies

Asset sensors can monitor assets in different code locations by specifying the asset key:

```python
@dg.asset_sensor(
    asset_key=dg.AssetKey("other_location_asset"),
    job=my_job,
)
def cross_location_sensor(context, asset_event):
    return dg.RunRequest()
```

## Custom Evaluation Logic

Add conditional logic to control when to trigger:

```python
@dg.asset_sensor(asset_key=dg.AssetKey("daily_sales_data"), job=downstream_job)
def conditional_sensor(context, asset_event):
    # Access materialization metadata
    metadata = asset_event.dagster_event.event_specific_data.materialization.metadata

    if metadata.get("row_count").value > 1000:
        return dg.RunRequest()
    else:
        return dg.SkipReason("Row count too low")
```

## Triggering with Custom Configuration

Pass configuration to the triggered job:

```python
@dg.asset_sensor(asset_key=dg.AssetKey("source_data"), job=processing_job)
def config_sensor(context, asset_event):
    partition_key = asset_event.dagster_event.logging_tags.get("dagster/partition")

    return dg.RunRequest(
        run_key=partition_key,
        tags={"dagster/partition": partition_key},
    )
```

## Accessing Upstream Tags

Retrieve partition keys or other tags from the upstream materialization:

```python
partition_key = asset_event.dagster_event.logging_tags.get("dagster/partition")
```

## Multi-Asset Sensors (Deprecated)

`@multi_asset_sensor` monitors multiple assets but is deprecated. Use declarative automation instead
for asset-to-asset dependencies.

## Asset Sensors vs Declarative Automation

**Use asset sensors when:**

- Triggering side effects (notifications, external API calls)
- Launching jobs imperatively with custom logic
- Cross-code location dependencies with complex conditions

**Use declarative automation when:**

- Automating asset-to-asset execution
- Defining dependencies based on asset state
- Requiring sophisticated dependency logic

Declarative automation is recommended for asset-centric workflows. Asset sensors remain useful for
triggering non-asset actions in response to materializations.

## Key Parameters

- `asset_key`: `AssetKey` to monitor
- `job`: Job to trigger (optional if returning custom actions)
- `minimum_interval_seconds`: Minimum seconds between evaluations
- `default_status`: `DefaultSensorStatus.RUNNING` or `STOPPED`

## Context and Event

**`context` (SensorEvaluationContext):**

- `cursor`: State tracking
- `instance`: DagsterInstance
- `log`: Logger

**`asset_event` (EventLogEntry):**

- `dagster_event`: Event details including materialization metadata
- `dagster_event.logging_tags`: Tags from the run (e.g., partition key)
