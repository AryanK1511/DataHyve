import typer
from app.utils.configfiles import create_config_file, remove_config_file

app = typer.Typer()


@app.command()
def create_config():
    """Creates the .datahyve.toml configuration file with placeholders."""
    create_config_file()


@app.command()
def remove_config():
    """Removes the .datahyve.toml configuration file."""
    remove_config_file()


if __name__ == "__main__":
    app()
