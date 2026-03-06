import json
import shlex
import sys
import tempfile
from pathlib import Path

import typer

from dagster_skills_evals.benchmark_display import SpinnerDisplay, render_single_run
from dagster_skills_evals.cli._shared import (
    build_summary,
    run_setup_scripts,
    save_run_logs,
    summary_to_dict,
)
from dagster_skills_evals.console import console
from dagster_skills_evals.execution import execute_prompt_stream_json

__all__ = ["run"]


def run(
    prompt: str = typer.Option(..., "--prompt", "-p", help="The prompt to run."),
    setup_script: Path | None = typer.Option(
        None, "--setup-script", help="Script to run before execution."
    ),
    claude_args: str | None = typer.Option(
        None, "--claude-args", help="Extra CLI args for the run (shell-quoted string)."
    ),
    logs_dir: Path | None = typer.Option(
        None, "--logs-dir", "-l", help="Directory for logs. Defaults to a temp directory."
    ),
    timeout: int = typer.Option(300, "--timeout", "-t", help="Timeout in seconds."),
    skip_narrative: bool = typer.Option(
        False, "--skip-narrative", help="Skip narrative summary generation."
    ),
    narrative_context: str | None = typer.Option(
        None,
        "--narrative-context",
        help="Extra context to include in narrative summary generation.",
    ),
    output_json: bool = typer.Option(False, "--json", help="Output results as JSON to stdout."),
) -> None:
    """Run a single prompt execution and display stats."""
    if output_json:
        skip_narrative = True

    extra_args = shlex.split(claude_args) if claude_args else []

    resolved_logs = (
        Path(logs_dir).resolve() if logs_dir else Path(tempfile.mkdtemp(prefix="dg-eval-run-"))
    )

    if not output_json:
        console.print(f"[bold]Prompt:[/bold] {prompt}")
        if setup_script:
            console.print(f"[bold]Setup script:[/bold] {setup_script}")
        if extra_args:
            console.print(f"[bold]Claude args:[/bold] {extra_args}")
        console.print(f"[bold]Logs:[/bold]   {resolved_logs}")
        console.print()

    tmp_dir = tempfile.mkdtemp(prefix="dg-eval-run-")

    if output_json:
        run_setup_scripts(tmp_dir, setup_script)
        result = execute_prompt_stream_json(
            prompt=prompt,
            target_dir=tmp_dir,
            extra_args=extra_args or None,
            timeout=timeout,
        )
        summary = build_summary(
            result, skip_narrative=skip_narrative, narrative_context=narrative_context
        )
    else:
        total_phases = 1 if skip_narrative else 2
        with SpinnerDisplay() as display:
            display.set_phase(1, total_phases, "Running prompt")
            run_setup_scripts(tmp_dir, setup_script)
            result = execute_prompt_stream_json(
                prompt=prompt,
                target_dir=tmp_dir,
                extra_args=extra_args or None,
                timeout=timeout,
            )

            if not skip_narrative:
                display.set_phase(2, total_phases, "Generating narrative summary")
            summary = build_summary(
                result, skip_narrative=skip_narrative, narrative_context=narrative_context
            )

            display.finish()

    # Save logs
    save_run_logs(resolved_logs, result)

    if output_json:
        json.dump(
            {
                "result": summary_to_dict(summary),
                "logs_dir": str(resolved_logs),
                "run_dir": tmp_dir,
            },
            sys.stdout,
            indent=2,
        )
        sys.stdout.write("\n")
    else:
        render_single_run(summary)
        console.print()
        console.print(f"[dim]Run dir:       {tmp_dir}[/dim]")
        console.print(f"[dim]Logs saved to: {resolved_logs}[/dim]")
