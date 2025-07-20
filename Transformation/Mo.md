Absolutely! Here’s a **full set of parameterized PySpark notebook templates** for your HomeLoanIQ project’s dataflow pipelines — all following best practices with metadata-driven parameters from your metadata tables (like `Process_Parameter_Metadata`), designed to run on Databricks notebooks.

---

# 📝 **All Notebooks for HomeLoanIQ Dataflow Pipelines**

---

## 1. **Ingestion Batch Notebook: `batch_ingestion.py`**

```python
# batch_ingestion.py

from pyspark.sql.functions import current_timestamp

def get_process_parameters(spark, jdbc_url, jdbc_props, process_id):
    query = f"(SELECT param_name, param_value FROM Process_Parameter_Metadata WHERE process_id = {process_id}) AS params"
    df_params = spark.read.jdbc(url=jdbc_url, table=query, properties=jdbc_props)
    return {row['param_name']: row['param_value'] for row in df_params.collect()}

# Setup JDBC connection info
jdbc_url = "<your-jdbc-url>"
jdbc_props = {
    "user": "<username>",
    "password": "<password>",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Get process_id param from notebook widget or default
dbutils.widgets.text("process_id", "1")
process_id = int(dbutils.widgets.get("process_id"))

params = get_process_parameters(spark, jdbc_url, jdbc_props, process_id)

input_path = params.get('input_path')
output_path = params.get('output_path')
write_mode = params.get('write_mode', 'append')

# Read raw batch data (CSV/JSON/parquet etc)
batch_df = spark.read.format(params.get('input_format', 'csv')) \
    .option("header", "true") \
    .load(input_path)

# Add ingestion metadata columns
batch_df = batch_df.withColumn("ingestion_time", current_timestamp())

# Write raw data to Bronze Delta table partitioned by application_date
batch_df.write.format("delta") \
    .mode(write_mode) \
    .partitionBy("application_date") \
    .save(output_path)
```

---

## 2. **Ingestion Streaming Notebook: `streaming_ingestion.py`**

```python
# streaming_ingestion.py

from pyspark.sql.functions import current_timestamp

def get_process_parameters(spark, jdbc_url, jdbc_props, process_id):
    query = f"(SELECT param_name, param_value FROM Process_Parameter_Metadata WHERE process_id = {process_id}) AS params"
    df_params = spark.read.jdbc(url=jdbc_url, table=query, properties=jdbc_props)
    return {row['param_name']: row['param_value'] for row in df_params.collect()}

jdbc_url = "<your-jdbc-url>"
jdbc_props = {
    "user": "<username>",
    "password": "<password>",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

dbutils.widgets.text("process_id", "2")
process_id = int(dbutils.widgets.get("process_id"))

params = get_process_parameters(spark, jdbc_url, jdbc_props, process_id)

kafka_bootstrap_servers = params.get('kafka_bootstrap_servers')
kafka_topic = params.get('kafka_topic')
output_path = params.get('output_path')
checkpoint_path = params.get('checkpoint_path')

stream_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

stream_df = stream_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .withColumn("ingestion_time", current_timestamp()) \
    .withColumn("application_date", current_timestamp().cast("date"))

query = stream_df.writeStream.format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", checkpoint_path) \
    .partitionBy("application_date") \
    .start(output_path)

query.awaitTermination()
```

---

## 3. **Transformation Bronze to Silver Notebook: `bronze_to_silver.py`**

```python
# bronze_to_silver.py

def get_process_parameters(spark, jdbc_url, jdbc_props, process_id):
    query = f"(SELECT param_name, param_value FROM Process_Parameter_Metadata WHERE process_id = {process_id}) AS params"
    df_params = spark.read.jdbc(url=jdbc_url, table=query, properties=jdbc_props)
    return {row['param_name']: row['param_value'] for row in df_params.collect()}

jdbc_url = "<your-jdbc-url>"
jdbc_props = {
    "user": "<username>",
    "password": "<password>",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

dbutils.widgets.text("process_id", "3")
process_id = int(dbutils.widgets.get("process_id"))

params = get_process_parameters(spark, jdbc_url, jdbc_props, process_id)

bronze_path = params.get('bronze_path')
silver_path = params.get('silver_path')
write_mode = params.get('write_mode', 'overwrite')

# Read raw data from bronze
bronze_df = spark.read.format("delta").load(bronze_path)

# Example transformations (data cleaning, type casting, filtering nulls)
silver_df = bronze_df.dropDuplicates() \
    .filter("application_date IS NOT NULL") \
    .withColumnRenamed("old_col_name", "new_col_name")  # example rename

# Write to silver
silver_df.write.format("delta") \
    .mode(write_mode) \
    .partitionBy("application_date") \
    .save(silver_path)
```

---

## 4. **Transformation Silver to Gold Notebook: `silver_to_gold.py`**

```python
# silver_to_gold.py

def get_process_parameters(spark, jdbc_url, jdbc_props, process_id):
    query = f"(SELECT param_name, param_value FROM Process_Parameter_Metadata WHERE process_id = {process_id}) AS params"
    df_params = spark.read.jdbc(url=jdbc_url, table=query, properties=jdbc_props)
    return {row['param_name']: row['param_value'] for row in df_params.collect()}

jdbc_url = "<your-jdbc-url>"
jdbc_props = {
    "user": "<username>",
    "password": "<password>",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

dbutils.widgets.text("process_id", "4")
process_id = int(dbutils.widgets.get("process_id"))

params = get_process_parameters(spark, jdbc_url, jdbc_props, process_id)

silver_path = params.get('silver_path')
gold_path = params.get('gold_path')
write_mode = params.get('write_mode', 'overwrite')

silver_df = spark.read.format("delta").load(silver_path)

# Example KPI calculation (e.g., daily application volume by branch)
from pyspark.sql.functions import count, col

gold_df = silver_df.groupBy("application_date", "branch_id") \
    .agg(count("loan_application_id").alias("daily_application_volume"))

gold_df.write.format("delta") \
    .mode(write_mode) \
    .partitionBy("application_date") \
    .save(gold_path)
```

---

## 5. **Extraction Notebook: `extract_for_dashboard.py`**

```python
# extract_for_dashboard.py

def get_process_parameters(spark, jdbc_url, jdbc_props, process_id):
    query = f"(SELECT param_name, param_value FROM Process_Parameter_Metadata WHERE process_id = {process_id}) AS params"
    df_params = spark.read.jdbc(url=jdbc_url, table=query, properties=jdbc_props)
    return {row['param_name']: row['param_value'] for row in df_params.collect()}

jdbc_url = "<your-jdbc-url>"
jdbc_props = {
    "user": "<username>",
    "password": "<password>",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

dbutils.widgets.text("process_id", "5")
process_id = int(dbutils.widgets.get("process_id"))

params = get_process_parameters(spark, jdbc_url, jdbc_props, process_id)

gold_path = params.get('gold_path')
dashboard_output_path = params.get('dashboard_output_path')

gold_df = spark.read.format("delta").load(gold_path)

# For example, filter last 30 days data for dashboard
from pyspark.sql.functions import current_date, date_sub

dashboard_df = gold_df.filter(col("application_date") >= date_sub(current_date(), 30))

dashboard_df.write.format("parquet") \
    .mode("overwrite") \
    .save(dashboard_output_path)
```

---

# Summary:

| Notebook Name              | Purpose                                      | Uses Metadata Parameter | Input Layer   | Output Layer    |
| -------------------------- | -------------------------------------------- | ----------------------- | ------------- | --------------- |
| `batch_ingestion.py`       | Batch data ingestion from landing zone       | Yes                     | Landing (raw) | Bronze (delta)  |
| `streaming_ingestion.py`   | Streaming ingestion from Kafka               | Yes                     | Kafka         | Bronze (delta)  |
| `bronze_to_silver.py`      | Clean and enrich raw data, dedupe, type cast | Yes                     | Bronze        | Silver          |
| `silver_to_gold.py`        | KPI aggregates and metrics                   | Yes                     | Silver        | Gold            |
| `extract_for_dashboard.py` | Extract gold data for BI dashboards          | Yes                     | Gold          | Dashboard-ready |

---

# How to use:

* Pass the **`process_id`** widget param when running the notebook to dynamically load the metadata parameters.
* Update the `Process_Parameter_Metadata` table to change source/target paths, batch sizes, topics, etc.
* Combine these notebooks into your ADF or Airflow pipelines or Databricks Jobs workflows.

---

If you want, I can help generate **full working notebooks** with logging, error handling, and reusable utility functions too! Would you like me to do that?
