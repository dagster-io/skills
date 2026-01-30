# Declarative Automation: Operators

Operators combine operands and other conditions into complex expressions using boolean logic and
transformations.

## Boolean Operators

### & (AND)

Both conditions must be true:

```python
import dagster as dg

condition = (
    dg.AutomationCondition.newly_updated()
    & ~dg.AutomationCondition.in_progress()
)
```

### | (OR)

Either condition must be true:

```python
condition = (
    dg.AutomationCondition.missing()
    | dg.AutomationCondition.newly_updated()
)
```

### ~ (NOT)

Negates the condition:

```python
condition = ~dg.AutomationCondition.any_deps_missing()
```

## Transformation Operators

### since(reset_condition)

Converts two events into a status. Becomes true when the operand becomes true and remains true until
the reset condition becomes true.

```python
# True from when dependency updates until asset is requested
condition = dg.AutomationCondition.any_deps_updated().since(
    dg.AutomationCondition.newly_requested()
)
```

**Pattern:** `A.since(B)` means "A has occurred more recently than B"

**Use case:** Create persistent states from transient events. For example, "upstream updated" is an
event, but "upstream updated since I was last requested" is a status that stays true.

### newly_true()

Converts a status into an event. True only on the tick when the operand transitions from false to
true.

```python
# True only on the tick when the asset becomes missing
condition = dg.AutomationCondition.missing().newly_true()
```

**Use case:** Prevent repeated actions during persistent states. For example, `missing()` stays true
for many ticks, but `missing().newly_true()` is only true once when it becomes missing.

### since_last_handled()

Convenience method equivalent to
`.since(newly_requested() | newly_updated() | initial_evaluation())`.

```python
condition = dg.AutomationCondition.any_deps_updated().since_last_handled()
```

True from when the condition becomes true until the asset is requested, updated, or the condition is
first applied.

## Dependency Operators

### any_deps_match(condition)

True if the condition is true for at least one partition of any upstream dependency.

```python
condition = dg.AutomationCondition.any_deps_match(
    dg.AutomationCondition.missing()
)
```

Supports filtering with `.allow()` and `.ignore()` (see
[Dependency Filtering](#dependency-filtering)).

### all_deps_match(condition)

True if the condition is true for at least one partition of all upstream dependencies.

```python
condition = dg.AutomationCondition.all_deps_match(
    dg.AutomationCondition.newly_updated()
)
```

Requires every upstream asset to have at least one partition matching the condition.

Supports filtering with `.allow()` and `.ignore()`.

## Dependency Filtering

### allow(selection)

Restricts which dependencies are checked to only those in the `AssetSelection`:

```python
# Only consider dependencies in the "important" group
condition = dg.AutomationCondition.any_deps_match(
    dg.AutomationCondition.missing()
).allow(dg.AssetSelection.groups("important"))
```

Creates an intersection: `dep_keys & allowed_selection`

### ignore(selection)

Excludes dependencies in the `AssetSelection` from being checked:

```python
# Ignore the "foo" asset when checking for updates
condition = dg.AutomationCondition.any_deps_updated().ignore(
    dg.AssetSelection.assets("foo")
)
```

Creates a subtraction: `dep_keys - ignored_selection`

### Propagation Through Boolean Operators

When applied to `AND`/`OR` conditions, `.allow()` and `.ignore()` propagate to all sub-conditions:

```python
# Applies allow() to all dependency checks within eager()
condition = dg.AutomationCondition.eager().allow(
    dg.AssetSelection.groups("critical")
)
```

## Check Operators

### any_checks_match(condition, blocking_only)

True if any of the asset's checks match the condition.

```python
condition = dg.AutomationCondition.any_checks_match(
    dg.AutomationCondition.check_failed(),
    blocking_only=True,
)
```

**Parameters:**

- `condition`: Condition to evaluate against checks
- `blocking_only` (bool): If True, only considers blocking checks (default: False)

### all_checks_match(condition, blocking_only)

True if all of the asset's checks match the condition.

```python
condition = dg.AutomationCondition.all_checks_match(
    dg.AutomationCondition.check_passed(),
    blocking_only=True,
)
```

## Downstream Operators

### any_downstream_conditions()

True if any downstream asset's `AutomationCondition` evaluates to true.

```python
condition = dg.AutomationCondition.any_downstream_conditions()
```

Used for advanced coordination between assets.

## Labeling

### with_label(label)

Adds a human-readable label to a condition for debugging and UI display:

```python
condition = (
    dg.AutomationCondition.any_deps_updated()
    .since(dg.AutomationCondition.newly_requested())
).with_label("updated_since_requested")
```

Labels appear in condition evaluation traces in the Dagster UI.

## Composition Example

```python
import dagster as dg

# Complex condition combining multiple operators
condition = (
    dg.AutomationCondition.in_latest_time_window()  # Status operand
    & (
        dg.AutomationCondition.missing().newly_true()  # Status → Event
        | dg.AutomationCondition.any_deps_updated()     # Dependency operator
    ).since_last_handled()                              # Event → Status
    & ~dg.AutomationCondition.any_deps_match(           # Dependency operator with NOT
        dg.AutomationCondition.missing()
    ).allow(dg.AssetSelection.groups("critical"))       # Dependency filtering
).with_label("custom_condition")                        # Label
```

This condition materializes the latest time partition when it becomes missing or dependencies
update, but only if critical dependencies are not missing, and only once per update.
