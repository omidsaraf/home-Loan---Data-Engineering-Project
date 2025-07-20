# Databricks notebook source
# MAGIC %md
# MAGIC ### 📘 Stream Ingestion: Kafka → Bronze Layer
# MAGIC - Uses metadata parameters
# MAGIC - Streams data from Kafka to ADLS Gen2 (bronze zone)
# MAGIC - Tracks micro-batches using job metadata

# COMMAND ----------

from pyspark.sql.functions import col, from_json, current_timestamp, expr
from pyspark.sql.types import StructType, StringType, TimestampType
import uuid

# COMMAND ----------

# ✅ Parameters (externalized from metadata)
dbutils.widgets.text("job_name", "homeloan_stream_ingestion")
dbutils.widgets.text("job_id", str(uuid.uuid4()))
dbutils.widgets.text("job_exec_id", str(uuid.uuid4()))
dbutils.widgets.text("kafka_bootstrap_servers", "<KAFKA_BOOTSTRAP>")
dbutils.widgets.text("kafka_topic", "homeloan_applications_stream")
dbutils.widgets.text("target_bronze_path", "/mnt/bronze/homeloan_applications_stream/")
dbutils.widgets.text("target_bronze_table", "bronze.homeloan_applications_stream")
dbutils.widgets.text("archive_path", "/mnt/archive/homeloan_applications_stream/")
dbutils.widgets.text("partition_column", "application_date")

# COMMAND ----------

# Get widget values
job_name = dbutils.widgets.get("job_name")
job_id = dbutils.widgets.get("job_id")
job_exec_id = dbutils.widgets.get("job_exec_id")
kafka_bootstrap_servers = dbutils.widgets.get("kafka_bootstrap_servers")
kafka_topic = dbutils.widgets.get("kafka_topic")
target_bronze_path = dbutils.widgets.get("target_bronze_path")
target_bronze_table = dbutils.widgets.get("target_bronze_table")
archive_path = dbutils.widgets.get("archive_path")
partition_column = dbutils.widgets.get("partition_column")

# COMMAND ----------

# Define schema (use metadata if applicable)
schema = StructType() \
    .add("application_id", StringType()) \
    .add("customer_id", StringType()) \
    .add("loan_amount", StringType()) \
    .add("application_date", StringType()) \
    .add("status", StringType())

# COMMAND ----------

# 🟡 Read from Kafka
stream_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
    .option("subscribe", kafka_topic)
    .option("startingOffsets", "latest")
    .load()
)

# Parse value column
json_df = stream_df.selectExpr("CAST(value AS STRING) as json_str") \
    .withColumn("data", from_json("json_str", schema)) \
    .select("data.*") \
    .withColumn("ingest_timestamp", current_timestamp())

# COMMAND ----------

# 🟢 Write to Bronze Delta Table (partitioned)
def write_to_bronze(batch_df, batch_id):
    batch_df.write \
        .format("delta") \
        .mode("append") \
        .partitionBy(partition_column) \
        .save(target_bronze_path)

    # Register table if needed
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {target_bronze_table}
        USING DELTA
        LOCATION '{target_bronze_path}'
    """)

    # Write log to metadata.job_logs
    log_df = spark.createDataFrame([(
        job_id,
        job_name,
        job_exec_id,
        kafka_topic,
        "SUCCEEDED",
        current_timestamp()
    )], ["job_id", "job_name", "job_exec_id", "source_name", "status", "executed_at"])

    log_df.write \
        .mode("append") \
        .format("jdbc") \
        .option("url", "jdbc:sqlserver://<SQL_SERVER>;databaseName=<DB>") \
        .option("dbtable", "metadata.job_logs") \
        .option("user", "<USER>") \
        .option("password", "<PASSWORD>") \
        .save()

# COMMAND ----------

# 🔄 Start the streaming query
query = (
    json_df.writeStream
    .foreachBatch(write_to_bronze)
    .option("checkpointLocation", f"{target_bronze_path}/_checkpoint")
    .start()
)

query.awaitTermination()
