# Query used to create the SERVER_METRICS table in the DB
create_server_metrics_table_query = """
    CREATE TABLE IF NOT EXISTS server_metrics (
        username VARCHAR(16777216) NOT NULL PRIMARY KEY,
        server_name VARCHAR(16777216) NOT NULL,
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

# Query used to insert metrics data rows into the database
insert_server_metrics_query = """
    INSERT INTO server_metrics (
        username, server_name, cpu_usage, memory_usage, disk_usage, 
        network_sent, network_recv, uptime, load_avg_1min, load_avg_5min, 
        load_avg_15min, total_processes, running_processes, sleeping_processes, 
        zombie_processes, io_read_bytes, io_write_bytes, timestamp
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
