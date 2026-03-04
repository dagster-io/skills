---
description: Designing component integrations for external services and tools.
triggers:
  - "component integration, external service, modeling concepts"
---

# Modeling Concepts

To design an integration, you first need to determine how Dagster is intended to interact with the external service or tool. Broadly, there are three levels of control / insight that a given component may provide:

- Definitions: Dagster understands a set of assets defined in an external service or tool, and their dependencies on other assets.
- Observation: The above, and Dagster is also able to monitor for new events / updates that happen.
- Orchestration: The above, and Dagster is also able to kick off executions of the assets defined in the external service or tool.

## Orchestration

Dagster is directly responsible for both understanding the assets defined in the external service AND directly kicking off executions.

## Observation

This is typically a strict subset of the orchestration case, in which Dagster just extracts definitions from the tool

## Definition Only
