
This directory contains the **core data processing logic** for the Home Loan Intelligence platform, following a **Bronze → Silver → Gold** architecture.

---

### 📁 Folder Structure

```plaintext
src/
├── ingestion/          # Raw file ingestion logic (batch/API/stream)
├── transformation/     # ETL scripts categorized into Bronze/Silver/Gold
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── extraction/         # Export scripts for Tableau, APIs, Salesforce
├── notebooks/          # Exploratory notebooks (Databricks/Zeppelin)
└── utils/              # Reusable functions, validations, config loaders
```

---

## 🔄 1. `ingestion/` – Data Ingestion Pipelines

Handles ingestion from:

* Core banking (via ADF or API)
* CRM / Loan Origination System (REST, JSON)
* Bureau Data (CSV/Excel, SFTP)
* Real-time Kafka streams

**Key Files:**

| File                              | Purpose                                |
| --------------------------------- | -------------------------------------- |
| `ingest_crm_applications.py`      | Load CRM application data              |
| `ingest_corebank_loanbook.py`     | Load core banking disbursal data       |
| `ingest_credit_bureau_batch.py`   | Batch load credit scores               |
| `ingest_stream_kafka_realtime.py` | Consume Kafka topic for real-time apps |

All ingestion jobs follow this **pattern**:

```python
def run_ingestion(metadata: dict):
    df = read_source(metadata)
    df_clean = clean_and_standardize(df)
    write_to_delta(df_clean, metadata['target_path'])
```

---

## 🔁 2. `transformation/` – ETL Pipeline Logic

Organized into **Bronze**, **Silver**, and **Gold** layers:

### 🪵 `bronze/`: Raw Ingested Staging

* Minimal processing (deduplication, timestamp formatting)
* Schema alignment using JSON contracts
* Saved as Delta Tables partitioned by date

Example: `bronze_crm_applications.py`

```python
df = spark.read.format("delta").load(bronze_path)
df = deduplicate(df, ["ApplicationID"])
df.write.mode("overwrite").saveAsTable("bronze.crm_applications")
```

---

### ✨ `silver/`: Cleansed, Enriched Data

* Joins across sources (CRM ↔ CoreBank ↔ Bureau)
* Adds derived columns: `LoanToValue`, `IsHighRisk`, etc.
* Standardizes timestamp, customer keys, channel types

Example: `silver_enriched_loans.py`

```python
df = join_crm_core(df_crm, df_core)
df = enrich_with_bureau_score(df, df_bureau)
df.write.format("delta").mode("overwrite").saveAsTable("silver.enriched_loans")
```

---

### 🏅 `gold/`: KPI and Reporting Models

* Pre-aggregated KPI tables for dashboarding
* Modular SQL templates (Net Disbursal, Approval Rate, TAT)
* Filters and dimensions applied (Region, Branch, Product)

Example: `gold_kpi_disbursal_rate.py`

```python
df = calculate_disbursal_kpi(df_enriched)
df.write.mode("overwrite").saveAsTable("gold.kpi_disbursal_rate")
```

---

## 📤 3. `extraction/` – Data Serving & APIs

* Exports data to:

  * Tableau extracts (via Hyper API)
  * Salesforce updates
  * External APIs

**Examples:**

* `extract_tableau_loan_kpi.py`
* `push_to_salesforce.py`
* `api_borrower_profile.py`

---

## 📓 4. `notebooks/` – Analysis & Debugging

Contains Databricks/Zeppelin notebooks for:

* Profiling new sources
* Data quality explorations
* KPI validation and stakeholder walkthroughs

Naming pattern: `explore_<source>.ipynb`

---

## 🧰 5. `utils/` – Shared Functions

Reusable modules for:

* Spark validation logic (e.g., null checks, schema match)
* Great Expectations integration
* Metadata reading
* Logging and alerting

**Key files:**

* `validator.py`
* `metadata_reader.py`
* `alert_slack.py`
* `spark_utils.py`

---

## ✅ Best Practices

| Area                     | Practice                                                   |
| ------------------------ | ---------------------------------------------------------- |
| File Naming              | `verb_source_context.py` (`ingest_crm_applications.py`)    |
| Function Reuse           | Move generic logic to `utils/`                             |
| Parameterization         | Metadata-driven (via `job.csv`, `proc_param.csv`)          |
| Delta Lake Usage         | Bronze → Silver → Gold format                              |
| Data Contract Compliance | Schema validation via JSON or Great Expectations           |
| Modularity               | Break up large flows by domain (Customer, Loans, Products) |


