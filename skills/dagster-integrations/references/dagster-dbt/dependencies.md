# Dependencies

## How Dependencies Work

Dagster parses the dependencies already present in your dbt project:

- dbt `ref()` calls create dependencies between models
- dbt `source()` calls create dependencies on upstream assets

## Defining Upstream Dagster Assets

Define a Dagster asset as a dbt source in `sources.yml`:

```yaml
sources:
  - name: dagster
    tables:
      - name: my_upstream_asset
```

Then reference it in your dbt model:

```sql
select * from {{ source('dagster', 'my_upstream_asset') }}
```

This creates a data dependency where the dbt model reads from the Dagster asset.

## Adding Dependencies via Jinja Comments

To add dependencies not encoded in dbt's data lineage (e.g., scheduling constraints without data
reading), use a Jinja comment in your model:

```sql
-- depends_on: {{ source('dagster', 'upstream') }}

SELECT ...
```

When dbt compiles the project, it evaluates this Jinja template and adds the source to the model's
dependency list in the manifest. Dagster parses the manifest and creates the dependency edge. This
creates a scheduling dependency without requiring the model to SELECT from that source.
