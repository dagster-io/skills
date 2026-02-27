---
description: Decision tree for choosing between schedules, sensors, and declarative automation.
triggers:
  - "which automation approach, schedule vs sensor vs declarative"
  - "set up automation, choose automation type"
---

# Choosing an Automation Approach

Dagster provides three main approaches to automation: schedules for time-based execution, sensors for event-driven triggers, and declarative automation for asset-centric condition-based orchestration.

## Workflow Decision Tree

Choose your automation approach based on your use case:

```
What are you trying to automate?

├─ Fixed time-based execution?
│  └─ Schedules (schedules.md)
│
├─ Event-driven automation?
│  ├─ File arrives or external event → Basic Sensors (../sensors/basic-sensors.md)
│  ├─ Asset materialization completes → Asset Sensors (../sensors/asset-sensors.md)
│  └─ Run status changes (success/failure) → Run Status Sensors (../sensors/run-status-sensors.md)
│
└─ Modern asset-centric automation with conditions?
   └─ Declarative Automation (declarative-automation/) (recommended for asset pipelines)
```

## Core Concepts

### Jobs

A **job** is a selection of assets to execute together. Jobs are the unit of execution that schedules and sensors trigger.

```python
import dagster as dg

# Define a job that selects specific assets
analytics_job = dg.define_asset_job(
    name="analytics_job",
    selection=["sales_data", "customer_metrics"]
)
```

Jobs can also select assets by tags, groups, or patterns:

```python
# Select all assets with a specific tag
tagged_job = dg.define_asset_job(
    name="daily_job",
    selection=dg.AssetSelection.tag("priority", "high")
)

# Select all assets in a group
group_job = dg.define_asset_job(
    name="etl_job",
    selection=dg.AssetSelection.groups("etl")
)
```

### Automation Approaches

**Schedules**: Time-based execution with cron expressions. Best for predictable, recurring tasks.

**Sensors**: Poll for external events and trigger runs. Best for file arrivals, API events, or custom conditions.

**Declarative Automation**: Set conditions directly on assets. Best for complex dependency logic and asset-centric workflows.
