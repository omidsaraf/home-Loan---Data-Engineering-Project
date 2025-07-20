This module enables **advanced graph analytics** to model **customer influence networks**, **relationship discovery**, and **entity resolution** on top of the HomeLoanIQ data platform.

---

## 📁 Directory Structure

```plaintext
src/
└── graph_modeling/
    └── customer_influence_network.py   # Core graph pipeline for influence & entity resolution
```

---

## 🧠 Overview

* Build **multi-hop graphs** capturing loan cosigners, referrals, guarantors, and branch relationships.
* Use **graph theory metrics** (PageRank, centrality, community detection) to find key influencers and clusters.
* Perform **entity resolution** to unify and deduplicate customer identities across diverse sources.
* Enable **fraud detection**, **risk propagation**, and **referral marketing** insights.
* Integrate with **Silver layer cleansed datasets** for enriched node/edge attributes.
* Persist graph outputs as **Delta Lake tables** for downstream ML and KPI models.

---

## 🔍 `customer_influence_network.py` Core Features

* Load graph nodes (customers) and edges (relationships) from Silver layer tables.
* Construct scalable graphs using **GraphFrames** on Spark.
* Compute metrics like **PageRank**, **degree**, **betweenness**, and **community detection**.
* Write results incrementally to Delta tables (`graph.referral_edges`, `graph.influence_scores`).
* Utilize **metadata-driven parameters** from `proc_param.csv` for batch scheduling and configuration.
* Apply **PII masking** and enforce **Unity Catalog row-level and column-level security**.
* Log process metadata in `job_metadata` and `proc_metadata` tables for audit and lineage.

---

## 🔨 Example Workflow (PySpark + GraphFrames)

```python
from graphframes import GraphFrame
from delta.tables import DeltaTable
from pyspark.sql.functions import current_timestamp

# Load vertices and edges from Silver layer
vertices = spark.table("silver.customers")
edges = spark.table("silver.customer_relationships")

# Build the graph
g = GraphFrame(vertices, edges)

# Run PageRank
results = g.pageRank(resetProbability=0.15, maxIter=10)

# Prepare output dataframe with timestamp for metadata logging
influence_scores_df = results.vertices.withColumn("processed_at", current_timestamp())

# Upsert results to Delta Lake table for influence scores
delta_table = DeltaTable.forName(spark, "graph.influence_scores")
(delta_table.alias("target")
 .merge(
    influence_scores_df.alias("source"),
    "target.customer_id = source.id AND target.processed_at = source.processed_at"
 )
 .whenMatchedUpdateAll()
 .whenNotMatchedInsertAll()
 .execute())
```

---

## 🛡️ Best Practices & Data Governance

| Focus Area       | Implementation Details                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| **Data Quality** | Validate vertices and edges for nulls, duplicates; reject incomplete records before graph construction     |
| **Scalability**  | Use distributed graph processing with GraphFrames; avoid small data local tools like NetworkX              |
| **Privacy**      | Mask sensitive fields (e.g., SSN, email) before graphing; enforce Unity Catalog ACLs and RLS on tables     |
| **Traceability** | Track job runs via `job_metadata` and `proc_metadata` tables with timestamps, status, and parameters       |
| **Reusability**  | Modularize graph construction and metric functions; use parameter-driven notebooks for batch and streaming |
| **Security**     | Use Unity Catalog to enable column-level masking and row-level filters on graph tables                     |

---

## 📈 Use Cases

* Risk propagation and default prediction enhancement
* Referral influence scoring for marketing targeting
* Fraud network detection via suspicious connectivity
* Customer segmentation by community clusters

---

## 🔧 Dependencies

* Apache Spark with GraphFrames library
* Delta Lake format on Azure Databricks with Unity Catalog
* Azure SQL Database for metadata tables
* PySpark for ETL and graph analytics
* Metadata-driven orchestration via Airflow/ADF/Databricks Workflows

---

