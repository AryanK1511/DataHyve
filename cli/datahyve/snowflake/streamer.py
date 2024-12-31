import logging
import time

from datahyve.constants import LOG_FILE, METRICS_STREAM_INTERVAL_SECONDS
from datahyve.snowflake.connection import connect_to_snowflake
from datahyve.snowflake.helpers import collect_metrics, create_table, insert_metrics
from datahyve.utils.configfiles import get_config_file_content

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def stream_metrics():
    """Streams metrics to the database on Snowflake."""
    try:
        # 1. Get user config from the config file
        config_data = get_config_file_content()
        datahyve_username = config_data["credentials"].get("username")
        unique_server_name = config_data["credentials"].get("unique_server_name")
        snowflake_user = config_data["env_vars"].get("SNOWFLAKE_USER")
        snowflake_password = config_data["env_vars"].get("SNOWFLAKE_PASSWORD")
        snowflake_account = config_data["env_vars"].get("SNOWFLAKE_ACCOUNT")

        if not all(
            [
                datahyve_username,
                unique_server_name,
                snowflake_user,
                snowflake_password,
                snowflake_account,
            ]
        ):
            logging.error("Missing Snowflake credentials in the config file")
            raise Exception("Missing Snowflake credentials in the config file")

        logging.info("Config data successfully retrieved")

        # 2. Connect to the Snowflake DB
        conn = connect_to_snowflake(
            snowflake_user=snowflake_user,
            snowflake_password=snowflake_password,
            snowflake_account=snowflake_account,
        )
        logging.info("Successfully connected to Snowflake")

        # 3. Create the table if it doesn't exist already
        create_table(conn)
        logging.info("Table created or already exists")

        # 4. Start Streaming Metrics
        while True:
            try:
                if conn.is_closed():
                    conn = connect_to_snowflake(
                        snowflake_user=snowflake_user,
                        snowflake_password=snowflake_password,
                        snowflake_account=snowflake_account,
                    )

                # 5. Collect the metrics from the server
                metrics = collect_metrics()
                metrics["username"] = datahyve_username
                metrics["server_name"] = unique_server_name

                # 6. Push the data to the DB
                insert_metrics(metrics, conn)
                logging.info(f"Inserted metrics: {metrics}")

                # 7. Back to step 4. Rinse and repeat until the process is stopped.
                time.sleep(METRICS_STREAM_INTERVAL_SECONDS - 55)
            except Exception as e:
                logging.error(f"Error while streaming metrics: {e}", exc_info=True)
    except Exception as e:
        logging.critical(f"Critical error in stream_metrics: {e}", exc_info=True)


if __name__ == "__main__":
    stream_metrics()
