# 🏠 HomeLoanIQ – Loan Approval & Risk Monitoring with Customer Influence

**HomeLoanIQ** is a scalable, metadata-driven data platform designed to analyze and optimize the **home loan lifecycle** within large financial institutions. It supports **real-time and batch ingestion**, leverages **graph-based customer influence modeling**, provides **KPI-driven modular SQL transformations**, and enforces **enterprise-grade data governance** and security.

<img width="1006" height="424" alt="image" src="https://github.com/user-attachments/assets/f301b823-71ff-4356-aae2-9a76aba30ddc" />


---

## 📚 Table of Contents

1. [💼 Executive Summary](#-executive-summary)
2. [🎯 Business Objectives](#-business-objectives)
3. [🏗️ Architecture Overview](#-architecture-overview)
4. [📁 Repository Structure](#-repository-structure)
5. [📥 Ingestion Design (Batch & Streaming)](#-ingestion-design-batch--streaming)
6. [🧱 Data Modeling (Bronze → Silver → Gold)](#-data-modeling-bronze--silver--gold)
7. [🔗 Graph Data Modeling Layer](#-graph-data-modeling-layer)
8. [📊 KPIs & Gold Layer Examples](#-kpis--gold-layer-examples)
9. [🔐 Governance, Metadata & Security](#-governance-metadata--security)
10. [🚀 CI/CD & Deployment](#-cicd--deployment)
11. [🧪 Testing & Observability](#-testing--observability)
12. [📦 Containerization](#-containerization)
---

## 💼 Executive Summary

The **HomeLoanIQ** platform empowers banks and mortgage lenders to:

* ✅ Accelerate loan application to disbursal cycles
* 📊 Monitor portfolio health, delinquency, and risk metrics in near real-time
* 🧠 Incorporate predictive ML models enriched by graph-based customer insights
* 🔗 Deliver governed, secure, and auditable data pipelines to BI tools, APIs, and CRM systems
* ⚙️ Seamlessly integrate with Tableau, Salesforce, and RESTful APIs via a unified data mesh

---

## 🎯 Business Objectives

| Goal                        | Description                                               |
| --------------------------- | --------------------------------------------------------- |
| 📈 Loan Lifecycle KPIs      | Improve approval rates and reduce non-performing assets   |
| 🔄 Real-time Processing     | Support streaming ingestion for near real-time dashboards |
| 🧱 Data Lineage & Quality   | Ensure traceability and validation of all transformations |
| 🛡️ Governance & Compliance | Enforce role-based access, masking, and audit policies    |

---

## 🏗️ Architecture Overview

| Layer              | Tools / Technologies                                         |
| ------------------ | ------------------------------------------------------------ |
| Ingestion          | Azure Data Factory (batch), PySpark + Kafka (streaming)      |
| Transformation     | Spark SQL (Bronze → Gold)                                    |
| Graph Modeling     | GraphFrames + Delta Lake for customer influence networks     |
| Serving            | Tableau, Power BI, Salesforce APIs, FastAPI application APIs |
| Orchestration      | Airflow DAGs driven by metadata configurations               |
| Metadata & Lineage | Unity Catalog, OpenLineage integration                       |
| Deployment         | Docker containers, Azure DevOps, GitHub Actions              |

---

## 📁 Repository Structure

```plaintext
src/
├── ingestion/
│   ├── adf_templates/               # Azure Data Factory JSON templates
│   ├── pyspark_streaming/           # Kafka streaming ingestion code
│   └── metadata_ingestion.py        # Metadata-driven ingestion orchestration
│
├── transformation/
│   ├── bronze/                      # Raw data Spark SQL notebooks & tables
│   ├── silver/                      # Cleaned, enriched entity views & logic
│   └── gold/                        # KPI-ready aggregates and data marts
│
├── graph_modeling/                 # Graph analytics & entity resolution logic
│   └── customer_influence_network.py
│
├── extraction/
│   ├── tableau_views/              # SQL views optimized for BI consumption
│   └── application_apis/           # FastAPI-based REST APIs exposing gold data
│
metadata/
│   └── job.csv, proc.csv, proc_param.csv   # Metadata configurations
```

---

## 📥 Ingestion Design (Batch & Streaming)

**Batch Sources**

* Core Banking DB (Loan Book, Repayment History)
* Credit Bureau CSVs (Risk Scores)
* Salesforce CRM (via REST API)

**Streaming Sources**

* Kafka (Application events, status updates)
* REST APIs (Mortgage calculators, property lookup)

> All ingestion pipelines are metadata-driven with Airflow-managed DAGs and parameterized job configs.

---

## 🧱 Data Modeling (Bronze → Silver → Gold)

### Bronze Layer

* Raw, schema-on-read Delta tables partitioned by ingestion date
* No transformations except schema validation and archival

### Silver Layer

* Cleaned, de-duplicated, enriched data (joined with credit bureau, property values)
* Entity resolution and denormalized entity tables

### Gold Layer

* Aggregated KPIs and curated views consumed by BI, APIs, and ML pipelines
* Modular SQL artifacts with thorough testing and documentation

---

## 🔗 Graph Data Modeling Layer

* Uses GraphFrames to build customer influence and risk propagation networks
* Models multi-hop relationships: borrowers, guarantors, branches, referrals
* Calculates centrality, community detection, and risk scoring metrics
* Outputs stored in Delta Lake for ML feature generation and dashboards

---

## 📊 KPIs & Gold Layer

| KPI Name              | Description                                          |
| --------------------- | ---------------------------------------------------- |
| ApplicationVolume     | Number of applications per day per region            |
| ApprovalRate          | Percentage of approved loans over total applications |
| ProcessingTime        | Average duration from application to disbursal       |
| DefaultRate           | Percentage of loans defaulted within 90 days         |
| DelinquencyBucket     | Segmentation by days past due (30/60/90+ DPD)        |
| RevenueForecast       | Earnings forecast based on net interest spread       |
| BranchEfficiencyScore | Composite KPI combining SLA, loan size, and risk     |




---

## 🔐 Governance, Metadata & Security

| Feature         | Implementation                                   |
| --------------- | ------------------------------------------------ |
| Data Lineage    | Unity Catalog, OpenLineage, Airflow DAG tracking |
| Data Contracts  | Great Expectations rules, PySpark tests          |
| Access Control  | Unity Catalog RBAC, Azure Key Vault, ACLs        |
| PII Masking     | Column-level security policies, dynamic masking  |
| Audit & Logging | Usage logs, metadata-driven job auditing         |

---

## 🚀 CI/CD & Deployment

* Azure DevOps and GitHub Actions pipelines automate testing and deployment
* Docker containers host Spark jobs and APIs
* Infrastructure as Code provisions data lake and compute resources

---

## 🧪 Testing & Observability

| Validation Type    | Tools                                  |
| ------------------ | -------------------------------------- |
| Schema Validation  | Great Expectations, PySpark tests      |
| Volume & Freshness | Airflow SLAs, freshness monitors       |
| Alerting           | Prometheus + Grafana monitoring        |
| Regression QA      | Snapshot diffs and contract validation |

---

## 📦 Containerization

* Spark jobs containerized via Docker
* FastAPI apps serve dashboards and APIs behind load balancers
* Secrets managed with Azure Key Vault, deployed via secure pipelines

---

## 📄 License


