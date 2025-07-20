Let's design the **Bronze Layer** for your **HomeLoanIQ Data Engineering Platform** using the project context. In this layer, we will focus on **raw ingestion** (both **batch** and **streaming**) into **Azure Data Lake Storage Gen2 (ADLS Gen2)** with **no transformations**. The data will be stored in Delta format to enable **ACID transactions**, **schema evolution**, and **versioning**.

Below are the **required tables for the Bronze layer** that include both **streaming** and **batch ingestion**.

---

### **1. Batch Ingestion: Loan Applications (Raw Data)**

This table captures **loan application data** directly ingested via batch processes (e.g., via ADF, CSV files, etc.).

```sql
-- Bronze Table for Loan Applications (Batch Ingestion)
CREATE TABLE IF NOT EXISTS bronze.bronze_loan_applications_batch (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DOUBLE,
    loan_type STRING,
    region STRING,
    application_date DATE,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/loan_applications_batch/';
```

**Explanation**:

* This table captures **raw loan applications** that are ingested in **batch mode**.
* Stored in Delta format and **partitioned by `ingestion_date`**.

---

### **2. Batch Ingestion: Loan Approvals (Raw Data)**

This table captures **loan approval data** ingested via **batch** jobs (e.g., from core banking systems).

```sql
-- Bronze Table for Loan Approvals (Batch Ingestion)
CREATE TABLE IF NOT EXISTS bronze.bronze_loan_approvals_batch (
    loan_id STRING,
    approval_status STRING,
    approval_date DATE,
    approval_amount DOUBLE,
    region STRING,
    decision_maker STRING,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/loan_approvals_batch/';
```

**Explanation**:

* This table stores **raw loan approval data** ingested through **batch jobs**.
* Data is stored in Delta format, partitioned by **ingestion\_date**.

---

### **3. Streaming Ingestion: Loan Applications (Raw Data)**

For streaming data (e.g., via **Kafka** or **Event Hub**), this table stores **loan applications** as they are ingested in real-time.

```sql
-- Bronze Table for Loan Applications (Streaming Ingestion)
CREATE TABLE IF NOT EXISTS bronze.bronze_loan_applications_streaming (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DOUBLE,
    loan_type STRING,
    region STRING,
    application_date DATE,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/loan_applications_streaming/';
```

**Explanation**:

* This table captures **raw loan application data** from **streaming sources** like Kafka/Event Hub.
* Stored in Delta format and partitioned by **ingestion\_date**.

---

### **4. Streaming Ingestion: Loan Approvals (Raw Data)**

This table captures **loan approval data** ingested in **real-time** via **streaming** technologies.

```sql
-- Bronze Table for Loan Approvals (Streaming Ingestion)
CREATE TABLE IF NOT EXISTS bronze.bronze_loan_approvals_streaming (
    loan_id STRING,
    approval_status STRING,
    approval_date DATE,
    approval_amount DOUBLE,
    region STRING,
    decision_maker STRING,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/loan_approvals_streaming/';
```

**Explanation**:

* This table captures **raw loan approval data** ingested in **real-time** via **streaming** sources.
* Stored in Delta format and partitioned by **ingestion\_date**.

---

### **5. Streaming Ingestion: Loan Disbursements (Raw Data)**

Captures **loan disbursement data** ingested via streaming (e.g., Kafka).

```sql
-- Bronze Table for Loan Disbursements (Streaming Ingestion)
CREATE TABLE IF NOT EXISTS bronze.bronze_loan_disbursements_streaming (
    loan_id STRING,
    disbursement_amount DOUBLE,
    disbursement_date DATE,
    region STRING,
    disbursement_status STRING,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/loan_disbursements_streaming/';
```

**Explanation**:

* This table stores **loan disbursement data** ingested in **real-time**.
* Stored in Delta format and partitioned by **ingestion\_date**.

---

### **6. Bronze Archival Table: Historical Loan Data (Batch + Streaming)**

An **archival table** capturing **all historical records** (both batch and streaming) for **audit purposes**. This will combine data from all raw sources.

```sql
-- Bronze Archival Table for Historical Loan Data (Batch + Streaming)
CREATE TABLE IF NOT EXISTS bronze.bronze_historical_loan_data (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DOUBLE,
    loan_type STRING,
    approval_status STRING,
    approval_date DATE,
    approval_amount DOUBLE,
    disbursement_amount DOUBLE,
    disbursement_date DATE,
    region STRING,
    application_date DATE,
    disbursement_status STRING,
    decision_maker STRING,
    ingestion_date TIMESTAMP,
    version STRING  -- To track version of each record over time
)
USING DELTA
LOCATION '/mnt/bronze/historical_loan_data/';
```

**Explanation**:

* The **archival table** captures both **batch and streaming** data and includes a **version column** to store historical versions of records.
* This allows tracking of data changes over time.
* Stored in Delta format and partitioned by **ingestion\_date**.

---

### **7. Consolidated Bronze Table for Loan Data (Optional)**

If required, we can consolidate all loan-related data into one table in the **Bronze layer** to simplify the architecture.

```sql
-- Consolidated Bronze Table for Loan Data (Batch + Streaming)
CREATE TABLE IF NOT EXISTS bronze.bronze_loan_data_consolidated (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DOUBLE,
    loan_type STRING,
    approval_status STRING,
    approval_date DATE,
    approval_amount DOUBLE,
    disbursement_amount DOUBLE,
    disbursement_date DATE,
    region STRING,
    application_date DATE,
    disbursement_status STRING,
    decision_maker STRING,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/loan_data_consolidated/';
```

**Explanation**:

* This table consolidates all **raw data** related to **loan applications**, **approvals**, and **disbursements** into a **single table**.
* This can be used as a **catch-all** table for any downstream transformations in the **Silver** layer.
* Stored in Delta format and partitioned by **ingestion\_date**.

---

### **Key Best Practices for Bronze Layer (Stream + Batch)**

1. **No Transformation**: The **Bronze layer** stores data **as-is**. Raw data from batch and streaming sources is stored with minimal changes.

2. **Delta Lake Format**: All tables are stored in **Delta format** to leverage ACID transactions, schema evolution, and versioning.

3. **Partitioning**: Data is **partitioned by `ingestion_date`** to ensure scalability and better performance for queries, especially as data grows.

4. **Historical Tracking**: For full **auditability**, we use a **version column** in the **Bronze Archival Table** to track changes in the data over time.

5. **Stream + Batch Data Handling**: Both **batch** and **streaming** data are stored separately in different tables to maintain clean separation between these ingestion types. You can later join or combine them in the **Silver layer**.

6. **Use of Mounts for Unity Catalog**: Ensure that tables are mounted correctly for **Unity Catalog** and that each table has the necessary **data governance** and **security** policies applied.

7. **Data Integrity**: All raw data is stored in its original form without transformation, ensuring integrity for downstream processes.

---


