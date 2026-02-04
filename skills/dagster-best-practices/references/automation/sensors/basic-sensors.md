# Basic Sensors

For the basic sensor pattern with cursors, see the main SKILL.md Quick Reference section.

## File Watching Sensor

A canonical file sensor that monitors a directory for new files and triggers runs:

```python
import os
import json
import dagster as dg

@dg.sensor(job=my_job, minimum_interval_seconds=30)
def file_sensor(context: dg.SensorEvaluationContext):
    # Load cursor (tracks files we've already processed)
    processed_files = json.loads(context.cursor) if context.cursor else {}

    # Check directory for files
    directory = "/data/incoming"
    current_files = {}
    runs_to_request = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        mtime = os.path.getmtime(filepath)
        current_files[filename] = mtime

        # File is new or modified
        if filename not in processed_files or processed_files[filename] != mtime:
            runs_to_request.append(
                dg.RunRequest(
                    run_key=f"{filename}_{mtime}",
                    run_config={"ops": {"my_op": {"config": {"filepath": filepath}}}},
                )
            )

    # Update cursor to track current state
    return dg.SensorResult(
        run_requests=runs_to_request,
        cursor=json.dumps(current_files),
    )
```

**Key pattern**: Store file names and modification times in the cursor to track which files have been processed.

## Cursor State Management

**Best practices for cursors**:

- **Use JSON for structured state**: `json.dumps()` and `json.loads()` make it easy to store dictionaries or lists
- **Handle missing cursor**: Always check if `context.cursor` is None on first evaluation
- **Update cursor atomically**: Return the new cursor value in `SensorResult` or call `context.update_cursor()`
- **Keep cursors small**: Cursors are stored in the database; avoid storing large data structures

**Two ways to update cursors**:

```python
# Option 1: Return SensorResult
return dg.SensorResult(
    run_requests=[...],
    cursor=json.dumps(new_state)
)

# Option 2: Call update_cursor() directly
context.update_cursor(json.dumps(new_state))
yield dg.RunRequest(...)
```

## Evaluation Configuration

**Control evaluation frequency**:

```python
@dg.sensor(
    job=my_job,
    minimum_interval_seconds=60,  # Minimum 60 seconds between evaluations
    default_status=dg.DefaultSensorStatus.RUNNING,  # Auto-enable when deployed
)
def my_sensor(context):
    ...
```

**Important**: `minimum_interval_seconds` is a minimum, not exact. If sensor evaluation takes 10 seconds and the interval is 30 seconds, the next evaluation happens 30 seconds after the previous evaluation started (20 seconds after it completed).

## SensorEvaluationContext

Properties available in sensor context:

- `cursor`: String cursor from the previous evaluation (None if first evaluation)
- `update_cursor(str)`: Update the cursor for the next evaluation
- `instance`: DagsterInstance for querying the event log or other instance data
- `log`: Logger for recording sensor evaluation details
- `repository_def`: Repository containing the sensor
- `resources`: Access configured resources (if defined)

**Example using context.log**:

```python
@dg.sensor(job=my_job)
def logging_sensor(context):
    context.log.info(f"Evaluating sensor, cursor: {context.cursor}")
    # ... sensor logic
```
