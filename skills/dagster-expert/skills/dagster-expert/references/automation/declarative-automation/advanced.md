# Declarative Automation: Advanced Concepts

This document covers advanced topics for deep understanding of the declarative automation system.

## Status vs Events

Understanding the distinction between statuses and events is fundamental to building correct automation conditions.

### Statuses

**Statuses** are persistent conditions that remain true for multiple evaluation ticks.

Examples:

- `AutomationCondition.missing()` - Stays true until the partition is materialized
- `AutomationCondition.in_progress()` - True while a run is executing
- `AutomationCondition.in_latest_time_window()` - True for the latest time partition(s)

**Characteristic**: If the underlying state doesn't change, the status will be true for consecutive evaluations.

### Events

**Events** are transient conditions that are true only on a single evaluation tick.

Examples:

- `AutomationCondition.newly_updated()` - True only on the tick when materialization occurs
- `AutomationCondition.code_version_changed()` - True only on the first tick after code changes
- `AutomationCondition.cron_tick_passed()` - True only on the first tick after the cron tick

**Characteristic**: Even if evaluated immediately again, the event would be false (assuming no new change).

### Converting Between Status and Event

**Status → Event with `newly_true()`**:

```python
# missing() is a status (stays true for many ticks)
# newly_true() converts it to an event (true only when becoming missing)
condition = dg.AutomationCondition.missing().newly_true()
```

**Use case**: Prevent repeated requests during persistent states. A partition stays missing while a run is in progress. Using `newly_true()` ensures you only request it once.

**Two Events → Status with `since()`**:

```python
# Both newly_updated() and newly_requested() are events
# since() converts them to a status: "updated more recently than requested"
condition = dg.AutomationCondition.newly_updated().since(
    dg.AutomationCondition.newly_requested()
)
```

**Use case**: Create persistent states from transient events. This condition becomes true when an update occurs and stays true until a request is made.

### Example: Preventing Duplicate Requests

The default `eager()` condition uses this pattern:

```python
(
    AutomationCondition.newly_missing()
    | AutomationCondition.any_deps_updated()
).since_last_handled()
```

- `newly_missing()` and `any_deps_updated()` are events
- `since_last_handled()` converts them to a status that persists until the asset is requested or updated
- Without this conversion, the condition would only be true for a single tick, potentially missing the opportunity to launch a run

## Run Grouping

Run grouping allows multiple assets to execute in a single run even though downstream assets' dependencies haven't been materialized yet.

### The Problem

Consider assets A → B → C, all with `eager()` conditions:

1. A's upstream updates, triggering A
2. A is requested and begins executing
3. On the next tick, B sees that A hasn't finished materializing
4. Without run grouping, B would wait for A to complete
5. This results in three separate runs instead of one

### The Solution: will_be_requested()

The `will_be_requested()` operand is true for assets that will be requested in the current tick. Dependency conditions use this to group assets:

```python
# From any_deps_updated() definition:
AutomationCondition.any_deps_match(
    (
        AutomationCondition.newly_updated()
        & ~AutomationCondition.executed_with_root_target()
    )
    | AutomationCondition.will_be_requested()  # Enables run grouping
)
```

When evaluating B:

1. B checks if any dependencies are updated OR will be requested this tick
2. A is marked as "will be requested" this tick
3. B treats A as if it were already updated
4. B is also marked for execution in the same run as A

### Requirements for Same-Run Execution

Two assets can execute in the same run if:

1. **Same repository**: They must be in the same code location
2. **Compatible partitions**: They must have matching `PartitionsDefinition` objects
3. **Compatible partition mapping**: Must use `TimeWindowPartitionMapping` or `IdentityPartitionMapping`

If these requirements aren't met, assets execute in separate runs even with run grouping logic.

## Dependency Filtering with allow() and ignore()

Dependency operators (`any_deps_match()`, `all_deps_match()`) check conditions on upstream assets. Filtering controls which upstreams are checked.

### allow() Creates Intersection

Only dependencies in the selection are checked:

```python
condition = dg.AutomationCondition.any_deps_match(
    dg.AutomationCondition.missing()
).allow(dg.AssetSelection.groups("critical"))
```

If the asset has 10 upstreams but only 2 are in the "critical" group, only those 2 are checked.

### ignore() Creates Subtraction

Dependencies in the selection are excluded:

```python
condition = dg.AutomationCondition.any_deps_updated().ignore(
    dg.AssetSelection.assets("test_data", "staging_data")
)
```

Updates to "test_data" and "staging_data" won't trigger the condition.

### Propagation Through Operators

When applied to composite conditions (AND/OR), filtering propagates to all sub-conditions:

```python
# Applies to both any_deps_missing() and any_deps_in_progress() within eager()
condition = dg.AutomationCondition.eager().allow(
    dg.AssetSelection.groups("production")
)
```

**What gets filtered**: All `any_deps_match()` and `all_deps_match()` calls

**What doesn't get filtered**: Direct operands like `missing()` on the asset itself

## Understanding since_last_handled()

`since_last_handled()` is a convenience method that converts events to a status:

```python
# These are equivalent:
condition.since_last_handled()

condition.since(
    AutomationCondition.newly_requested()
    | AutomationCondition.newly_updated()
    | AutomationCondition.initial_evaluation()
)
```

**Behavior**:

- Becomes true when `condition` becomes true
- Stays true until the asset is requested, updated, or the condition is first applied
- Resets on initial evaluation to handle condition changes

**Use case**: Persist an event until it's "handled" by either requesting or materializing the asset. This prevents duplicate requests while ensuring the event isn't lost.

## Composite Conditions Deep Dive

### any_deps_updated()

```python
AutomationCondition.any_deps_match(
    (AutomationCondition.newly_updated() & ~AutomationCondition.executed_with_root_target())
    | AutomationCondition.will_be_requested()
)
```

Checks if any dependency has newly updated (excluding same-run updates) OR will be requested this tick.

### any_deps_missing()

```python
AutomationCondition.any_deps_match(
    AutomationCondition.missing() & ~AutomationCondition.will_be_requested()
)
```

Checks if any dependency is missing AND will NOT be requested this tick. Dependencies that will be requested aren't considered blocking.

### all_deps_updated_since_cron()

```python
AutomationCondition.all_deps_match(
    AutomationCondition.newly_updated().since(
        AutomationCondition.cron_tick_passed(cron_schedule, cron_timezone)
    )
)
```

For each dependency, checks if it has been updated since the last cron tick. All dependencies must have at least one partition updated since the tick.
