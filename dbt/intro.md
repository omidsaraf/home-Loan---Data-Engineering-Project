
This directory contains **dbt project artifacts** that implement the **business logic and KPI transformations** for the HomeLoanIQ platform’s Gold layer. It follows modern **dbt best practices** to ensure maintainable, testable, and documented analytics models.

---

## 📁 Directory Structure

```plaintext
src/
└── dbt/
    ├── models/        # Modular SQL models defining KPIs, facts, dimensions
    ├── snapshots/     # Historical snapshots for slowly changing dimensions (SCDs)
    └── tests/         # Custom dbt tests and schema validations
````

---

## 🏗️ Project Overview

* **Models**: Defines reusable, modular SQL models encapsulating KPIs such as loan approval rates, disbursement velocity, default risk, and borrower segmentation.
* **Snapshots**: Implements SCD Type 2 logic for key entities (customers, loans, branches) enabling historical trend analysis.
* **Tests**: Enforces data integrity with built-in and custom dbt tests (uniqueness, not null, referential integrity).

---

## 📂 Directory Details

### 1. `models/` – Modular KPI Logic

* Organize models by domain: e.g., `loan_metrics.sql`, `customer_segments.sql`, `branch_performance.sql`
* Use **CTEs** and macros to modularize SQL and improve readability
* Apply **configurations** for materializations (`table`, `view`, or `incremental`) based on use case
* Document models inline with dbt’s built-in **description** fields for auto-generated docs

### 2. `snapshots/` – Historical Entity Tracking

* Capture slowly changing dimension states (SCD Type 2) for customers, loans, and branches
* Version entity attributes over time for auditability and lineage
* Use dbt snapshots’ **unique key** and **updated\_at** fields for change detection

### 3. `tests/` – Data Quality & Integrity

* Use **dbt built-in tests** for uniqueness, not null, accepted values, and relationships
* Implement **custom tests** to validate KPIs thresholds and anomalies
* Run tests automatically during CI/CD to enforce quality gates

---

## 🎯 Key Best Practices

| Aspect               | Implementation                                                |
| -------------------- | ------------------------------------------------------------- |
| **Modularity**       | Small, composable models; reusable macros                     |
| **Documentation**    | Use `description` metadata for automated docs                 |
| **Testing**          | Extensive schema and data tests, custom KPI checks            |
| **Versioning**       | Snapshot SCDs for full audit trail                            |
| **Materializations** | Use incremental for large tables, views for fast querying     |
| **Security**         | Access control via Unity Catalog and Row Level Security (RLS) |

---

## 🚀 Integration & Deployment

* Models are triggered via **CI/CD pipelines** post-ingestion and transformation layers
* Use `dbt run`, `dbt test`, and `dbt docs generate` as part of automated workflows
* Document lineage and dependencies within dbt DAG for transparency and impact analysis

---

## 🧩 Additional Resources

* [dbt Documentation](https://docs.getdbt.com/)
* [dbt Best Practices Guide](https://docs.getdbt.com/docs/building-a-dbt-project/best-practices)
* [HomeLoanIQ Data Governance Policies](../../docs/data_governance.md)

---
