
### Steps for Integrating Airflow and Azure SQL for Metadata

---

### **1. Set Up Airflow Environment**

1. **Install Airflow with Azure SQL dependencies**:

   * Install Airflow with the necessary Azure SQL connectors and operators.

   ```bash
   pip install apache-airflow[azure]
   pip install apache-airflow-providers-microsoft-azure
   ```

2. **Configure Airflow Connections**:

   * In the **Airflow UI**, navigate to **Admin > Connections**.
   * Create a **new connection** for **Azure SQL**:

     * **Connection Type**: `Microsoft SQL Server`
     * **Host**: Your Azure SQL Server name
     * **Schema**: Your Database name (e.g., `homeLoanMetadataDB`)
     * **Login**: SQL Server user
     * **Password**: Password
     * **Port**: `1433`
     * **Extra**: `{}`

---

### **2. Create Metadata Tables in Azure SQL**

Ensure you already have the required **metadata tables** in **Azure SQL** as shown in previous steps:

```sql
-- 1. ADF Metadata Table
CREATE TABLE ADF_Metadata (
    pipeline_id INT PRIMARY KEY IDENTITY(1,1),
    pipeline_name NVARCHAR(255),
    source_system NVARCHAR(100),
    frequency NVARCHAR(50),
    start_time DATETIME,
    end_time DATETIME,
    status NVARCHAR(50),
    last_run_status NVARCHAR(50),
    parameters NVARCHAR(MAX)
);
.................
-- Continue creating other tables for Airflow DAG Metadata, Batch, Process, and Process Parameter...
```

---

### **3. Airflow DAG Integration with Azure SQL Database**

#### 3.1 **Example Airflow DAG for Metadata Integration**

The **Airflow DAG** will:

* Trigger jobs and processes.
* Log metadata into **Azure SQL** after each job's execution.
* Update job status (e.g., `Started`, `Completed`, `Failed`).

Here’s how you can create an Airflow DAG that interacts with the **Azure SQL Database** metadata tables.

#### Example DAG to Track Job Execution

```python
from airflow import DAG
from airflow.providers.microsoft.azure.transfers.sql_to_sql import SqlToSqlOperator
from airflow.providers.microsoft.azure.hooks.sql import AzureSQLHook
from airflow.utils.dates import days_ago
from datetime import datetime

# Set the default_args
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
}

# Define the DAG
with DAG(
    'metadata_airflow_sql_integration',
    default_args=default_args,
    description='DAG to Integrate Airflow with Azure SQL for Metadata Logging',
    schedule_interval=None,  # You can change this to schedule as needed
    catchup=False,
) as dag:

    # Task: Insert Job Metadata into SQL Database (Azure SQL)
    def insert_job_metadata():
        # Create a hook to connect to Azure SQL
        azure_sql_hook = AzureSQLHook(conn_id="azure_sql_conn")

        # Insert metadata for a Job into the Job_Metadata table
        job_insert_query = """
            INSERT INTO Job_Metadata (job_name, job_type, frequency, status, start_time, end_time)
            VALUES ('HomeLoan Data Ingestion', 'Batch', 'Daily', 'Started', @start_time, @end_time)
        """
        
        # Use the hook to execute the SQL
        azure_sql_hook.run(sql=job_insert_query, parameters={'start_time': datetime.now(), 'end_time': datetime.now()})

    # Task to insert metadata into SQL
    insert_metadata_task = PythonOperator(
        task_id='insert_job_metadata',
        python_callable=insert_job_metadata,
        dag=dag,
    )

    # Further tasks can be added here based on different steps in your DAG

    insert_metadata_task  # This task will run first in your DAG
```

#### Key Steps:

1. **AzureSQLHook**: This hook is used to connect to **Azure SQL** from Airflow.
2. **SQL Query**: We use an `INSERT` SQL query to add **job metadata** like the job name, type, frequency, status, start time, and end time.
3. **Parameters**: Pass **parameters** like the current timestamp to be inserted into the metadata table.
4. **PythonOperator**: The `PythonOperator` allows us to define a custom function (`insert_job_metadata`) that inserts the metadata.

---

#### 3.2 **Airflow Task Dependencies**

For more complex workflows, you can set task dependencies between Airflow tasks, including metadata updates after each task's completion.

```python
# Define the task for executing a job
execute_batch_job_task = BashOperator(
    task_id='execute_batch_job',
    bash_command='python /path/to/your/script.py',
    dag=dag,
)

# Define the task for updating the job metadata in SQL
update_metadata_task = PythonOperator(
    task_id='update_job_metadata',
    python_callable=update_job_metadata,
    dag=dag,
)

# Set dependencies (Job execution followed by metadata update)
execute_batch_job_task >> update_metadata_task
```

In this setup, after the **`execute_batch_job_task`** finishes, the **`update_metadata_task`** is executed to log the status and other metadata about the batch job.

---

### **4. Airflow Integration with ADF**

If your **Airflow DAG** orchestrates ADF pipelines, you can use the **Azure Data Factory Operator** in Airflow to trigger ADF pipelines.

#### 4.1 **Example of Triggering ADF Pipeline from Airflow**

```python
from airflow.providers.microsoft.azure.operators.data_factory import AzureDataFactoryRunPipelineOperator

# Define the task for triggering ADF pipeline
trigger_adf_pipeline = AzureDataFactoryRunPipelineOperator(
    task_id='trigger_adf_pipeline',
    pipeline_name='HomeLoanPipeline',
    parameters={"param1": "value1", "param2": "value2"},
    azure_data_factory_conn_id='azure_sql_conn',
    resource_group_name='your_resource_group',
    factory_name='your_data_factory',
    dag=dag,
)

trigger_adf_pipeline  # This will trigger the ADF pipeline
```

Once the ADF pipeline completes, you can log metadata to Azure SQL using the same approach as described in the previous section.

---

### **5. Logging and Monitoring of Metadata**

You can also integrate **logging** to ensure that any changes to the metadata are recorded. This includes capturing the execution status and timestamps for all Airflow tasks and their corresponding metadata entries.

#### Example: Adding Log Table for Metadata in Azure SQL

```sql
CREATE TABLE Airflow_Metadata_Log (
    log_id INT PRIMARY KEY IDENTITY(1,1),
    job_id INT,
    task_id NVARCHAR(255),
    status NVARCHAR(50),
    start_time DATETIME,
    end_time DATETIME,
    execution_time DATETIME,
    FOREIGN KEY (job_id) REFERENCES Job_Metadata(job_id)
);
```

You can then insert log records every time an Airflow task runs, and track execution time, status, and other relevant metadata.

---

### **6. Conclusion**

By integrating **Airflow** with **Azure SQL Database** for managing metadata, we can:

* **Automate metadata logging** as part of the job execution pipeline.
* **Track the status and progress** of each job, process, and parameter.
* **Ensure full traceability** and **auditability** of your data pipeline through the metadata.
* **Monitor and troubleshoot** using Airflow's monitoring tools, with detailed logs stored in **Azure SQL**.

This ensures that **data quality**, **accuracy**, **security**, and **compliance** are maintained across the entire data pipeline lifecycle.
