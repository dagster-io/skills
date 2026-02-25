---
description: Integration libraries index for 40+ tools and technologies (dbt, Fivetran, Snowflake, AWS, etc.).
type: index
triggers:
  - "integration, external tool, dagster-*"
  - "dbt, fivetran, airbyte, snowflake, bigquery, sling, aws, gcp"
---

# Integrations Reference

Dagster provides integration libraries for a range of tools and technologies. This reference directory contains detailed information about specific integrations.

Integration libraries are typically named `dagster-<technology>`, where `<technology>` is the name of the tool or technology being integrated. Integrations marked as _(community)_ are maintained by the community rather than the Dagster team.

All integration reference files contain a link to the official documentation for the integration library, which can be referenced in cases where the local documentation does not provide sufficient information.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [dagster-airbyte](./dagster-airbyte/INDEX.md) — Integration with Airbyte for EL (Extract-Load) syncs as Dagster assets. _(airbyte, extract-load sync)_
- [dagster-airlift](./dagster-airlift/INDEX.md) — Integration with Airflow for migrating and co-orchestrating Airflow DAGs. _(airflow, airlift, DAG migration)_
- [dagster-aws](./dagster-aws/INDEX.md) — Integration with AWS services (S3, ECS, Lambda, etc.). _(aws, s3, ecs, lambda, amazon)_
- [dagster-azure](./dagster-azure/INDEX.md) — Integration with Azure services (ADLS, Blob Storage, etc.). _(azure, adls, blob storage, microsoft cloud)_
- [dagster-celery](./dagster-celery/INDEX.md) — Integration with Celery for distributed task execution. _(celery, distributed task queue)_
- [dagster-census](./dagster-census/INDEX.md) — Integration with Census for reverse ETL syncs (community-maintained). _(census, reverse ETL)_
- [dagster-dask](./dagster-dask/INDEX.md) — Integration with Dask for parallel and distributed computing. _(dask, parallel computing)_
- [dagster-databricks](./dagster-databricks/INDEX.md) — Integration with Databricks for Spark-based data processing. _(databricks, spark cluster)_
- [dagster-datadog](./dagster-datadog/INDEX.md) — Integration with Datadog for monitoring and observability. _(datadog, monitoring, observability)_
- [dagster-datahub](./dagster-datahub/INDEX.md) — Integration with DataHub for metadata management and data cataloging. _(datahub, metadata, data catalog)_
- [dagster-dbt](./dagster-dbt/INDEX.md) — Integration with dbt Core and dbt Cloud for model-level orchestration. _(dbt, dbt Core, dbt Cloud; dagster-dbt, dbt model, dbt project)_
- [dagster-deltalake](./dagster-deltalake/INDEX.md) — Integration with Delta Lake for lakehouse storage (community-maintained). _(delta lake, lakehouse)_
- [dagster-docker](./dagster-docker/INDEX.md) — Integration with Docker for containerized execution. _(docker, container execution)_
- [dagster-duckdb](./dagster-duckdb/INDEX.md) — Integration with DuckDB for in-process analytical queries. _(duckdb, analytical database)_
- [dagster-fivetran](./dagster-fivetran/INDEX.md) — Integration with Fivetran for managed EL (Extract-Load) connectors. _(fivetran, managed connectors, extract-load)_
- [dagster-gcp](./dagster-gcp/INDEX.md) — Integration with Google Cloud Platform (BigQuery, GCS, etc.). _(gcp, bigquery, gcs, google cloud)_
- [dagster-github](./dagster-github/INDEX.md) — Integration with GitHub for repository event handling. _(github, repository events)_
- [dagster-great-expectations](./dagster-great-expectations/INDEX.md) — Integration with Great Expectations for data validation and testing. _(great expectations, data validation)_
- [dagster-hightouch](./dagster-hightouch/INDEX.md) — Integration with Hightouch for reverse ETL and data activation. _(hightouch, reverse ETL, data activation)_
- [dagster-iceberg](./dagster-iceberg/INDEX.md) — Integration with Apache Iceberg for table format management (community-maintained). _(iceberg, table format)_
- [dagster-jupyter](./dagster-jupyter/INDEX.md) — Integration with Jupyter for notebook-based assets. _(jupyter, notebook asset)_
- [dagster-k8s](./dagster-k8s/INDEX.md) — Integration with Kubernetes for container orchestration and execution. _(kubernetes, k8s, container orchestration)_
- [dagster-looker](./dagster-looker/INDEX.md) — Integration with Looker for BI dashboard assets. _(looker, BI dashboard)_
- [dagster-mlflow](./dagster-mlflow/INDEX.md) — Integration with MLflow for ML experiment tracking and model management. _(mlflow, ML tracking, model management)_
- [dagster-msteams](./dagster-msteams/INDEX.md) — Integration with Microsoft Teams for notifications and alerts. _(microsoft teams, msteams, notifications)_
- [dagster-mysql](./dagster-mysql/INDEX.md) — Integration with MySQL for database storage backends. _(mysql, database backend)_
- [dagster-omni](./dagster-omni/INDEX.md) — Integration with Omni for analytics and BI. _(omni, analytics)_
- [dagster-openai](./dagster-openai/INDEX.md) — Integration with OpenAI for LLM-powered assets. _(openai, LLM, AI integration)_
- [dagster-pagerduty](./dagster-pagerduty/INDEX.md) — Integration with PagerDuty for incident management alerts. _(pagerduty, incident management, alerting)_
- [dagster-pandas](./dagster-pandas/INDEX.md) — Integration with Pandas for DataFrame type checking and validation. _(pandas, dataframe validation)_
- [dagster-pandera](./dagster-pandera/INDEX.md) — Integration with Pandera for DataFrame schema validation. _(pandera, schema validation)_
- [dagster-papertrail](./dagster-papertrail/INDEX.md) — Integration with Papertrail for log management. _(papertrail, log management)_
- [dagster-polars](./dagster-polars/INDEX.md) — Integration with Polars for fast DataFrame processing (community-maintained). _(polars, fast dataframe)_
- [dagster-postgres](./dagster-postgres/INDEX.md) — Integration with PostgreSQL for database storage backends. _(postgres, postgresql, database backend)_
- [dagster-powerbi](./dagster-powerbi/INDEX.md) — Integration with Power BI for BI dashboard assets. _(power bi, powerbi, BI dashboard)_
- [dagster-prometheus](./dagster-prometheus/INDEX.md) — Integration with Prometheus for metrics collection. _(prometheus, metrics)_
- [dagster-pyspark](./dagster-pyspark/INDEX.md) — Integration with PySpark for distributed data processing. _(pyspark, spark, distributed processing)_
- [dagster-sigma](./dagster-sigma/INDEX.md) — Integration with Sigma for BI and analytics assets. _(sigma, BI analytics)_
- [dagster-slack](./dagster-slack/INDEX.md) — Integration with Slack for notifications and alerts. _(slack, notifications, chat alerts)_
- [dagster-sling](./dagster-sling/INDEX.md) — Integration with Sling for EL (Extract-Load) data replication. _(sling, data replication, extract-load)_
- [dagster-snowflake](./dagster-snowflake/INDEX.md) — Integration with Snowflake for cloud data warehouse operations. _(snowflake, cloud data warehouse)_
- [dagster-spark](./dagster-spark/INDEX.md) — Integration with Apache Spark for distributed data processing. _(spark, distributed processing)_
- [dagster-ssh](./dagster-ssh/INDEX.md) — Integration with SSH for remote command execution. _(ssh, remote execution)_
- [dagster-tableau](./dagster-tableau/INDEX.md) — Integration with Tableau for BI dashboard assets. _(tableau, BI dashboard)_
- [dagster-twilio](./dagster-twilio/INDEX.md) — Integration with Twilio for SMS and communication. _(twilio, SMS, communication)_
- [dagster-wandb](./dagster-wandb/INDEX.md) — Integration with Weights and Biases for ML experiment tracking (community-maintained). _(wandb, weights and biases, ML tracking)_
<!-- END GENERATED INDEX -->
