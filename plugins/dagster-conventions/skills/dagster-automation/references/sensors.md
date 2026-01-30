# Sensors

Sensors poll for events at regular intervals and perform actions when events occur. They evaluate at
discrete times controlled by `minimum_interval_seconds`.

## Basic Sensor

Sensors are defined with the `@sensor` decorator:

```python
import dagster as dg

@dg.sensor(job=my_job)
def new_file_sensor(context: dg.SensorEvaluationContext):
    new_files = check_for_new_files()

    if new_files:
        for filename in new_files:
            yield dg.RunRequest(run_key=filename)
    else:
        yield dg.SkipReason("No new files found")
```

## RunRequest and Deduplication

`RunRequest` launches a run. The `run_key` parameter prevents duplicate runs:

```python
yield dg.RunRequest(run_key=filename)
```

For a given sensor, only one run is created per unique `run_key`. Subsequent requests with the same
key are skipped.

## SkipReason

`SkipReason` provides a message explaining why the sensor didn't launch a run:

```python
yield dg.SkipReason("No new files found")
```

Messages appear in the Dagster UI tick history.

## Cursors for State Management

Cursors track state across sensor evaluations:

```python
@dg.sensor(job=my_job)
def file_sensor(context: dg.SensorEvaluationContext):
    last_mtime = float(context.cursor) if context.cursor else 0

    max_mtime = last_mtime
    for filename, mtime in get_files_with_timestamps():
        if mtime > last_mtime:
            max_mtime = max(max_mtime, mtime)
            yield dg.RunRequest(run_key=filename)

    context.update_cursor(str(max_mtime))
```

## Evaluation Interval

`minimum_interval_seconds` controls the minimum time between evaluations:

```python
@dg.sensor(job=my_job, minimum_interval_seconds=30)
def new_file_sensor(context):
    ...
```

The interval is a minimum, not exact. If evaluation takes longer than the interval, the next
evaluation is delayed.

## Default Status

Sensors default to `STOPPED` (disabled). Use `default_status` to auto-enable:

```python
@dg.sensor(
    job=my_job,
    default_status=dg.DefaultSensorStatus.RUNNING,
)
def auto_enabled_sensor(context):
    ...
```

Without `RUNNING` status, sensors must be manually enabled in the Dagster UI under **Automation >
Sensors**.

## SensorEvaluationContext Properties

- `cursor`: String cursor from previous evaluation
- `update_cursor(str)`: Update cursor for next evaluation
- `instance`: DagsterInstance
- `log`: Logger for sensor evaluation
- `repository_def`: Repository the sensor belongs to
- `resources`: Access to resource definitions

## Works With

- Asset-based jobs (jobs containing assets)
- Op-based jobs (jobs containing ops and graphs)
