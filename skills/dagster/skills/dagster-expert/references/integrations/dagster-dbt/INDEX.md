---
title: dagster-dbt
type: index
triggers:
  - "integrating dbt Core or dbt Cloud with Dagster"
---

# dagster-dbt Integration Reference

Docs: https://docs.dagster.io/integrations/libraries/dbt

The dagster-dbt integration represents each dbt models as Dagster assets, enabling granular orchestration
at the individual model level.

### Workflow Decision Tree

Depending on the user's request, choose the appropriate reference file:

- Creating/scaffolding a new dbt component? → [Scaffolding](scaffolding.md)
- Configuring or customizing an existing dbt component? → [Component-Based Integration](component-based-integration.md)
- Using dbt Cloud? → [dbt Cloud Integration](dbt-cloud.md)
- General questions about dbt and Dagster?
  - Determine which reference file from the [Reference Files Index](#reference-files-index) below is most relevant to the user's request.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [dbt: Asset Checks](./asset-checks.md) — how dbt tests map to Dagster asset checks
- [dbt: Component-Based Integration](./component-based-integration.md) — configuring or customizing DbtProjectComponent
- [dbt: Cloud Integration](./dbt-cloud.md) — integrating dbt Cloud with Dagster
- [dbt: Dependencies](./dependencies.md) — understanding or defining upstream dependencies for dbt models
- [dbt: Pythonic Integration](./pythonic-integration.md) — using @dbt_assets decorator for programmatic dbt integration
- [dbt: Scaffolding](./scaffolding.md) — scaffolding a new dbt component in a Dagster project
<!-- END GENERATED INDEX -->
