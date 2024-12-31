from pathlib import Path

# Name of the config file
CONFIG_FILE_NAME = ".datahyve.toml"

# The CONFIG_FILE_PATH will always be the user's home dir
CONFIG_FILE_PATH = Path.home() / CONFIG_FILE_NAME

# This will be the default content of the config file that this tool creates
DEFAULT_CONFIG_FILE_CONTENT = {
    "credentials": {
        "username": "your_username_here",
        "unique_server_name": "your_unique_server_name_here",
    },
    "env_vars": {
        "SNOWFLAKE_USER": "dummy_username123",
        "SNOWFLAKE_PASSWORD": "dummyPassword123!",
        "SNOWFLAKE_ACCOUNT": "dummy_account12345",
    },
}

# This is the file where we would be tracking the streaming process
PID_FILE = "stream_pid.txt"

# This is the frequency of the metrics stream to the snowflake DB (in seconds)
METRICS_STREAM_INTERVAL_SECONDS = 60

# This is where all the logs for this CLI tool will be stored
LOG_FILE = "datahyve_metrics.log"
