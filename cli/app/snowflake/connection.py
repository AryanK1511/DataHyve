import snowflake.connector
from app.config import SNOWFLAKE_CONFIG


# Ref Doc: https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect
def connect_to_snowflake(
    snowflake_user=SNOWFLAKE_CONFIG["user"],
    snowflake_password=SNOWFLAKE_CONFIG["password"],
    snowflake_account=SNOWFLAKE_CONFIG["account"],
    snowflake_database="datamyne",
    snowflake_schema="datamyne_schema",
):
    """Connects to Snowflake database instance on the cloud"""
    return snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        database=snowflake_database,
        schema=snowflake_schema,
    )
