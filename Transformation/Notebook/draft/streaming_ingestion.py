# streaming_ingestion.py

from pyspark.sql.functions import col, current_timestamp
from utils import get_jdbc_properties, read_metadata_params, write_log_to_metadata, safe_execute
from pyspark.sql.streaming import StreamingQueryListener
import datetime

dbutils.widgets.text("process_id", "2")
process_id = int(dbutils.widgets.get("process_id"))

jdbc_url = "<jdbc-url>"
jdbc_user = "<jdbc-user>"
jdbc_password = "<jdbc-password>"
jdbc_props = get_jdbc_properties(jdbc_user, jdbc_password)

log_table = "Metadata_Logs"

@safe_execute
def run_streaming_ingestion():
    params = read_metadata_params(spark, jdbc_url, jdbc_props, process_id)

    kafka_bootstrap = params.get("kafka_bootstrap_servers")
    topic = params.get("kafka_topic")
    checkpoint_location = params.get("checkpoint_location")
    output_path = params.get("output_path")
    partition_col = params.get("partition_column", "application_date")

    if not kafka_bootstrap or not topic or not checkpoint_location or not output_path:
        raise ValueError("kafka_bootstrap_servers, kafka_topic, checkpoint_location, output_path must be set")

    start_time = datetime.datetime.now()

    stream_df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap) \
        .option("subscribe", topic) \
        .option("startingOffsets", "latest") \
        .load()

    # Convert key and value from binary to string and add ingestion time
    processed_df = stream_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
        .withColumn("ingestion_time", current_timestamp())

    # Write stream to delta table partitioned by partition_col
    query = processed_df.writeStream.format("delta") \
        .option("checkpointLocation", checkpoint_location) \
        .partitionBy(partition_col) \
        .outputMode("append") \
        .start(output_path)

    # Register a listener to log query start and termination events
    class LogStreamingListener(StreamingQueryListener):
        def onQueryStarted(self, event):
            log_dict = {
                "metadata_type": "Streaming_Ingestion",
                "metadata_id": process_id,
                "action": "START",
                "previous_value": None,
                "new_value": f"Stream started with id {event.id}",
                "updated_by": "streaming_ingestion_notebook",
                "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            write_log_to_metadata(spark, jdbc_url, jdbc_props, log_table, log_dict)

        def onQueryTerminated(self, event):
            log_dict = {
                "metadata_type": "Streaming_Ingestion",
                "metadata_id": process_id,
                "action": "TERMINATE",
                "previous_value": None,
                "new_value": f"Stream terminated with id {event.id}",
                "updated_by": "streaming_ingestion_notebook",
                "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            write_log_to_metadata(spark, jdbc_url, jdbc_props, log_table, log_dict)

        def onQueryProgress(self, event):
            # Optionally log progress metrics here
            pass

    spark.streams.addListener(LogStreamingListener())

    query.awaitTermination()

run_streaming_ingestion()
