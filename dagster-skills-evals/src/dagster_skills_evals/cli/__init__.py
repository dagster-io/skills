import typer

from dagster_skills_evals.cli.index import app as index_app

app = typer.Typer(help="Dagster skills development tools.")
app.add_typer(index_app)
