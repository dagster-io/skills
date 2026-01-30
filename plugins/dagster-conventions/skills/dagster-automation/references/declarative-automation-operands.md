# Declarative Automation: Operands

Operands are base conditions that evaluate to true or false for a given asset or asset partition.
They represent fundamental states and events.

## Complete List of Operands

| Operand                                                     | Description                                                            | Type   |
| ----------------------------------------------------------- | ---------------------------------------------------------------------- | ------ |
| `AutomationCondition.missing()`                             | Target has not been executed                                           | Status |
| `AutomationCondition.in_progress()`                         | Target is part of an in-progress run or backfill                       | Status |
| `AutomationCondition.execution_failed()`                    | Target failed in its latest run                                        | Status |
| `AutomationCondition.newly_updated()`                       | Target was updated since the previous evaluation                       | Event  |
| `AutomationCondition.newly_requested()`                     | Target was requested on the previous evaluation                        | Event  |
| `AutomationCondition.code_version_changed()`                | Target has a new code version since the previous evaluation            | Event  |
| `AutomationCondition.cron_tick_passed(schedule, timezone)`  | A new tick of the cron schedule occurred since previous evaluation     | Event  |
| `AutomationCondition.in_latest_time_window(lookback_delta)` | Target falls within the latest time window of the PartitionsDefinition | Status |
| `AutomationCondition.will_be_requested()`                   | Target will be requested in this tick                                  | Status |
| `AutomationCondition.initial_evaluation()`                  | This is the first evaluation of this condition                         | Event  |

## Status vs Event Operands

**Status operands** are persistent and remain true for multiple evaluations:

- `missing()` - Stays true until the asset is materialized
- `in_progress()` - True while a run is executing
- `execution_failed()` - True until the asset succeeds or is re-requested
- `in_latest_time_window()` - True for the latest time partition(s)
- `will_be_requested()` - True during the tick when a request will be made

**Event operands** are transient and true for only one evaluation:

- `newly_updated()` - True only on the tick when the update occurs
- `newly_requested()` - True only on the tick when the request is made
- `code_version_changed()` - True only on the first tick after the change
- `cron_tick_passed()` - True only on the first tick after the cron tick
- `initial_evaluation()` - True only on the very first evaluation

## Detailed Descriptions

### missing()

True if the asset partition has never been materialized or observed.

### in_progress()

True if the asset partition is part of an in-progress run or backfill that has not yet executed it.
Combines `run_in_progress()` and `backfill_in_progress()`.

### execution_failed()

True if the latest execution of the asset partition failed.

### newly_updated()

True if the asset partition was materialized or observed since the previous evaluation. For
observations, only true if the data version changed.

### newly_requested()

True if the asset partition was requested on the previous evaluation tick.

### code_version_changed()

True if the asset's code version has changed since the previous evaluation.

### cron_tick_passed(cron_schedule, cron_timezone)

True on the first evaluation after a tick of the specified cron schedule occurs.

**Parameters:**

- `cron_schedule` (str): Cron expression
- `cron_timezone` (str): Timezone string (default: "UTC")

### in_latest_time_window(lookback_delta)

True for time partitions within the latest time window. For unpartitioned or non-time-partitioned
assets, always true.

**Parameters:**

- `lookback_delta` (Optional[timedelta]): If provided, returns partitions within this delta of the
  latest window end. For daily partitions with `lookback_delta=timedelta(hours=48)`, returns the
  latest 2 partitions.

### will_be_requested()

True if the asset partition will be requested in the current tick. Used internally for run grouping
(see [declarative-automation-advanced.md](declarative-automation-advanced.md#run-grouping)).

### initial_evaluation()

True only on the first evaluation after the condition is applied or modified.

## Composite Conditions

Built from base operands for convenience:

| Composite Condition                                                   | Expansion                                                                                 |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `AutomationCondition.any_deps_updated()`                              | `any_deps_match((newly_updated() & ~executed_with_root_target()) \| will_be_requested())` |
| `AutomationCondition.any_deps_missing()`                              | `any_deps_match(missing() & ~will_be_requested())`                                        |
| `AutomationCondition.any_deps_in_progress()`                          | `any_deps_match(in_progress())`                                                           |
| `AutomationCondition.all_deps_updated_since_cron(schedule, timezone)` | `all_deps_match(newly_updated().since(cron_tick_passed(schedule, timezone)))`             |

## Usage

Operands are composed using operators (see
[declarative-automation-operators.md](declarative-automation-operators.md)) to build complex
conditions:

```python
import dagster as dg

# Using operands directly
condition = dg.AutomationCondition.missing() & ~dg.AutomationCondition.in_progress()

# Using composite conditions
condition = dg.AutomationCondition.any_deps_updated()
```
