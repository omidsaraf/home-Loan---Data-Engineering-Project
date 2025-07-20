
#### **1. Ingest Batch Data (to Bronze Layer)**

**Notebook: `Ingest_Batch_Data_Bronze`**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp
from delta.tables import DeltaTable

# Initialize Spark session
spark = SparkSession.builder.appName("Ingest_Batch_Data_Bronze").getOrCreate()

# Define file paths using mounted paths
batch_input_path = "/mnt/your-container-name/raw-batch-data/"
bronze_output_path = "/mnt/your-container-name/bronze/loan_applications_batch/"

# Read batch data into a DataFrame
batch_df = spark.read.csv(batch_input_path, header=True, inferSchema=True)

# Add metadata (ingestion time)
batch_df = batch_df.withColumn("ingestion_time", current_timestamp())

# Write data to Bronze layer (Delta format)
batch_df.write.format("delta").mode("overwrite").save(bronze_output_path)
```

* **Explanation**: This notebook reads **batch data** from the mounted **`raw-batch-data`** path and writes it to the **`bronze/loan_applications_batch/`** path.

---

#### **2. Ingest Streaming Data (to Bronze Layer)**

**Notebook: `Ingest_Streaming_Data_Bronze`**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

# Initialize Spark session
spark = SparkSession.builder.appName("Ingest_Streaming_Data_Bronze").getOrCreate()

# Set Kafka parameters
kafka_bootstrap_servers = "your_kafka_broker:9092"
kafka_topic = "loan_applications"

# Read stream from Kafka
stream_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Convert Kafka value from binary to string and add metadata
stream_df = stream_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .withColumn("ingestion_time", current_timestamp())

# Write stream to Bronze layer (Delta format) with checkpointing
checkpoint_path = "/mnt/your-container-name/checkpoints/loan_applications_stream/"
stream_output_path = "/mnt/your-container-name/bronze/loan_applications_stream/"

stream_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", checkpoint_path) \
    .start(stream_output_path)
```

* **Explanation**: This notebook reads **streaming data** from **Kafka**, adds metadata, and writes it to the **Bronze Layer** in **Delta format** with checkpointing.

---

#### **3. Transform Data from Bronze to Silver Layer**

**Notebook: `Transform_Bronze_to_Silver`**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Initialize Spark session
spark = SparkSession.builder.appName("Transform_Bronze_to_Silver").getOrCreate()

# Define paths using mounted paths
bronze_input_path = "/mnt/your-container-name/bronze/loan_applications_batch/"
silver_output_path = "/mnt/your-container-name/silver/loan_applications/"

# Read the data from the Bronze layer
bronze_df = spark.read.format("delta").load(bronze_input_path)

# Apply data transformations: Clean, Enrich, and Filter data
silver_df = bronze_df.withColumn("loan_amount", col("loan_amount").cast("double")) \
    .withColumn("approved", when(col("loan_status") == "Approved", 1).otherwise(0)) \
    .filter(col("loan_amount") > 0)

# Write the transformed data into the Silver Layer
silver_df.write.format("delta").mode("overwrite").save(silver_output_path)
```

* **Explanation**: This notebook reads data from the **Bronze Layer**, applies transformations (like casting and filtering), and writes the results to the **Silver Layer**.

---

#### **4. Aggregate Data from Silver to Gold Layer**

**Notebook: `Aggregate_Silver_to_Gold`**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg

# Initialize Spark session
spark = SparkSession.builder.appName("Aggregate_Silver_to_Gold").getOrCreate()

# Define paths using mounted paths
silver_input_path = "/mnt/your-container-name/silver/loan_applications/"
gold_output_path = "/mnt/your-container-name/gold/loan_application_summary/"

# Read the Silver data
silver_df = spark.read.format("delta").load(silver_input_path)

# Aggregate data to generate KPIs (e.g., total loan amount, average loan amount)
gold_df = silver_df.groupBy("loan_type") \
    .agg(
        sum("loan_amount").alias("total_loan_amount"),
        avg("loan_amount").alias("average_loan_amount"),
        sum("approved").alias("approved_count")
    )

# Write the aggregated data to the Gold Layer
gold_df.write.format("delta").mode("overwrite").save(gold_output_path)
```

* **Explanation**: This notebook performs **data aggregation** (KPIs) on the **Silver Layer** and writes the results to the **Gold Layer**.

---

### **Orchestrating the Pipeline**

To automate the execution, you can schedule these notebooks to run in sequence using **Databricks Jobs** or an **Azure Data Factory (ADF) pipeline**:

1. **Databricks Jobs**: Create a job that runs these notebooks in sequence, passing necessary parameters (e.g., file paths, topic names).

2. **Azure Data Factory**: Create a pipeline in ADF that orchestrates the execution of these Databricks notebooks. ADF can trigger a Databricks notebook, passing required parameters such as file paths, topic names, and batch sizes.

---

### **Summary of Notebooks with Mounted Storage Paths:**

1. **`Ingest_Batch_Data_Bronze`** – Ingests batch data from the **mounted storage** into the **Bronze Layer**.
2. **`Ingest_Streaming_Data_Bronze`** – Ingests streaming data from **Kafka** into the **Bronze Layer**.
3. **`Transform_Bronze_to_Silver`** – Transforms and cleans data from **Bronze** to **Silver Layer**.
4. **`Aggregate_Silver_to_Gold`** – Aggregates data from **Silver** to **Gold Layer**.

These notebooks, using mounted storage paths, simplify the management of data in your **Bronze**, **Silver**, and **Gold** layers while ensuring you follow best practices in Databricks.
