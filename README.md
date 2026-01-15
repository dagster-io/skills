# Claude Plugins for Dagster

A collection of Claude Code plugins for building workflows and data pipelines using Dagster.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add dagster-io/dagster-claude-plugins
```

Install a plugin:

```
/plugin install dg@claude-plugins-dagster
```

To update your marketplace plugins:

```
/plugin marketplace update
```

## Plugins

### dg

Commands for building and debugging.

Build:
  - `/dg:create-project <name>` - Create a new Dagster project with recommended structure
  - `/dg:create-workspace <name>` - Initialize a workspace for managing multiple projects
  - `/dg:prototype <requirements>` - Build production-ready Dagster implementations with best practices, testing, and validation

Debug:
  - `/dg:logs <run-id> [level] [limit]` - Retrieve and display logs for a run
  - `/dg:troubleshoot <run-id>` - Debug failing runs by analyzing error logs

### dagster-conventions

Comprehensive Dagster development conventions and best practices.

This skill provides expert guidance for Dagster data orchestration including assets, resources, schedules, sensors, partitions, testing, and ETL patterns.

### dagster-integrations

Comprehensive index of 82+ Dagster integrations including cloud platforms, data warehouses, ETL tools, AI/ML, data quality, monitoring, and more.

This skill helps you discover and integrate with the right tools for your data pipelines.

---

<div align="center">
  <img alt="dagster logo" src="https://github.com/user-attachments/assets/6fbf8876-09b7-4f4a-8778-8c0bb00c5237" width="auto" height="32px">
</div>
