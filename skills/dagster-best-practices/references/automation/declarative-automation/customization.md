# Declarative Automation: Customization

Start with one of the three main conditions (`eager()`, `on_cron()`, `on_missing()`) and customize them using these patterns.

## Pattern 1: Removing Sub-conditions with without()

Remove unwanted sub-conditions from composite conditions.

**Allow missing upstreams**: By default, `eager()` waits for all dependencies. Remove this requirement:

```python
import dagster as dg

condition = (
    dg.AutomationCondition.eager()
    .without(~dg.AutomationCondition.any_deps_missing())
    .with_label("eager_allow_missing")
)
```

**Update all time partitions**: By default, `eager()` only updates the latest time partition. Remove this restriction:

```python
condition = (
    dg.AutomationCondition.eager()
    .without(dg.AutomationCondition.in_latest_time_window())
    .with_label("eager_all_partitions")
)
```

## Pattern 2: Replacing Sub-conditions with replace()

Swap one sub-condition for another with different parameters.

**Multiple cron schedules**: Execute at 9 AM but wait for dependencies to update since midnight:

```python
NINE_AM_CRON = "0 9 * * *"
MIDNIGHT_CRON = "0 0 * * *"

condition = dg.AutomationCondition.on_cron(NINE_AM_CRON).replace(
    old=dg.AutomationCondition.all_deps_updated_since_cron(NINE_AM_CRON),
    new=dg.AutomationCondition.all_deps_updated_since_cron(MIDNIGHT_CRON),
)
```

**Partition lookback window**: Expand `on_missing()` to consider the last 24 hours of partitions:

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

**Only specific dependencies**: Only trigger on updates from assets in the "abc" group:

```python
condition = dg.AutomationCondition.eager().allow(
    dg.AssetSelection.groups("abc")
)
```

**Exclude specific dependencies**: Ignore updates from the "foo" asset:

```python
condition = dg.AutomationCondition.eager().ignore(
    dg.AssetSelection.assets("foo")
)
```

## Pattern 4: Boolean Composition

Combine multiple conditions with AND (`&`), OR (`|`), NOT (`~`).

**Scheduled with dependency-driven fallback**: Run every 5 minutes or when dependencies update (if updated today):

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

**Only execute when checks pass**: Ensure all blocking checks on dependencies pass:

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

**On code version change**: Execute when code version changes:

```python
condition = (
    dg.AutomationCondition.code_version_changed().since_last_handled()
    & ~dg.AutomationCondition.any_deps_missing()
)
```

**After upstream success**: Execute only after a specific upstream asset updates:

```python
condition = (
    dg.AutomationCondition.any_deps_match(
        dg.AutomationCondition.newly_updated()
    ).allow(dg.AssetSelection.assets("critical_upstream"))
    .since_last_handled()
)
```

## Combining Patterns

Multiple patterns can be combined for complex requirements:

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

This condition uses `eager()` as the base, removes the latest partition restriction, ignores a specific dependency, and adds a check requirement.
