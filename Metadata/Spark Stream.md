
### **Steps for Metadata Integration with Spark Streaming**

1. **Metadata Ingestion**: Each streaming job will have an associated **metadata ingestion process** that inserts relevant metadata into the Azure SQL database. This can include:

   * Task status updates (`status`)
   * Start and end times of streaming jobs
   * Error logs for troubleshooting

2. **Tracking Parameters**: Each Spark streaming process will use metadata tables like **Process\_Parameter\_Metadata** to track the parameters used in each job (e.g., batch size, topic names, model parameters).

3. **Job and Task Tracking**: Use the **Job\_Metadata** and **Task\_Metadata** tables to track the execution of jobs and their statuses, including whether they are running, completed, or failed.

4. **Change Tracking (Logs)**: Any change to the status or parameters of the processes will be recorded in the **Metadata\_Logs** table to allow for full auditability and traceability. This is crucial for ensuring transparency in your data pipeline and governance.

5. **SQL Integration**: After each **micro-batch** of data is processed in Spark, the status is updated in the **metadata** table to reflect the current state of the process.

---

### **Implementation Example in Spark Structured Streaming**:

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

#
```


Example Stream Ingestion (Kafka source, can be any source)
stream\_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "<server>").option("subscribe", "<topic>").load()

# Transform the streaming data

processed\_df = stream\_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")&#x20;
.withColumn("timestamp", current\_timestamp())  # Add timestamp for tracking

# Function to update metadata in Azure SQL

def update\_metadata(batch\_df, batch\_id):
try:
batch\_df.withColumn("batch\_id", col("timestamp"))&#x20;
.write.jdbc(url=jdbc\_url, table=metadata\_table, mode="append", properties=connection\_properties)
except Exception as e:
print(f"Error writing batch {batch\_id} to metadata table: {e}")

# Use foreachBatch to update metadata after each micro-batch

query = processed\_df.writeStream.foreachBatch(update\_metadata).start()
query.awaitTermination()

```

