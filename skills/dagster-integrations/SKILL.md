---
name: dagster-integrations
description:
  Skill that helps users discover and understand Dagster integration libraries. Used when users have requests related to
  integrating with other tools / technologies, or when have users have questions related to specific integration
  libraries (dagster-*).
---

# Dagster Integrations Skill

This skill is a thin wrapper around more complex and detailed reference documents. It helps guide users through workflows that require using or understanding Dagster integration libraries.

## Workflow Decision Tree

Depending on the user's request, choose the appropriate reference file:

- Using a specific integration library?
  - Try to find a `references/dagster-<technology>/` folder in this directory. This will be named directly after the integration library name (e.g. `dagster-dbt`, `dagster-fivetran`, `dagster-airbyte`, etc.). This folder will contain a `README.md` file that will contain references to more detailed reference files relevant to the specific request.
  - If no such folder exists, use the more general reference files outlined in the `Reference Files Index` section.
  - **Examples**:
    - "How do asset checks work with dagster-dbt?"
    - "Load my Fivetran connector into Dagster"
    - "Can I use Tableau with Dagster?"
  - **NOTE**: If the user is attempting to use a specific integration library for the first time (often the case when adding a new component to a project), ensure the integration library is installed in the project before scaffolding the component.
    - `uv`-compatible projects (most common): `uv add dagster-<technology>`
- General integration requests?
  - Use the more general reference files outlined in the `Reference Files Index` section.
  - **Examples**:
    - "How do I load data from a CSV file into Dagster?"
    - "What data quality tools does Dagster support?"

These reference files contain detailed instructions specific to the given workflow. If it is unclear which reference file to use, ask the user to clarify their request.

Note that some requests may require multiple reference files in order to complete.

## Reference Files Index

- [ai.md](./references/ai.md)
  - Contains information related to all integrations that are related to AI and ML.
- [etl.md](./references/etl.md)
  - Contains information related to all integrations that are related to ETL and ELT.
- [storage.md](./references/storage.md)
  - Contains information related to all integrations that are related to data storage.
- [compute.md](./references/compute.md)
  - Contains information related to all integrations that are related to compute.
- [bi.md](./references/bi.md)
  - Contains information related to all integrations that are related to BI and visualization.
- [monitoring.md](./references/monitoring.md)
  - Contains information related to all integrations that are related to monitoring and observability.
- [alerting.md](./references/alerting.md)
  - Contains information related to all integrations that are related to alerting and notifications.
- [testing.md](./references/testing.md)
  - Contains information related to all integrations that are related to testing and data quality.
- [dagster-dbt/README.md](./references/dagster-dbt/README.md)
  - Contains information related to the dagster-dbt integration library.
