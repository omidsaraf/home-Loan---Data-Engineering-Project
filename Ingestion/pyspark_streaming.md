
### **Project Structure for `pyspark_streaming/`**

```plaintext
src/
└── ingestion/
    ├── pyspark_streaming/
        ├── kafka_consumer.py         # PySpark Kafka consumer logic
        ├── stream_processor.py       # PySpark stream data processing
        ├── stream_writer.py          # Write stream data to storage or databases
        ├── metadata_tracking.py      # Metadata tracking for Spark streaming
        ├── config.py                # Configuration for Kafka and Spark
        ├── requirements.txt         # Python dependencies
        └── README.md                # Documentation for PySpark streaming module
```

---

### **1. `kafka_consumer.py`** – **PySpark Kafka Consumer Logic**

This script is responsible for connecting to **Kafka** and reading real-time data from a Kafka topic. It sets up the **Spark Structured Streaming** to consume data.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
import json

def create_spark_session():
    spark = SparkSession.builder \
        .appName("KafkaStreamConsumer") \
        .getOrCreate()
    return spark

def consume_kafka_stream(spark, kafka_bootstrap_servers, topic_name):
    """
    Consume data from a Kafka topic in real-time using Spark Structured Streaming.
    """
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", topic_name) \
        .load()

    # Parse the value from the Kafka message
    parsed_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
                  .withColumn("timestamp", expr("current_timestamp()"))

    return parsed_df

if __name__ == "__main__":
    spark = create_spark_session()
    kafka_bootstrap_servers = "<kafka_broker>"
    topic_name = "<topic_name>"
    
    df = consume_kafka_stream(spark, kafka_bootstrap_servers, topic_name)
    df.printSchema()
    # Further processing and streaming to next stage (processing/writing) can be done
```

---

### **2. `stream_processor.py`** – **PySpark Stream Data Processing**

This file processes the incoming Kafka stream data, performing necessary transformations such as filtering, aggregating, or enriching data.

```python
from pyspark.sql import functions as F

def process_stream(df):
    """
    Process incoming stream data, e.g., filtering, aggregation, and transformation.
    """
    # Example: Split the JSON data into columns (assuming JSON format)
    processed_df = df.select(F.from_json(F.col("value"), "start_date STRING, end_date STRING").alias("data")) \
                     .select("data.*") \
                     .filter(F.col("start_date").isNotNull())
                     
    return processed_df
```

---

### **3. `stream_writer.py`** – **Write Stream Data to Storage/Databases**

This file will define the logic to **write the processed streaming data** either into a **storage location** (like **Azure Blob Storage** or **Azure Data Lake**), or into a **database** like **Azure SQL** or **Databricks Delta tables**.

```python
def write_to_parquet(df, output_path):
    """
    Write the processed stream data to Parquet format for storage.
    """
    df.writeStream \
      .outputMode("append") \
      .format("parquet") \
      .option("path", output_path) \
      .option("checkpointLocation", "/mnt/checkpoints/loan_applications") \
      .start()

def write_to_sql(df, jdbc_url, table_name, connection_properties):
    """
    Write the processed stream data to Azure SQL.
    """
    df.writeStream \
      .foreachBatch(lambda batch_df, batch_id: batch_df.write.jdbc(
          url=jdbc_url,
          table=table_name,
          mode="append",
          properties=connection_properties)) \
      .start()
```

---

### **4. `metadata_tracking.py`** – **Metadata Tracking for Spark Streaming**

To enable **real-time tracking** of stream jobs, you need to track **batch IDs**, **status**, and **timestamps** in your **metadata database**.

```python
from pyspark.sql.functions import current_timestamp
import pyodbc

def update_metadata(batch_df, batch_id, jdbc_url, metadata_table, connection_properties):
    """
    Update metadata tracking for each batch processed in the stream.
    """
    batch_df = batch_df.withColumn("batch_id", batch_id) \
                       .withColumn("timestamp", current_timestamp())

    try:
        batch_df.write.jdbc(url=jdbc_url, table=metadata_table, mode="append", properties=connection_properties)
    except Exception as e:
        print(f"Error writing batch {batch_id} to metadata table: {e}")
```

---

### **5. `config.py`** – **Configuration for Kafka and Spark**

This file stores the necessary **configuration details** for the **Kafka** stream and the **Spark settings**.

```python
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = "your_kafka_broker:9092"
KAFKA_TOPIC = "loan_applications"

# Spark Configuration (can be expanded for more settings)
SPARK_MASTER = "spark://<master_url>"
SPARK_APP_NAME = "LoanApplicationStream"
```

---

### **6. `requirements.txt`** – **Python Dependencies**

This file lists the required Python libraries for **PySpark** and **Kafka** integration.

```
pyspark==3.2.0
pyodbc==4.0.32
kafka-python==2.0.2
```

---

### **7. `README.md`** – **Documentation for PySpark Streaming**

This document provides an overview of how to use the **PySpark Streaming** module for real-time data ingestion from Kafka.

````markdown
# PySpark Streaming Ingestion

This module is designed to handle real-time data ingestion from Kafka using **PySpark Structured Streaming**. The data is processed and can be written to Azure storage or Azure SQL.

## Folder Structure

- `kafka_consumer.py`: Connects to Kafka and consumes messages from a topic.
- `stream_processor.py`: Processes the incoming Kafka stream data.
- `stream_writer.py`: Writes the processed data to storage or a database.
- `metadata_tracking.py`: Tracks the streaming job's metadata.
- `config.py`: Contains configurations for Kafka and Spark.
- `requirements.txt`: Lists the dependencies for the PySpark Streaming jobs.

## Running the PySpark Streaming Jobs

1. Ensure Kafka is running and is accessible from the Spark cluster.
2. Configure your **Kafka** and **Azure SQL** settings in `config.py`.
3. Run the streaming process with:

```bash
python kafka_consumer.py
````

This will start consuming the data from Kafka and process the stream.

## Real-Time Data Pipeline

1. **Consume data** from Kafka.
2. **Process data** (e.g., filtering, transforming).
3. **Write processed data** to Azure Blob Storage or Azure SQL.
4. **Track metadata** for each stream batch.

## Requirements

* PySpark 3.2.0+
* Kafka server running and accessible
* Azure SQL Database or Azure Blob Storage


---

### **How the Ingestion Process Works**

1. **Kafka Consumer**: The `kafka_consumer.py` connects to Kafka and continuously pulls messages from a specified topic. It uses **Spark Structured Streaming** to handle real-time ingestion.
   
2. **Stream Processing**: The `stream_processor.py` takes care of transforming the stream, such as parsing the Kafka messages and applying any necessary transformations or filters.

3. **Data Writer**: The `stream_writer.py` handles writing the data to either **Azure SQL** or **Parquet files** in Azure Blob Storage, depending on your storage preferences.

4. **Metadata Tracking**: Every micro-batch processed by Spark is logged in the `metadata_tracking.py` using **metadata tables** in your **Azure SQL** database.

---

