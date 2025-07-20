
## 📦 Final Delivery Layer for Business Consumption

This directory contains **modular, production-ready artifacts** that deliver curated and enriched datasets from the Gold layer to downstream consumers. These include **interactive Python dashboards**, **data APIs**, and **business-aligned reporting views**. It ensures **fast, secure, and governed access** to insights across the HomeLoanIQ platform.

---

## 📁 Directory Structure

```plaintext
src/
└── extraction/
    ├── dashboard_views/      # SQL views optimized for interactive Python/BI dashboards
    └── application_apis/     # Python APIs delivering curated Gold data to external apps
```

---

## 📊 `dashboard_views/` – BI-Optimized & Parameterized SQL Views

These SQL views serve as **semantic-ready layers** for data analysts, data scientists, and dashboard developers.

### ✅ Key Features:

* **KPI-ready** Delta SQL views: Includes pre-aggregated metrics like approval rates, default trends, top influencers.
* **Parameterized logic**: Views adapt to filters like region, product type, or date range using session variables or passthrough config.
* **Performance-optimized**:

  * Leverages **Gold-layer materialized tables**
  * Partitioning by `processing_date` and customer segments
  * Uses **summary tables** for fast loading
* **Governed** via Unity Catalog:

  * PII masking
  * View-specific ACLs based on consumer roles

### 📘 Example Views:

| View Name                    | Description                                 |
| ---------------------------- | ------------------------------------------- |
| `vw_dashboard_kpi_summary`   | Daily approval and default rate KPIs        |
| `vw_influence_top_customers` | Top 100 customers by influence score        |
| `vw_monthly_volume_metrics`  | Monthly loan volume and default counts      |
| `vw_graph_metrics`           | Precomputed graph centralities and clusters |

---

## 🚀 `application_apis/` – Secure Python APIs for Embedded Consumption

This module provides **RESTful Python APIs** built using **FastAPI** or **Flask**, deployed on Azure Kubernetes Services or Azure Functions. They expose business data for use in apps like:

* Customer onboarding UIs
* Salesforce enrichment tools
* Internal risk & fraud monitoring tools

### 🔐 Security Features:

* OAuth2 and Azure AD authentication with token validation
* Role-based access control (RBAC) tied to Unity Catalog
* PII masking and logging of access attempts via Azure Monitor

### 🧠 Key Capabilities:

| Feature       | Description                                         |
| ------------- | --------------------------------------------------- |
| Pagination    | Efficient scroll and slicing of large result sets   |
| Filtering     | On fields like date range, region, loan type        |
| Caching       | API-level caching with TTL and freshness checks     |
| Observability | Logging, tracing, and alerting integrated via Azure |

---

## 🛠️ Development Best Practices

| Focus              | Implementation Highlights                                 |
| ------------------ | --------------------------------------------------------- |
| **Modular Design** | SQL views split by KPI domain; APIs split by service path |
| **Testing**        | Unit tests for SQL logic and FastAPI test clients         |
| **CI/CD**          | Automated deployments using GitHub Actions                |
| **Performance**    | Delta caching, partitioned queries, query hints           |
| **Documentation**  | YAML data contracts, OpenAPI specs for APIs               |
| **Compliance**     | GDPR masking, encrypted secrets via Key Vault             |

---

## 🔗 Integration Points

* **Python Dashboards (Streamlit/Plotly/Seaborn)**: Consume `vw_dashboard_*` views via Databricks or JDBC
* **Data APIs**: Pull from Gold-layer KPIs and graph outputs (`customer_influence_metrics`, `loan_kpi_daily`, etc.)
* **Pipeline Orchestration**: Extraction processes triggered via **Databricks Workflows** and **Airflow DAGs** using metadata

---
