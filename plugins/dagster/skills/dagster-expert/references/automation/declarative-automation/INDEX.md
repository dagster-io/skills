---
title: Declarative Automation
type: index
triggers:
  - "asset-centric condition-based automation using AutomationCondition"
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

- [Advanced](./advanced.md) — status vs events, run grouping, or filtering in declarative automation
- [Core Concepts](./core-concepts.md) — using eager(), on_cron(), or on_missing() conditions
- [Customization](./customization.md) — customizing conditions with without(), replace(), allow(), or ignore()
- [Operands](./operands.md) — base condition building blocks like missing() or newly_updated()
- [Operators](./operators.md) — combining conditions using since, any_deps_match, or boolean operators
<!-- END GENERATED INDEX -->
