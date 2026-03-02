---
description: "Core declarative automation concepts: eager(), on_cron(), and on_missing() conditions."
triggers:
  - "eager, on_cron, on_missing"
  - "declarative automation basics, AutomationCondition"
---

# Declarative Automation: Core Concepts

For basic examples, see the main SKILL.md Quick Reference section on Declarative Automation.

## The Three Main Conditions

Dagster provides three primary conditions optimized for common use cases. Start with one of these rather than building conditions from scratch.

### eager()

Executes an asset whenever any dependency updates. Also materializes partitions that become missing after the condition is applied.

```python
import dagster as dg

@dg.asset(automation_condition=dg.AutomationCondition.eager())
def downstream_asset(upstream_asset):
    # Executes immediately when upstream_asset materializes
    ...
```

**Behavior**:

- Triggers immediately when any upstream updates
- Waits for all upstreams to be materialized or in-progress
- Does not execute if any dependencies are missing
- **Does not execute if any dependencies are currently in-progress** (waits for all deps to finish first)
- Does not execute if the asset is already in-progress
- For time-partitioned assets, only considers the latest partition
- For static/dynamic-partitioned assets, considers all partitions

**Full expanded form**:

```python
(
    dg.AutomationCondition.in_latest_time_window()          # latest partition only (time-partitioned)
    & (
        dg.AutomationCondition.newly_missing()
        | dg.AutomationCondition.any_deps_updated()
    ).since_last_handled()                                  # trigger event, persisted until handled
    & ~dg.AutomationCondition.any_deps_missing()            # no deps missing
    & ~dg.AutomationCondition.any_deps_in_progress()        # no deps currently running
    & ~dg.AutomationCondition.in_progress()                 # asset itself not running
).with_label("eager")
```

The `~any_deps_in_progress()` guard is critical: it prevents the asset from firing until ALL upstream deps have finished materializing. Without it, the asset would fire each time an individual dep completes, causing redundant executions when multiple deps update in quick succession (e.g., from the same scheduled job).

**Use when**: You want updates to propagate downstream immediately without waiting for a schedule.

### on_cron()

Executes an asset on a cron schedule after all dependencies have updated since the latest cron tick.

```python
@dg.asset(
    automation_condition=dg.AutomationCondition.on_cron("0 9 * * *", "America/Los_Angeles")
)
def daily_summary(hourly_data):
    # Executes at 9 AM only if hourly_data has updated since the previous 9 AM tick
    ...
```

**Behavior**:

- Waits for a cron tick to occur
- After the tick, waits for all dependencies to update since that tick
- Once all dependencies are updated, executes immediately
- For time-partitioned assets, only considers the latest partition
  **Full expanded form**:

```python
(
    dg.AutomationCondition.in_latest_time_window()
    & dg.AutomationCondition.cron_tick_passed(
        cron_schedule, cron_timezone
    ).since_last_handled()
    & dg.AutomationCondition.all_deps_updated_since_cron(cron_schedule, cron_timezone)
).with_label(f"on_cron({cron_schedule}, {cron_timezone})")
```

**Use when**: You want scheduled execution but only after upstream data is ready. More intelligent than simple schedules.

### on_missing()

Executes missing asset partitions when all upstream partitions are available.

```python
@dg.asset(automation_condition=dg.AutomationCondition.on_missing())
def backfill_asset(upstream):
    # Executes for any missing partitions when upstream is ready
    ...
```

**Behavior**:

- Only materializes partitions that are missing
- Only considers partitions added after the condition was applied (not historical)
- Waits for all upstream dependencies to be available
- For time-partitioned assets, only considers the latest partition
  **Full expanded form**:

```python
(
    dg.AutomationCondition.in_latest_time_window()
    & (
        dg.AutomationCondition.missing()
        .newly_true()
        .since_last_handled()
        .with_label("missing_since_last_handled")
    )
    & ~dg.AutomationCondition.any_deps_missing()
).with_label("on_missing")
```

**Use when**: You want to fill in missing partitions as upstream data becomes available. Good for backfilling or catching up.

## Identifying Built-in vs Custom Conditions from the API

When debugging DA behavior via `dg api asset get`, the `automation_condition.expanded_label` field shows the condition tree as a list of strings. Compare this against the full expanded forms above to determine if the asset is using a built-in condition or a custom one with missing guards. When you see a condition that looks similar to but doesn't match a built-in, always identify the missing sub-conditions and explain how their absence changes behavior.

## Evaluation by Sensor

The `AutomationConditionSensorDefinition` evaluates conditions at regular intervals.

**Default sensor**: A sensor named `default_automation_condition_sensor` is created automatically in code locations with automation conditions.

**Configuration**:

- Evaluates all conditions every 30 seconds
- Must be toggled on in the UI under **Automation → Sensors**
- Launches runs when conditions evaluate to true

**Important**: If the sensor is not enabled, conditions will not be evaluated and no runs will launch.

## Basic Customization

All three main conditions are built from smaller components and can be customized.

### Modifying conditions

```python
# Remove sub-conditions
condition = dg.AutomationCondition.eager().without(
    ~dg.AutomationCondition.any_deps_missing()
)

# Replace sub-conditions
condition = dg.AutomationCondition.on_cron("0 9 * * *").replace(
    old=dg.AutomationCondition.all_deps_updated_since_cron("0 9 * * *"),
    new=dg.AutomationCondition.all_deps_updated_since_cron("0 0 * * *"),
)
```

### Boolean composition

```python
# AND: Both conditions must be true
condition = (
    dg.AutomationCondition.eager()
    & ~dg.AutomationCondition.in_progress()
)

# OR: Either condition can be true
condition = (
    dg.AutomationCondition.on_cron("0 9 * * *")
    | dg.AutomationCondition.any_deps_updated()
)
```

See [customization.md](customization.md) for detailed patterns and examples.

## When to Use Declarative Automation

**Use declarative automation when**:

- Asset-centric pipelines with complex update logic
- Condition-based triggers (data availability, freshness)
- Dependency-aware execution is needed
- You prefer declarative over imperative

**Use schedules when**:

- Simple time-based execution without dependency logic
- Predictable, fixed-time execution is sufficient

**Use sensors when**:

- Custom polling logic for external systems
- Imperative actions beyond asset execution
- File watching or API event monitoring
