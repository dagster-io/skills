# Declarative Automation: Advanced Concepts

This document covers advanced topics for deep understanding of the declarative automation system.

## Status vs Events

Understanding the distinction between statuses and events is fundamental to building correct
automation conditions.

### Statuses

**Statuses** are persistent conditions that remain true for multiple evaluation ticks.

Examples:

- `AutomationCondition.missing()` - Stays true from when the partition is created until it is
  materialized
- `AutomationCondition.in_progress()` - True while a run is executing the partition
- `AutomationCondition.in_latest_time_window()` - True for the latest time partition(s)

**Characteristic:** If the underlying state doesn't change, the status will be true for consecutive
evaluations.

### Events

**Events** are transient conditions that are true only on a single evaluation tick.

Examples:

- `AutomationCondition.newly_updated()` - True only on the tick when the materialization occurs
- `AutomationCondition.code_version_changed()` - True only on the first tick after the code changes
- `AutomationCondition.cron_tick_passed()` - True only on the first tick after the cron tick occurs

**Characteristic:** Even if evaluated immediately again, the event would be false (assuming no new
change occurred).

### Converting Between Status and Event

**Status → Event with `newly_true()`:**

```python
# missing() is a status (stays true for many ticks)
# newly_true() converts it to an event (true only when becoming missing)
condition = dg.AutomationCondition.missing().newly_true()
```

**Use case:** Prevent repeated requests during persistent states. For example, a partition stays
missing while a run is in progress. Using `newly_true()` ensures you only request it once when it
becomes missing, not on every tick while it remains missing.

**Two Events → Status with `since()`:**

```python
# Both newly_updated() and newly_requested() are events
# since() converts them to a status: "updated more recently than requested"
condition = dg.AutomationCondition.newly_updated().since(
    dg.AutomationCondition.newly_requested()
)
```

**Use case:** Create persistent states from transient events. This condition becomes true when an
update occurs and stays true until a request is made. This describes the state "there's an unhandled
update."

### Example: Preventing Duplicate Requests

The default `eager()` condition uses this pattern:

```python
(
    AutomationCondition.newly_missing()
    | AutomationCondition.any_deps_updated()
).since_last_handled()
```

- `newly_missing()` and `any_deps_updated()` are events
- `since_last_handled()` converts them to a status that persists until the asset is requested or
  updated
- Without `since_last_handled()`, the condition would only be true for a single tick, potentially
  missing the opportunity to launch a run if the sensor is busy
- But without `newly_true()` in `newly_missing()`, the condition would repeatedly request missing
  partitions on every tick

## Run Grouping

Run grouping allows multiple assets to execute in a single run even though downstream assets'
dependencies haven't technically been materialized yet.

### The Problem

Consider assets A → B → C, all with `eager()` conditions:

1. A's upstream updates, triggering A
2. A is requested and begins executing
3. On the next evaluation tick, B sees that A hasn't finished materializing yet
4. Without run grouping, B would wait for A to complete
5. This would result in three separate runs: one for A, one for B, one for C

### The Solution: will_be_requested()

The `will_be_requested()` operand is true for assets that will be requested in the current tick.
Dependency conditions use this to group assets:

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

1. **Same repository**: They must be in the same code location and repository
2. **Compatible partitions**: They must have matching `PartitionsDefinition` objects
3. **Compatible partition mapping**: For partitioned assets, they must use
   `TimeWindowPartitionMapping` or `IdentityPartitionMapping`

If these requirements aren't met, assets execute in separate runs even with run grouping logic.

### Usage in Built-in Conditions

**eager() and on_missing():** Both use `any_deps_updated()` which includes `will_be_requested()`,
enabling run grouping.

**any_deps_missing():** Explicitly excludes `will_be_requested()` to avoid blocking on dependencies
that will be handled in the same run:

```python
AutomationCondition.any_deps_match(
    AutomationCondition.missing() & ~AutomationCondition.will_be_requested()
)
```

## Dependency Filtering with allow() and ignore()

### How Filtering Works

Dependency operators (`any_deps_match()`, `all_deps_match()`) check conditions on upstream assets.
Filtering controls which upstreams are checked.

**Implementation:**

```python
dep_keys = asset_graph.get(key).parent_entity_keys  # Start with all upstreams

if allow_selection is not None:
    dep_keys &= allow_selection.resolve(asset_graph)  # Intersection: only allowed

if ignore_selection is not None:
    dep_keys -= ignore_selection.resolve(asset_graph)  # Subtraction: remove ignored
```

### allow() Creates Intersection

Only dependencies in the selection are checked:

```python
condition = dg.AutomationCondition.any_deps_match(
    dg.AutomationCondition.missing()
).allow(dg.AssetSelection.groups("critical"))
```

If the asset has 10 upstreams but only 2 are in the "critical" group, only those 2 are checked for
missing status.

### ignore() Creates Subtraction

Dependencies in the selection are excluded:

```python
condition = dg.AutomationCondition.any_deps_updated().ignore(
    dg.AssetSelection.assets("test_data", "staging_data")
)
```

Updates to "test_data" and "staging_data" won't trigger the condition, even if they are
dependencies.

### Propagation Through Operators

When applied to composite conditions (AND/OR), filtering propagates to all sub-conditions that
support it:

```python
# Applies to both any_deps_missing() and any_deps_in_progress() within eager()
condition = dg.AutomationCondition.eager().allow(
    dg.AssetSelection.groups("production")
)
```

**What gets filtered:**

- All `any_deps_match()` calls
- All `all_deps_match()` calls
- Any nested conditions that support `.allow()` and `.ignore()`

**What doesn't get filtered:**

- Direct operands like `missing()` or `newly_updated()` on the asset itself
- Conditions that don't examine dependencies

### Combining allow() and ignore()

Both can be used together:

```python
condition = (
    dg.AutomationCondition.eager()
    .allow(dg.AssetSelection.groups("critical", "important"))
    .ignore(dg.AssetSelection.assets("flaky_sensor_data"))
)
```

Result: Only check dependencies in "critical" or "important" groups, but exclude "flaky_sensor_data"
even if it's in those groups.

## Understanding since_last_handled()

`since_last_handled()` is a convenience method that converts events to a status using `since()`:

```python
# These are equivalent:
condition.since_last_handled()

condition.since(
    AutomationCondition.newly_requested()
    | AutomationCondition.newly_updated()
    | AutomationCondition.initial_evaluation()
)
```

**Behavior:**

- Becomes true when `condition` becomes true
- Stays true until the asset is requested, updated, or the condition is first applied
- Resets on initial evaluation to handle condition changes

**Use case:** Persist an event until it's "handled" by either requesting or materializing the asset.
This prevents duplicate requests while ensuring the event isn't lost if the sensor is busy during
the tick when the event occurs.

## Composite Conditions Deep Dive

### any_deps_updated()

```python
AutomationCondition.any_deps_match(
    (
        AutomationCondition.newly_updated()
        & ~AutomationCondition.executed_with_root_target()
    ).with_label("newly_updated_without_root")
    | AutomationCondition.will_be_requested()
).with_label("any_deps_updated")
```

**Logic:**

1. Check if any dependency has `newly_updated()` AND wasn't executed in the same run as this asset's
   root (prevents double-triggering when assets are grouped)
2. OR check if any dependency `will_be_requested()` this tick (enables run grouping)

### any_deps_missing()

```python
AutomationCondition.any_deps_match(
    AutomationCondition.missing() & ~AutomationCondition.will_be_requested()
).with_label("any_deps_missing")
```

**Logic:**

- Check if any dependency is `missing()` AND will NOT be requested this tick
- If a dependency will be requested, it's not considered "blocking" because it will be handled in
  the same run

### all_deps_updated_since_cron()

```python
AutomationCondition.all_deps_match(
    AutomationCondition.newly_updated().since(
        AutomationCondition.cron_tick_passed(cron_schedule, cron_timezone)
    )
).with_label(f"all_deps_updated_since_cron({cron_schedule})")
```

**Logic:**

- For each dependency, check if it has been updated since the last cron tick
- All dependencies must have at least one partition that's been updated since the tick
- The `since()` operator creates a status from the two events (updated and cron tick)

## Evaluation Context

Conditions are evaluated by `AutomationConditionSensorDefinition`:

- **Evaluation frequency**: Default every 30 seconds
- **Evaluation scope**: Can evaluate all conditions or be split into multiple sensors for
  performance
- **Cursor management**: Each condition maintains a cursor tracking previous evaluation state
- **Candidate subset**: Conditions receive a candidate subset (partitions to consider) which may be
  filtered by parent conditions

## Performance Considerations

- **Condition complexity**: Deep condition trees with many dependencies can slow evaluation
- **Partition count**: Large numbers of partitions increase evaluation time
- **Multiple sensors**: Split automation into multiple sensors to parallelize and isolate failures
- **Lazy evaluation**: Conditions short-circuit when possible (e.g., AND stops at first false)
