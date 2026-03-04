import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

from dagster_skills_evals.execution import execute_prompt
from dagster_skills_evals_tests.conftest import BaselineManager
from dagster_skills_evals_tests.utils import unset_virtualenv, write_function_body

pytestmark = pytest.mark.benchmark


def test_create_dagster_project(baseline_manager: BaselineManager):
    project_name = "acme_co_dataeng"
    prompt = f"/dagster-expert Create a new Dagster project named {project_name}"

    # Run with skills enabled
    with unset_virtualenv(), tempfile.TemporaryDirectory() as tmp_dir:
        result = execute_prompt(prompt, tmp_dir)

        # make sure the generated project is valid
        project_dir = Path(tmp_dir) / project_name

        subprocess.run(["uv", "run", "dg", "list", "projects"], cwd=project_dir, check=True)
        subprocess.run(["uv", "run", "dg", "list", "defs"], cwd=project_dir, check=True)

        baseline_manager.assert_improved(result)


def test_scaffold_asset(baseline_manager: BaselineManager, empty_project_path: Path):
    asset_name = "dwh_asset"
    prompt = f"/dagster-expert Add a new asset with an empty body named '{asset_name}'"

    # Run with skills enabled
    result = execute_prompt(prompt, empty_project_path.as_posix())

    # make sure the asset was scaffolded
    defs_result = subprocess.run(
        ["uv", "run", "dg", "list", "defs"],
        cwd=empty_project_path,
        check=True,
        capture_output=True,
        text=True,
    )
    assert asset_name in defs_result.stdout

    baseline_manager.assert_improved(result)


def test_create_dbt_component(baseline_manager: BaselineManager, empty_project_path: Path):
    prompt = """
    /dagster-expert Create a new dbt component named 'acme_dbt'. It should point to the https://github.com/dagster-io/jaffle_shop repo.
    """

    result = execute_prompt(prompt, empty_project_path.as_posix())

    # make sure the dbt component was created
    defs_result = subprocess.run(
        ["uv", "run", "dg", "list", "defs"],
        cwd=empty_project_path,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "stg_payments" in defs_result.stdout
    assert "customers:not_null_customers_customer_id" in defs_result.stdout

    baseline_manager.assert_improved(result)


def test_complex_automation_condition(baseline_manager: BaselineManager, empty_project_path: Path):
    prompt = """
    /dagster-expert Make it so that the customer_summary asset executes whenever any of the upstream assets update,
    except for the zip_codes asset, which just needs to have been executed since the start of the month.
    """

    def _original_source():
        import dagster as dg

        @dg.asset(deps=["customer_events", "sales_data", "zip_codes"])
        def customer_summary() -> None: ...

    asset_path = empty_project_path / "src" / "acme_co_dataeng" / "defs" / "customer_summary.py"
    write_function_body(_original_source, asset_path)

    result = execute_prompt(prompt, empty_project_path.as_posix())

    # make sure the automation condition was added
    defs_result = subprocess.run(
        ["uv", "run", "dg", "list", "defs"],
        cwd=empty_project_path,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "customer_summary" in defs_result.stdout
    assert "default_automation_condition_sensor" in defs_result.stdout
    with asset_path.open() as f:
        # should be using declarative automation with eager as the base condition
        assert "dg.AutomationCondition.eager()" in f.read()

    baseline_manager.assert_improved(result)


def test_get_run_failure_logs(baseline_manager: BaselineManager):
    run_id = "ca5aba5e-fade-bead-cafe-dec0de5c0de5"
    prompt = f"/dagster-expert What command would you run to figure out why this run failed: https://acme_co.dagster.cloud/prod/runs/{run_id}?"

    with tempfile.TemporaryDirectory() as tmp_dir:
        result = execute_prompt(prompt, tmp_dir)

        # should recommend the correct command from the reference docs
        assert f"dg api log get {run_id}" in result.conversation_summary()
        assert "--level ERROR" in result.conversation_summary()

        baseline_manager.assert_improved(result)


def test_missing_env_vars(baseline_manager: BaselineManager):
    prompt = "/dagster-expert I can't run my dagster Plus pipelines locally because I'm missing some required env vars, how can I fix this?"

    with tempfile.TemporaryDirectory() as tmp_dir:
        result = execute_prompt(prompt, tmp_dir)

        summary = result.conversation_summary()
        # should recommend pulling env vars from Plus
        assert "dg plus pull env" in summary

        baseline_manager.assert_improved(result)


def test_list_available_components(baseline_manager: BaselineManager):
    prompt = "/dagster-expert What components do I currently have access to?"

    with tempfile.TemporaryDirectory() as tmp_dir:
        result = execute_prompt(prompt, tmp_dir)

        summary = result.conversation_summary()
        # should recommend listing available component types
        assert "dg list components" in summary

        baseline_manager.assert_improved(result)


def test_complex_asset_selection(baseline_manager: BaselineManager):
    prompt = "/dagster-expert How can I select all my dbt assets that have an immediate upstream fivetran asset as a dependency? Just give me the command, do not run it."

    with tempfile.TemporaryDirectory() as tmp_dir:
        result = execute_prompt(prompt, tmp_dir)

        summary = result.conversation_summary()

        # should reference asset selection syntax with kind selectors
        assert "kind:fivetran+1" in summary.lower()
        assert "kind:dbt" in summary.lower()

        baseline_manager.assert_improved(result)


def test_create_custom_component(baseline_manager: BaselineManager, empty_project_path: Path):
    prompt = """/dagster-expert Create a new custom component called 'ApiAssetsComponent' that:
- Accepts cluster config with 'cluster_id' (str), 'api_key' (str), mem_request (float), and lifespan (datetime.timedelta) fields
- Accepts a list of asset definitions provided by the user
- All created asset definitions should include the cluster_id as a tag (in addition to any user-provided tags)
- The execution function should be left as a no-op
- When generating defintions, we should assert that the api_key is set to 'test-token-123'

Then instantiate this component with:
- cluster_id: "api.example.com"
- api_token: use the TOKEN environment variable (and set this to 'test-token-123' for the project)
- mem_request: 1.0
- lifespan: 1 hour 30 minutes (make sure the user can configure this with separate yaml fields for days, hours, minutes and seconds)
- Three assets:
  - key 'a' with tags {domain: sales, tier: raw}
  - key 'b' with tags {domain: marketing, tier: raw}
  - key 'c' with tags {domain: finance, tier: curated}
Make sure to verify that the new tags are included in the asset definitions.
"""

    old_token = os.environ.get("TOKEN")
    os.environ["TOKEN"] = "test-token-123"
    try:
        result = execute_prompt(prompt, empty_project_path.as_posix())

        # 1. Verify assets exist and have correct tags
        defs_result = subprocess.run(
            ["uv", "run", "dg", "list", "defs", "--json"],
            cwd=empty_project_path,
            capture_output=True,
            text=True,
            check=True,
        )
        defs_json = json.loads(defs_result.stdout)
        assets = {a["key"]: a for a in defs_json["assets"]}

        for key in ["a", "b", "c"]:
            assert key in assets, f"Asset '{key}' not found in defs"

        def _parse_tags(tag_list: list[str]) -> dict[str, str]:
            """Parse tags from '"key"="value"' format to a dict."""
            result = {}
            for tag in tag_list:
                k, v = tag.split("=", 1)
                result[k.strip('"')] = v.strip('"')
            return result

        # Check cluster_id tag on all assets
        for key in ["a", "b", "c"]:
            tags = _parse_tags(assets[key]["tags"])
            assert (
                tags["cluster_id"] == "api.example.com"
            ), f"Asset '{key}' cluster_id tag: {tags.get('cluster_id')}"

        # Check specific tags
        assert _parse_tags(assets["a"]["tags"])["domain"] == "sales"
        assert _parse_tags(assets["b"]["tags"])["domain"] == "marketing"
        assert _parse_tags(assets["c"]["tags"])["domain"] == "finance"

        # 2. Verify defs.yaml uses {{ env.TOKEN }}
        defs_yamls = list(empty_project_path.rglob("defs.yaml"))
        assert any(
            "{{ env.TOKEN }}" in f.read_text() for f in defs_yamls
        ), "No defs.yaml contains {{ env.TOKEN }}"

        # 3. Verify ResolvedAssetSpec is used within the component definition
        component_files_using_resolved = [
            f
            for f in empty_project_path.rglob("*.py")
            if "ApiAssetsComponent" in (text := f.read_text()) and "ResolvedAssetSpec" in text
        ]
        assert (
            component_files_using_resolved
        ), "No component definition file found that uses ResolvedAssetSpec"

        baseline_manager.assert_improved(result)
    finally:
        if old_token is None:
            os.environ.pop("TOKEN", None)
        else:
            os.environ["TOKEN"] = old_token
