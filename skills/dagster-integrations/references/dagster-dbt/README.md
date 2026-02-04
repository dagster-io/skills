# dagster-dbt Integration Reference

The dagster-dbt integration represents each dbt models as Dagster assets, enabling granular orchestration
at the individual model level.

### Workflow Decision Tree

Depending on the user's request, choose the appropriate reference file:

- Loading a dbt project into Dagster?
  - dbt Core projects: [Component-Based Integration](component-based-integration.md)
    - Note: the component-based approach is recommended for new projects as it is significantly simpler to configure and manage.
  - dbt Cloud projects: [dbt Cloud Integration](dbt-cloud.md)
  - Note: ensure that `dagster-dbt` is installed in the project before scaffolding the component:
    - `uv`-compatible projects: `uv add dagster-dbt`
- General questions about dbt and Dagster?
  - Determine which reference file from the [Reference Files Index](#reference-files-index) below is most relevant to the user's request.

## Reference Files Index

- [Component-Based Integration](component-based-integration.md)
  - Contains information about the `DbtProjectComponent`, including how to configure and modify it.
- [Pythonic Integration](pythonic-integration.md)
  - Contains information about the `@dbt_assets` decorator and patterns for using it.
- [Asset Checks](asset-checks.md)
  - Contains information regarding how dbt tests relate to Dagster asset checks.
- [Dependencies](dependencies.md)
  - Contains information about how Dagster parses dbt project dependencies (upstream assets) and patterns for defining additional dependencies.
- [dbt Cloud Integration](dbt-cloud.md)
  - Contains information about how to integrate dbt Cloud projects into Dagster.
