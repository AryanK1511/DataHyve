import os
import signal

import typer
from datahyve.config import console, err_console
from datahyve.constants import PID_FILE
from datahyve.utils.configfiles import (
    check_config_exists,
    create_config_file,
    remove_config_file,
)
from datahyve.utils.streaming import get_pid, run_streaming

# ========== Initialize typer application ==========

app = typer.Typer()


# ========== Commands ==========


@app.command()
def start():
    """Streams the server metrics to the DataHyve cloud database instance on Snowflake"""
    check_config_exists()
    run_streaming()


@app.command()
def stop():
    """Stops the background streaming process."""
    check_config_exists()
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            console.print(
                f"[bold green]Streaming process with PID {pid} stopped.[/bold green]"
            )
        except ProcessLookupError:
            err_console.print(f"[bold red]No process with PID {pid} found.[/bold red]")
        os.remove(PID_FILE)
    else:
        console.print(
            "[bold yellow]No streaming process is currently running.[/bold yellow]"
        )


@app.command()
def create_config():
    """Creates the .datahyve.toml configuration file with placeholders."""
    create_config_file()


@app.command()
def remove_config():
    """Removes the .datahyve.toml configuration file."""
    check_config_exists()
    remove_config_file()


# ========== Start the Application ===========
if __name__ == "__main__":
    app()
