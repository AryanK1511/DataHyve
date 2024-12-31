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
    if CONFIG_FILE_PATH.exists():
        try:
            CONFIG_FILE_PATH.unlink()
            console.print(
                f"Configuration file removed from {CONFIG_FILE_PATH}",
                style="bold green",
            )
        except Exception as e:
            err_console.print(
                f"Error removing configuration file: {e}", style="bold red"
            )
    else:
        err_console.print(
            "Configuration file not found. To create the configuration file, run the following command:",
            style="bold yellow",
        )
        console.print("  datahyve create-config", style="bold cyan")
