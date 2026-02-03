---
name: dagster-best-practices
description:
  Expert guidance for working with Dagster. ALWAYS use before doing any task that requires
  knowledge specific to Dagster, or that reference assets, materialization, or data pipelines.
  Common tasks may include creating new definitions, understanding the project structure, answering
  general questions about the codebase (finding asset, schedule, sensor, component or job definitions),
  or providing deep information about a specific Dagster concept.
---

# Dagster Best Practices Skill

Expert guidance for building production-quality Dagster projects. Routes you to detailed reference documentation for assets, automation, and project structure.

## Workflow Decision Tree

Choose the appropriate reference based on what you need:

- **Working with assets?** [`references/assets.md`](references/assets.md)
  - Covers: Basic patterns, dependencies, partitions, multi-assets, metadata, groups
- **Automating compute?** [`references/automation/`](references/automation/)
  - Schedules: [`automation/schedules.md`](references/automation/schedules.md)
  - Sensors: [`automation/sensors/`](references/automation/sensors/) (basic, asset, run-status)
  - Declarative automation: [`automation/declarative-automation/`](references/automation/declarative-automation/)
- **Project structure?** [`references/project-structure.md`](references/project-structure.md)
  - Covers: Single projects, workspaces, components, code locations, definitions
- **Specific dg CLI commands?**
  - Use the [`/dagster-skills:dg`](../dg/SKILL.md) skill to guide users through the CLI.

These reference files contain detailed patterns, code examples, and best practices for each topic.

## Core Dagster Concepts

Brief definitions only (see reference files for detailed examples):

- **Asset**: Persistent object (table, file, model) produced by your pipeline
- **Job**: Selection of assets to execute together
- **Schedule**: Time-based automation using cron
- **Sensor**: Event-driven automation that watches for changes
- **Declarative Automation**: Modern automation where you set conditions on assets
- **Partition**: Logical division of data (by date, category)
- **Component**: Reusable, declarative building block (YAML-based)
