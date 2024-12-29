import time
from datetime import datetime

import psutil
from utils.snowflake import connect_to_snowflake


# Create the server_metrics table
def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS server_metrics (
        id NUMBER AUTOINCREMENT PRIMARY KEY,
        server_id VARCHAR(16777216) NOT NULL,
        cpu_usage FLOAT,
        memory_usage FLOAT,
        disk_usage FLOAT,
        network_sent FLOAT,
        network_recv FLOAT, 
        uptime NUMBER,
        load_avg_1min FLOAT,
        load_avg_5min FLOAT,
        load_avg_15min FLOAT,
        total_processes NUMBER,
        running_processes NUMBER,
        sleeping_processes NUMBER,
        zombie_processes NUMBER,
        io_read_bytes NUMBER,
        io_write_bytes NUMBER,
        timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = connect_to_snowflake()
    cur = conn.cursor()
    cur.execute(query)
    conn.close()


# Collect server metrics
def collect_metrics():
    metrics = {}
    metrics["server_id"] = "windows-server"
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
def insert_metrics(metrics):
    conn = connect_to_snowflake()
    cur = conn.cursor()
    query = """
    INSERT INTO server_metrics (
        server_id, cpu_usage, memory_usage, disk_usage, 
        network_sent, network_recv, uptime, load_avg_1min, load_avg_5min, 
        load_avg_15min, total_processes, running_processes, sleeping_processes, 
        zombie_processes, io_read_bytes, io_write_bytes, timestamp
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(
        query,
        (
            metrics["server_id"],
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


# Main function
if __name__ == "__main__":
    create_table()
    while True:
        metrics = collect_metrics()
        insert_metrics(metrics)
        print(f"Inserted metrics: {metrics}")
        time.sleep(60)
