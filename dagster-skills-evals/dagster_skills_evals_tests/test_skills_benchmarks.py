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
