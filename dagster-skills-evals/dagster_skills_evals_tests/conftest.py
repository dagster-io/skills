import json
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
from dagster_shared.serdes import deserialize_value, serialize_value

from dagster_skills_evals.execution import ClaudeExecutionResult, ClaudeExecutionResultSummary
from dagster_skills_evals_tests.utils import unset_virtualenv


class BaselineManager:
    """Manages performance baselines with simple JSON storage."""

    def __init__(self, baseline_dir: Path, test_name: str, update_mode: bool = False):
        self.baseline_dir = baseline_dir
        self.test_name = test_name
        self.update_mode = update_mode
        self.baseline_dir.mkdir(exist_ok=True)

    @property
    def baseline_path(self) -> Path:
        return self.baseline_dir / f"{self.test_name}.json"

    @property
    def logs_dir(self) -> Path:
        return self.baseline_dir / "logs"

    @property
    def baseline(self) -> ClaudeExecutionResultSummary | None:
        if not self.baseline_path.exists():
            return None
        with self.baseline_path.open() as f:
            return deserialize_value(f.read(), ClaudeExecutionResultSummary)

    def save_baseline(self, summary: ClaudeExecutionResultSummary) -> None:
        with self.baseline_path.open("w") as f:
            f.write(serialize_value(summary, indent=2))

    def save_log(self, messages: list[dict[str, Any]]) -> Path:
        """Save messages to a timestamped log file."""
        self.logs_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_path = self.logs_dir / f"{self.test_name}_{timestamp}.json"
        with log_path.open("w") as f:
            json.dump(messages, f, indent=2)
        return log_path

    def _assert_improvement(
        self,
        old: ClaudeExecutionResultSummary | None,
        new: ClaudeExecutionResultSummary,
    ) -> None:
        """Assert that the new summary is an improvement over the old summary."""
        if old is None:
            return

        metrics = {
            "tools_used": {
                "baseline": len(old.tools_used),
                "current": len(new.tools_used),
                "delta": len(new.tools_used) - len(old.tools_used),
            },
            "input_tokens": {
                "baseline": old.input_tokens,
                "current": new.input_tokens,
                "delta": new.input_tokens - old.input_tokens,
            },
            "output_tokens": {
                "baseline": old.output_tokens,
                "current": new.output_tokens,
                "delta": new.output_tokens - old.output_tokens,
            },
            "execution_time_ms": {
                "baseline": old.execution_time_ms,
                "current": new.execution_time_ms,
                "delta": new.execution_time_ms - old.execution_time_ms,
            },
        }

        regressions = [name for name, m in metrics.items() if m["delta"] > 0]

        if regressions:
            import json

            raise AssertionError(
                f"Performance regression detected in: {', '.join(regressions)}\n"
                + json.dumps(metrics, indent=2)
            )

    def assert_improved(self, result: ClaudeExecutionResult) -> None:
        if self.update_mode:
            self.save_baseline(result.summary)

        self.save_log(result.messages)
        self._assert_improvement(self.baseline, result.summary)


def pytest_addoption(parser):
    parser.addoption(
        "--snapshot-update",
        action="store_true",
        default=False,
        help="Update baseline snapshots instead of comparing against them",
    )


@pytest.fixture
def baseline_manager(request) -> BaselineManager:
    """Provides baseline management with --snapshot-update support."""
    baseline_dir = Path(__file__).parent / "__baselines__"
    update_mode = request.config.getoption("--snapshot-update")
    return BaselineManager(baseline_dir, test_name=request.node.name, update_mode=update_mode)


@pytest.fixture(scope="session")
def project_name() -> str:
    return "acme_co_dataeng"


@pytest.fixture(scope="session")
def _empty_project(project_name: str) -> Iterator[Path]:
    # base empty project that we'll copy into others to avoid having to
    # run create-dagster for each test
    with tempfile.TemporaryDirectory() as tmp_dir:
        subprocess.run(
            ["uvx", "create-dagster", "project", project_name, "--no-uv-sync"],
            cwd=tmp_dir,
            check=False,
        )
        yield Path(tmp_dir) / project_name


@pytest.fixture
def empty_project_path(_empty_project: Path) -> Iterator[Path]:
    with unset_virtualenv(), tempfile.TemporaryDirectory() as tmp_dir:
        project_dir = Path(tmp_dir) / _empty_project.name
        shutil.copytree(_empty_project, project_dir)
        # Create a fresh venv in the copy
        subprocess.run(["uv", "sync"], cwd=project_dir, check=True)
        yield project_dir
