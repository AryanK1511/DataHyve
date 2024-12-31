import toml
import typer
from app.config import console, err_console
from app.constants import CONFIG_FILE_PATH, DEFAULT_CONFIG_FILE_CONTENT


def create_config_file():
    """Creates the .datahyve.toml configuration file."""
    if CONFIG_FILE_PATH.exists():
        overwrite = typer.confirm(
            f"The file {CONFIG_FILE_PATH} already exists. Do you want to overwrite it?"
        )
        if overwrite:
            try:
                with open(CONFIG_FILE_PATH, "w") as f:
                    toml.dump(DEFAULT_CONFIG_FILE_CONTENT, f)
                console.print(
                    f"Configuration file successfully overwritten at {CONFIG_FILE_PATH}",
                    style="bold green",
                )
            except Exception as e:
                err_console.print(
                    f"Error overwriting configuration file: {e}", style="bold red"
                )
        else:
            console.print(
                "Operation canceled. The file was not overwritten.", style="yellow"
            )
    else:
        try:
            with open(CONFIG_FILE_PATH, "w") as f:
                toml.dump(DEFAULT_CONFIG_FILE_CONTENT, f)
            console.print(
                f"Configuration file created at {CONFIG_FILE_PATH}", style="bold green"
            )
        except Exception as e:
            err_console.print(
                f"Error creating configuration file: {e}", style="bold red"
            )


def remove_config_file():
    """Removes the .datahyve.toml configuration file."""
    try:
        CONFIG_FILE_PATH.unlink()
        console.print(
            f"Configuration file removed from {CONFIG_FILE_PATH}",
            style="bold green",
        )
    except Exception as e:
        err_console.print(f"Error removing configuration file: {e}", style="bold red")


def check_config_exists():
    """Check if the config file exists"""
    if not CONFIG_FILE_PATH.exists():
        err_console.print(
            "[bold red]Configuration file not found. Please create the configuration file first using 'create-config' command.[/bold red]"
        )
        raise typer.Exit()


def get_config_file_content():
    """Reads the configuration file and returns its content as a dictionary."""
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config_data = toml.load(f)
        return config_data
    except Exception as e:
        err_console.print(f"[bold red]Error reading configuration file: {e}[/bold red]")
        raise typer.Exit()
