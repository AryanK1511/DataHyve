import os

from dotenv import load_dotenv

load_dotenv()

# Ref Doc: https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#importing-the-snowflake-connector-module
SNOWFLAKE_CONFIG = {
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
}
