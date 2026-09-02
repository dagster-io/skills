---
title: create-dagster
triggers:
  - "creating a new Dagster project from scratch"
---

The `create-dagster` command scaffolds a new Dagster project with the proper Python package structure and Dagster-specific configuration.

Two structures are available:

- `project` — a single Dagster project (default choice unless user needs multiple independent packages)
- `workspace` — a collection of related Dagster projects with independent dependencies

**IMPORTANT** NEVER create a new Dagster project manually / without using the `create-dagster` command, as it will almost certainly be configured or structured improperly.

## Project Creation

```bash
uvx create-dagster project <name> --uv-sync  # --uv-sync creates venv and installs deps (recommended)
```

## Workspace Creation

```bash
uvx create-dagster workspace <name>          # For multiple related projects
```
