1. **Ingestion Pipeline**:

   * Moves **batch** data from external sources into **Bronze layer** (i.e., landing zone).
   * Moves **stream** data (via Spark Streaming) into **Bronze layer**.
2. **Transformation Pipeline**:

   * Cleans and enriches **Bronze data** into **Silver** (i.e., processing and cleansing).
3. **Aggregation Pipeline**:

   * Aggregates **Silver** data into **Gold layer** (i.e., KPI metrics and business intelligence).

---

### **1. Ingestion Pipeline: Batch & Streaming Data**

#### **1.1. Batch Data Ingestion (Batch Pipeline)**

In this pipeline, we’ll move **batch data** (for example, Loan Applications, Disbursements) into the **Bronze layer**.

```json
{
  "name": "Loan_Application_Batch_Ingestion",
  "properties": {
    "activities": [
      {
        "name": "Copy_Loan_Application_Data_Batch",
        "type": "Copy",
        "inputs": [
          {
            "referenceName": "BlobStorageLinkedService",
            "type": "LinkedServiceReference"
          }
        ],
        "outputs": [
          {
            "referenceName": "Bronze_Loan_Applications_Batch",
            "type": "DatasetReference"
          }
        ],
        "typeProperties": {
          "source": {
            "type": "BlobSource",
            "blobPath": "azure_blob_path/loan_applications_batch/"
          },
          "sink": {
            "type": "AzureSqlSink",
            "tableName": "bronze.bronze_loan_applications_batch"
          }
        }
      }
    ]
  }
}
```

* **Step Description**:

  * **Source**: Data from Blob Storage or any external system.
  * **Sink**: Writes data into the **bronze** tables in **ADLS Gen2** or **SQL Database**.

---

#### **1.2. Streaming Data Ingestion (Stream Pipeline)**

For **streaming data**, we can ingest real-time data into the **Bronze layer** using Spark Structured Streaming (as covered previously) but will trigger it through **ADF**.

Here, ADF will trigger a **Databricks Notebook** for processing **streaming data**:

```json
{
  "name": "Loan_Application_Stream_Ingestion",
  "properties": {
    "activities": [
      {
        "name": "Trigger_Streaming_Job",
        "type": "DatabricksNotebook",
        "linkedServiceName": {
          "referenceName": "AzureDatabricksLinkedService",
          "type": "LinkedServiceReference"
        },
        "typeProperties": {
          "notebookPath": "/Shared/StreamingJobs/LoanApplicationStream",
          "baseParameters": {
            "topicName": "loan_applications",
            "kafkaBroker": "your_kafka_broker"
          }
        }
      }
    ]
  }
}
```

* **Step Description**:

  * **Trigger**: ADF will trigger a Databricks notebook running a **Spark Streaming job**.
  * **Action**: The Spark Streaming job reads real-time data from **Kafka** (or any streaming source), processes it, and stores it in the **Bronze layer**.

---

### **2. Transformation Pipeline (Bronze to Silver)**

Once the **raw data** is in the **Bronze layer**, we need to clean, filter, and enrich it to populate the **Silver layer**.

#### **2.1. Bronze to Silver Transformation Pipeline**

```json
{
  "name": "Loan_Application_Bronze_to_Silver_Transformation",
  "properties": {
    "activities": [
      {
        "name": "Run_Spark_SQL_Transformation",
        "type": "DatabricksNotebook",
        "linkedServiceName": {
          "referenceName": "AzureDatabricksLinkedService",
          "type": "LinkedServiceReference"
        },
        "typeProperties": {
          "notebookPath": "/Shared/Transformations/BronzeToSilverLoanApplication",
          "baseParameters": {
            "input_table": "bronze.bronze_loan_applications_batch",
            "output_table": "silver.silver_loan_applications"
          }
        }
      }
    ]
  }
}
```

* **Step Description**:

  * **Input**: Data from **bronze** layer (`bronze.bronze_loan_applications_batch`).
  * **Transformation**: The notebook applies transformations using **Spark SQL** and **PySpark** for cleaning and enrichment.
  * **Output**: Data is stored in the **Silver** layer (`silver.silver_loan_applications`).

---

### **3. Aggregation Pipeline (Silver to Gold)**

In the **Gold layer**, we aggregate the data for **KPI metrics**, **business intelligence** reports, and other performance metrics.

#### **3.1. Silver to Gold Aggregation Pipeline**

```json
{
  "name": "Loan_Application_Silver_to_Gold_Aggregation",
  "properties": {
    "activities": [
      {
        "name": "Run_SQL_Aggregation",
        "type": "DatabricksNotebook",
        "linkedServiceName": {
          "referenceName": "AzureDatabricksLinkedService",
          "type": "LinkedServiceReference"
        },
        "typeProperties": {
          "notebookPath": "/Shared/Aggregations/SilverToGoldLoanApplication",
          "baseParameters": {
            "input_table": "silver.silver_loan_applications",
            "output_table": "gold.gold_loan_application_summary"
          }
        }
      }
    ]
  }
}
```

* **Step Description**:

  * **Input**: Data from **Silver** layer (`silver.silver_loan_applications`).
  * **Aggregation**: The notebook runs **Spark SQL** queries to generate aggregate metrics (e.g., loan counts, total loan amounts).
  * **Output**: Data is written to the **Gold** layer (`gold.gold_loan_application_summary`).

---

### **4. Complete Dataflow Example (Ingestion → Transformation → Aggregation)**

The full dataflow pipeline might look like the following:

1. **ADF Trigger**: The **ADF** pipeline can be triggered based on a schedule or via event-driven triggers (e.g., new batch data available).
2. **Ingestion**: ADF will ingest **batch** data (or streaming data) into the **Bronze Layer**.
3. **Transformation**: The **Bronze Layer** data is cleaned, transformed, and written to the **Silver Layer**.
4. **Aggregation**: The **Silver Layer** is aggregated into **Gold** for reporting and KPIs.

---

### **Pipeline Execution and Monitoring**

* **Failure Handling**: For each activity, ADF supports retry policies and alerts. You can define retries based on failure conditions and send notifications using **Azure Logic Apps** or **Azure Functions**.
* **Monitoring**: Use **Azure Monitor** or **Azure Data Factory Monitoring** to monitor pipeline success, failure, and performance.

---

### **Key Recommendations for Best Practices**:

* **Parameterization**: Use parameters for dynamic values like **table names**, **source names**, and **configurations** to avoid hardcoding.
* **Modular Pipelines**: Break down large workflows into smaller, reusable pipelines for easier debugging and management.
* **Retry Logic**: Implement retry logic for all activities to handle intermittent failures.
* **Logging and Monitoring**: Enable detailed logging and error tracking for all pipelines to facilitate troubleshooting.

---
