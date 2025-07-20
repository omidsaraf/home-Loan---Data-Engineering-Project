# Databricks notebook source
# MAGIC %md
# MAGIC ### 🔁 Bronze (Stream) → Silver (Curated Stream) Layer
# MAGIC - Ingests raw stream from bronze
# MAGIC - Deduplicates by latest timestamp
# MAGIC - Writes to Silver Delta table
# MAGIC - Logs job using metadata

# COMMAND ----------

from pyspark.sql.functions import col, current_timestamp, row_number
from pyspark.sql.window import Window
import uuid

# COMMAND ----------

# 🧩 Metadata Parameters
dbutils.widgets.text("job_name", "homeloan_bronze_to_silver_stream")
dbutils.widgets.text("job_id", str(uuid.uuid4()))
dbutils.widgets.text("job_exec_id", str(uuid.uuid4()))
dbutils.widgets.text("bronze_table", "bronze.homeloan_applications_stream")
dbutils.widgets.text("silver_path", "/mnt/silver/homeloan_applications_stream/")
dbutils.widgets.text("silver_table", "silver.homeloan_applications_stream")
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

# ⚙️ Read from Bronze Stream Table (Delta Streaming)
df_stream = spark.readStream \
    .format("delta") \
    .table(bronze_table)

# COMMAND ----------

# 🧹 Deduplicate using Spark Windowing (latest per application_id)
window_spec = Window.partitionBy("application_id").orderBy(col("ingest_timestamp").desc())

df_clean = df_stream \
    .withWatermark("ingest_timestamp", "10 minutes") \
    .withColumn("row_num", row_number().over(window_spec)) \
    .filter("row_num = 1") \
    .drop("row_num")

# COMMAND ----------

# 🔄 Write to Silver Stream Table (Delta)
stream_query = df_clean.writeStream \
    .format("delta") \
    .outputMode("append") \
    .partitionBy(partition_column) \
    .option("checkpointLocation", f"{silver_path}/_checkpoint") \
    .start(silver_path)

# COMMAND ----------

# Create Silver Table if not exists
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {silver_table}
    USING DELTA
    LOCATION '{silver_path}'
""")

# COMMAND ----------

# Optional: Logging batch-wise if using foreachBatch for metadata tracking
