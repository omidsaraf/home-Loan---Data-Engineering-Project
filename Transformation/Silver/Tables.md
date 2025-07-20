
### **1. Silver Layer – Transformed Tables**

These tables will be created by joining or cleansing data from the **Bronze Layer**.

---

### **1.1. Loan Applications (Cleaned and Enriched)**

The **Silver Layer** cleans up the raw loan application data, adds necessary business logic, and might join it with external data sources like CRM or risk scores.

```sql
CREATE TABLE silver.silver_loan_applications (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DECIMAL(18, 2),
    loan_type STRING,
    region STRING,
    application_date DATE,
    disbursement_date DATE,
    credit_score INT,
    employment_status STRING,
    application_status STRING,
    ingestion_date TIMESTAMP,
    enriched_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/silver/loan_applications';
```

---

### **1.2. Loan Disbursement Table (Cleansed and Enriched)**

This table integrates information from the **Bronze Layer** and any other relevant data sources (e.g., risk models or external APIs) to cleanse the disbursement data.

```sql
CREATE TABLE silver.silver_loan_disbursements (
    disbursement_id STRING,
    loan_id STRING,
    disbursement_amount DECIMAL(18, 2),
    disbursement_date DATE,
    region STRING,
    disbursement_status STRING,
    processing_date TIMESTAMP,
    enriched_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/silver/loan_disbursements';
```

---

### **1.3. Customer Profile Table (Cleaned)**

This is an enriched version of the customer profile, potentially joining data from various sources like CRM, core banking systems, or external data sources (e.g., credit score).

```sql
CREATE TABLE silver.silver_customer_profiles (
    customer_id STRING,
    customer_name STRING,
    email STRING,
    phone STRING,
    region STRING,
    date_of_birth DATE,
    credit_score INT,
    annual_income DECIMAL(18, 2),
    employment_status STRING,
    address STRING,
    registration_date TIMESTAMP,
    last_updated TIMESTAMP
)
USING DELTA
LOCATION '/mnt/silver/customer_profiles';
```

---

### **1.4. Loan Default Risk Model (Cleansed)**

This table will be enriched with risk model outputs, such as probability of loan default, customer behavior patterns, etc.

```sql
CREATE TABLE silver.silver_loan_default_risk (
    loan_id STRING,
    customer_id STRING,
    loan_amount DECIMAL(18, 2),
    risk_score INT,
    predicted_default_probability DECIMAL(5, 4),
    model_version STRING,
    evaluation_date TIMESTAMP,
    enriched_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/silver/loan_default_risk';
```

---

### **1.5. Loan Repayment Table (Cleansed)**

This table contains cleaned loan repayment data. It tracks the repayment progress of loans and links to the customer profiles.

```sql
CREATE TABLE silver.silver_loan_repayments (
    repayment_id STRING,
    loan_id STRING,
    repayment_amount DECIMAL(18, 2),
    repayment_date DATE,
    outstanding_balance DECIMAL(18, 2),
    repayment_status STRING,
    processing_date TIMESTAMP,
    enriched_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/silver/loan_repayments';
```

---

### **2. Silver Layer Views (Cleaned Data)**

#### **2.1. View for Loan Applications (Cleaned)**

This view will give analysts access to cleaned **loan applications** with all the enriched columns such as **credit score** and **employment status**.

```sql
CREATE OR REPLACE VIEW silver.view_loan_applications_cleaned AS
SELECT 
    loan_id,
    applicant_name,
    loan_amount,
    loan_type,
    region,
    application_date,
    disbursement_date,
    credit_score,
    employment_status,
    application_status,
    ingestion_date,
    enriched_date
FROM silver.silver_loan_applications;
```

---

#### **2.2. View for Loan Disbursements (Cleaned)**

This view will present **loan disbursements** after cleansing and enrichment.

```sql
CREATE OR REPLACE VIEW silver.view_loan_disbursements_cleaned AS
SELECT 
    disbursement_id,
    loan_id,
    disbursement_amount,
    disbursement_date,
    region,
    disbursement_status,
    processing_date,
    enriched_date
FROM silver.silver_loan_disbursements;
```

---

#### **2.3. View for Customer Profiles (Cleaned)**

A cleaned and enriched version of the customer profiles, accessible for reporting or further analysis.

```sql
CREATE OR REPLACE VIEW silver.view_customer_profiles_cleaned AS
SELECT 
    customer_id,
    customer_name,
    email,
    phone,
    region,
    date_of_birth,
    credit_score,
    annual_income,
    employment_status,
    address,
    registration_date,
    last_updated
FROM silver.silver_customer_profiles;
```

---

#### **2.4. View for Loan Default Risk (Cleaned)**

A **view** of the **loan default risk** model, showing risk scores and the likelihood of default for each loan.

```sql
CREATE OR REPLACE VIEW silver.view_loan_default_risk_cleaned AS
SELECT 
    loan_id,
    customer_id,
    loan_amount,
    risk_score,
    predicted_default_probability,
    model_version,
    evaluation_date,
    enriched_date
FROM silver.silver_loan_default_risk;
```

---

#### **2.5. View for Loan Repayments (Cleaned)**

This view is for analysts to track loan repayment status, outstanding balances, and related information.

```sql
CREATE OR REPLACE VIEW silver.view_loan_repayments_cleaned AS
SELECT 
    repayment_id,
    loan_id,
    repayment_amount,
    repayment_date,
    outstanding_balance,
    repayment_status,
    processing_date,
    enriched_date
FROM silver.silver_loan_repayments;
```

---

### **3. Silver Layer Transformation Pipelines**

These **SQL-based transformation pipelines** will clean and enrich the raw data from the **Bronze Layer**.

#### **3.1. Load Loan Applications (Transform)**

```sql
-- Load and transform Loan Applications into Silver Layer
INSERT INTO silver.silver_loan_applications
SELECT 
    loan_id,
    applicant_name,
    loan_amount,
    loan_type,
    region,
    application_date,
    disbursement_date,
    credit_score,
    employment_status,
    application_status,
    ingestion_date,
    current_timestamp() AS enriched_date
FROM bronze.bronze_loan_applications
WHERE application_date IS NOT NULL;
```

---

#### **3.2. Load Loan Disbursements (Transform)**

```sql
-- Load and transform Loan Disbursements into Silver Layer
INSERT INTO silver.silver_loan_disbursements
SELECT 
    disbursement_id,
    loan_id,
    disbursement_amount,
    disbursement_date,
    region,
    disbursement_status,
    processing_date,
    current_timestamp() AS enriched_date
FROM bronze.bronze_loan_disbursements
WHERE disbursement_amount IS NOT NULL;
```

---

#### **3.3. Load Customer Profiles (Transform)**

```sql
-- Load and transform Customer Profiles into Silver Layer
INSERT INTO silver.silver_customer_profiles
SELECT 
    customer_id,
    customer_name,
    email,
    phone,
    region,
    date_of_birth,
    credit_score,
    annual_income,
    employment_status,
    address,
    registration_date,
    current_timestamp() AS last_updated
FROM bronze.bronze_customer_profiles
WHERE customer_id IS NOT NULL;
```

---

#### **3.4. Load Loan Default Risk (Transform)**

```sql
-- Load and transform Loan Default Risk into Silver Layer
INSERT INTO silver.silver_loan_default_risk
SELECT 
    loan_id,
    customer_id,
    loan_amount,
    risk_score,
    predicted_default_probability,
    model_version,
    evaluation_date,
    current_timestamp() AS enriched_date
FROM bronze.bronze_loan_default_risk
WHERE loan_id IS NOT NULL;
```

---

#### **3.5. Load Loan Repayments (Transform)**

```sql
-- Load and transform Loan Repayments into Silver Layer
INSERT INTO silver.silver_loan_repayments
SELECT 
    repayment_id,
    loan_id,
    repayment_amount,
    repayment_date,
    outstanding_balance,
    repayment_status,
    processing_date,
    current_timestamp() AS enriched_date
FROM bronze.bronze_loan_repayments
WHERE repayment_amount IS NOT NULL;
```

---

### **Conclusion**

The **Silver Layer** cleanses and enriches the raw data from the **Bronze Layer** and creates reusable, enriched datasets that are ready for analysis or further processing. These datasets:

