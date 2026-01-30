# Schedules

Schedules execute jobs at specified times using cron expressions. They trigger at exact cron tick
times regardless of dependency status.

## Basic Schedule

A schedule requires a `JobDefinition` and a `cron_schedule`:

```python
import dagster as dg

daily_refresh_job = dg.define_asset_job("daily_refresh_job", selection="*")

daily_schedule = dg.ScheduleDefinition(
    job=daily_refresh_job,
    cron_schedule="0 0 * * *",  # Midnight UTC daily
)
```

## Execution Timezone

Schedules default to UTC. Specify a different timezone with `execution_timezone`:

```python
daily_schedule = dg.ScheduleDefinition(
    job=daily_refresh_job,
    cron_schedule="0 0 * * *",
    execution_timezone="America/Los_Angeles",
)
```

## Schedules from Partitioned Assets/Jobs

For partitioned assets or jobs, use `build_schedule_from_partitioned_job` to automatically create a
schedule matching the partition cadence:

```python
from dagster import (
    DailyPartitionsDefinition,
    asset,
    build_schedule_from_partitioned_job,
    define_asset_job,
)

@asset(partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"))
def daily_asset():
    ...

partitioned_asset_job = define_asset_job("partitioned_job", selection=[daily_asset])

# Schedule inherits the daily cadence from the partition definition
schedule = build_schedule_from_partitioned_job(partitioned_asset_job)
```

The schedule inherits the cron expression from the `PartitionsDefinition`.

## Key Parameters

- `job`: `JobDefinition` to execute
- `cron_schedule`: Cron expression string
- `execution_timezone`: Timezone string (default: "UTC")
- `default_status`: `DefaultScheduleStatus.RUNNING` or `STOPPED` (default: STOPPED)

## Works With

- Asset-based jobs (jobs containing assets)
- Op-based jobs (jobs containing ops and graphs)
