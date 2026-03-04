from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from dagster_skills_evals.console import console
from dagster_skills_evals.execution import ClaudeExecutionResultSummary


class SpinnerDisplay:
    """Live spinner panel that shows the current phase."""

    def __init__(self):
        self._label = ""
        self._done = False
        self._live: Live | None = None

    def __enter__(self):
        self._live = Live(self._render(), console=console, refresh_per_second=4)
        self._live.__enter__()
        return self

    def __exit__(self, *args):
        if self._live:
            self._live.__exit__(*args)

    def set_phase(self, phase: int, total_phases: int, label: str) -> None:
        self._label = f"[{phase}/{total_phases}] {label}"
        self._done = False
        if self._live:
            self._live.update(self._render())

    def finish(self) -> None:
        self._done = True
        self._label = "Done"
        if self._live:
            self._live.update(self._render())

    def _render(self) -> Panel:
        content = Table.grid(padding=(0, 1))
        if self._done:
            content.add_row(Text("✓", style="green bold"), Text(self._label))
        else:
            content.add_row(Spinner("dots"), Text(self._label or "Starting..."))
        return Panel(content, border_style="blue")


def _delta_text(baseline: int | float, current: int | float, lower_is_better: bool = True) -> Text:
    """Format a delta value with color and percentage."""
    delta = current - baseline
    if baseline == 0:
        return Text(f"{current:,}")

    pct = (delta / baseline) * 100
    sign = "+" if delta > 0 else ""
    text = f"{current:,} ({sign}{pct:.1f}%)"

    if delta == 0:
        return Text(text)
    if lower_is_better:
        color = "red" if delta > 0 else "green"
    else:
        color = "green" if delta > 0 else "red"
    return Text(text, style=color)


def render_comparison(
    baseline: ClaudeExecutionResultSummary,
    treatment: ClaudeExecutionResultSummary,
) -> None:
    """Render a formatted comparison of two execution results."""
    # Metrics table
    metrics_table = Table(title="Benchmark Comparison", show_header=True, header_style="bold")
    metrics_table.add_column("Metric", style="bold")
    metrics_table.add_column("Baseline", justify="right")
    metrics_table.add_column("Treatment", justify="right")

    metrics_table.add_row(
        "Input Tokens",
        f"{baseline.input_tokens:,}",
        _delta_text(baseline.input_tokens, treatment.input_tokens),
    )
    metrics_table.add_row(
        "Output Tokens",
        f"{baseline.output_tokens:,}",
        _delta_text(baseline.output_tokens, treatment.output_tokens),
    )
    metrics_table.add_row(
        "Cost",
        f"${baseline.cost_usd:.4f}",
        _delta_text(baseline.cost_usd, treatment.cost_usd),
    )

    baseline_time = baseline.execution_time_ms / 1000
    treatment_time = treatment.execution_time_ms / 1000
    metrics_table.add_row(
        "Execution Time",
        f"{baseline_time:.1f}s",
        _delta_text(baseline_time, treatment_time),
    )
    metrics_table.add_row(
        "Tool Calls",
        str(len(baseline.tools_used)),
        _delta_text(len(baseline.tools_used), len(treatment.tools_used)),
    )
    metrics_table.add_row(
        "Skills Used",
        str(len(baseline.skills_used)),
        str(len(treatment.skills_used)),
    )

    console.print()
    console.print(metrics_table)

    # Tool usage details
    if baseline.tools_used or treatment.tools_used:
        tools_table = Table(title="Tool Usage", show_header=True, header_style="bold")
        tools_table.add_column("Run", style="bold")
        tools_table.add_column("Tools")

        if baseline.tools_used:
            tools_table.add_row("Baseline", ", ".join(baseline.tools_used))
        if treatment.tools_used:
            tools_table.add_row("Treatment", ", ".join(treatment.tools_used))
        if treatment.skills_used:
            tools_table.add_row("Skills Invoked", ", ".join(treatment.skills_used))

        console.print()
        console.print(tools_table)

    # Narrative summaries
    if baseline.narrative_summary:
        console.print()
        console.print(
            Panel(
                "\n".join(baseline.narrative_summary),
                title="Narrative: Baseline",
                border_style="yellow",
            )
        )

    if treatment.narrative_summary:
        console.print()
        console.print(
            Panel(
                "\n".join(treatment.narrative_summary),
                title="Narrative: Treatment",
                border_style="green",
            )
        )


def render_single_run(summary: ClaudeExecutionResultSummary) -> None:
    """Render stats for a single execution run."""
    metrics_table = Table(title="Execution Summary", show_header=True, header_style="bold")
    metrics_table.add_column("Metric", style="bold")
    metrics_table.add_column("Value", justify="right")

    metrics_table.add_row("Input Tokens", f"{summary.input_tokens:,}")
    metrics_table.add_row("Output Tokens", f"{summary.output_tokens:,}")
    metrics_table.add_row("Cost", f"${summary.cost_usd:.4f}")
    metrics_table.add_row("Execution Time", f"{summary.execution_time_ms / 1000:.1f}s")
    metrics_table.add_row("Tool Calls", str(len(summary.tools_used)))
    metrics_table.add_row("Skills Used", str(len(summary.skills_used)))

    console.print()
    console.print(metrics_table)

    if summary.tools_used:
        tools_table = Table(title="Tool Usage", show_header=True, header_style="bold")
        tools_table.add_column("Category", style="bold")
        tools_table.add_column("Details")

        tools_table.add_row("Tools", ", ".join(summary.tools_used))
        if summary.skills_used:
            tools_table.add_row("Skills Invoked", ", ".join(summary.skills_used))

        console.print()
        console.print(tools_table)

    if summary.narrative_summary:
        console.print()
        console.print(
            Panel(
                "\n".join(summary.narrative_summary),
                title="Narrative Summary",
                border_style="green",
            )
        )
