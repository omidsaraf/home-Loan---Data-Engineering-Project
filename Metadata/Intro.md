
This directory holds **core metadata files** that drive the orchestration, parameterization, and processing logic of the HomeLoanIQ data engineering pipelines. These files enable **declarative, reusable, and scalable workflows** supporting batch and streaming ingestion, transformation, and extraction.

---

## 📁 Files Overview

| File Name       | Purpose                                              |
|-----------------|------------------------------------------------------|
| `job.csv`       | Defines pipeline jobs, scheduling, and dependencies  |
| `proc.csv`      | Maps processing steps to notebooks/scripts           |
| `proc_param.csv`| Specifies parameters injected into processing steps  |

---

## 📝 Metadata File Details

### 1. `job.csv` – Pipeline Job Configuration

- Lists all data engineering jobs with metadata:
  - **Job ID** and **Name**
  - **Schedule** (cron expressions or event triggers)
  - **Dependencies** (job sequencing)
  - **Type** (batch, streaming)
  - **Owner** and **Environment** (Dev/Test/Prod)
- Enables orchestrators (Airflow, ADF) to programmatically build DAGs and manage execution.

### 2. `proc.csv` – Process to Notebook/Script Mapping

- Maps logical processing steps (e.g., ingestion, bronze transform, silver transform) to:
  - Notebook file paths or script references
  - Execution order within a job
  - Retry policies and timeout configurations
- Supports metadata-driven modular pipeline execution and reusability.

### 3. `proc_param.csv` – Parameter Injection

- Defines dynamic parameters passed into notebooks/scripts, such as:
  - Date ranges (`start_date`, `end_date`)
  - Environment-specific variables (`env`, `cluster_name`)
  - Feature toggles and flags
- Allows flexible, context-aware execution without code changes.

---

## 🔧 Usage & Integration

- These metadata files are **loaded at pipeline runtime** by orchestration engines (Airflow, ADF).
- Enable **dynamic DAG construction** and **parameterized notebook executions** in Databricks.
- Facilitate environment promotion by changing parameters rather than code.
- Support **auditability** by logging executed jobs, parameters, and statuses.

---

## 🛠️ Best Practices

| Practice                    | Description                                  |
|-----------------------------|----------------------------------------------|
| Declarative Configurations | Manage orchestration logic outside code      |
| Version Control             | Store metadata in Git for traceability       |
| Environment Separation     | Use parameters to switch Dev/Test/Prod modes  |
| Validation                  | Implement schema and data validation on CSVs |
| Documentation               | Keep metadata files well-documented and consistent |

---

## 📚 Related Modules

- [`pipelines/`](../pipelines/) – Orchestration scripts and templates leveraging metadata
- [`src/ingestion/`](../ingestion/) – Processing scripts referenced by `proc.csv`
- [`src/transformation/`](../transformation/) – Transformation notebooks parameterized by metadata

---
