# 📥 `src/ingestion/` – Unified Data Ingestion Framework

This directory implements **metadata-driven, enterprise-grade ingestion pipelines** for the HomeLoanIQ platform, enabling ingestion from both batch and streaming data sources. It adheres to **data quality, governance, and operational excellence standards** aligned with banking regulations and scalable FinTech architecture.

---

## 📁 Directory Structure

```plaintext
src/
└── ingestion/
    ├── adf_templates/           # Batch ingestion templates (Azure Data Factory)
    ├── pyspark_streaming/       # Real-time PySpark ingestion from Kafka
    └── metadata_ingestion.py    # Unified metadata-based ingestion driver
````

---

## 🔄 1. `adf_templates/` – Batch Ingestion (ADF)

Contains parameterized **Azure Data Factory JSON templates** that ingest data from:

* 📂 **Core banking systems** (loan book, repayments)
* 📊 **Salesforce CRM** (loan leads, interactions)
* 🧾 **External sources** (credit bureaus, property APIs)

### 🔧 Features

| Feature                      | Description                                     |
| ---------------------------- | ----------------------------------------------- |
| Modular Datasets & Pipelines | Reusable ADF templates with parameter injection |
| Retry & Timeout Policies     | Fault tolerance and SLA handling                |
| Source/Target Abstraction    | Controlled via metadata configuration files     |
| Audit & Logging              | Azure Monitor integration                       |

> ✅ All pipelines use metadata (`job.csv`, `proc.csv`) for dynamic binding and config validation.

---

## ⚡ 2. `pyspark_streaming/` – Real-time Kafka Ingestion

Includes **PySpark Structured Streaming** jobs for Kafka topics such as:

* `loan_applications`
* `customer_engagement`
* `approval_events`
* `loan_disbursements`

### 🔧 Capabilities

* Schema-on-read + schema evolution
* Delta Lake streaming sink with checkpointing
* PII redaction and GDPR-compliant handling
* DLQ (Dead Letter Queue) for invalid/malformed records
* Streaming expectations validated via **Great Expectations**

### 📌 Example Flow

```python
spark.readStream \
  .format("kafka") \
  .option("subscribe", "loan_applications") \
  .load() \
  .transform(parse_and_validate) \
  .writeStream \
  .format("delta") \
  .option("checkpointLocation", "...") \
  .start("/mnt/bronze/loan_apps")
```

---

## 📋 3. `metadata_ingestion.py` – Metadata-Driven Controller

A **centralized PySpark ingestion driver** that dynamically controls batch and stream pipelines using configuration files.

### 🗂️ Metadata Inputs

| File Name        | Purpose                                      |
| ---------------- | -------------------------------------------- |
| `job.csv`        | Defines job ID, type, frequency, enable flag |
| `proc.csv`       | Source → target mappings                     |
| `proc_param.csv` | Column transformations, lookups, validations |

### 🧠 Highlights

* Add or modify ingestion jobs **without touching code**
* Built-in logging, audit, SLA breach alerting
* Secure path masking using Azure Key Vault
* Scales horizontally across new data sources

### 🔁 Usage

```bash
python metadata_ingestion.py \
  --job_id HL_DISBURSEMENTS \
  --env dev \
  --config metadata/job.csv
```

---

## 🛡️ Governance & Quality Controls

| Area             | Implementation Details                          |
| ---------------- | ----------------------------------------------- |
| **Data Quality** | Great Expectations for schema and null checks   |
| **Security**     | AKV + Unity Catalog column-level ACLs           |
| **Lineage**      | Auto-traced via metadata configs and audit logs |
| **Idempotency**  | Delta Lake UPSERTs using `merge` logic          |
| **Logging**      | Azure Monitor + custom ingestion audit trail    |

---

## 🌍 Compliance & Scale

This ingestion architecture adheres to:

* 🔐 **Banking security regulations** (RBAC, PII redaction)
* 📈 **Operational scalability** (Kafka partitioning, ADF concurrency)
* 📑 **Metadata traceability** (pipeline and transformation-level logging)
* 🧪 **Data contracts** enforced at ingestion boundary

---

## 🔮 Future Roadmap

* [ ] Kafka → Delta Live Tables integration
* [ ] Streaming alerting to Slack/MS Teams
* [ ] Real-time schema drift detection with Prometheus + Airflow
* [ ] Auto-document ingestion lineage for dbt + Unity Catalog

