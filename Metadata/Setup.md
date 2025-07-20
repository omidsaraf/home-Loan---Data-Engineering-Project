
### **1. Create Azure SQL Database**

Before you can implement the metadata tables, you need to create an **Azure SQL Database** that ADF will interact with.

#### Steps:

1. **Log in to Azure Portal**.
2. **Navigate to the SQL Database** service.
3. Create a **new SQL Database**:

   * Define the resource group.
   * Choose a name for the database (e.g., `homeLoanMetadataDB`).
   * Select the appropriate **pricing tier** for your requirements.
4. Once created, go to the **Connection strings** section to get the details for connecting ADF to the database.

### **2. Create Metadata Tables in Azure SQL**

Once you have your **Azure SQL Database**, you will need to create tables that store the metadata information such as **ADF metadata, Airflow metadata, Batch metadata, Job metadata**, and others.

#### Example of Creating Metadata Tables

You can use **SQL Scripts** to create the metadata tables. Below are the SQL scripts for each table.

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

-- 2. Airflow DAG Metadata Table
CREATE TABLE Airflow_DAG_Metadata (
    dag_id INT PRIMARY KEY IDENTITY(1,1),
    dag_name NVARCHAR(255),
    job_id INT,
    task_id NVARCHAR(255),
    task_dependencies NVARCHAR(MAX),
    execution_time DATETIME,
    task_type NVARCHAR(50),
    FOREIGN KEY (job_id) REFERENCES Job_Metadata(job_id)
);

-- 3. Batch Metadata Table
CREATE TABLE Batch_Metadata (
    batch_id INT PRIMARY KEY IDENTITY(1,1),
    job_id INT,
    batch_schedule NVARCHAR(50),
    batch_start_time DATETIME,
    batch_end_time DATETIME,
    status NVARCHAR(50),
    FOREIGN KEY (job_id) REFERENCES Job_Metadata(job_id)
);

-- 4. Job Metadata Table
CREATE TABLE Job_Metadata (
    job_id INT PRIMARY KEY IDENTITY(1,1),
    job_name NVARCHAR(255),
    job_type NVARCHAR(50),
    frequency NVARCHAR(50),
    status NVARCHAR(50),
    start_time DATETIME,
    end_time DATETIME
);

-- 5. Process Metadata Table
CREATE TABLE Process_Metadata (
    proc_id INT PRIMARY KEY IDENTITY(1,1),
    proc_name NVARCHAR(255),
    job_id INT,
    proc_type NVARCHAR(50),
    input_source NVARCHAR(255),
    output_target NVARCHAR(255),
    FOREIGN KEY (job_id) REFERENCES Job_Metadata(job_id)
);

-- 6. Process Parameter Metadata Table
CREATE TABLE Process_Parameter_Metadata (
    param_id INT PRIMARY KEY IDENTITY(1,1),
    proc_id INT,
    param_name NVARCHAR(100),
    param_value NVARCHAR(255),
    param_description NVARCHAR(255),
    FOREIGN KEY (proc_id) REFERENCES Process_Metadata(proc_id)
);
```

### **3. Configure ADF to Interact with the Metadata Database**

Now, to interact with these tables in **Azure SQL Database** from **Azure Data Factory (ADF)**, you'll need to:

#### Step 1: Create Linked Services in ADF

* **Linked Service** connects ADF to the **Azure SQL Database**. You'll need to create a linked service for **Azure SQL Database**.

##### Steps:

1. In **ADF**, go to the **Author** tab.
2. Click on **Connections** and then **New Linked Service**.
3. Choose **Azure SQL Database**.
4. Provide the connection details (server name, database name, username, password) for your **SQL Database**.

#### Step 2: Use **Copy Data** or **Stored Procedure** Activity in ADF

Once the Linked Service is created, you can use ADF to perform **Copy Data** or **Execute Stored Procedure** activities to interact with the metadata.

##### Example: Copy Data Activity

1. **Create a Pipeline** in ADF.
2. Add a **Copy Data** activity:

   * Set the **Source** dataset as **SQL Server**.
   * Set the **Destination** dataset as **SQL Server** (or another destination).
   * For metadata processing, you would map the required tables in the SQL Database as **source** and **destination** datasets in your pipeline.

```json
{
  "name": "Copy_ADF_Metadata",
  "type": "Copy",
  "inputs": [
    {
      "referenceName": "ADF_Metadata_Input",
      "type": "DatasetReference"
    }
  ],
  "outputs": [
    {
      "referenceName": "ADF_Metadata_Output",
      "type": "DatasetReference"
    }
  ]
}
```

##### Example: Stored Procedure Activity

You can execute a stored procedure in the **SQL Database** to insert metadata or perform other actions. Below is an example of how to create a stored procedure to insert metadata:

```sql
-- Stored Procedure to Insert Metadata
CREATE PROCEDURE InsertADFMetadata
    @pipeline_name NVARCHAR(255),
    @source_system NVARCHAR(100),
    @frequency NVARCHAR(50),
    @start_time DATETIME,
    @end_time DATETIME,
    @status NVARCHAR(50),
    @last_run_status NVARCHAR(50),
    @parameters NVARCHAR(MAX)
AS
BEGIN
    INSERT INTO ADF_Metadata (pipeline_name, source_system, frequency, start_time, end_time, status, last_run_status, parameters)
    VALUES (@pipeline_name, @source_system, @frequency, @start_time, @end_time, @status, @last_run_status, @parameters);
END
```

Now, in **ADF**:

1. Add an **Execute Stored Procedure** activity.
2. Link it to your **Azure SQL Database** linked service.
3. Specify the **Stored Procedure** name (`InsertADFMetadata`), and pass in the metadata values as **parameters** to insert records into the **ADF\_Metadata** table.

---

### **4. Manage Metadata Using ADF Pipelines**

* **Scheduled Metadata Insertion:** Set up ADF to automatically collect and insert metadata into the SQL Database after each pipeline run. This ensures the metadata is always up to date.
* **Dynamic Metadata Processing:** Use **variables** and **parameterization** in ADF pipelines to dynamically populate metadata values.

#### Example of Dynamic Metadata Processing in ADF

```json
{
  "name": "Dynamic_Metadata_Insert",
  "type": "ExecutePipeline",
  "linkedServiceName": {
    "referenceName": "AzureSQLDBLinkedService",
    "type": "LinkedServiceReference"
  },
  "parameters": {
    "pipeline_name": "@pipeline().Name",
    "source_system": "Salesforce",
    "start_time": "@utcnow()",
    "end_time": "@utcnow()",
    "status": "Succeeded",
    "last_run_status": "Completed",
    "parameters": "{...}"
  }
}
```

In the above example, ADF dynamically collects metadata parameters such as **pipeline name**, **source system**, **start time**, **end time**, and others, and inserts them into the **ADF\_Metadata** table after the pipeline run.

---

### **5. Monitoring Metadata in ADF**

For monitoring and logging purposes, ADF provides options to capture **activity run logs** and **pipeline run logs**. You can set up logging to track metadata updates and store them in a **Log** table within the same SQL Database.

**Example Log Table:**

```sql
CREATE TABLE ADF_Run_Log (
    run_id INT PRIMARY KEY IDENTITY(1,1),
    pipeline_id INT,
    start_time DATETIME,
    end_time DATETIME,
    status NVARCHAR(50),
    error_message NVARCHAR(MAX),
    FOREIGN KEY (pipeline_id) REFERENCES ADF_Metadata(pipeline_id)
);
```

---

### **6. Automation & Scaling**

Finally, once the metadata is implemented in **Azure SQL Database**, you can leverage **ADF triggers** and **monitoring** to automatically process and maintain the metadata, ensuring data quality, traceability, and governance.

* **Triggering Pipelines:** Use ADF triggers (e.g., schedule-based or event-based) to execute pipeline runs and collect metadata.
* **Scaling:** Ensure that ADF activities are optimized for performance. You can set up multiple ADF triggers to handle multiple workloads.

---
