### **Steps for Metadata Integration with Spark Streaming in ADF and Azure SQL**

To effectively integrate **Spark Streaming** with **Azure Data Factory (ADF)** and **Azure SQL** for metadata tracking, follow these refined steps for better control and monitoring.

---

### **1. Metadata Ingestion Process**

Each streaming job has an associated **metadata ingestion process** that inserts relevant metadata into Azure SQL. This ensures all events related to data flows (both **batch** and **streaming**) are tracked for governance, auditing, and operational transparency.

#### Key metadata attributes:

* **Task status updates** (`status`)
* **Start and end times** of streaming jobs
* **Error logs** for troubleshooting

#### Example Metadata Entry:

* **Job Name**: Loan\_Application\_Stream\_Job
* **Job Type**: Streaming
* **Status**: Completed
* **Start Time**: `2023-08-01 00:00:00`
* **End Time**: `2023-08-01 01:00:00`
* **Error Message**: None

---

### **2. Tracking Parameters**

For every Spark Streaming process, metadata tables like `Process_Parameter_Metadata` are used to track the parameters passed to the job, like:

* **Batch Size**
* **Topic Names** (e.g., Kafka topic)
* **Model Parameters** (for machine learning pipelines)

#### Sample Tracking Metadata (Batch Job):

```sql
-- Sample entry for tracking parameters used in Spark Streaming job
INSERT INTO Process_Parameter_Metadata (job_id, parameter_name, parameter_value)
VALUES
(1, 'Kafka_Topic', 'loanApplications'),
(1, 'Kafka_Broker', 'your_kafka_broker'),
(1, 'Batch_Size', '1000');
```

---

### **3. Job and Task Tracking**

Track job execution and their statuses in **Job\_Metadata** and **Task\_Metadata** tables. This includes the real-time updates of job status, whether they are:

* **Running**
* **Completed**
* **Failed**

This enables auditability and real-time monitoring.

#### Sample Metadata for Task Tracking:

```sql
-- Sample entry in Job_Metadata for tracking streaming job status
INSERT INTO Job_Metadata (job_name, job_type, status, start_time, end_time, duration, error_message, streaming_source, micro_batch_id)
VALUES
('Loan_Application_Stream_Job', 'Streaming', 'Completed', '2023-08-01 00:00:00', '2023-08-01 01:00:00', '1 hour', NULL, 'Kafka', 'batch_12345');
```

---

### **4. Change Tracking (Logs)**

Changes to the status, parameters, or results of any process (including streaming micro-batches) will be recorded in the **Metadata\_Logs** table. This supports full auditability and traceability, which is essential for maintaining **data governance** and **compliance**.

#### Example of Logging Metadata Change:

```sql
-- Sample entry in Metadata_Logs for a status update
INSERT INTO Metadata_Logs (job_id, status, timestamp, log_message)
VALUES
(1, 'Started', '2023-08-01 00:00:00', 'Streaming job for loan applications started.');
```

---

### **5. SQL Integration**

After processing each **micro-batch** in Spark, the **metadata** table is updated with the current status of the job, which could be a **success** or **failure**. These updates are automatically logged at the **Azure SQL** database.

---

### **Implementation Example in Spark Structured Streaming**

Now, let’s move to the **implementation example** in Spark Structured Streaming, where we use **Spark Streaming** to process data from Kafka, and update the metadata table in **Azure SQL**:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp
import pyodbc

# Create a Spark session
spark = SparkSession.builder \
    .appName("SparkStreamWithMetadata") \
    .getOrCreate()

# Define JDBC connection for Azure SQL Database
jdbc_url = "jdbc:sqlserver://<server_name>.database.windows.net:1433;database=<database_name>"
connection_properties = {
    "user": "<username>",
    "password": "<password>",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Metadata tracking table
metadata_table = "<metadata_table>"

# Example of stream ingestion from Kafka
stream_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "<server>") \
    .option("subscribe", "<topic>") \
    .load()

# Transform the streaming data
processed_df = stream_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .withColumn("timestamp", current_timestamp())  # Add timestamp for tracking

# Function to update metadata in Azure SQL after each micro-batch
def update_metadata(batch_df, batch_id):
    try:
        batch_df.withColumn("batch_id", col("timestamp")) \
            .write.jdbc(url=jdbc_url, table=metadata_table, mode="append", properties=connection_properties)
    except Exception as e:
        print(f"Error writing batch {batch_id} to metadata table: {e}")

# Use foreachBatch to update metadata after each micro-batch
query = processed_df.writeStream.foreachBatch(update_metadata).start()
query.awaitTermination()
```

### Key Points:

1. **Kafka** is the stream source.
2. Each micro-batch has its **timestamp** added, along with a **batch\_id** for unique tracking.
3. Metadata is written to **Azure SQL Database** via JDBC after each batch of data is processed.

---

### **Additional Considerations for Metadata Logging with Spark Streaming in ADF**

1. **Streaming Source**: We track the source of streaming data (e.g., **Kafka**, **Event Hubs**) for better differentiation and issue resolution.

2. **Micro-batch ID**: For **Spark Streaming**, we track **micro-batch IDs** to trace each processed batch in detail.

3. **Error Handling**: We log any errors that occur during the streaming job and include retry attempts or failed batch IDs for detailed troubleshooting.

---

### **Integrate Spark Streaming with ADF**

1. **Create a Spark Job in Databricks**: Write your **Spark Streaming** logic in **Azure Databricks**.

2. **Trigger Spark Job from ADF**: In ADF, use the **Databricks Notebook activity** to trigger the Databricks job, which will handle the **Spark Streaming** ingestion.

3. **Track Job Metadata**: Once the **Spark Streaming job** is triggered from ADF, metadata such as the **job status**, **micro-batch ID**, and **streaming source** is logged in the Azure SQL database for auditing and tracking.

---

### **ADF Pipeline Example to Trigger Spark Streaming Job**

Here’s how to create an **ADF pipeline** that triggers **Spark Streaming** in **Azure Databricks**:

```json
{
    "name": "Loan_Application_Stream_Job_Pipeline",
    "properties": {
        "activities": [
            {
                "name": "Trigger_Spark_Streaming_Job",
                "type": "DatabricksNotebook",
                "linkedServiceName": {
                    "referenceName": "AzureDatabricksLinkedService",
                    "type": "LinkedServiceReference"
                },
                "typeProperties": {
                    "notebookPath": "/Shared/SparkStreamingNotebooks/LoanApplicationStream",
                    "baseParameters": {
                        "topicName": "loanApplications",
                        "kafkaBroker": "your_kafka_broker"
                    }
                }
            }
        ]
    }
}
```

This **ADF pipeline** will trigger a **Databricks notebook** containing the **Spark Streaming job**, ensuring the streaming data (loan applications) is processed in real-time, and the metadata is continuously logged.

---
