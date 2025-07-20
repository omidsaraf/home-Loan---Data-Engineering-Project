
In the **Silver Layer**, we clean, filter, and enrich data for analysis. We don't apply **security policies** in this layer.

#### **1. Silver Loan Application Table (Cleaned Data)**

```sql
CREATE TABLE silver.silver_loan_applications AS
SELECT 
    loan_id,
    applicant_name,
    loan_amount,
    application_date,
    application_status,
    source_system,
    created_at,
    updated_at
FROM bronze.bronze_loan_applications_batch
WHERE application_date IS NOT NULL
  AND loan_amount > 0
  AND application_status IS NOT NULL;
```

#### **2. Silver Loan Disbursement Table (Cleaned Data)**

```sql
CREATE TABLE silver.silver_loan_disbursements AS
SELECT 
    loan_id,
    disbursement_amount,
    disbursement_date,
    disbursement_status,
    source_system,
    created_at,
    updated_at
FROM bronze.bronze_loan_disbursements_batch
WHERE disbursement_date IS NOT NULL
  AND disbursement_amount > 0;
```

#### **3. Silver Loan Repayment Table (Cleaned Data)**

```sql
CREATE TABLE silver.silver_loan_repayment_stream AS
SELECT 
    loan_id,
    repayment_amount,
    repayment_date,
    repayment_status,
    source_system,
    event_time,
    created_at,
    updated_at
FROM bronze.bronze_loan_repayment_stream
WHERE repayment_date IS NOT NULL
  AND repayment_amount > 0;
```

