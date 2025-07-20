
### 1. **`job.csv` - Pipeline Job Configuration**

```csv
job_id   | job_name                | schedule          | dependencies          | job_type   | owner            | environment | description                                           | retry_policy     | failure_notification
---------|------------------------|-------------------|-----------------------|------------|------------------|-------------|-------------------------------------------------------|------------------|----------------------
J001     | ingest_loan_applications| 0 2 * * *         |                       | batch      | data_eng_team    | dev,prod    | Daily ingestion of loan application data from CRM     | 3 retries, backoff 5m | email@company.com
J002     | ingest_loan_book       | 0 3 * * *         | J001                  | batch      | data_eng_team    | dev,prod    | Daily ingestion of loan book data from core banking   | 2 retries, backoff 10m | email@company.com
J003     | bronze_transform       | 0 4 * * *         | J001,J002             | batch      | data_eng_team    | dev,prod    | Bronze layer transformation for raw loan datasets     | 3 retries, backoff 5m  | slack@company.com
J004     | silver_transform       | 0 5 * * *         | J003                  | batch      | data_eng_team    | dev,prod    | Silver layer enrichment & entity relationships        | 2 retries, backoff 10m | slack@company.com
J005     | gold_kpi_aggregation   | 0 6 * * *         | J004                  | batch      | analytics        | dev,prod    | KPI computation & aggregation for dashboards          | 3 retries, backoff 10m | slack@company.com
J006     | streaming_loan_events  | continuous        |                       | streaming  | data_eng_team    | prod        | Real-time streaming ingestion of loan event messages  | 5 retries, backoff 5m  | email@company.com
```

* **Retry Policy:** Implements automatic retries with an exponential backoff to ensure robust handling of transient errors.
* **Failure Notification:** Provides an immediate alert via email or Slack if any job fails after retries, ensuring quick resolution.
* **Auditability:** Track execution logs and failure alerts for post-mortem analysis.

---

### 2. **Updated `proc.csv` - Process to Notebook/Script Mapping with Dependencies**
```csv
proc_id | job_id | proc_name           | notebook_path                               | order | retry_count | timeout_minutes | description                                    | scheduler_type | dag_id            | dependencies
--------|--------|---------------------|---------------------------------------------|-------|-------------|-----------------|------------------------------------------------|----------------|-------------------|--------------
P001    | J001   | loan_app_ingest     | src/ingestion/adf_templates/loan_app_ingest.json | 1     | 3           | 60              | Runs ADF pipeline to ingest loan applications  | ADF            | adf_loan_app_dag  | 
P002    | J002   | loan_book_ingest    | src/ingestion/adf_templates/loan_book_ingest.json| 1     | 3           | 60              | Runs ADF pipeline to ingest loan book data     | ADF            | adf_loan_book_dag | P001
P003    | J003   | bronze_loan_raw     | src/transformation/bronze/bronze_loan_raw.sql     | 1     | 2           | 120             | Spark SQL notebook for bronze raw transformation | Airflow        | airflow_bronze_dag| P001,P002
P004    | J004   | silver_loan_enrich  | src/transformation/silver/silver_loan_enrich.sql | 1     | 2           | 120             | Spark SQL notebook for silver layer enrichment | Airflow        | airflow_silver_dag| P003
P005    | J005   | gold_kpi_metrics    | src/transformation/gold/gold_kpi_metrics.sql      | 1     | 2           | 60              | Spark SQL notebook for gold KPI aggregations   | Airflow        | airflow_gold_dag  | P004
P006    | J006   | streaming_loan_proc | src/ingestion/pyspark_streaming/streaming_loan.py| 1     | 5           | 0 (continuous)  | PySpark streaming job for real-time loan events | Airflow        | airflow_streaming_dag| 
```

* **Dependencies:** Clearly defines **downstream dependencies**. For example, `P003 (bronze_loan_raw)` can only start after `P001 (loan_app_ingest)` and `P002 (loan_book_ingest)` finish.
* **Retry Policy:** Ensures that if a process fails, it will be retried based on the defined retry count and timeout.

---

### 3. ** `proc_param.csv` - Parameter Injection with Security and Flexibility**

We ensure **secure parameterization** (e.g., using **Azure Key Vault** for sensitive data) and **dynamic injection** of job-specific configurations (e.g., dynamic date ranges, environment-specific values).

```csv
proc_id | param_name       | param_value              | param_type | description                                | secure |
--------|------------------|--------------------------|------------|--------------------------------------------|--------|
P001    | start_date       | {{ yesterday() }}         | date       | Start date for batch ingestion window      | No     |
P001    | end_date         | {{ today() }}             | date       | End date for batch ingestion window        | No     |
P003    | partition_date   | {{ today() }}             | date       | Date partition for bronze transformation   | No     |
P004    | batch_id         | {{ run_id() }}            | string     | Unique batch identifier for silver load    | No     |
P005    | kpi_window_days  | 30                       | int        | Lookback window size for KPI calculations  | No     |
P006    | kafka_topic      | loan_events               | string     | Kafka topic for streaming ingestion        | No     |
P006    | checkpoint_path  | /mnt/checkpoints/loan     | string     | Spark streaming checkpoint directory       | No     |
P003    | job_name         | {{ job_name }}            | string     | Dynamic job name for logging & monitoring  | No     |
P001    | sensitive_api_key| {{ secret('api_key') }}   | string     | Secure API key for accessing the CRM       | Yes    |
```

* **Secure Parameters:** Sensitive data, like API keys or credentials, are fetched securely from **Azure Key Vault** using `{{ secret('api_key') }}`.
* **Dynamic Values:** Uses dynamic templates (e.g., `{{ yesterday() }}` and `{{ run_id() }}`) to provide contextual parameters, reducing hardcoding and improving flexibility.

