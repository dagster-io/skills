# Run Status Sensors

Run status sensors monitor runs for specific status changes and trigger actions when those statuses
occur.

## Run Failure Sensor

The `@run_failure_sensor` decorator monitors run failures:

```python
import dagster as dg

@dg.run_failure_sensor
def failure_alert_sensor(context: dg.RunFailureSensorContext):
    slack_client.chat_postMessage(
        channel="#alerts",
        text=f'Job "{context.dagster_run.job_name}" failed: {context.failure_event.message}',
    )
```

## Run Status Sensor

The `@run_status_sensor` decorator monitors any run status:

```python
@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.SUCCESS,
    request_job=downstream_job,
)
def success_sensor(context: dg.RunStatusSensorContext):
    if context.dagster_run.job_name == "upstream_job":
        return dg.RunRequest(run_key=context.dagster_run.run_id)
```

## Available Run Statuses

- `DagsterRunStatus.SUCCESS` - Run completed successfully
- `DagsterRunStatus.FAILURE` - Run failed
- `DagsterRunStatus.STARTED` - Run execution started
- `DagsterRunStatus.CANCELED` - Run was canceled
- `DagsterRunStatus.CANCELING` - Run is being canceled

Additional statuses: `QUEUED`, `NOT_STARTED`, `MANAGED`, `STARTING`

## RunStatusSensorContext

Properties available in the context:

- `dagster_run`: The run that triggered the sensor
- `dagster_event`: The event associated with the status change
- `sensor_name`: Name of the sensor
- `instance`: DagsterInstance
- `log`: Logger
- `partition_key`: Partition key from run tags (if partitioned)

## RunFailureSensorContext

Additional properties for failure sensors:

- `failure_event`: The run failure event
- `get_step_failure_events()`: List of step-level failures with stack traces

## Monitoring Specific Jobs

Use `monitored_jobs` to filter which jobs trigger the sensor:

```python
@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.SUCCESS,
    monitored_jobs=[job1, job2],
)
def job_specific_sensor(context):
    ...
```

## Cross-Code Location Monitoring

Set `monitor_all_code_locations=True` to monitor runs across all code locations in the deployment:

```python
@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.FAILURE,
    monitor_all_code_locations=True,
)
def global_failure_sensor(context):
    ...
```

## Triggering Downstream Jobs

Use `request_job` to automatically launch a job when the sensor triggers:

```python
@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.SUCCESS,
    request_job=downstream_job,
)
def trigger_downstream(context: dg.RunStatusSensorContext):
    return dg.RunRequest()
```

## Use Cases

- **Alerting**: Send notifications on run failures via Slack, email, PagerDuty
- **Job coordination**: Launch downstream jobs after upstream success
- **Error handling**: Trigger cleanup jobs on failure
- **Monitoring**: Track run metrics and update dashboards

## Key Parameters

- `run_status`: `DagsterRunStatus` to monitor
- `monitored_jobs`: List of jobs to monitor (optional)
- `monitor_all_code_locations`: Monitor all code locations (default: False)
- `request_job`: Job to launch when sensor triggers (optional)
- `minimum_interval_seconds`: Minimum seconds between evaluations
- `default_status`: `DefaultSensorStatus.RUNNING` or `STOPPED`
