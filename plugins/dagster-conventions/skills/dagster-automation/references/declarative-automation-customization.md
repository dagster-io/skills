# Declarative Automation: Customization

Start with one of the three main conditions (`eager()`, `on_cron()`, `on_missing()`) and customize
them using these patterns.

## Pattern 1: Removing Sub-conditions with without()

Remove unwanted sub-conditions from composite conditions.

### Allow Missing Upstreams

By default, `eager()` waits for all dependencies. Remove this requirement:

```python
import dagster as dg

condition = (
    dg.AutomationCondition.eager()
    .without(~dg.AutomationCondition.any_deps_missing())
    .with_label("eager_allow_missing")
)
```

### Update All Time Partitions

By default, `eager()` only updates the latest time partition. Remove this restriction:

```python
condition = (
    dg.AutomationCondition.eager()
    .without(dg.AutomationCondition.in_latest_time_window())
    .with_label("eager_all_partitions")
)
```

## Pattern 2: Replacing Sub-conditions with replace()

Swap one sub-condition for another with different parameters.

### Multiple Cron Schedules

Execute at 9 AM but wait for dependencies to update since midnight:

```python
NINE_AM_CRON = "0 9 * * *"
MIDNIGHT_CRON = "0 0 * * *"

condition = dg.AutomationCondition.on_cron(NINE_AM_CRON).replace(
    old=dg.AutomationCondition.all_deps_updated_since_cron(NINE_AM_CRON),
    new=dg.AutomationCondition.all_deps_updated_since_cron(MIDNIGHT_CRON),
)
```

### Partition Lookback Window

Expand `on_missing()` to consider the last 24 hours of partitions:

```python
import datetime

condition = dg.AutomationCondition.on_missing().replace(
    old=dg.AutomationCondition.in_latest_time_window(),
    new=dg.AutomationCondition.in_latest_time_window(
        lookback_delta=datetime.timedelta(hours=24)
    ),
)
```

## Pattern 3: Filtering Dependencies with allow() and ignore()

Control which dependencies are considered.

### Only Specific Dependencies

Only trigger on updates from assets in the "abc" group:

```python
condition = dg.AutomationCondition.eager().allow(
    dg.AssetSelection.groups("abc")
)
```

### Exclude Specific Dependencies

Ignore updates from the "foo" asset:

```python
condition = dg.AutomationCondition.eager().ignore(
    dg.AssetSelection.assets("foo")
)
```

## Pattern 4: Boolean Composition

Combine multiple conditions with AND, OR, NOT.

### Scheduled with Dependency-Driven Fallback

Run every 5 minutes or when dependencies update (if updated today):

```python
daily_success_condition = dg.AutomationCondition.newly_updated().since(
    dg.AutomationCondition.cron_tick_passed("0 0 * * *")
)

condition = (
    dg.AutomationCondition.cron_tick_passed("*/5 * * * *")
    | (
        dg.AutomationCondition.any_deps_updated()
        & daily_success_condition
        & ~dg.AutomationCondition.any_deps_missing()
        & ~dg.AutomationCondition.any_deps_in_progress()
    )
)
```

### Only Execute When Checks Pass

Ensure all blocking checks on dependencies pass before executing:

```python
condition = (
    dg.AutomationCondition.eager()
    & dg.AutomationCondition.all_deps_match(
        dg.AutomationCondition.all_checks_match(
            dg.AutomationCondition.check_passed(),
            blocking_only=True,
        )
    )
)
```

## Pattern 5: Custom Event-Based Conditions

Build conditions from operands and operators for specific scenarios.

### On Code Version Change

Execute when code version changes, once per change:

```python
condition = (
    dg.AutomationCondition.code_version_changed().since_last_handled()
    & ~dg.AutomationCondition.any_deps_missing()
)
```

### After Upstream Success

Execute only after a specific upstream asset is updated:

```python
condition = (
    dg.AutomationCondition.any_deps_match(
        dg.AutomationCondition.newly_updated()
    ).allow(dg.AssetSelection.assets("critical_upstream"))
    .since_last_handled()
)
```

## Understanding Built-in Condition Structure

To customize effectively, understand how the main conditions are structured.

### eager() Structure

```python
AutomationCondition.in_latest_time_window()
& (
    AutomationCondition.newly_missing()
    | AutomationCondition.any_deps_updated()
).since_last_handled()
& ~AutomationCondition.any_deps_missing()
& ~AutomationCondition.any_deps_in_progress()
& ~AutomationCondition.in_progress()
```

**Key sub-conditions to customize:**

- `in_latest_time_window()` - Restricts to latest partition
- `any_deps_missing()` - Blocks on missing dependencies
- `any_deps_in_progress()` - Waits for in-progress dependencies

### on_cron() Structure

```python
AutomationCondition.in_latest_time_window()
& AutomationCondition.cron_tick_passed(cron_schedule, cron_timezone).since_last_handled()
& AutomationCondition.all_deps_updated_since_cron(cron_schedule, cron_timezone)
```

**Key sub-conditions to customize:**

- `in_latest_time_window()` - Restricts to latest partition
- `cron_tick_passed()` - Defines the schedule
- `all_deps_updated_since_cron()` - Waits for dependencies

### on_missing() Structure

```python
AutomationCondition.in_latest_time_window()
& (
    AutomationCondition.missing()
    .newly_true()
    .since_last_handled()
)
& ~AutomationCondition.any_deps_missing()
```

**Key sub-conditions to customize:**

- `in_latest_time_window()` - Restricts to latest partition
- `missing().newly_true()` - Triggers only when becoming missing
- `any_deps_missing()` - Blocks on missing dependencies

## Combining Patterns

Multiple patterns can be combined:

```python
condition = (
    dg.AutomationCondition.eager()
    .without(dg.AutomationCondition.in_latest_time_window())  # Pattern 1
    .ignore(dg.AssetSelection.assets("staging_data"))         # Pattern 3
    & dg.AutomationCondition.all_checks_match(                # Pattern 4
        dg.AutomationCondition.check_passed(),
        blocking_only=True,
    )
).with_label("custom_backfill_with_checks")
```

This condition:

1. Uses `eager()` as the base
2. Removes the latest partition restriction (updates all partitions)
3. Ignores the "staging_data" dependency
4. Adds a requirement that all blocking checks pass
5. Labels the condition for debugging
