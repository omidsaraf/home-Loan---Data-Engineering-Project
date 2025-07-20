
### **1. Create the Base Bronze Tables (without transformation)**

These are your raw ingestion tables that store data directly from the landing zone, either from batch or stream, before any transformation.

#### **Loan Applications Table**

```sql
CREATE TABLE bronze.bronze_loan_applications (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DECIMAL(18, 2),
    loan_type STRING,
    region STRING,
    application_date DATE,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/loan_applications';
```

#### **Loan Disbursement Table**

```sql
CREATE TABLE bronze.bronze_loan_disbursements (
    disbursement_id STRING,
    loan_id STRING,
    disbursement_amount DECIMAL(18, 2),
    disbursement_date DATE,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/loan_disbursements';
```

---

### **2. Apply Row-Level Security (RLS)**

We create an RLS function that restricts data based on user region. This is a reusable function.

#### **RLS Function (For Loan Applications by Region)**

```sql
CREATE OR REPLACE FUNCTION rls_loan_applications(region STRING)
RETURNS BOOLEAN
LANGUAGE SQL
AS
BEGIN
    IF current_role() IN ('admin', 'loan_officer') THEN
        RETURN TRUE; -- Allow all for admin/loan_officer
    ELSE
        RETURN region = current_user_region(); -- Filter based on the user's region
    END IF;
END;
```

---

### **3. Apply Column-Level Security (CLS)**

This function will mask sensitive columns like loan amount and applicant name for users with limited roles.

#### **Column Masking Functions**

```sql
-- Mask Loan Amount
CREATE OR REPLACE FUNCTION cls_loan_amount(loan_amount DECIMAL)
RETURNS DECIMAL
LANGUAGE SQL
AS
BEGIN
    IF current_role() IN ('admin', 'analyst') THEN
        RETURN loan_amount; -- Show full amount
    ELSE
        RETURN NULL; -- Mask for other roles
    END IF;
END;

-- Mask Applicant Name
CREATE OR REPLACE FUNCTION cls_applicant_name(applicant_name STRING)
RETURNS STRING
LANGUAGE SQL
AS
BEGIN
    IF current_role() IN ('admin', 'analyst') THEN
        RETURN applicant_name; -- Show full name
    ELSE
        RETURN '****'; -- Mask for other roles
    END IF;
END;
```

---

### **4. Apply Dynamic Data Masking (DDM)**

#### **Create Tables with DDM Masking for Sensitive Data**

```sql
CREATE TABLE bronze.bronze_loan_applications (
    loan_id STRING,
    applicant_name STRING MASKED WITH (FUNCTION = 'default()'),
    loan_amount DECIMAL(18, 2) MASKED WITH (FUNCTION = 'default()'),
    loan_type STRING,
    region STRING,
    application_date DATE,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/loan_applications';
```

---

### **5. Create Views with Security Policies**

These views apply **RLS**, **CLS**, and **DDM** to filter, mask, or allow access to data based on roles.

#### **View for Loan Applications (with RLS and CLS applied)**

```sql
CREATE OR REPLACE VIEW bronze.view_loan_applications_rls AS
SELECT 
    loan_id,
    cls_applicant_name(applicant_name) AS applicant_name,
    cls_loan_amount(loan_amount) AS loan_amount,
    loan_type,
    region,
    application_date,
    ingestion_date
FROM bronze.bronze_loan_applications
WHERE rls_loan_applications(region);
```

---

#### **View for Loan Disbursements (with CLS applied)**

```sql
CREATE OR REPLACE VIEW bronze.view_loan_disbursements_cls AS
SELECT 
    disbursement_id,
    loan_id,
    cls_loan_amount(disbursement_amount) AS disbursement_amount,
    disbursement_date,
    ingestion_date
FROM bronze.bronze_loan_disbursements;
```

---

### **6. Metadata Integration for Security Policies**

You can track metadata of RLS, CLS, and DDM policies applied using a **Metadata Logs** table.

#### **Create Metadata Log Table**

```sql
CREATE TABLE bronze.metadata_logs (
    log_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    metadata_type STRING,
    metadata_id STRING,
    action STRING,
    previous_value STRING,
    new_value STRING,
    updated_by STRING,
    updated_at TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/metadata_logs';
```

#### **Sample Metadata Log Entry for Security Application**

```sql
INSERT INTO bronze.metadata_logs (
    metadata_type, metadata_id, action, previous_value, new_value, updated_by, updated_at
) VALUES 
('RLS', 'loan_applications', 'ADD', 'NULL', 'Region-based RLS applied', 'admin', current_timestamp()),
('CLS', 'loan_applications', 'ADD', 'NULL', 'CLS for loan_amount applied', 'admin', current_timestamp()),
('DDM', 'loan_applications', 'ADD', 'NULL', 'Masked loan_amount and applicant_name', 'admin', current_timestamp());
```

---

### **7. Final Views and Tables with Security Applied**

Finally, ensure that all your views are created with RLS, CLS, and DDM enforced, and users can query these views securely.

#### **View for Secured Loan Applications**

```sql
CREATE OR REPLACE VIEW bronze.view_loan_applications_secured AS
SELECT 
    loan_id,
    cls_applicant_name(applicant_name) AS applicant_name,
    cls_loan_amount(loan_amount) AS loan_amount,
    loan_type,
    region,
    application_date,
    ingestion_date
FROM bronze.bronze_loan_applications
WHERE rls_loan_applications(region);
```

---

### **8. Archival Policy for Bronze Layer**

For **data archival**, we can create an additional **archival table** that stores older records, ensuring that the **Bronze Layer** remains efficient.

```sql
CREATE TABLE bronze.archived_loan_applications (
    loan_id STRING,
    applicant_name STRING,
    loan_amount DECIMAL(18, 2),
    loan_type STRING,
    region STRING,
    application_date DATE,
    ingestion_date TIMESTAMP
)
USING DELTA
LOCATION '/mnt/bronze/archived_loan_applications';
```

---

### **Conclusion**

This approach follows best practices for **RLS**, **CLS**, **DDM**, and **metadata integration** in the **Bronze Layer**. Key considerations:

* **RLS**: Filters data at the row level based on user roles, such as region-based filtering.
* **CLS**: Masks sensitive columns, like **loan amount** and **applicant name**, for non-admin users.
* **DDM**: Ensures that sensitive data is automatically masked in the database.
* **Metadata Logging**: Tracks any changes in security policies for auditing and compliance.

Each **view** and **table** is designed to ensure data governance while also providing flexibility for different roles in your organization.

