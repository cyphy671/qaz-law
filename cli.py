import typer
from rich.console import Console

from tools.zangov.ingest_pg import ingest_all

app = typer.Typer(help="qaz-law CLI")
console = Console()


@app.command()
def ingest(
    recreate: bool = typer.Option(False, "--recreate", "-r"),
    start_page: int = typer.Option(1, "--start-page", "-s"),
):
    console.print("[bold green]Starting ingest...[/bold green]")
    ingest_all(recreate=recreate, start_page=start_page)
    console.print("[bold green]Data ingest completed successfully.[/bold green]")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


if __name__ == "__main__":
    app()
