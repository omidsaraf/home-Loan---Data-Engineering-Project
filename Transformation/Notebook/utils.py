# utils.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
import traceback

def get_jdbc_properties(user, password, driver="com.microsoft.sqlserver.jdbc.SQLServerDriver"):
    return {
        "user": user,
        "password": password,
        "driver": driver
    }

def read_metadata_params(spark: SparkSession, jdbc_url: str, jdbc_props: dict, process_id: int) -> dict:
    """
    Reads process parameters from Process_Parameter_Metadata table for given process_id.
    Returns dict param_name: param_value.
    """
    try:
        query = f"(SELECT param_name, param_value FROM Process_Parameter_Metadata WHERE process_id = {process_id}) AS params"
        df = spark.read.jdbc(url=jdbc_url, table=query, properties=jdbc_props)
        params = {row['param_name']: row['param_value'] for row in df.collect()}
        return params
    except Exception as e:
        print(f"ERROR reading metadata params for process_id {process_id}: {e}")
        raise

def write_log_to_metadata(spark: SparkSession, jdbc_url: str, jdbc_props: dict, log_table: str, log_dict: dict):
    """
    Append a log record to the Metadata_Logs table.
    """
    try:
        log_df = spark.createDataFrame([log_dict])
        log_df.write.jdbc(url=jdbc_url, table=log_table, mode="append", properties=jdbc_props)
    except Exception as e:
        print(f"ERROR writing log to {log_table}: {e}")

def safe_execute(func):
    """
    Decorator to wrap function calls in try-except with traceback.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Exception in {func.__name__}: {str(e)}")
            traceback.print_exc()
            raise
    return wrapper
