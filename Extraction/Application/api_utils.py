from pyspark.sql import SparkSession

def get_spark_session():
    return SparkSession.builder \
        .appName("HomeLoanIQ API") \
        .getOrCreate()

def load_delta_table(spark, table_path):
    return spark.read.format("delta").load(table_path)
