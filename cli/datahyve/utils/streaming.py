import os
import subprocess
from pathlib import Path

from datahyve.config import console
from datahyve.constants import PID_FILE


def get_pid():
    """Reads the process ID from a file."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            return int(f.read().strip())
    return None


def save_pid(pid: int):
    """Saves the process ID to a file."""
    with open(PID_FILE, "w") as f:
        f.write(str(pid))


def run_streaming():
    """Run the streaming task as an asynchronous subprocess."""
    # Define the absolute path to the directory where 'streamer.py' is located
    script_directory = (
        Path(__file__).resolve().parent.parent / "snowflake"
    )  # Going two levels up to the root directory

    if not script_directory.exists():
        console.print(
            f"[bold red]Error: Directory {script_directory} does not exist![/bold red]"
        )
        return

    process = subprocess.Popen(
        ["python", "streamer.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=script_directory,  # Ensure the process runs in the correct directory
        preexec_fn=os.setpgrp,
    )

    save_pid(process.pid)

    console.print(
        f"[bold green]Streaming started with PID {process.pid}. Running in the background.[/bold green]"
    )
