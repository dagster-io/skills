---
title: Integration libraries index for 40+ tools and technologies (dbt, Fivetran, Snowflake, AWS, etc.).
type: index
triggers:
  - "integration, external tool, dagster-\\*"
  - "dbt, fivetran, airbyte, snowflake, bigquery, sling, aws, gcp"
---

# Integrations Reference

Dagster provides integration libraries for a range of tools and technologies. This reference directory contains detailed information about specific integrations.

Integration libraries are typically named `dagster-<technology>`, where `<technology>` is the name of the tool or technology being integrated. Integrations marked as _(community)_ are maintained by the community rather than the Dagster team.

All integration reference files contain a link to the official documentation for the integration library, which can be referenced in cases where the local documentation does not provide sufficient information.

## Reference Files Index

<!-- BEGIN GENERATED INDEX -->

- [dagster-airbyte](./dagster-airbyte/INDEX.md) — Airbyte extract-load syncs as Dagster assets
- [Integration with Apache Airflow for running Dagster pipelines in Airflow.](./dagster-airflow/INDEX.md) — airflow, apache airflow, DAG
- [dagster-airlift](./dagster-airlift/INDEX.md) — migrating or co-orchestrating Airflow DAGs with Dagster
- [dagster-aws](./dagster-aws/INDEX.md) — AWS services (S3, ECS, Lambda) from Dagster
- [dagster-azure](./dagster-azure/INDEX.md) — Azure services (ADLS, Blob Storage) from Dagster
- [dagster-celery](./dagster-celery/INDEX.md) — distributed task execution with Celery
- [Integration with Celery and Docker for distributed containerized execution.](./dagster-celery-docker/INDEX.md) — celery docker, distributed container execution
- [Integration with Celery and Kubernetes for distributed container orchestration.](./dagster-celery-k8s/INDEX.md) — celery kubernetes, celery k8s, distributed orchestration
- [dagster-census](./dagster-census/INDEX.md) — reverse ETL syncs with Census
- [dagster-dask](./dagster-dask/INDEX.md) — parallel and distributed computing with Dask
- [dagster-databricks](./dagster-databricks/INDEX.md) — Spark-based data processing on Databricks
- [dagster-datadog](./dagster-datadog/INDEX.md) — monitoring and observability with Datadog
- [dagster-datahub](./dagster-datahub/INDEX.md) — metadata management and data cataloging with DataHub
- [dagster-dbt](./dagster-dbt/INDEX.md) — integrating dbt Core or dbt Cloud with Dagster
- [dagster-deltalake](./dagster-deltalake/INDEX.md) — lakehouse storage with Delta Lake
- [Integration with Delta Lake and Pandas for DataFrame IO managers.](./dagster-deltalake-pandas/INDEX.md) — delta lake pandas, deltalake dataframe
- [Integration with Delta Lake and Polars for DataFrame IO managers.](./dagster-deltalake-polars/INDEX.md) — delta lake polars, deltalake dataframe
- [Integration with dlt (data load tool) for declarative data pipelines.](./dagster-dlt/INDEX.md) — dlt, data load tool, declarative pipelines
- [dagster-docker](./dagster-docker/INDEX.md) — containerized execution with Docker
- [dagster-duckdb](./dagster-duckdb/INDEX.md) — in-process analytical queries with DuckDB
- [Integration with DuckDB and Pandas for DataFrame IO managers.](./dagster-duckdb-pandas/INDEX.md) — duckdb pandas, duckdb dataframe
- [Integration with DuckDB and Polars for DataFrame IO managers.](./dagster-duckdb-polars/INDEX.md) — duckdb polars, duckdb dataframe
- [Integration with DuckDB and PySpark for DataFrame IO managers.](./dagster-duckdb-pyspark/INDEX.md) — duckdb pyspark, duckdb spark
- [Integration for embedded ELT with Sling and dlt support.](./dagster-embedded-elt/INDEX.md) — embedded elt, sling, dlt, extract load transform
- [dagster-fivetran](./dagster-fivetran/INDEX.md) — managed extract-load connectors with Fivetran
- [dagster-gcp](./dagster-gcp/INDEX.md) — Google Cloud Platform (BigQuery, GCS) from Dagster
- [Integration with GCP BigQuery and Pandas for DataFrame IO managers.](./dagster-gcp-pandas/INDEX.md) — gcp pandas, bigquery pandas, bigquery dataframe
- [Integration with GCP BigQuery and PySpark for DataFrame IO managers.](./dagster-gcp-pyspark/INDEX.md) — gcp pyspark, bigquery pyspark, bigquery spark
- [dagster-github](./dagster-github/INDEX.md) — GitHub repository event handling from Dagster
- [dagster-great-expectations](./dagster-great-expectations/INDEX.md) — data validation and testing with Great Expectations
- [dagster-hightouch](./dagster-hightouch/INDEX.md) — reverse ETL and data activation with Hightouch
- [dagster-iceberg](./dagster-iceberg/INDEX.md) — Apache Iceberg table format management
- [dagster-jupyter](./dagster-jupyter/INDEX.md) — notebook-based assets with Jupyter
- [dagster-k8s](./dagster-k8s/INDEX.md) — Kubernetes container orchestration and execution
- [dagster-looker](./dagster-looker/INDEX.md) — Looker BI dashboard assets
- [dagster-mlflow](./dagster-mlflow/INDEX.md) — ML experiment tracking and model management with MLflow
- [dagster-msteams](./dagster-msteams/INDEX.md) — Microsoft Teams notifications and alerts from Dagster
- [dagster-mysql](./dagster-mysql/INDEX.md) — MySQL as a Dagster storage backend
- [dagster-omni](./dagster-omni/INDEX.md) — analytics and BI with Omni
- [dagster-openai](./dagster-openai/INDEX.md) — LLM-powered assets with OpenAI
- [dagster-pagerduty](./dagster-pagerduty/INDEX.md) — incident management alerts with PagerDuty
- [dagster-pandas](./dagster-pandas/INDEX.md) — Pandas DataFrame type checking and validation
- [dagster-pandera](./dagster-pandera/INDEX.md) — DataFrame schema validation with Pandera
- [dagster-papertrail](./dagster-papertrail/INDEX.md) — log management with Papertrail
- [dagster-polars](./dagster-polars/INDEX.md) — fast DataFrame processing with Polars
- [Integration with Polytomic for data syncing.](./dagster-polytomic/INDEX.md) — polytomic, data sync
- [dagster-postgres](./dagster-postgres/INDEX.md) — PostgreSQL as a Dagster storage backend
- [dagster-powerbi](./dagster-powerbi/INDEX.md) — Power BI dashboard assets
- [dagster-prometheus](./dagster-prometheus/INDEX.md) — metrics collection with Prometheus
- [dagster-pyspark](./dagster-pyspark/INDEX.md) — distributed data processing with PySpark
- [dagster-sigma](./dagster-sigma/INDEX.md) — BI and analytics assets with Sigma
- [dagster-slack](./dagster-slack/INDEX.md) — Slack notifications or alerts from Dagster
- [dagster-sling](./dagster-sling/INDEX.md) — EL data replication with Sling
- [dagster-snowflake](./dagster-snowflake/INDEX.md) — interacting with Snowflake from Dagster
- [Integration with Snowflake and Pandas for DataFrame IO managers.](./dagster-snowflake-pandas/INDEX.md) — snowflake pandas, snowflake dataframe
- [Integration with Snowflake and Polars for DataFrame IO managers.](./dagster-snowflake-polars/INDEX.md) — snowflake polars, snowflake dataframe
- [Integration with Snowflake and PySpark for DataFrame IO managers.](./dagster-snowflake-pyspark/INDEX.md) — snowflake pyspark, snowflake spark
- [dagster-spark](./dagster-spark/INDEX.md) — distributed data processing with Apache Spark
- [dagster-ssh](./dagster-ssh/INDEX.md) — remote command execution via SSH
- [dagster-tableau](./dagster-tableau/INDEX.md) — Tableau BI dashboard assets
- [dagster-twilio](./dagster-twilio/INDEX.md) — SMS and communication with Twilio
- [dagster-wandb](./dagster-wandb/INDEX.md) — ML experiment tracking with Weights & Biases
<!-- END GENERATED INDEX -->
