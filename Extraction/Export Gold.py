# Databricks notebook source
# MAGIC %md
# MAGIC ## 📤 Export Gold to Dashborad/External Layer
# MAGIC - Loads Gold table
# MAGIC - Flattens structure if needed
# MAGIC - Writes to external consumption zone
# MAGIC - Parametrized via metadata

# COMMAND ----------

from pyspark.sql.functions import current_timestamp
import uuid

# COMMAND ----------

# 📦 Metadata Parameters
dbutils.widgets.text("job_name", "homeloan_export_gold_to_tableau")
dbutils.widgets.text("job_id", str(uuid.uuid4()))
dbutils.widgets.text("job_exec_id", str(uuid.uuid4()))
dbutils.widgets.text("gold_table", "gold.homeloan_applications")
dbutils.widgets.text("export_table", "external.tableau_homeloan_applications")
dbutils.widgets.text("export_path", "/mnt/external/tableau/homeloan_applications/")
dbutils.widgets.text("partition_column", "application_date")

# COMMAND ----------

# 🧩 Read parameters
job_name = dbutils.widgets.get("job_name")
job_id = dbutils.widgets.get("job_id")
job_exec_id = dbutils.widgets.get("job_exec_id")
gold_table = dbutils.widgets.get("gold_table")
export_table = dbutils.widgets.get("export_table")
export_path = dbutils.widgets.get("export_path")
partition_column = dbutils.widgets.get("partition_column")

# COMMAND ----------

# 🔄 Read Gold Data
df_gold = spark.read.table(gold_table)

# Optional: Apply any transformations for BI optimization
df_export = df_gold.select(
    "application_id",
    "customer_name",
    "product_type",
    "loan_amount",
    "approval_status",
    "application_date",
    "source_type",
    "processed_at"
).withColumn("exported_at", current_timestamp())

# COMMAND ----------

# 💾 Write Export Data
df_export.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .partitionBy(partition_column) \
    .save(export_path)

# COMMAND ----------

# 📌 Register as External Table
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {export_table}
    USING DELTA
    LOCATION '{export_path}'
""")

# COMMAND ----------

# 🧾 Optional Metadata Logging (if integrated)
# Insert into METADATA_LOG for job_exec_id, status, etc.
