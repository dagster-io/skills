---
description: "Create a new Dagster project using the `uvx create-dagster` command."
triggers:
  - "create a new Dagster project"
  - "initial project setup"
---

# Overview

The `create-dagster` command is the standard entrypoint for creating a new Dagster project. It will scaffold out the proper structure of the python package and all relevant Dagster-specific configuration.

There are two main structures you can create:

- `project`: A single Dagster project
- `workspace`: A collection of related Dagster projects each with independent dependencies and configurations.

Unless the user specifically indicates that their use case requires multiple independent python packages, you should default to creating a project.

## Project Creation

By default, the following command should be executed when the user requests a new Dagster project to be created:

```bash
uvx create-dagster project <name> --uv-sync  # --uv-sync creates venv and installs deps (recommended)
```

## Workspace Creation

For more complex use cases, the following command may be used:

```bash
uvx create-dagster workspace <name>          # For multiple related projects
```
