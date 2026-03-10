import json
import subprocess
from pathlib import Path

from dagster_skills_evals.execution import (
    ClaudeExecutionResult,
    ClaudeExecutionResultSummary,
)


def build_summary(
    result: ClaudeExecutionResult,
    *,
    skip_narrative: bool,
    narrative_context: str | None = None,
) -> ClaudeExecutionResultSummary:
    """Build a summary, optionally skipping the expensive narrative generation."""
    if not skip_narrative:
        return ClaudeExecutionResultSummary(
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            cost_usd=result.cost_usd,
            execution_time_ms=result.execution_time_ms,
            tools_used=[tool["name"] for tool in result.tool_usages],
            model_usage=result.model_usage,
            narrative_summary=result.generate_narrative_summary(narrative_context),
        )

    return ClaudeExecutionResultSummary(
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        cost_usd=result.cost_usd,
        execution_time_ms=result.execution_time_ms,
        tools_used=[tool["name"] for tool in result.tool_usages],
        model_usage=result.model_usage,
        narrative_summary=[],
    )


def save_run_logs(run_dir: Path, result: ClaudeExecutionResult) -> None:
    """Save execution logs to a directory."""
    run_dir.mkdir(parents=True, exist_ok=True)

    with (run_dir / "summary.json").open("w") as f:
        json.dump(result.messages, f, indent=2)
    with (run_dir / "stdout.txt").open("w") as f:
        f.write(result.stdout)
    with (run_dir / "stderr.txt").open("w") as f:
        f.write(result.stderr)


def summary_to_dict(summary: ClaudeExecutionResultSummary) -> dict:
    """Convert a summary to a JSON-serializable dict."""
    return {
        "input_tokens": summary.input_tokens,
        "output_tokens": summary.output_tokens,
        "cost_usd": summary.cost_usd,
        "execution_time_ms": summary.execution_time_ms,
        "tools_used": summary.tools_used,
    }


def run_setup_scripts(
    tmp_dir: str,
    setup_script: Path | None,
    run_specific_script: Path | None = None,
) -> None:
    """Run setup scripts in the given directory."""
    if setup_script:
        subprocess.run(str(setup_script.resolve()), cwd=tmp_dir, shell=True, check=True)
    if run_specific_script:
        subprocess.run(str(run_specific_script.resolve()), cwd=tmp_dir, shell=True, check=True)
