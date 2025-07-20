#### **1. Bronze Loan Application Table (Batch Data)**

This table is for storing **batch**-processed loan application data.

```sql
CREATE TABLE bronze.bronze_loan_applications_batch (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DECIMAL(10,2),
    application_date DATE,
    application_status STRING,
    source_system STRING,
    raw_data STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
USING DELTA
PARTITIONED BY (application_date)
LOCATION '/mnt/bronze/loan_applications_batch/';
```

#### **2. Bronze Loan Application Table (Stream Data)**

This table is for storing **stream**-processed loan application data (using Spark Structured Streaming).

```sql
CREATE TABLE bronze.bronze_loan_applications_stream (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DECIMAL(10,2),
    application_date DATE,
    application_status STRING,
    source_system STRING,
    raw_data STRING,
    event_time TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
USING DELTA
PARTITIONED BY (application_date)
LOCATION '/mnt/bronze/loan_applications_stream/';
```

#### **3. Bronze Loan Disbursement Table (Batch Data)**

```sql
CREATE TABLE bronze.bronze_loan_disbursements_batch (
    loan_id STRING,
    disbursement_amount DECIMAL(10,2),
    disbursement_date DATE,
    disbursement_status STRING,
    source_system STRING,
    raw_data STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
USING DELTA
PARTITIONED BY (disbursement_date)
LOCATION '/mnt/bronze/loan_disbursements_batch/';
```

#### **4. Bronze Loan Repayment Table (Stream Data)**

```sql
CREATE TABLE bronze.bronze_loan_repayment_stream (
    loan_id STRING,
    repayment_amount DECIMAL(10,2),
    repayment_date DATE,
    repayment_status STRING,
    source_system STRING,
    raw_data STRING,
    event_time TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
USING DELTA
PARTITIONED BY (repayment_date)
LOCATION '/mnt/bronze/loan_repayment_stream/';
```

#### **5. Archival Table for Loan Application (Archival Data)**

The **archival table** stores older or historical data to keep the Bronze Layer lean and efficient. This can be used for long-term storage and periodic data aging.

```sql
CREATE TABLE bronze.archival_loan_applications (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DECIMAL(10,2),
    application_date DATE,
    application_status STRING,
    source_system STRING,
    raw_data STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
USING DELTA
PARTITIONED BY (application_date)
LOCATION '/mnt/bronze/archival_loan_applications/';
```
