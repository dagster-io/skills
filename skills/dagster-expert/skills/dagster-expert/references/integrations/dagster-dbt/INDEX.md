---
description: Integration with dbt Core and dbt Cloud for model-level orchestration.
type: index
triggers:
  - "dbt, dbt Core, dbt Cloud"
  - "dagster-dbt, dbt model, dbt project"
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

- [asset-checks](./asset-checks.md) — How dbt tests map to Dagster asset checks for data quality validation. (dbt test, asset check; dbt data quality, test mapping)
- [component-based-integration](./component-based-integration.md) — DbtProjectComponent configuration and customization for dbt Core projects in Dagster. (DbtProjectComponent configuration, customize dbt component; dbt component settings, dbt translation)
- [dbt-cloud](./dbt-cloud.md) — Integrating dbt Cloud projects into Dagster for cloud-based dbt orchestration. (dbt Cloud, cloud-based dbt; dbt Cloud integration)
- [dependencies](./dependencies.md) — How Dagster parses dbt project dependencies and patterns for defining additional upstream dependencies. (dbt dependency, upstream asset; dbt source, dependency parsing)
- [pythonic-integration](./pythonic-integration.md) — @dbt_assets decorator for programmatic dbt integration with maximum flexibility. (dbt_assets decorator, pythonic dbt; programmatic dbt integration)
- [scaffolding](./scaffolding.md) — Step-by-step guide for scaffolding a new dbt component in a Dagster project. (scaffold dbt, create dbt component; new dbt project in Dagster, set up dbt)
<!-- END GENERATED INDEX -->
