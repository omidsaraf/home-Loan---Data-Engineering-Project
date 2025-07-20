The **Gold Layer** aggregates data for KPIs, metrics, and final business insights.

#### **1. Gold Loan Application Summary (Aggregate)**

```sql
CREATE TABLE gold.gold_loan_application_summary AS
SELECT 
    application_date,
    COUNT(DISTINCT loan_id) AS total_applications,
    SUM(loan_amount) AS total_loan_amount,
    AVG(loan_amount) AS avg_loan_amount
FROM silver.silver_loan_applications
GROUP BY application_date;
```

#### **2. Gold Loan Disbursement Summary (Aggregate)**

```sql
CREATE TABLE gold.gold_loan_disbursement_summary AS
SELECT 
    disbursement_date,
    COUNT(DISTINCT loan_id) AS total_disbursements,
    SUM(disbursement_amount) AS total_disbursed_amount,
    AVG(disbursement_amount) AS avg_disbursed_amount
FROM silver.silver_loan_disbursements
GROUP BY disbursement_date;
```

#### **3. Gold Loan Repayment Summary (Aggregate)**

```sql
CREATE TABLE gold.gold_loan_repayment_summary AS
SELECT 
    repayment_date,
    COUNT(DISTINCT loan_id) AS total_repayments,
    SUM(repayment_amount) AS total_repayment_amount,
    AVG(repayment_amount) AS avg_repayment_amount
FROM silver.silver_loan_repayment_stream
GROUP BY repayment_date;
```
