import snowflake.connector
from config import SNOWFLAKE_CONFIG


# Ref Doc: https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect
def connect_to_snowflake():
    return snowflake.connector.connect(
        user=SNOWFLAKE_CONFIG["user"],
        password=SNOWFLAKE_CONFIG["password"],
        account=SNOWFLAKE_CONFIG["account"],
        database="datamyne",
        schema="datamyne_schema",
    )
