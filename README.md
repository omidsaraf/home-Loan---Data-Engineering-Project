# 🏠 HomeLoanIQ – Loan Approval & Risk Monitoring with Customer Influence

**HomeLoanIQ** is a modular, metadata-driven data platform that modernizes the end-to-end **home loan analytics lifecycle**. Designed for scale, it enables real-time and batch data ingestion, **customer risk prediction through graph modeling**, and **enterprise-grade KPI monitoring** through streamlined APIs and dashboards.

---
### 🔎 Why Risk Monitoring with Customer Influence Matters

Traditional risk scoring treats each borrower as independent. But in reality, borrowers form **influence networks** via:
- 🔗 Referrals (agents, staff, family)
- 👥 Co-applicants and guarantors
- 🏢 Shared employment or branch origin

When an influential borrower misses a payment, **risk propagates** to others they’re linked to — often before defaults occur.

> HomeLoanIQ uses **graph analytics** to uncover these indirect risks, calculate influence scores, and enable **early intervention**.

This enhances:
- 📉 NPL (Non-Performing Loan) prevention
- 🔍 Risk clustering and subnetwork tracing
- 📈 Performance visibility at staff/branch level

---
<img width="1244" height="468" alt="image" src="https://github.com/user-attachments/assets/09c3cb8f-bbf9-4229-83ea-71e4922dc6f0" />

---

## 📚 Table of Contents

1. [💼 Executive Summary](#-executive-summary)
2. [🎯 Business Objectives](#-business-objectives)
3. [🏗️ Architecture Overview](#-architecture-overview)
4. [📁 Repository Structure](#-repository-structure)
5. [📥 Ingestion Design (Batch & Streaming)](#-ingestion-design-batch--streaming)
6. [🧱 Data Modeling (Bronze → Silver → Gold)](#-data-modeling-bronze--silver--gold)
7. [🔗 Graph Data Modeling Layer](#-graph-data-modeling-layer)
8. [📊 Extraction](#-extraction)
9. [🔐 Governance, Metadata & Security](#-governance-metadata--security)
10. [🚀 CI/CD & Deployment](#-cicd--deployment)
11. [🧪 Testing & Observability](#-testing--observability)
12. [📦 Containerization](#-containerization)
    [📄 License](#-license)

---

## 💼 Executive Summary

The **HomeLoanIQ** platform empowers banks and mortgage providers to:

- ✅ Accelerate the loan lifecycle through automation
- 🔍 Monitor default risks using real-time and historical insights
- 🧠 Enrich traditional models with **graph-based customer influence scores**
- 🔐 Ensure secure, governed access to sensitive customer data
- 📊 Serve insights via Seaborn dashboards, APIs, and CRM systems

---

## 🎯 Business Objectives

| Objective                  | Description                                                 |
|---------------------------|-------------------------------------------------------------|
| 📈 Optimize KPIs           | Approval rate, default detection, processing SLA            |
| 🔄 Real-time Monitoring    | Trigger alerts on live loan and influence activity          |
| 🔗 Influence-Aware Risk    | Proactively track social/branch-level exposure               |
| 🛡️ Regulatory Compliance  | Metadata, lineage, role-based access, and data contracts     |

---

## 🏗️ Architecture Overview

| Layer              | Tools / Technologies                                           |
|--------------------|---------------------------------------------------------------|
| Ingestion          | Azure Data Factory (batch), Kafka + PySpark (streaming)       |
| Transformation     | PySpark SQL (Bronze → Silver → Gold)                          |
| Graph Modeling     | GraphFrames, Delta Lake, PageRank, NetworkX                   |
| Serving            | Seaborn, Pandas, FastAPI                                      |
| Orchestration      | Apache Airflow (metadata-driven DAGs)                         |
| Metadata & Lineage | Unity Catalog, OpenLineage                                    |
| Deployment         | Docker, Azure DevOps, GitHub Actions                          |

---

## 📁 Repository Structure

```plaintext

├── Ingestion/
│   ├── adf_templates/               # Azure Data Factory JSON templates
│   ├── pyspark_streaming/           # Kafka streaming ingestion code
│   └── metadata_ingestion.py        # Metadata-driven ingestion orchestration
│
├── Transformation/
│   ├── bronze/                      # Raw data Spark SQL notebooks & tables
│   ├── silver/                      # Cleaned, enriched entity views & logic
│   └── gold/                        # KPI-ready aggregates and data marts
│
├── Graph_modeling/                 # Graph analytics & entity resolution logic
│   └── customer_influence_network.py
│
├── Extraction/
│   ├── Dashboard_views/             # SQL views for dashboard/BI use
│   └── Application_apis/            # FastAPI apps for KPI & influence metrics
│
├── Test/                           # PySpark + validation tests
│
Metadata/
│   └── jobs.csv, contracts.csv      # Metadata for pipelines and validation
```

---

## 📥 Ingestion Design (Batch & Streaming)

### Batch Sources

- Core Banking DB: Loan master, repayments, branches
- Salesforce CRM: Leads, agents, referrals
- Credit Bureau Files: CSV-based scoring & history

### Streaming Sources

- Kafka: Loan status, real-time decision events
- REST APIs: Mortgage calculator, property lookup

> All ingestion paths are controlled by metadata configs and DAG templates

---

## 🧱 Data Modeling (Bronze → Silver → Gold)

### 🥉 Bronze
- Raw schema-on-read format, partitioned by load date
- Retains source fidelity for auditing

### 🥈 Silver
- Validated, deduplicated, enriched data
- Consolidated customer entities with referential joins

### 🥇 Gold
- Ready-to-serve KPI models and influence metrics
- SQL modularity for maintainability and version control

---

## 🔗 Graph Data Modeling Layer

- Constructs influence networks using customer referrals, co-applicants, and loan agents
- Applies **PageRank**, **degree centrality**, and **community detection**
- Maps how influence spreads across borrowers and branches
- Outputs influence scores used in approval decisions and risk alerts

---

## 📊 Extraction

| KPI Name              | Description                                               |
|-----------------------|-----------------------------------------------------------|
| ApplicationVolume     | Daily loan applications per region                        |
| ApprovalRate          | Percentage of approved loans per day                      |
| ProcessingTime        | Time from submission to disbursal                         |
| DefaultRate           | Loans defaulted within 90 days of issue                   |
| DelinquencyBucket     | Categorized by 30/60/90+ days past due                    |
| RevenueForecast       | Predicted net revenue from active loans                   |
| BranchEfficiencyScore | SLA compliance × loan value × customer influence factor   |

- 📈 **Seaborn Dashboards**: In `extraction/Dashboard_views/`
- 🌐 **FastAPI Services**: Expose KPIs & influence insights via `/application_apis/`

---

## 🔐 Governance, Metadata & Security

| Feature           | Implementation                                         |
|-------------------|-------------------------------------------------------|
| Lineage           | Unity Catalog + OpenLineage integration               |
| Metadata Control  | CSV + JSON-based configs for job parameters           |
| Data Contracts    | Great Expectations + PySpark tests                    |
| Access Control    | Unity Catalog RBAC, token-based FastAPI auth          |
| PII Masking       | Column-level policies and role-based views            |
| Audit Trails      | Metadata tables log every job run and change         |

---

## 🚀 CI/CD & Deployment

- GitHub Actions: Automated build + test for every commit
- Azure DevOps: Promotion and deployment workflows
- Dockerized Spark & FastAPI apps deployed as services

---

## 🧪 Testing & Observability

| Check Type         | Tools Used                                    |
|--------------------|-----------------------------------------------|
| Schema & Null Checks | Great Expectations, PySpark assert tests     |
| Volume & SLA        | Airflow + metadata volume audits              |
| Alerts & Logging    | Prometheus + structured pipeline logging      |
| Regression Tests    | Snapshot diffs, test gold table outputs       |

---

## 📦 Containerization

- Spark jobs and APIs containerized with **Docker**
- External secrets managed with **Azure Key Vault**
- Deployable to cloud VMs, App Services, or private networks

## 📄 License

