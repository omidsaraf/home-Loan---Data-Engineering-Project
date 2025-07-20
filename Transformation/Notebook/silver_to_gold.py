# silver_to_gold.py

from pyspark.sql.functions import col, count, avg, sum as _sum
from utils import get_jdbc_properties, read_metadata_params, write_log_to_metadata, safe_execute
import datetime

dbutils.widgets.text("process_id", "4")
process_id = int(dbutils.widgets.get("process_id"))

jdbc_url = "<jdbc-url>"
jdbc_user = "<jdbc-user>"
jdbc_password = "<jdbc-password>"
jdbc_props = get_jdbc_properties(jdbc_user, jdbc_password)

log_table = "Metadata_Logs"

@safe_execute
def run_silver_to_gold():
    params = read_metadata_params(spark, jdbc_url, jdbc_props, process_id)

    silver_path = params.get("silver_path")
    gold_output_path = params.get("gold_output_path")
    partition_col = params.get("partition_column", "application_date")

    if not silver_path or not gold_output_path:
        raise ValueError("silver_path and gold_output_path must be set")

    start_time = datetime.datetime.now()

    df = spark.read.format("delta").load(silver_path)

    # Example KPIs
    kpi_df = df.groupBy(partition_col) \
        .agg(
            count("application_id").alias("total_applications"),
            avg("loan_amount").alias("avg_loan_amount"),
            _sum("disbursed_amount").alias("total_disbursed"),
            (count("application_id") - count("approved")).alias("rejected_count")
        )

    kpi_df.write.format("delta").mode("overwrite").partitionBy(partition_col).save(gold_output_path)

    end_time = datetime.datetime.now()

    log_dict = {
        "metadata_type": "Silver_to_Gold",
        "metadata_id": process_id,
        "action": "RUN",
        "previous_value": None,
        "new_value": f"Success: Calculated KPIs for {kpi_df.count()} partitions",
        "updated_by": "silver_to_gold_notebook",
        "updated_at": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    write_log_to_metadata(spark, jdbc_url, jdbc_props, log_table, log_dict)

run_silver_to_gold()
