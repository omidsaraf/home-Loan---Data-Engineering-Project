
This directory implements **advanced graph-based data modeling and analytics** to support **customer influence networks**, **relationship discovery**, and **entity resolution** for the HomeLoanIQ platform.

---

## 📁 Directory Structure

```plaintext
src/
└── graph_modeling/
    └── customer_influence_network.py   # Graph construction & analytics pipeline
````

---

## 🧠 Overview

* Utilize **graph theory** and **network analytics** to uncover hidden relationships among borrowers, guarantors, branches, and external entities.
* Implement **entity resolution** to deduplicate and link customer records across heterogeneous sources.
* Support **fraud detection**, **referral analysis**, and **risk propagation modeling** through graph insights.
* Leverage scalable graph processing frameworks (e.g., GraphFrames on Spark, NetworkX for small-scale) within PySpark ecosystem.

---

## 🔍 `customer_influence_network.py`

### Core Features:

* Constructs multi-hop **customer influence graphs** using loan co-signers, referrals, and social connections.
* Calculates **centrality metrics** (degree, betweenness, closeness) to identify key influencers.
* Performs **community detection** to segment borrowers by influence clusters.
* Integrates with upstream Silver-layer cleansed entities for enriched node attributes.
* Outputs graph metrics as Delta Lake tables for downstream ML models and dashboards.

### Example Workflow:

```python
from graphframes import GraphFrame

# Load nodes and edges from Silver layer tables
vertices = spark.table("silver_customers")
edges = spark.table("silver_customer_relationships")

# Build GraphFrame
g = GraphFrame(vertices, edges)

# Run PageRank or community detection
results = g.pageRank(resetProbability=0.15, maxIter=10)

# Persist results to Gold layer for KPI aggregation
results.vertices.write.format("delta").mode("overwrite").save("/mnt/gold/customer_influence")
```

---

## 🛡️ Best Practices & Governance

| Focus Area       | Implementation Details                                          |
| ---------------- | --------------------------------------------------------------- |
| **Data Quality** | Validate input graphs for missing nodes/edges                   |
| **Scalability**  | Use distributed graph processing (GraphFrames)                  |
| **Privacy**      | Mask PII on graph nodes, restrict access via Unity Catalog ACLs |
| **Traceability** | Log graph build runs with timestamps and job IDs                |
| **Reusability**  | Modular functions for graph construction & metrics              |

---

## 📈 Use Cases

* **Risk propagation modeling** for loan default risk assessment
* **Referral influence scoring** to boost marketing campaigns
* **Fraud detection** by uncovering suspicious networks
* **Customer segmentation** for personalized offers

---

## 🔧 Dependencies

* Apache Spark with GraphFrames package
* PySpark
* Delta Lake for graph output storage
* Azure Databricks environment with Unity Catalog for governance

---

## 📚 Related Modules

* [`src/transformation/silver/`](../transformation/silver/) – Cleaned entity views feeding graph nodes
* [`src/dbt/`](../dbt/) – KPI aggregation models consuming graph metrics
* [`metadata/`](../../metadata/) – Config files for graph job orchestration

---

