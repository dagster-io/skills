import json
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import typer

from dagster_skills_evals.benchmark_display import SpinnerDisplay, render_comparison
from dagster_skills_evals.console import console
from dagster_skills_evals.execution import (
    ClaudeExecutionResult,
    ClaudeExecutionResultSummary,
    execute_prompt_stream_json,
)

__all__ = ["benchmark"]


@dataclass
class _BenchmarkRun:
    result: ClaudeExecutionResult
    summary: ClaudeExecutionResultSummary


def _build_summary(
    result: ClaudeExecutionResult, *, skip_narrative: bool
) -> ClaudeExecutionResultSummary:
    """Build a summary, optionally skipping the expensive narrative generation."""
    if not skip_narrative:
        return result.summary

    return ClaudeExecutionResultSummary(
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        cost_usd=result.cost_usd,
        execution_time_ms=result.execution_time_ms,
        tools_used=[tool["name"] for tool in result.tool_usages],
        skills_used=[skill["skill"] for skill in result.skill_usages],
        model_usage=result.model_usage,
        narrative_summary=[],
    )


def _save_run_logs(run_dir: Path, result: ClaudeExecutionResult) -> None:
    """Save execution logs to a directory (mirrors BaselineManager.save_log pattern)."""
    run_dir.mkdir(parents=True, exist_ok=True)

    with (run_dir / "summary.json").open("w") as f:
        json.dump(result.messages, f, indent=2)
    with (run_dir / "stdout.txt").open("w") as f:
        f.write(result.stdout)
    with (run_dir / "stderr.txt").open("w") as f:
        f.write(result.stderr)


def _summary_to_dict(summary: ClaudeExecutionResultSummary) -> dict:
    """Convert a summary to a JSON-serializable dict."""
    return {
        "input_tokens": summary.input_tokens,
        "output_tokens": summary.output_tokens,
        "cost_usd": summary.cost_usd,
        "execution_time_ms": summary.execution_time_ms,
        "tools_used": summary.tools_used,
        "skills_used": summary.skills_used,
    }


def _run_setup_scripts(
    tmp_dir: str,
    setup_script: Path | None,
    run_specific_script: Path | None,
) -> None:
    """Run setup scripts in the given directory."""
    if setup_script:
        subprocess.run(str(setup_script), cwd=tmp_dir, shell=True, check=True)
    if run_specific_script:
        subprocess.run(str(run_specific_script), cwd=tmp_dir, shell=True, check=True)


def _run_benchmarks(
    prompt: str,
    timeout: int,
    skip_narrative: bool,
    quiet: bool,
    setup_script: Path | None,
    baseline_setup_script: Path | None,
    treatment_setup_script: Path | None,
    baseline_extra_args: list[str],
    treatment_extra_args: list[str],
) -> tuple[_BenchmarkRun, _BenchmarkRun]:
    """Execute both benchmark runs. When quiet=False, shows a live spinner."""
    total_phases = 2 if skip_narrative else 3

    def _execute(tmp_dir: str, extra_args: list[str]) -> ClaudeExecutionResult:
        return execute_prompt_stream_json(
            prompt=prompt,
            target_dir=tmp_dir,
            extra_args=extra_args or None,
            timeout=timeout,
        )

    def _run_baseline() -> ClaudeExecutionResult:
        tmp_dir = tempfile.mkdtemp(prefix="dg-eval-baseline-")
        _run_setup_scripts(tmp_dir, setup_script, baseline_setup_script)
        return _execute(tmp_dir, baseline_extra_args)

    def _run_treatment() -> ClaudeExecutionResult:
        tmp_dir = tempfile.mkdtemp(prefix="dg-eval-treatment-")
        _run_setup_scripts(tmp_dir, setup_script, treatment_setup_script)
        return _execute(tmp_dir, treatment_extra_args)

    if quiet:
        result_baseline = _run_baseline()
        result_treatment = _run_treatment()
        summary_baseline = _build_summary(result_baseline, skip_narrative=skip_narrative)
        summary_treatment = _build_summary(result_treatment, skip_narrative=skip_narrative)
    else:
        with SpinnerDisplay() as display:
            display.set_phase(1, total_phases, "Running baseline")
            result_baseline = _run_baseline()

            display.set_phase(2, total_phases, "Running treatment")
            result_treatment = _run_treatment()

            if not skip_narrative:
                display.set_phase(3, total_phases, "Generating narrative summaries")
            summary_baseline = _build_summary(result_baseline, skip_narrative=skip_narrative)
            summary_treatment = _build_summary(result_treatment, skip_narrative=skip_narrative)

            display.finish()

    return (
        _BenchmarkRun(result=result_baseline, summary=summary_baseline),
        _BenchmarkRun(result=result_treatment, summary=summary_treatment),
    )


def benchmark(
    prompt: str = typer.Option(..., "--prompt", "-p", help="The prompt to benchmark."),
    setup_script: Path | None = typer.Option(
        None, "--setup-script", help="Script to run before each benchmark run."
    ),
    baseline_setup_script: Path | None = typer.Option(
        None, "--baseline-setup-script", help="Script to run before the baseline run only."
    ),
    treatment_setup_script: Path | None = typer.Option(
        None, "--treatment-setup-script", help="Script to run before the treatment run only."
    ),
    claude_args: str | None = typer.Option(
        None, "--claude-args", help="Extra CLI args for both runs (shell-quoted string)."
    ),
    baseline_claude_args: str | None = typer.Option(
        None, "--baseline-claude-args", help="Extra CLI args for baseline run only."
    ),
    treatment_claude_args: str | None = typer.Option(
        None, "--treatment-claude-args", help="Extra CLI args for treatment run only."
    ),
    logs_dir: Path | None = typer.Option(
        None, "--logs-dir", "-l", help="Directory for logs. Defaults to a temp directory."
    ),
    timeout: int = typer.Option(300, "--timeout", "-t", help="Timeout in seconds per run."),
    skip_narrative: bool = typer.Option(
        False, "--skip-narrative", help="Skip narrative summary generation."
    ),
    output_json: bool = typer.Option(False, "--json", help="Output results as JSON to stdout."),
) -> None:
    """Run a prompt as baseline vs treatment and compare results."""
    if output_json:
        skip_narrative = True

    common_args = shlex.split(claude_args) if claude_args else []
    baseline_extra_args = common_args + (
        shlex.split(baseline_claude_args) if baseline_claude_args else []
    )
    treatment_extra_args = common_args + (
        shlex.split(treatment_claude_args) if treatment_claude_args else []
    )

    resolved_logs = (
        Path(logs_dir).resolve() if logs_dir else Path(tempfile.mkdtemp(prefix="dg-eval-"))
    )

    if not output_json:
        console.print(f"[bold]Prompt:[/bold] {prompt}")
        if setup_script:
            console.print(f"[bold]Setup script:[/bold] {setup_script}")
        if baseline_setup_script:
            console.print(f"[bold]Baseline setup:[/bold] {baseline_setup_script}")
        if treatment_setup_script:
            console.print(f"[bold]Treatment setup:[/bold] {treatment_setup_script}")
        if baseline_extra_args:
            console.print(f"[bold]Baseline args:[/bold] {baseline_extra_args}")
        if treatment_extra_args:
            console.print(f"[bold]Treatment args:[/bold] {treatment_extra_args}")
        console.print(f"[bold]Logs:[/bold]   {resolved_logs}")
        console.print()

    result_baseline, result_treatment = _run_benchmarks(
        prompt=prompt,
        timeout=timeout,
        skip_narrative=skip_narrative,
        quiet=output_json,
        setup_script=setup_script,
        baseline_setup_script=baseline_setup_script,
        treatment_setup_script=treatment_setup_script,
        baseline_extra_args=baseline_extra_args,
        treatment_extra_args=treatment_extra_args,
    )

    # Save logs
    _save_run_logs(resolved_logs / "baseline", result_baseline.result)
    _save_run_logs(resolved_logs / "treatment", result_treatment.result)

    if output_json:
        json.dump(
            {
                "baseline": _summary_to_dict(result_baseline.summary),
                "treatment": _summary_to_dict(result_treatment.summary),
                "logs_dir": str(resolved_logs),
            },
            sys.stdout,
            indent=2,
        )
        sys.stdout.write("\n")
    else:
        render_comparison(result_baseline.summary, result_treatment.summary)
        console.print()
        console.print(f"[dim]Logs saved to: {resolved_logs}[/dim]")
