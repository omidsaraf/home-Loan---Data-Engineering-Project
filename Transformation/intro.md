This directory contains the **modular Spark SQL notebooks** implementing the **Bronze → Silver → Gold** layered architecture for HomeLoanIQ’s data pipeline. It supports scalable, auditable, and high-quality transformations aligned with banking-grade data governance.

---

## 📁 Directory Structure

```plaintext
src/
└── transformation/
    ├── bronze/    # Raw ingestion data, minimal transformations
    ├── silver/    # Cleansed, enriched, validated entity views
    └── gold/      # Business KPIs and aggregated fact/dimension views
````

---

## 🪵 Bronze Layer – Raw Ingestion Data

* **Purpose**: Landing zone for raw ingested datasets from batch and streaming sources.
* **Characteristics**:

  * Minimal transformation (parsing, standardization)
  * Schema enforcement with Spark SQL DDL
  * Partitioned by ingestion timestamp or batch date for performance
  * Data Quality checks for completeness, duplicates, and nulls
* **Examples**:

  * `bronze_loan_applications.sql` — Raw loan application event landing
  * `bronze_customer_info.sql` — Raw customer profile snapshots
* **Best Practices**:

  * Use **idempotent writes** and Delta Lake `merge` for reprocessing
  * Capture ingestion metadata (source, file name, ingestion time)
  * Avoid business logic here — keep it a pure landing zone

---

## ✨ Silver Layer – Cleansed and Enriched Entities

* **Purpose**: Apply business rules, data cleansing, and join reference data to create trusted datasets.
* **Characteristics**:

  * Data validation and correction (e.g., standardize address formats)
  * Entity resolution and deduplication (e.g., customer ID unification)
  * Enrich with credit bureau scores, branch hierarchies, geo info
  * Implement slowly changing dimensions (Type 1/2) where applicable
* **Examples**:

  * `silver_loan_accounts.sql` — Clean loan accounts enriched with credit risk
  * `silver_customers.sql` — De-duplicated, validated customer profiles
* **Best Practices**:

  * Modular SQL notebooks with parameterized filters (date ranges, batch IDs)
  * Use **views** or **materialized views** where applicable for performance
  * Maintain audit columns (`created_at`, `updated_at`, `source_system`)

---

## 🏅 Gold Layer – KPI-Ready Aggregates and Views

* **Purpose**: Business-facing datasets tailored for reporting, ML models, and API consumption.
* **Characteristics**:

  * Aggregations (e.g., application volumes, approval rates, default rates)
  * Calculated metrics with time-windowing (e.g., rolling 30-day averages)
  * Dimension tables for loan products, branches, and borrower segments
  * Conformed datasets for Tableau dashboards, Salesforce, and APIs
* **Examples**:

  * `gold_loan_kpis.sql` — Daily KPI aggregates for loan approvals and defaults
  * `gold_branch_performance.sql` — Branch-level performance metrics
* **Best Practices**:

  * Encapsulate complex business logic in reusable SQL macros or UDFs
  * Follow strict naming conventions for views and tables (`gold_` prefix)
  * Include partitioning and indexing hints for query performance
  * Document metric definitions and lineage inline

---

## 🛠️ Development & Deployment Practices

* Use **Delta Lake** ACID transactions across all layers for data integrity.
* Version notebooks and SQL scripts in GitHub with PR-based code reviews.
* Parameterize date and environment context for Dev/Test/Prod deployments.
* Integrate transformations in CI/CD pipelines with automated tests.
* Leverage Databricks Unity Catalog for **data governance** and access control.
* Enable **data lineage** tracking through metadata-driven orchestration.

---

## 🔒 Data Governance & Quality

* Enforce **schema validation** at each layer with Great Expectations or native Spark checks.
* Implement **row-level security** and PII masking in Silver/Gold layers via Unity Catalog.
* Capture audit metadata: processing timestamps, job run IDs, and error metrics.
* Monitor data freshness and anomaly detection with operational dashboards.

