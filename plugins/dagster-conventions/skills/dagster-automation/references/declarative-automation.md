# Declarative Automation

Declarative automation uses `AutomationCondition` objects to describe when assets should execute.
The system evaluates conditions and launches runs automatically.

## Requirements

- **Assets only**: Declarative automation does not work with ops or graphs
- **Sensor enabled**: The `default_automation_condition_sensor` must be enabled in the UI under
  **Automation**

## AutomationCondition

An `AutomationCondition` describes when an asset should be executed based on its state and
dependencies.

```python
import dagster as dg

@dg.asset(automation_condition=dg.AutomationCondition.eager())
def my_asset():
    ...
```

## The Three Main Conditions

Dagster provides three primary conditions optimized for common use cases. Start with one of these
rather than building conditions from scratch.

### eager()

Executes an asset whenever any dependency updates. Also materializes partitions that become missing
after the condition is applied.

```python
@dg.asset(automation_condition=dg.AutomationCondition.eager())
def downstream_asset(upstream_asset):
    ...
```

**Behavior:**

- Triggers immediately when any upstream updates
- Waits for all upstreams to be materialized or in-progress
- Does not execute if any dependencies are missing
- Does not execute if the asset is already in-progress
- For time-partitioned assets, only considers the latest partition
- For static/dynamic-partitioned assets, considers all partitions

**Use when:** You want updates to propagate downstream immediately

### on_cron()

Executes an asset on a cron schedule after all dependencies have updated since the latest cron tick.

```python
@dg.asset(
    automation_condition=dg.AutomationCondition.on_cron("0 9 * * *", "America/Los_Angeles")
)
def daily_summary(hourly_data):
    ...
```

**Behavior:**

- Waits for a cron tick to occur
- After the tick, waits for all dependencies to update since that tick
- Once all dependencies are updated, executes immediately
- For time-partitioned assets, only considers the latest partition

**Use when:** You want scheduled execution but only after upstream data is ready

### on_missing()

Executes missing asset partitions when all upstream partitions are available.

```python
@dg.asset(automation_condition=dg.AutomationCondition.on_missing())
def backfill_asset(upstream):
    ...
```

**Behavior:**

- Only materializes partitions that are missing
- Only considers partitions added after the condition was applied (not historical)
- Waits for all upstream dependencies to be available
- For time-partitioned assets, only considers the latest partition

**Use when:** You want to fill in missing partitions as upstream data becomes available

## Evaluation by Sensor

The `AutomationConditionSensorDefinition` evaluates conditions. By default, a sensor named
`default_automation_condition_sensor` is created automatically in code locations with automation
conditions.

**Default behavior:**

- Evaluates all conditions every 30 seconds
- Must be toggled on in the UI under **Automation**
- Launches runs when conditions evaluate to true

## Customization

All three main conditions can be customized to fit specific needs:

- Modify sub-conditions using `.replace()` and `.without()`
- Filter dependencies using `.allow()` and `.ignore()`
- Combine with boolean operators: `&` (AND), `|` (OR), `~` (NOT)
- Build complex conditions from operands and operators

See [declarative-automation-customization.md](declarative-automation-customization.md) for patterns
and examples.

## Advanced Concepts

For deeper understanding of the declarative automation system:

- [declarative-automation-operands.md](declarative-automation-operands.md) - Base conditions
- [declarative-automation-operators.md](declarative-automation-operators.md) - Composition tools
- [declarative-automation-advanced.md](declarative-automation-advanced.md) - Status vs events, run
  grouping, dependency filtering
