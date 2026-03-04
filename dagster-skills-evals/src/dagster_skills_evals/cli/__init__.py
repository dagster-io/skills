import typer

from dagster_skills_evals.cli.benchmark import benchmark
from dagster_skills_evals.cli.index import app as index_app
from dagster_skills_evals.cli.run import run

app = typer.Typer(
    help="Dagster skills development tools.",
    context_settings={"help_option_names": ["-h", "--help"]},
)
app.add_typer(index_app)
app.command()(benchmark)
app.command()(run)
