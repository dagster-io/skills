---
name: dagster-automation
description:
  Comprehensive guide to Dagster automation methods including schedules, sensors, and declarative
  automation. Covers time-based scheduling, event-driven execution, run status monitoring, and
  complex automation conditions with operands and operators.
---

# Dagster Automation Expert

## When to Use This Skill

| If User Says...                        | Use This Section/Reference                                                |
| -------------------------------------- | ------------------------------------------------------------------------- |
| "schedule this to run daily"           | [Schedules Quick Reference](#schedules-quick-reference)                   |
| "trigger when file arrives"            | [Sensors Quick Reference](#sensors-quick-reference)                       |
| "notify on job failure"                | [Run Status Sensors Quick Reference](#run-status-sensors-quick-reference) |
| "run after upstream updates"           | [Declarative Automation](#declarative-automation-quick-reference)         |
| "automation conditions"                | [Declarative Automation](#declarative-automation-quick-reference)         |
| "how do I customize eager()"           | `references/declarative-automation-customization.md`                      |
| "what operands are available"          | `references/declarative-automation-operands.md`                           |
| "status vs event"                      | `references/declarative-automation-advanced.md`                           |
| "run grouping"                         | `references/declarative-automation-advanced.md`                           |
| "which automation method should I use" | [Selection Criteria](#selection-criteria)                                 |
| "cross-code location dependencies"     | `references/asset-sensors.md`                                             |

## Core Philosophy

**Schedules for Simplicity**: Use schedules when you need fixed-time execution without dependency
logic. Do not attempt to use Declarative Automation in cases where a schedule would suffice.

**Sensors for Flexibility**: Use sensors when you need custom polling logic, external system
integration, or imperative actions beyond asset execution.

**Prefer Declarative Automation For Complex Use Cases**: For asset-based pipelines, use declarative
automation over schedules or sensors when possible. It provides:

- **Asset-native**: Set conditions directly on assets without separate job definitions
- **Dependency-aware**: Automatically considers upstream state
- **Composable**: Build complex conditions from simple building blocks
- **Maintainable**: Conditions are declarative and easier to reason about

**Think in Conditions**: Declarative automation uses a status/event model where conditions can be
persistent states (statuses) or transient moments (events). Understanding this distinction is key to
building correct automation.

---

## Quick Reference

| If you're writing...                     | Check this section/reference                                                                    |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `ScheduleDefinition`                     | [Schedules](#schedules-quick-reference) or `references/schedules.md`                            |
| `@dg.sensor`                             | [Sensors](#sensors-quick-reference) or `references/sensors.md`                                  |
| `@dg.run_status_sensor`                  | [Run Status Sensors](#run-status-sensors-quick-reference) or `references/run-status-sensors.md` |
| `@dg.run_failure_sensor`                 | [Run Status Sensors](#run-status-sensors-quick-reference) or `references/run-status-sensors.md` |
| `@dg.asset_sensor`                       | [Asset Sensors](#asset-sensors-quick-reference) or `references/asset-sensors.md`                |
| `AutomationCondition.eager()`            | [Declarative Automation](#declarative-automation-quick-reference)                               |
| `AutomationCondition.on_cron()`          | [Declarative Automation](#declarative-automation-quick-reference)                               |
| `AutomationCondition.on_missing()`       | [Declarative Automation](#declarative-automation-quick-reference)                               |
| Custom automation conditions             | `references/declarative-automation-customization.md`                                            |
| `.since()` or `.newly_true()`            | `references/declarative-automation-operators.md`                                                |
| `any_deps_match()` or `all_deps_match()` | `references/declarative-automation-operators.md`                                                |
| `.allow()` or `.ignore()`                | `references/declarative-automation-advanced.md`                                                 |

---

## Schedules Quick Reference

Execute jobs at specified times using cron expressions.

### Basic Schedule

```python
import dagster as dg

daily_refresh_job = dg.define_asset_job("daily_refresh_job", selection="*")

daily_schedule = dg.ScheduleDefinition(
    job=daily_refresh_job,
    cron_schedule="0 0 * * *",  # Midnight UTC daily
)
```

### Timezone Configuration

```python
daily_schedule = dg.ScheduleDefinition(
    job=daily_refresh_job,
    cron_schedule="0 9 * * *",
    execution_timezone="America/Los_Angeles",
)
```

### Partitioned Job Schedules

```python
from dagster import DailyPartitionsDefinition, build_schedule_from_partitioned_job

@dg.asset(partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"))
def daily_asset():
    ...

partitioned_job = dg.define_asset_job("partitioned_job", selection=[daily_asset])

# Schedule inherits daily cadence from partition definition
schedule = build_schedule_from_partitioned_job(partitioned_job)
```

**Works with**: Both asset-based and op-based jobs

**Details**: `references/schedules.md`

---

## Sensors Quick Reference

Poll for events at regular intervals and perform actions when events occur.

### Basic Sensor

```python
@dg.sensor(job=my_job)
def new_file_sensor(context: dg.SensorEvaluationContext):
    new_files = check_for_new_files()

    if new_files:
        for filename in new_files:
            yield dg.RunRequest(run_key=filename)
    else:
        yield dg.SkipReason("No new files found")
```

### Sensor with Cursor

Track state across evaluations:

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

### Key Concepts

- **`RunRequest(run_key=...)`**: Launch a run. Use `run_key` for deduplication.
- **`SkipReason("message")`**: Explain why no run was launched.
- **`context.cursor`**: Read previous state.
- **`context.update_cursor(str)`**: Update state for next evaluation.
- **`minimum_interval_seconds`**: Control evaluation frequency.

### Auto-Enable Sensor

```python
@dg.sensor(
    job=my_job,
    default_status=dg.DefaultSensorStatus.RUNNING,
)
def auto_enabled_sensor(context):
    ...
```

**Works with**: Both asset-based and op-based jobs

**Details**: `references/sensors.md`

---

## Run Status Sensors Quick Reference

Monitor runs for status changes and trigger actions.

### Run Failure Sensor

```python
@dg.run_failure_sensor
def failure_alert(context: dg.RunFailureSensorContext):
    slack_client.chat_postMessage(
        channel="#alerts",
        text=f'Job "{context.dagster_run.job_name}" failed: {context.failure_event.message}',
    )
```

### Run Status Sensor

```python
@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.SUCCESS,
    request_job=downstream_job,
)
def success_sensor(context: dg.RunStatusSensorContext):
    return dg.RunRequest()
```

### Available Statuses

- `DagsterRunStatus.SUCCESS` - Run completed successfully
- `DagsterRunStatus.FAILURE` - Run failed
- `DagsterRunStatus.STARTED` - Run execution started
- `DagsterRunStatus.CANCELED` - Run was canceled

### Monitor Specific Jobs

```python
@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.SUCCESS,
    monitored_jobs=[job1, job2],
)
def job_specific_sensor(context):
    ...
```

### Cross-Code Location Monitoring

```python
@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.FAILURE,
    monitor_all_code_locations=True,
)
def global_failure_sensor(context):
    ...
```

**Use cases**: Alerting, job coordination, error handling, monitoring

**Details**: `references/run-status-sensors.md`

---

## Asset Sensors Quick Reference

Monitor asset materializations and trigger actions.

### Basic Asset Sensor

```python
@dg.asset_sensor(asset_key=dg.AssetKey("daily_sales_data"), job=downstream_job)
def sales_sensor(context: dg.SensorEvaluationContext, asset_event: dg.EventLogEntry):
    return dg.RunRequest()
```

### Conditional Logic

```python
@dg.asset_sensor(asset_key=dg.AssetKey("source_data"), job=processing_job)
def conditional_sensor(context, asset_event):
    metadata = asset_event.dagster_event.event_specific_data.materialization.metadata

    if metadata.get("row_count").value > 1000:
        return dg.RunRequest()
    else:
        return dg.SkipReason("Row count too low")
```

### Access Partition Key

```python
partition_key = asset_event.dagster_event.logging_tags.get("dagster/partition")
```

**Use cases**: Cross-job dependencies, cross-code location dependencies, side effects

**When to use**: Triggering non-asset actions or imperatively launching jobs

**Prefer**: Declarative automation for asset-to-asset execution

**Details**: `references/asset-sensors.md`

---

## Declarative Automation Quick Reference

Define conditions on assets describing when they should execute.

### Requirement

Enable `default_automation_condition_sensor` in the UI under **Automation**.

### The Three Main Conditions

#### eager() - Immediate Propagation

Execute when any dependency updates:

```python
@dg.asset(automation_condition=dg.AutomationCondition.eager())
def downstream_asset(upstream_asset):
    ...
```

**Behavior**: Triggers immediately when upstreams update, waits for missing/in-progress
dependencies, only latest partition for time-partitioned assets.

#### on_cron() - Scheduled with Dependency Awareness

Execute on schedule after dependencies update:

```python
@dg.asset(
    automation_condition=dg.AutomationCondition.on_cron("0 9 * * *", "America/Los_Angeles")
)
def daily_summary(hourly_data):
    ...
```

**Behavior**: Waits for cron tick, then waits for all dependencies to update since that tick,
executes immediately after.

#### on_missing() - Fill Missing Partitions

Execute missing partitions when dependencies are available:

```python
@dg.asset(automation_condition=dg.AutomationCondition.on_missing())
def backfill_asset(upstream):
    ...
```

**Behavior**: Only materializes missing partitions added after condition was applied, waits for all
upstream dependencies.

### Combining Conditions

```python
# OR: Execute on either condition
condition = (
    dg.AutomationCondition.on_missing()
    | dg.AutomationCondition.on_cron("0 0 * * *")
)

# AND: Execute only when both conditions are true
condition = (
    dg.AutomationCondition.eager()
    & dg.AutomationCondition.all_checks_match(
        dg.AutomationCondition.check_passed(),
        blocking_only=True,
    )
)

# NOT: Negate a condition
condition = ~dg.AutomationCondition.any_deps_missing()
```

### Customization Patterns

See
[references/declarative-automation-customization.md](references/declarative-automation-customization.md)
for:

- **Pattern 1**: `.without()` to remove sub-conditions
- **Pattern 2**: `.replace()` to swap sub-conditions
- **Pattern 3**: `.allow()` and `.ignore()` to filter dependencies
- **Pattern 4**: Boolean composition with `&`, `|`, `~`
- **Pattern 5**: Custom conditions from operands

**Works with**: Assets only (not ops/graphs)

**Details**:

- Core concepts: `references/declarative-automation.md`
- Operands: `references/declarative-automation-operands.md`
- Operators: `references/declarative-automation-operators.md`
- Customization: `references/declarative-automation-customization.md`
- Advanced: `references/declarative-automation-advanced.md`

---

## Selection Criteria

| Factor                 | Schedules           | Sensors                            | Declarative Automation                  |
| ---------------------- | ------------------- | ---------------------------------- | --------------------------------------- |
| **Pipeline structure** | Assets or ops       | Assets or ops                      | Assets only                             |
| **Timing**             | Fixed schedule      | Event-driven (polling)             | Condition-based                         |
| **Dependency logic**   | None                | Custom (you implement)             | Built-in (automatic)                    |
| **Complexity**         | Simple              | Medium (requires state management) | High (requires condition understanding) |
| **Use case**           | "Run daily at 9 AM" | "Run when file arrives"            | "Run after upstream updates"            |

**Decision tree**:

1. **Assets only + complex dependency logic** → Declarative Automation
2. **Fixed schedule, no dependency logic** → Schedules
3. **External events or custom polling** → Sensors
4. **Run completion/failure monitoring** → Run Status Sensors
5. **Asset materialization monitoring** → Asset Sensors (or declarative automation)

---

## When to Load References

### Load `references/schedules.md` when:

- Creating schedules with cron expressions
- Configuring execution timezones
- Using `build_schedule_from_partitioned_job`

### Load `references/sensors.md` when:

- Implementing custom polling logic
- Managing sensor state with cursors
- Understanding `RunRequest`, `SkipReason`, run keys
- Configuring evaluation intervals

### Load `references/run-status-sensors.md` when:

- Monitoring run success/failure
- Implementing alerting on run status
- Coordinating jobs based on run completion
- Setting up cross-code location monitoring

### Load `references/asset-sensors.md` when:

- Monitoring asset materializations
- Implementing cross-job or cross-code location dependencies
- Deciding between asset sensors and declarative automation

### Load `references/declarative-automation.md` when:

- Getting started with declarative automation
- Understanding the three main conditions (`eager()`, `on_cron()`, `on_missing()`)
- Learning when to use declarative automation vs schedules/sensors

### Load `references/declarative-automation-operands.md` when:

- Need list of all available operands
- Understanding status vs event operands
- Looking up operand behavior

### Load `references/declarative-automation-operators.md` when:

- Composing conditions with `&`, `|`, `~`
- Using `since()` or `newly_true()`
- Working with dependency operators (`any_deps_match()`, `all_deps_match()`)
- Applying `.allow()` or `.ignore()` filters

### Load `references/declarative-automation-customization.md` when:

- Customizing `eager()`, `on_cron()`, or `on_missing()`
- Using `.without()` or `.replace()` to modify conditions
- Building complex conditions from scratch
- Need examples of common customization patterns

### Load `references/declarative-automation-advanced.md` when:

- Need deep understanding of status vs events
- Understanding run grouping and `will_be_requested()`
- Learning how `.allow()` and `.ignore()` work internally
- Understanding composite conditions like `any_deps_updated()`
- Performance tuning automation conditions

---

## References

- **Schedules**: `references/schedules.md`
- **Sensors**: `references/sensors.md`
- **Run Status Sensors**: `references/run-status-sensors.md`
- **Asset Sensors**: `references/asset-sensors.md`
- **Declarative Automation**: `references/declarative-automation.md`
- **Operands**: `references/declarative-automation-operands.md`
- **Operators**: `references/declarative-automation-operators.md`
- **Customization**: `references/declarative-automation-customization.md`
- **Advanced Concepts**: `references/declarative-automation-advanced.md`
- **Official Docs**: https://docs.dagster.io/guides/automate
