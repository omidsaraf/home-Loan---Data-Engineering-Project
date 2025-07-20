# Databricks notebook source
# MAGIC %md
# MAGIC ### 🚀 Bronze (Batch) → Silver (Curated) Layer
# MAGIC - Reads raw batch from bronze
# MAGIC - Deduplicates, applies schema normalization
# MAGIC - Writes to Silver Delta table
# MAGIC - Tracks job metadata

# COMMAND ----------

from pyspark.sql.functions import col, current_timestamp, row_number
from pyspark.sql.window import Window
import uuid

# COMMAND ----------

# ✅ Parameters from Metadata
dbutils.widgets.text("job_name", "homeloan_bronze_to_silver_batch")
dbutils.widgets.text("job_id", str(uuid.uuid4()))
dbutils.widgets.text("job_exec_id", str(uuid.uuid4()))
dbutils.widgets.text("bronze_table", "bronze.homeloan_applications_batch")
dbutils.widgets.text("silver_path", "/mnt/silver/homeloan_applications_batch/")
dbutils.widgets.text("silver_table", "silver.homeloan_applications_batch")
dbutils.widgets.text("partition_column", "application_date")

# COMMAND ----------

job_name = dbutils.widgets.get("job_name")
job_id = dbutils.widgets.get("job_id")
job_exec_id = dbutils.widgets.get("job_exec_id")
bronze_table = dbutils.widgets.get("bronze_table")
silver_path = dbutils.widgets.get("silver_path")
silver_table = dbutils.widgets.get("silver_table")
partition_column = dbutils.widgets.get("partition_column")

# COMMAND ----------

# 🟠 Read from Bronze Delta
df_bronze = spark.table(bronze_table)

# COMMAND ----------

# ✅ Deduplicate by application_id using latest record by timestamp
window_spec = Window.partitionBy("application_id").orderBy(col("ingest_timestamp").desc())

df_silver = df_bronze \
    .withColumn("row_num", row_number().over(window_spec)) \
    .filter(col("row_num") == 1) \
    .drop("row_num")

# COMMAND ----------

# 🟢 Write to Silver Delta (curated)
df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy(partition_column) \
    .save(silver_path)

spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {silver_table}
    USING DELTA
    LOCATION '{silver_path}'
""")

# COMMAND ----------

# ✅ Log job execution to metadata
log_df = spark.createDataFrame([(
    job_id,
    job_name,
    job_exec_id,
    bronze_table,
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
