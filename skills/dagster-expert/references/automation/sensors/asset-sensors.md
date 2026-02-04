# Asset Sensors

Asset sensors monitor asset materializations and trigger jobs when specific assets are materialized.

## Basic Asset Sensor

Use `@asset_sensor` to monitor a specific asset:

```python
import dagster as dg

@dg.asset_sensor(asset_key=dg.AssetKey("daily_sales_data"), job=downstream_job)
def sales_data_sensor(context: dg.SensorEvaluationContext, asset_event: dg.EventLogEntry):
    # Triggered whenever daily_sales_data is materialized
    yield dg.RunRequest(run_key=context.cursor)
```

The sensor is called once per materialization event with the event details in `asset_event`.

## Cross-Job Dependencies

Asset sensors enable dependencies across different jobs:

```python
# Job A contains upstream_asset
@dg.asset
def upstream_asset():
    ...

job_a = dg.define_asset_job("job_a", selection=[upstream_asset])

# Job B is triggered when upstream_asset materializes
@dg.asset_sensor(asset_key=dg.AssetKey("upstream_asset"), job=job_b)
def cross_job_sensor(context, asset_event):
    return dg.RunRequest()
```

This pattern is useful when you have logically separate jobs that need coordination.

## Cross-Code Location Dependencies

Asset sensors can monitor assets in different code locations:

```python
@dg.asset_sensor(
    asset_key=dg.AssetKey("other_location_asset"),
    job=my_job,
)
def cross_location_sensor(context, asset_event):
    return dg.RunRequest()
```

The sensor can be in a different code location than the monitored asset.

## Custom Evaluation Logic

Add conditional logic to control when to trigger:

```python
@dg.asset_sensor(asset_key=dg.AssetKey("daily_sales_data"), job=downstream_job)
def conditional_sensor(context, asset_event):
    # Access materialization metadata
    metadata = asset_event.dagster_event.event_specific_data.materialization.metadata

    row_count = metadata.get("row_count").value if "row_count" in metadata else 0

    if row_count > 1000:
        return dg.RunRequest()
    else:
        return dg.SkipReason(f"Row count {row_count} too low, threshold is 1000")
```

**Use cases for conditional logic**: Trigger downstream processing only when data volume is sufficient, quality checks pass, or specific metadata conditions are met.

## Triggering with Custom Configuration

Pass runtime configuration to the triggered job:

```python
@dg.asset_sensor(asset_key=dg.AssetKey("source_data"), job=processing_job)
def config_sensor(context, asset_event):
    # Extract partition key from the materialization
    partition_key = asset_event.dagster_event.logging_tags.get("dagster/partition")

    return dg.RunRequest(
        run_key=partition_key,
        tags={"dagster/partition": partition_key},
    )
```

This allows you to propagate partition information or other metadata from the upstream asset to the triggered job.

## Asset Sensors vs Declarative Automation

**Use asset sensors when**:

- Triggering imperative side effects (notifications, external API calls)
- Launching jobs with complex custom logic
- Cross-code location dependencies with conditional triggers
- Need to inspect materialization metadata before deciding to trigger

**Use declarative automation when**:

- Automating asset-to-asset execution within the same code location
- Defining dependencies based on asset freshness or missing status
- Requiring sophisticated dependency logic with composable conditions

Declarative automation is the recommended approach for asset-centric workflows. Asset sensors remain valuable for triggering actions outside the asset graph or when you need imperative control.
