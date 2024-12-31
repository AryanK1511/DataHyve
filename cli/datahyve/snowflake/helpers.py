import time
from datetime import datetime

import psutil
from datahyve.snowflake.queries import (
    create_server_metrics_table_query,
    insert_server_metrics_query,
)


def create_table(conn):
    """Create a table in the snowflake database"""
    cur = conn.cursor()
    cur.execute(create_server_metrics_table_query)


# Collect server metrics
def collect_metrics():
    metrics = {}
    metrics["cpu_usage"] = psutil.cpu_percent(interval=1)
    metrics["memory_usage"] = psutil.virtual_memory().percent
    metrics["disk_usage"] = psutil.disk_usage("/").percent
    net_io = psutil.net_io_counters()
    metrics["network_sent"] = net_io.bytes_sent
    metrics["network_recv"] = net_io.bytes_recv
    metrics["uptime"] = int(time.time() - psutil.boot_time())
    load_avg = psutil.getloadavg()
    metrics["load_avg_1min"], metrics["load_avg_5min"], metrics["load_avg_15min"] = (
        load_avg
    )
    processes = [p.info for p in psutil.process_iter(["status"])]
    metrics["total_processes"] = len(processes)
    metrics["running_processes"] = sum(
        p["status"] == psutil.STATUS_RUNNING for p in processes
    )
    metrics["sleeping_processes"] = sum(
        p["status"] == psutil.STATUS_SLEEPING for p in processes
    )
    metrics["zombie_processes"] = sum(
        p["status"] == psutil.STATUS_ZOMBIE for p in processes
    )
    metrics["io_read_bytes"] = psutil.disk_io_counters().read_bytes
    metrics["io_write_bytes"] = psutil.disk_io_counters().write_bytes
    metrics["timestamp"] = datetime.now().isoformat()

    return metrics


# Insert metrics into Snowflake
def insert_metrics(metrics, conn):
    cur = conn.cursor()
    cur.execute(
        insert_server_metrics_query,
        (
            metrics["username"],
            metrics["server_name"],
            metrics["cpu_usage"],
            metrics["memory_usage"],
            metrics["disk_usage"],
            metrics["network_sent"],
            metrics["network_recv"],
            metrics["uptime"],
            metrics["load_avg_1min"],
            metrics["load_avg_5min"],
            metrics["load_avg_15min"],
            metrics["total_processes"],
            metrics["running_processes"],
            metrics["sleeping_processes"],
            metrics["zombie_processes"],
            metrics["io_read_bytes"],
            metrics["io_write_bytes"],
            metrics["timestamp"],
        ),
    )
    conn.commit()
    conn.close()
