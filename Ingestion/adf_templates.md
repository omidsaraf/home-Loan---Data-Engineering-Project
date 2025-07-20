
#### **1. ADF Template Structure**

Here's a simplified directory structure for the **`adf_templates/`** folder:

```plaintext
adf_templates/
├── batch_ingestion/
│   ├── loan_applications_pipeline.json
│   ├── loan_approvals_pipeline.json
│   └── loan_defaults_pipeline.json
└── streaming_ingestion/
    ├── loan_application_stream_pipeline.json
    ├── loan_approval_stream_pipeline.json
    └── loan_default_stream_pipeline.json
```

* **Batch Ingestion**: Pipelines that ingest batch data from various sources like Azure Blob Storage, SQL Server, or external systems (via REST API).
* **Streaming Ingestion**: Pipelines designed for continuous ingestion, especially from streaming services like **Kafka** or **Event Hubs**.

---

### **2. Batch Ingestion ADF Template Example**

#### **Loan Applications Pipeline (Batch)**

This pipeline will fetch loan applications data from an Azure Blob Storage (or another data source) on a scheduled basis and load it into the raw layer (Bronze layer) in **Delta Lake**.

#### `loan_applications_pipeline.json`

```json
{
    "name": "loan_applications_pipeline",
    "properties": {
        "activities": [
            {
                "name": "Copy_Loan_Applications_Data",
                "type": "Copy",
                "inputs": [
                    {
                        "referenceName": "BlobSource",
                        "type": "DatasetReference"
                    }
                ],
                "outputs": [
                    {
                        "referenceName": "Bronze_Loan_Applications",
                        "type": "DatasetReference"
                    }
                ],
                "typeProperties": {
                    "source": {
                        "type": "AzureBlobStorage",
                        "blobSource": {
                            "type": "DelimitedText",
                            "delimiter": ","
                        }
                    },
                    "sink": {
                        "type": "AzureBlobStorage",
                        "azureBlobStorageSink": {
                            "type": "DeltaLake"
                        }
                    }
                }
            }
        ],
        "description": "Pipeline to ingest loan applications data into Delta Lake for further processing.",
        "annotations": []
    }
}
```

This **ADF JSON template** defines a **Copy activity** that pulls data from **Azure Blob Storage** (or other batch sources) and stores it in a **Delta Lake** for raw processing (Bronze layer).

##### **Explanation:**

* **BlobSource**: Defines the source dataset that points to the raw files (CSV/JSON/Parquet) in Azure Blob Storage.
* **Bronze\_Loan\_Applications**: Defines the destination where the data will be ingested. This is the **Bronze layer** (raw layer) in Delta Lake, which is partitioned and stored for further processing.

---

#### **Loan Approvals Pipeline (Batch)**

This template is similar to the Loan Applications pipeline but for loan approvals data.

#### `loan_approvals_pipeline.json`

```json
{
    "name": "loan_approvals_pipeline",
    "properties": {
        "activities": [
            {
                "name": "Copy_Loan_Approvals_Data",
                "type": "Copy",
                "inputs": [
                    {
                        "referenceName": "SQLSource_Loan_Approvals",
                        "type": "DatasetReference"
                    }
                ],
                "outputs": [
                    {
                        "referenceName": "Bronze_Loan_Approvals",
                        "type": "DatasetReference"
                    }
                ],
                "typeProperties": {
                    "source": {
                        "type": "AzureSqlDatabase",
                        "sqlSource": {
                            "type": "SqlQuery",
                            "query": "SELECT * FROM LoanApprovals WHERE CreatedAt > @LastRunTime"
                        }
                    },
                    "sink": {
                        "type": "AzureBlobStorage",
                        "azureBlobStorageSink": {
                            "type": "DeltaLake"
                        }
                    }
                }
            }
        ],
        "description": "Pipeline to ingest loan approvals data from SQL Database into Delta Lake for further processing.",
        "annotations": []
    }
}
```

* **SQLSource\_Loan\_Approvals**: This dataset fetches data from the **SQL Database** (e.g., Azure SQL Database) using an SQL query.
* **Bronze\_Loan\_Approvals**: Destination in the **Bronze layer** of Delta Lake.

---

### **3. Streaming Ingestion ADF Template Example**

#### **Loan Application Stream Pipeline (Streaming)**

For the **streaming ingestion**, we will use **Azure Event Hubs** as an example of the source. The pipeline will ingest loan application events and load them into the **Bronze layer** for streaming processing.

#### `loan_application_stream_pipeline.json`

```json
{
    "name": "loan_application_stream_pipeline",
    "properties": {
        "activities": [
            {
                "name": "Stream_Loan_Applications_Data",
                "type": "AzureStream",
                "inputs": [
                    {
                        "referenceName": "EventHubSource_Loan_Applications",
                        "type": "DatasetReference"
                    }
                ],
                "outputs": [
                    {
                        "referenceName": "Bronze_Loan_Applications_Stream",
                        "type": "DatasetReference"
                    }
                ],
                "typeProperties": {
                    "source": {
                        "type": "AzureEventHub",
                        "eventHubSource": {
                            "connectionString": "your_eventhub_connection_string",
                            "eventHubName": "loanApplications"
                        }
                    },
                    "sink": {
                        "type": "AzureBlobStorage",
                        "azureBlobStorageSink": {
                            "type": "DeltaLake"
                        }
                    }
                }
            }
        ],
        "description": "Pipeline to ingest streaming loan applications data from Event Hubs into Delta Lake for real-time processing.",
        "annotations": []
    }
}
```

* **EventHubSource\_Loan\_Applications**: Dataset to connect to **Azure Event Hubs**, where loan application events are streamed.
* **Bronze\_Loan\_Applications\_Stream**: Destination in **Delta Lake** (Bronze layer) where the streaming data is ingested.

---

### **4. ADF Metadata Integration**

You will need to manage metadata associated with these batch and streaming ingestion jobs, such as job names, start times, durations, statuses, and error messages.

#### Metadata Integration Workflow:

1. **Tracking ADF Metadata**: For each job, including batch and streaming, store metadata in an **Azure SQL Database** or **Azure Data Lake**.
2. **Job Tracking**: Track the completion status (success/failure) of the ADF pipelines.
3. **Error Handling**: Log error messages in case of failures, along with the reason for failure.

### Example of **Job Metadata Insertion** (for Batch)

```python
import pyodbc
from datetime import datetime

# Azure SQL Database connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=yourserver.database.windows.net;DATABASE=yourdb;UID=youruser;PWD=yourpassword')
cursor = conn.cursor()

# Insert job metadata into the database (ADF Batch job)
job_metadata_query = """
INSERT INTO Job_Metadata (job_name, status, start_time, end_time, duration, error_message)
VALUES (?, ?, ?, ?, ?, ?)
"""
params = (
    'Loan_Approval_Evaluation',
    'Completed',
    datetime(2023, 8, 1, 0, 0, 0),
    datetime(2023, 8, 1, 0, 45, 0),
    '45 minutes',
    ''
)

cursor.execute(job_metadata_query, params)
conn.commit()
cursor.close()
conn.close()
```

This will store the metadata of the **Loan\_Approval\_Evaluation** batch job into the **Job\_Metadata** table in Azure SQL Database, including the status, start time, end time, duration, and any errors that occurred.

---
