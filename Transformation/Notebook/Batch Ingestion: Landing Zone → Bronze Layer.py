# Databricks notebook source
# COMMAND ----------

# MAGIC %md
# MAGIC ### 📘 Batch Ingestion: Landing Zone → Bronze Layer
# MAGIC - Uses metadata tables for dynamic control
# MAGIC - Loads CSV/parquet/json data
# MAGIC - Applies partitioning by application_date
# MAGIC - Logs all actions to Metadata tables

# COMMAND ----------

# Imports
from pyspark.sql.functions import col, current_timestamp, input_file_name, lit
import datetime
import uuid

# COMMAND ----------

# ✅ Parameters (from metadata or ADF trigger)
dbutils.widgets.text("job_name", "homeloan_batch_ingestion")
dbutils.widgets.text("job_id", str(uuid.uuid4()))
dbutils.widgets.text("job_exec_id", str(uuid.uuid4()))
dbutils.widgets.text("source_name", "homeloan_applications")
dbutils.widgets.text("source_format", "csv")
dbutils.widgets.text("source_path", "/mnt/landing/homeloan_applications/")
dbutils.widgets.text("target_bronze_path", "/mnt/bronze/homeloan_applications/")
dbutils.widgets.text("target_bronze_table", "bronze.homeloan_applications")
dbutils.widgets.text("archive_path", "/mnt/archive/homeloan_applications/")
dbutils.widgets.text("partition_column", "application_date")

# COMMAND ----------

# Get parameter values
job_name = dbutils.widgets.get("job_name")
job_id = dbutils.widgets.get("job_id")
job_exec_id = dbutils.widgets.get("job_exec_id")
source_name = dbutils.widgets.get("source_name")
source_format = dbutils.widgets.get("source_format")
source_path = dbutils.widgets.get("source_path")
target_bronze_path = dbutils.widgets.get("target_bronze_path")
target_bronze_table = dbutils.widgets.get("target_bronze_table")
archive_path = dbutils.widgets.get("archive_path")
partition_column = dbutils.widgets.get("partition_column")

# COMMAND ----------

# 🔄 Load metadata config table (optional)
metadata_df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:sqlserver://<SQL_SERVER>;databaseName=<DB>") \
    .option("dbtable", "metadata.proc_param_metadata") \
    .option("user", "<USER>") \
    .option("password", "<PASSWORD>") \
    .load() \
    .filter(col("proc_name") == job_name)

# You can override above widgets from metadata_df if needed

# COMMAND ----------

# 🟡 Load source files
raw_df = spark.read \
    .format(source_format) \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(source_path)

# Add control columns
raw_df = raw_df.withColumn("ingest_timestamp", current_timestamp()) \
               .withColumn("source_file", input_file_name())

# COMMAND ----------

# 🔵 Write to bronze Delta table partitioned
raw_df.write \
    .mode("append") \
    .format("delta") \
    .partitionBy(partition_column) \
    .save(target_bronze_path)

# Register table
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {target_bronze_table}
    USING DELTA
    LOCATION '{target_bronze_path}'
""")

# COMMAND ----------

# 🗂️ Archive original files
dbutils.fs.mv(source_path, archive_path + f"run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}/", recurse=True)

# COMMAND ----------

# 📝 Insert Job Log Entry
log_df = spark.createDataFrame([(
    job_id,
    job_name,
    job_exec_id,
    source_name,
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

# MAGIC %md
# MAGIC ✅ Job completed successfully.
