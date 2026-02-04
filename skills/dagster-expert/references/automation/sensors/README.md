# Sensors Reference

Sensors poll for events at regular intervals and trigger actions when conditions are met. They evaluate at discrete times, not continuously.

## Sensor Fundamentals

**Evaluation interval**: Sensors evaluate at intervals controlled by `minimum_interval_seconds` (default: 30 seconds). This is a minimum interval, not exact—if evaluation takes longer, the next evaluation is delayed.

**State tracking with cursors**: Sensors can maintain state across evaluations using cursors. The cursor is a string that persists between evaluations, typically used to track which events have already been processed.

**RunRequest and SkipReason**: Sensors yield `RunRequest` objects to launch runs or `SkipReason` to explain why no run was triggered. The `run_key` parameter on `RunRequest` prevents duplicate runs.

**Basic example**: See the main SKILL.md for a simple file sensor pattern with cursor state management.

## Choosing a Sensor Type

Use the appropriate sensor type based on what you're monitoring:

- **File arrivals or external API events** → [Basic Sensors](basic-sensors.md)
- **Asset materializations** → [Asset Sensors](asset-sensors.md)
- **Run completion or failure** → [Run Status Sensors](run-status-sensors.md)

**When to use declarative automation instead**: For asset-to-asset dependencies and complex condition logic, prefer declarative automation over sensors. Sensors are best for imperative side effects, external system integration, and custom polling logic.

## Reference Files Index

- [Basic Sensors](basic-sensors.md) - File watching and custom polling with cursors
- [Asset Sensors](asset-sensors.md) - React to asset materialization events
- [Run Status Sensors](run-status-sensors.md) - Monitor run success/failure and trigger actions
