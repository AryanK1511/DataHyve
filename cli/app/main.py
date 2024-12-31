import os
import signal

import typer
from app.config import console, err_console
from app.constants import PID_FILE
from app.utils.configfiles import create_config_file, remove_config_file
from app.utils.streaming import get_pid, run_streaming

# ========== Initialize typer application ==========

app = typer.Typer()


# ========== Commands ==========


@app.command()
def stream_metrics():
    """Streams the server metrics to the DataHyve cloud database instance on Snowflake"""
    run_streaming()


@app.command()
def stop_stream():
    """Stops the background streaming process."""
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            console.print(
                f"[bold green]Streaming process with PID {pid} stopped.[/bold green]"
            )
            os.remove(PID_FILE)
        except ProcessLookupError:
            err_console.print(f"[bold red]No process with PID {pid} found.[/bold red]")
    else:
        console.print(
            "[bold yellow]No streaming process is currently running.[/bold yellow]"
        )


@app.command()
def create_config():
    """Creates the .datahyve.toml configuration file with placeholders."""
    create_config_file()
    console.print("[bold green]Configuration file created successfully.[/bold green]")


@app.command()
def remove_config():
    """Removes the .datahyve.toml configuration file."""
    remove_config_file()
    console.print("[bold green]Configuration file removed successfully.[/bold green]")


# ========== Start the Application ===========
if __name__ == "__main__":
    app()
