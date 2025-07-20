# batch_ingestion.py

from pyspark.sql.functions import current_timestamp
from utils import get_jdbc_properties, read_metadata_params, write_log_to_metadata, safe_execute
import datetime

# Databricks widgets for dynamic params
dbutils.widgets.text("process_id", "1")
process_id = int(dbutils.widgets.get("process_id"))

# JDBC config
jdbc_url = "<jdbc-url>"
jdbc_user = "<jdbc-user>"
jdbc_password = "<jdbc-password>"
jdbc_props = get_jdbc_properties(jdbc_user, jdbc_password)

log_table = "Metadata_Logs"

@safe_execute
def run_batch_ingestion():
    params = read_metadata_params(spark, jdbc_url, jdbc_props, process_id)

    input_path = params.get("input_path")
    output_path = params.get("output_path")
    input_format = params.get("input_format", "csv")
    write_mode = params.get("write_mode", "append")
    partition_col = params.get("partition_column", "application_date")

    if not input_path or not output_path:
        raise ValueError("input_path and output_path must be set in metadata")

    start_time = datetime.datetime.now()

    df = spark.read.format(input_format).option("header", "true").load(input_path)
    df = df.withColumn("ingestion_time", current_timestamp())

    df.write.format("delta").mode(write_mode).partitionBy(partition_col).save(output_path)

    end_time = datetime.datetime.now()

    log_dict = {
        "metadata_type": "Batch_Ingestion",
        "metadata_id": process_id,
        "action": "RUN",
        "previous_value": None,
        "new_value": f"Success: Loaded {df.count()} rows",
        "updated_by": "batch_ingestion_notebook",
        "updated_at": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    write_log_to_metadata(spark, jdbc_url, jdbc_props, log_table, log_dict)

run_batch_ingestion()
