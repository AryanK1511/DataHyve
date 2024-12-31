import os

from dotenv import load_dotenv
from rich.console import Console

# Load the environment variables into the application
load_dotenv()

# Initialize stdout and stderr
console = Console(soft_wrap=True)
err_console = Console(stderr=True, soft_wrap=True)

# Configure Snowflake Connection
# Ref Doc: https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#importing-the-snowflake-connector-module
SNOWFLAKE_CONFIG = {
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
}
