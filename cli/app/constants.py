from pathlib import Path

# Name of the config file
CONFIG_FILE_NAME = ".datahyve.toml"

# The CONFIG_FILE_PATH will always be the user's home dir
CONFIG_FILE_PATH = Path.home() / CONFIG_FILE_NAME

# This will be the default content of the config file that this tool creates
DEFAULT_CONFIG_FILE_CONTENT = {
    "credentials": {"username": "your_username_here"},
    "env_vars": {
        "SNOWFLAKE_USER": "dummy_username123",
        "SNOWFLAKE_PASSWORD": "dummyPassword123!",
        "SNOWFLAKE_ACCOUNT": "dummy_account12345",
    },
}
