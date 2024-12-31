import os
import subprocess

from app.config import console
from app.constants import PID_FILE


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
    process = subprocess.Popen(
        ["python", "app/snowflake/streamer.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        # Prevents child process from being terminated when the parent exits
        preexec_fn=os.setpgrp,
    )
    save_pid(process.pid)

    console.print(
        f"[bold green]Streaming started with PID {process.pid}. Running in the background.[/bold green]"
    )
