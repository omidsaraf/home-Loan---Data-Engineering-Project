# Databricks notebook source
# MAGIC %md
# MAGIC ## 🏅 Silver to Gold - Unified Loan Applications
# MAGIC - Merge silver batch + stream data
# MAGIC - Apply deduplication & business logic
# MAGIC - Persist unified table to Gold
# MAGIC - Metadata-driven execution

# COMMAND ----------

from pyspark.sql.functions import col, lit, current_timestamp, when
import uuid

# COMMAND ----------

# 📦 Metadata Parameters
dbutils.widgets.text("job_name", "homeloan_silver_to_gold_unified")
dbutils.widgets.text("job_id", str(uuid.uuid4()))
dbutils.widgets.text("job_exec_id", str(uuid.uuid4()))
dbutils.widgets.text("silver_batch_table", "silver.homeloan_applications_batch")
dbutils.widgets.text("silver_stream_table", "silver.homeloan_applications_stream")
dbutils.widgets.text("gold_table", "gold.homeloan_applications")
dbutils.widgets.text("gold_path", "/mnt/gold/homeloan_applications/")
dbutils.widgets.text("partition_column", "application_date")

# COMMAND ----------

# 🧩 Read parameters
job_name = dbutils.widgets.get("job_name")
job_id = dbutils.widgets.get("job_id")
job_exec_id = dbutils.widgets.get("job_exec_id")
silver_batch_table = dbutils.widgets.get("silver_batch_table")
silver_stream_table = dbutils.widgets.get("silver_stream_table")
gold_table = dbutils.widgets.get("gold_table")
gold_path = dbutils.widgets.get("gold_path")
partition_column = dbutils.widgets.get("partition_column")

# COMMAND ----------

# 🧪 Load Silver Data
df_batch = spark.read.table(silver_batch_table)
df_stream = spark.read.table(silver_stream_table)

# 👥 Add source columns for traceability
df_batch = df_batch.withColumn("source_type", lit("batch"))
df_stream = df_stream.withColumn("source_type", lit("stream"))

# COMMAND ----------

# 🔀 Union Stream and Batch
df_unified = df_batch.unionByName(df_stream)

# 🧠 Apply basic business rules
df_gold = df_unified \
    .withColumn("approval_status",
        when(col("loan_approved") == True, "Approved")
       .when(col("loan_approved") == False, "Rejected")
       .otherwise("Pending")) \
    .withColumn("processed_at", current_timestamp())

# COMMAND ----------

# 💾 Write to Gold
df_gold.write \
    .format("delta") \
    .mode("append") \
    .partitionBy(partition_column) \
    .option("mergeSchema", "true") \
    .save(gold_path)

# COMMAND ----------

# 📌 Create Gold Table if not exists
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {gold_table}
    USING DELTA
    LOCATION '{gold_path}'
""")

# COMMAND ----------

# 📝 Log metadata execution (optional)
# You may integrate this job_id and job_exec_id with metadata_log tracking table if needed

