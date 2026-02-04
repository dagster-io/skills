# Asset Checks

dbt tests are loaded as Dagster asset checks by default (enabled in dagster-dbt 0.23.0+).

## Enabling Source Tests

By default, only tests on dbt models are loaded as checks. To include tests on sources:

**Component approach:**

```yaml
attributes:
  translator_settings:
    enable_source_tests_as_checks: true
```

**Pythonic approach:**

```python
from dagster_dbt import DagsterDbtTranslator, DagsterDbtTranslatorSettings

translator = DagsterDbtTranslator(
    settings=DagsterDbtTranslatorSettings(
        enable_source_tests_as_checks=True
    )
)

@dbt_assets(
    manifest=my_dbt_project.manifest_path,
    dagster_dbt_translator=translator
)
def my_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
```

## Singular Tests with Multiple Dependencies

For singular tests that depend on multiple models, specify the target model in the test's config
block:

```sql
{{
    config(
        meta={
            'dagster': {
                'ref': {
                    'name': 'customers',
                    'package': 'my_dbt_assets',
                    'version': 1,
                },
            }
        }
    )
}}

SELECT ...
```

The `ref` structure mirrors dbt's
[ref function](https://docs.getdbt.com/reference/dbt-jinja-functions/ref) parameters. Without this
metadata, the test still runs but emits an AssetObservation instead of an asset check result.
