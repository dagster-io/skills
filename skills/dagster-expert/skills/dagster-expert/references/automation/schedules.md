# Schedules

Basic schedule patterns are covered in the main SKILL.md Quick Reference. This reference covers advanced schedule configuration and partitioned job automation.

## Basic Schedule Review

A schedule executes a job at specified times using cron expressions. See SKILL.md for the basic pattern.

```python
import dagster as dg

daily_job = dg.define_asset_job("daily_job", selection="*")

daily_schedule = dg.ScheduleDefinition(
    job=daily_job,
    cron_schedule="0 0 * * *",  # Midnight UTC
)
```

## Execution Timezone

Schedules default to UTC. Specify a different timezone with `execution_timezone`:

```python
daily_schedule = dg.ScheduleDefinition(
    job=daily_refresh_job,
    cron_schedule="0 9 * * *",  # 9 AM
    execution_timezone="America/Los_Angeles",
)
```

**Timezone string format**: Use IANA timezone database names like `"America/New_York"`, `"Europe/London"`, or `"Asia/Tokyo"`.

**Daylight saving time**: Dagster handles DST transitions automatically based on the specified timezone.

## Schedules from Partitioned Assets

For partitioned assets or jobs, use `build_schedule_from_partitioned_job` to automatically create a schedule matching the partition cadence:

```python
from dagster import (
    DailyPartitionsDefinition,
    asset,
    build_schedule_from_partitioned_job,
    define_asset_job,
)

@asset(partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"))
def daily_asset(context):
    partition_date = context.partition_key
    # Process data for this partition
    ...

partitioned_job = define_asset_job(
    name="daily_partitioned_job",
    selection=[daily_asset]
)

# Schedule automatically inherits daily cadence and timezone from partition definition
schedule = build_schedule_from_partitioned_job(partitioned_job)
```

**How it works**: The schedule's cron expression is derived from the `PartitionsDefinition`:

- `DailyPartitionsDefinition` → daily cron schedule
- `WeeklyPartitionsDefinition` → weekly cron schedule
- `MonthlyPartitionsDefinition` → monthly cron schedule
- `HourlyPartitionsDefinition` → hourly cron schedule

Each schedule run materializes the partition corresponding to the schedule time.

## Cron Expression Reference

Common cron patterns for schedules:

| Cron Expression  | Description                 |
| ---------------- | --------------------------- |
| `0 * * * *`      | Every hour                  |
| `0 0 * * *`      | Daily at midnight           |
| `0 9 * * *`      | Daily at 9 AM               |
| `0 0 * * 1`      | Weekly on Monday            |
| `0 0 1 * *`      | Monthly on the 1st          |
| `0 0 1 1 *`      | Yearly on January 1st       |
| `*/15 * * * *`   | Every 15 minutes            |
| `0 9-17 * * 1-5` | Hourly, 9 AM-5 PM, weekdays |

**Cron format**: `minute hour day_of_month month day_of_week`

## Configuration Options

```python
schedule = dg.ScheduleDefinition(
    job=my_job,
    cron_schedule="0 0 * * *",
    execution_timezone="UTC",
    default_status=dg.DefaultScheduleStatus.RUNNING,  # Start enabled
    description="Daily data refresh for analytics",
    tags={"team": "data-eng", "priority": "high"},
)
```

**Key parameters**:

- `default_status`: Set to `DefaultScheduleStatus.RUNNING` to enable schedule automatically when deployed (default is `STOPPED`)
- `description`: Human-readable description shown in the Dagster UI
- `tags`: Metadata tags for organization and filtering

## When to Use Schedules

**Use schedules when**:

- Execution time is predictable and fixed
- No dependency logic is needed (runs regardless of upstream status)
- Simple time-based triggers are sufficient

**Prefer declarative automation when**:

- You need dependency-aware execution
- Conditions involve asset freshness or upstream state
- Complex logic determines when to execute
