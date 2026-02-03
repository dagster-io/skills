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
- Does not execute if the asset is already in-progress
- For time-partitioned assets, only considers the latest partition
- For static/dynamic-partitioned assets, considers all partitions

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

**Use when**: You want to fill in missing partitions as upstream data becomes available. Good for backfilling or catching up.

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
