# Storage Integrations

Data warehouses, databases, object storage, and table formats for persistent data storage and analytics.

---

## Data Warehouses

### Snowflake
**Package:** `dagster-snowflake` | **Support:** Dagster-supported

Cloud data warehouse with IO managers for pandas, polars, and PySpark DataFrames. Store and query large-scale analytics data.

**Use cases:**
- Store processed analytics tables for BI tools
- Query large datasets with SQL
- Integrate with dbt for SQL transformations
- Use as persistent storage for Dagster assets

**Quick start:**
```python
from dagster_snowflake import SnowflakeResource
from dagster_snowflake_pandas import SnowflakePandasIOManager

snowflake = SnowflakeResource(
    account="abc12345.us-east-1",
    user=dg.EnvVar("SNOWFLAKE_USER"),
    password=dg.EnvVar("SNOWFLAKE_PASSWORD"),
    database="analytics",
    schema="public"
)

# Use as IO Manager to auto-save DataFrames
defs = dg.Definitions(
    assets=[...],
    resources={
        "snowflake": snowflake,
        "io_manager": SnowflakePandasIOManager(
            resource=snowflake
        )
    }
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/snowflake

---

### BigQuery
**Package:** `dagster-gcp` | **Support:** Dagster-supported

Google's serverless data warehouse with IO managers for pandas and PySpark. Automatically scales for large queries.

**Use cases:**
- Run SQL analytics on petabyte-scale data
- Store structured data for analysis
- Query data with standard SQL
- Integrate with GCP data pipeline

**Quick start:**
```python
from dagster_gcp import BigQueryResource
from dagster_gcp_pandas import BigQueryPandasIOManager

bigquery = BigQueryResource(
    project="my-project"
)

@dg.asset
def query_bigquery(bigquery: BigQueryResource):
    return bigquery.get_client().query(
        "SELECT * FROM `project.dataset.table` LIMIT 1000"
    ).to_dataframe()
```

**Docs:** https://docs.dagster.io/integrations/libraries/gcp

---

### DuckDB
**Package:** `dagster-duckdb` | **Support:** Dagster-supported

In-process SQL analytics database, excellent for local development and single-machine analytics.

**Use cases:**
- Local development without external database
- Fast SQL queries on parquet/CSV files
- Embedded analytics in applications
- Testing and prototyping

**Quick start:**
```python
from dagster_duckdb import DuckDBResource
from dagster_duckdb_pandas import DuckDBPandasIOManager

duckdb = DuckDBResource(database="analytics.duckdb")

# Use as IO Manager
defs = dg.Definitions(
    assets=[...],
    resources={
        "io_manager": DuckDBPandasIOManager(
            database="analytics.duckdb"
        )
    }
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/duckdb

---

### Redshift
**Package:** `dagster-aws` | **Support:** Dagster-supported

AWS managed data warehouse based on PostgreSQL, optimized for OLAP workloads.

**Use cases:**
- Store large analytics datasets on AWS
- Query data with PostgreSQL-compatible SQL
- Integrate with AWS data ecosystem
- Run complex analytical queries

**Quick start:**
```python
from dagster_aws.redshift import RedshiftResource

redshift = RedshiftResource(
    host="my-cluster.redshift.amazonaws.com",
    port=5439,
    user=dg.EnvVar("REDSHIFT_USER"),
    password=dg.EnvVar("REDSHIFT_PASSWORD"),
    database="analytics"
)

@dg.asset
def redshift_query(redshift: RedshiftResource):
    with redshift.get_connection() as conn:
        return pd.read_sql(
            "SELECT * FROM sales_summary",
            conn
        )
```

**Docs:** https://docs.dagster.io/integrations/libraries/aws

---

### Teradata
**Package:** `dagster-teradata` | **Support:** Community-supported

Enterprise data warehouse platform for large-scale analytics and parallel processing.

**Use cases:**
- Connect to enterprise Teradata deployments
- Execute parallel queries on large datasets
- Integrate Teradata with modern data stack
- Migrate from Teradata to cloud warehouses

**Quick start:**
```python
from dagster_teradata import TeradataResource

teradata = TeradataResource(
    host="teradata.company.com",
    user=dg.EnvVar("TERADATA_USER"),
    password=dg.EnvVar("TERADATA_PASSWORD")
)

@dg.asset
def teradata_data(teradata: TeradataResource):
    return teradata.execute_query(
        "SELECT * FROM enterprise_data"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/teradata

---

## Relational Databases

### Postgres
**Package:** `dagster-postgres` | **Support:** Dagster-supported

Open-source relational database with ACID compliance and rich feature set.

**Use cases:**
- Transactional data storage
- Relational data modeling
- Application backend database
- Dagster instance storage

**Quick start:**
```python
from dagster_postgres import PostgresResource
from dagster_postgres_pandas import PostgresPandasIOManager

postgres = PostgresResource(
    host="localhost",
    port=5432,
    user=dg.EnvVar("POSTGRES_USER"),
    password=dg.EnvVar("POSTGRES_PASSWORD"),
    database="analytics"
)

@dg.asset
def postgres_table(postgres: PostgresResource):
    with postgres.get_connection() as conn:
        return pd.read_sql("SELECT * FROM users", conn)
```

**Docs:** https://docs.dagster.io/integrations/libraries/postgres

---

### MySQL
**Package:** `dagster-mysql` | **Support:** Dagster-supported

Popular open-source relational database management system.

**Use cases:**
- Web application databases
- Transactional workloads
- Legacy system integration
- Read replicas for analytics

**Quick start:**
```python
from dagster_mysql import MySQLResource

mysql = MySQLResource(
    host="localhost",
    port=3306,
    user=dg.EnvVar("MYSQL_USER"),
    password=dg.EnvVar("MYSQL_PASSWORD"),
    database="production"
)

@dg.asset
def mysql_data(mysql: MySQLResource):
    with mysql.get_connection() as conn:
        return pd.read_sql("SELECT * FROM orders", conn)
```

**Docs:** https://docs.dagster.io/integrations/libraries/mysql

---

## NoSQL Databases

### MongoDB
**Package:** `dagster-mongo` | **Support:** Community-supported

Document-oriented NoSQL database for flexible schema and high scalability.

**Use cases:**
- Store semi-structured data
- High-write workloads
- Flexible schemas
- Document storage

**Quick start:**
```python
from dagster_mongo import MongoResource

mongo = MongoResource(
    host="localhost",
    port=27017,
    database="mydb"
)

@dg.asset
def mongo_data(mongo: MongoResource):
    client = mongo.get_client()
    collection = client["mydb"]["users"]
    return list(collection.find({"status": "active"}))
```

**Docs:** https://docs.dagster.io/integrations/libraries/mongo

---

## Vector Databases

### Weaviate
**Package:** `dagster-weaviate` | **Support:** Community-supported

Vector database for AI-powered search and semantic similarity.

**Use cases:**
- Store and search embeddings
- Semantic search applications
- Recommendation systems
- RAG (Retrieval Augmented Generation)

**Quick start:**
```python
from dagster_weaviate import WeaviateResource

weaviate = WeaviateResource(
    url="http://localhost:8080",
    auth_api_key=dg.EnvVar("WEAVIATE_API_KEY")
)

@dg.asset
def store_embeddings(
    embeddings: list[list[float]],
    weaviate: WeaviateResource
):
    client = weaviate.get_client()
    # Store vectors in Weaviate
    for i, vector in enumerate(embeddings):
        client.data_object.create(
            {"text": f"document_{i}"},
            "Document",
            vector=vector
        )
```

**Docs:** https://docs.dagster.io/integrations/libraries/weaviate

---

### Chroma
**Package:** `dagster-chroma` | **Support:** Community-supported

Open-source embedding database for AI applications and vector search.

**Use cases:**
- Store document embeddings
- Build RAG applications
- Semantic search
- AI memory systems

**Quick start:**
```python
from dagster_chroma import ChromaResource

chroma = ChromaResource(
    host="localhost",
    port=8000
)

@dg.asset
def chroma_collection(chroma: ChromaResource):
    client = chroma.get_client()
    collection = client.create_collection("documents")
    collection.add(
        documents=["doc1", "doc2"],
        embeddings=[[1, 2, 3], [4, 5, 6]],
        ids=["id1", "id2"]
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/chroma

---

### Qdrant
**Package:** `dagster-qdrant` | **Support:** Community-supported

High-performance vector similarity search engine.

**Use cases:**
- Large-scale vector search
- Recommendation engines
- Image similarity search
- Neural search applications

**Quick start:**
```python
from dagster_qdrant import QdrantResource

qdrant = QdrantResource(
    url="http://localhost:6333",
    api_key=dg.EnvVar("QDRANT_API_KEY")
)

@dg.asset
def qdrant_vectors(qdrant: QdrantResource):
    client = qdrant.get_client()
    # Create collection and add vectors
    client.create_collection(
        collection_name="documents",
        vectors_config={"size": 384, "distance": "Cosine"}
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/qdrant

---

## Table Formats & Storage Layers

### Delta Lake
**Package:** `dagster-deltalake` | **Support:** Dagster-supported

Open-source storage layer providing ACID transactions and time travel for data lakes.

**Use cases:**
- Reliable data lake storage with ACID guarantees
- Time travel and data versioning
- Schema evolution for data lakes
- Integration with Spark and Databricks

**Quick start:**
```python
from dagster_deltalake import DeltaLakeResource

deltalake = DeltaLakeResource(
    storage_options={
        "AWS_ACCESS_KEY_ID": dg.EnvVar("AWS_KEY"),
        "AWS_SECRET_ACCESS_KEY": dg.EnvVar("AWS_SECRET")
    }
)

@dg.asset
def delta_table(deltalake: DeltaLakeResource):
    return deltalake.read_table(
        "s3://bucket/delta/table"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/deltalake

---

### Iceberg
**Package:** `dagster-iceberg` | **Support:** Community-supported

Apache Iceberg table format for large analytic datasets with schema evolution and partition evolution.

**Use cases:**
- Manage large analytics tables in data lakes
- Schema and partition evolution
- Time travel queries
- Multi-engine table access (Spark, Trino, etc.)

**Quick start:**
```python
from dagster_iceberg import IcebergResource

iceberg = IcebergResource(
    catalog_uri="thrift://localhost:9083",
    warehouse="s3://my-bucket/warehouse"
)

@dg.asset
def iceberg_table(iceberg: IcebergResource):
    return iceberg.read_table(
        "database.table_name"
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/iceberg

---

## File & Object Storage

### LakeFS
**Package:** `dagster-lakefs` | **Support:** Community-supported

Git-like version control for data lakes with branching and merging.

**Use cases:**
- Version control for data lakes
- Data experimentation with branches
- Reproducible data pipelines
- Data rollback capabilities

**Quick start:**
```python
from dagster_lakefs import LakeFSResource

lakefs = LakeFSResource(
    endpoint_url="http://localhost:8000",
    access_key_id=dg.EnvVar("LAKEFS_ACCESS_KEY"),
    secret_access_key=dg.EnvVar("LAKEFS_SECRET_KEY")
)

@dg.asset
def lakefs_data(lakefs: LakeFSResource):
    client = lakefs.get_client()
    # Read from specific branch
    data = client.read_object(
        repository="my-repo",
        ref="main",
        path="data/file.parquet"
    )
    return data
```

**Docs:** https://docs.dagster.io/integrations/libraries/lakefs

---

### Obstore
**Package:** `dagster-obstore` | **Support:** Community-supported

Universal object store abstraction supporting S3, GCS, Azure, and local files.

**Use cases:**
- Cloud-agnostic object storage
- Unified API for multiple clouds
- Local development with production parity
- Multi-cloud deployments

**Quick start:**
```python
from dagster_obstore import ObstoreResource

obstore = ObstoreResource(
    store_url="s3://my-bucket/path"
    # or "gs://bucket", "az://container", "file:///local/path"
)

@dg.asset
def cloud_agnostic_storage(obstore: ObstoreResource):
    # Works with any cloud
    data = obstore.read("data.parquet")
    return pd.read_parquet(data)
```

**Docs:** https://docs.dagster.io/integrations/libraries/obstore

**Note**: For cloud-specific object storage (AWS S3, GCS, Azure Blob), see the Compute category's cloud platform integrations.

---

## Metadata & Catalog

### DataHub
**Package:** `dagster-datahub` | **Support:** Dagster-supported

Metadata catalog for data discovery, lineage, and governance.

**Use cases:**
- Publish Dagster lineage to DataHub
- Data discovery and search
- Metadata management
- Data governance

**Quick start:**
```python
from dagster_datahub import DataHubResource

datahub = DataHubResource(
    server_url="http://localhost:8080",
    token=dg.EnvVar("DATAHUB_TOKEN")
)

@dg.asset
def publish_to_datahub(datahub: DataHubResource):
    # Publish metadata to DataHub
    datahub.emit_metadata(
        dataset_urn="urn:li:dataset:my_table",
        metadata={"description": "User data"}
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/datahub

---

### Atlan
**Package:** `dagster-atlan` | **Support:** Dagster-supported

Modern data catalog for discovery, collaboration, and governance.

**Use cases:**
- Data catalog integration
- Metadata synchronization
- Data governance
- Lineage tracking

**Quick start:**
```python
from dagster_atlan import AtlanResource

atlan = AtlanResource(
    base_url="https://company.atlan.com",
    api_key=dg.EnvVar("ATLAN_API_KEY")
)

@dg.asset
def sync_to_atlan(atlan: AtlanResource):
    client = atlan.get_client()
    # Sync Dagster assets to Atlan catalog
    client.create_or_update_asset(
        name="my_asset",
        type="TABLE",
        metadata={...}
    )
```

**Docs:** https://docs.dagster.io/integrations/libraries/atlan

---

### Secoda
**Package:** `dagster-secoda` | **Support:** Community-supported

Data discovery and documentation platform.

**Use cases:**
- Automated documentation
- Data lineage visualization
- Team collaboration on data
- Data search and discovery

**Quick start:**
```python
from dagster_secoda import SecodaResource

secoda = SecodaResource(
    api_key=dg.EnvVar("SECODA_API_KEY"),
    workspace_url="https://company.secoda.co"
)

@dg.asset
def publish_to_secoda(secoda: SecodaResource):
    # Publish Dagster metadata to Secoda
    secoda.sync_assets()
```

**Docs:** https://docs.dagster.io/integrations/libraries/secoda

---

## Storage Selection Guide

| Type | Best For | Examples | Scale |
|------|----------|----------|-------|
| **Data Warehouses** | Analytical queries | Snowflake, BigQuery, Redshift | Petabytes |
| **Relational** | Transactional data | Postgres, MySQL | Small-Large |
| **NoSQL** | Semi-structured data | MongoDB | Medium-Large |
| **Vector** | Embeddings, AI | Weaviate, Chroma, Qdrant | Medium-Large |
| **Table Formats** | Data lake tables | Delta, Iceberg | Large |
| **Object Storage** | Files, unstructured | S3, GCS, Azure Blob | Any |
| **Metadata** | Catalogs, lineage | DataHub, Atlan, Secoda | N/A |

## Common Patterns

### IO Manager Pattern
Most warehouse integrations provide IO managers to automatically persist DataFrames:

```python
from dagster_<warehouse>_pandas import <Warehouse>PandasIOManager

defs = dg.Definitions(
    assets=[my_asset],
    resources={
        "io_manager": <Warehouse>PandasIOManager(
            # connection config
        )
    }
)

# Assets automatically save to warehouse
@dg.asset
def my_table() -> pd.DataFrame:
    return pd.DataFrame({"col": [1, 2, 3]})
    # Automatically saved to warehouse as table
```

### Multi-Storage Pattern
```python
@dg.asset
def raw_data() -> pd.DataFrame:
    return extract_data()

@dg.asset
def warehouse_table(raw_data: pd.DataFrame, snowflake: SnowflakeResource):
    # Store in warehouse for analytics
    snowflake.write_dataframe(raw_data, "analytics.raw")

@dg.asset
def app_database(raw_data: pd.DataFrame, postgres: PostgresResource):
    # Store in Postgres for application
    postgres.write_dataframe(raw_data, "public.users")

@dg.asset
def search_index(raw_data: pd.DataFrame, weaviate: WeaviateResource):
    # Create search index
    weaviate.index_documents(raw_data)
```

### Local Dev with DuckDB
```python
# Development
local_io_manager = DuckDBPandasIOManager(
    database="dev.duckdb"
)

# Production
prod_io_manager = SnowflakePandasIOManager(...)

defs = dg.Definitions(
    assets=[...],
    resources={
        "io_manager": (
            local_io_manager if dev_mode
            else prod_io_manager
        )
    }
)
```

## Tips

- **Development**: Use DuckDB for local development, production warehouse in deployment
- **Cost**: BigQuery charges by query size, Snowflake by compute time
- **Performance**: Use partitioning and clustering for large tables
- **Schema**: Define schemas explicitly to avoid type inference issues
- **Vector DBs**: Choose based on scale - Chroma for small, Qdrant/Weaviate for large
- **Object storage**: Use cloud-native (S3/GCS/Azure) over databases for large files
- **Table formats**: Delta/Iceberg add ACID to data lakes, worth the complexity
- **Catalogs**: DataHub/Atlan provide discoverability for large data platforms
- **Compression**: Parquet with compression saves storage and improves performance
- **Indexes**: Add indexes on frequently queried columns
