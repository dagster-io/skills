---
description: Declarative automation using AutomationCondition for asset-centric condition-based orchestration.
type: index
triggers:
  - "declarative automation, AutomationCondition, conditions"
  - "eager, on_cron, on_missing, complex triggers"
---

# Declarative Automation Reference

Declarative automation uses `AutomationCondition` objects to describe when assets should execute. Instead of scheduling jobs, you define conditions on assets that the system evaluates automatically.

## Overview

**Modern automation pattern**: Set conditions directly on assets rather than creating separate schedules or sensors. The system evaluates conditions every 30 seconds and launches runs when conditions are met.

**Benefits**:

- Asset-native: No separate job definitions needed
- Dependency-aware: Automatically considers upstream state
- Composable: Build complex conditions from simple building blocks
- Declarative: Easier to reason about than imperative sensors

**Basic examples**: See the main SKILL.md Quick Reference for `eager()`, `on_cron()`, and `on_missing()` examples.

## Requirements

- **Assets only**: Declarative automation does not work with ops or graphs
- **Sensor must be enabled**: The `default_automation_condition_sensor` must be toggled on in the Dagster UI under **Automation → Sensors**

## Core Concepts

### The Three Main Conditions

Start with one of these three conditions rather than building conditions from scratch:

- **`eager()`**: Execute immediately when dependencies update
- **`on_cron()`**: Execute on a schedule after dependencies update
- **`on_missing()`**: Execute missing partitions when dependencies are ready

### Customization

All three main conditions can be customized:

- Remove sub-conditions with `.without()`
- Replace sub-conditions with `.replace()`
- Filter dependencies with `.allow()` and `.ignore()`
- Combine with boolean operators: `&` (AND), `|` (OR), `~` (NOT)

### Advanced Concepts

- **Status vs Events**: Conditions can be persistent states or transient moments
- **Operands**: Base building blocks like `missing()`, `newly_updated()`
- **Operators**: Tools for composition like `since()`, `any_deps_match()`

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [advanced](./advanced.md) — Advanced declarative automation: status vs events, run grouping, and filtering. (advanced declarative automation; status vs events, run grouping, filtering)
- [core-concepts](./core-concepts.md) — Core declarative automation concepts: eager(), on_cron(), and on_missing() conditions. (eager, on_cron, on_missing; declarative automation basics, AutomationCondition)
- [customization](./customization.md) — Customizing declarative automation conditions with without(), replace(), allow(), and ignore(). (customize automation condition; without, replace, allow, ignore condition)
- [operands](./operands.md) — Declarative automation operands — base condition building blocks like missing() and newly_updated(). (automation operand, missing, newly_updated; base condition building block)
- [operators](./operators.md) — Declarative automation operators for combining and transforming conditions (since, any_deps_match). (automation operator, since, any_deps_match; combining conditions, boolean operators)
<!-- END GENERATED INDEX -->
