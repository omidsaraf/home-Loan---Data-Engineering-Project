# bronze_to_silver.py

from pyspark.sql.functions import col, lit
from utils import get_jdbc_properties, read_metadata_params, write_log_to_metadata, safe_execute
import datetime

dbutils.widgets.text("process_id", "3")
process_id = int(dbutils.widgets.get("process_id"))

jdbc_url = "<jdbc-url>"
jdbc_user = "<jdbc-user>"
jdbc_password = "<jdbc-password>"
jdbc_props = get_jdbc_properties(jdbc_user, jdbc_password)

log_table = "Metadata_Logs"

@safe_execute
def run_bronze_to_silver():
    params = read_metadata_params(spark, jdbc_url, jdbc_props, process_id)

    bronze_batch_path = params.get("bronze_batch_path")
    bronze_stream_path = params.get("bronze_stream_path")
    silver_output_path = params.get("silver_output_path")
    partition_col = params.get("partition_column", "application_date")

    if not bronze_batch_path or not bronze_stream_path or not silver_output_path:
        raise ValueError("bronze_batch_path, bronze_stream_path and silver_output_path must be defined")

    start_time = datetime.datetime.now()

    # Read batch and stream bronze tables
    batch_df = spark.read.format("delta").load(bronze_batch_path)
    stream_df = spark.read.format("delta").load(bronze_stream_path)

    # Example join: unify batch and stream data on application id, plus cleansing
    unified_df = batch_df.unionByName(stream_df) \
        .dropDuplicates(["application_id"]) \
        .filter(col("status").isNotNull()) \
        .withColumn("is_active", lit(True))

    # Write to silver
    unified_df.write.format("delta").mode("overwrite").partitionBy(partition_col).save(silver_output_path)

    end_time = datetime.datetime.now()

    log_dict = {
        "metadata_type": "Bronze_to_Silver",
        "metadata_id": process_id,
        "action": "RUN",
        "previous_value": None,
        "new_value": f"Success: Processed {unified_df.count()} rows",
        "updated_by": "bronze_to_silver_notebook",
        "updated_at": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    write_log_to_metadata(spark, jdbc_url, jdbc_props, log_table, log_dict)

run_bronze_to_silver()
