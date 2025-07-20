## ✅ Databricks Workflow: `HomeLoanIQ_MetadataDriven_Pipeline`

```json
{
  "name": "HomeLoanIQ_MetadataDriven_Pipeline",
  "job_clusters": [
    {
      "job_cluster_key": "shared_cluster",
      "new_cluster": {
        "spark_version": "13.3.x-scala2.12",
        "node_type_id": "Standard_DS3_v2",
        "num_workers": 2,
        "custom_tags": {
          "project": "HomeLoanIQ"
        },
        "spark_conf": {
          "spark.databricks.delta.preview.enabled": "true"
        },
        "aws_attributes": {},
        "azure_attributes": {
          "first_on_demand": 1,
          "availability": "ON_DEMAND_AZURE"
        }
      }
    }
  ],
  "timeout_seconds": 3600,
  "max_concurrent_runs": 1,
  "tasks": [
    {
      "task_key": "ingest_batch_csv",
      "notebook_task": {
        "notebook_path": "/Projects/HomeLoanIQ/nb_01_ingest_batch_csv",
        "base_parameters": {
          "job_name": "homeloan_ingest_batch_csv"
        }
      },
      "job_cluster_key": "shared_cluster"
    },
    {
      "task_key": "ingest_stream_kafka",
      "notebook_task": {
        "notebook_path": "/Projects/HomeLoanIQ/nb_02_ingest_stream_kafka",
        "base_parameters": {
          "job_name": "homeloan_ingest_stream_kafka"
        }
      },
      "job_cluster_key": "shared_cluster"
    },
    {
      "task_key": "stage_to_bronze_batch",
      "depends_on": [
        { "task_key": "ingest_batch_csv" }
      ],
      "notebook_task": {
        "notebook_path": "/Projects/HomeLoanIQ/nb_03_stage_to_bronze_batch",
        "base_parameters": {
          "job_name": "homeloan_stage_to_bronze_batch"
        }
      },
      "job_cluster_key": "shared_cluster"
    },
    {
      "task_key": "bronze_to_silver_stream",
      "depends_on": [
        { "task_key": "ingest_stream_kafka" }
      ],
      "notebook_task": {
        "notebook_path": "/Projects/HomeLoanIQ/nb_04_bronze_to_silver_stream",
        "base_parameters": {
          "job_name": "homeloan_bronze_to_silver_stream"
        }
      },
      "job_cluster_key": "shared_cluster"
    },
    {
      "task_key": "silver_to_gold_unified",
      "depends_on": [
        { "task_key": "stage_to_bronze_batch" },
        { "task_key": "bronze_to_silver_stream" }
      ],
      "notebook_task": {
        "notebook_path": "/Projects/HomeLoanIQ/nb_05_silver_to_gold_unified",
        "base_parameters": {
          "job_name": "homeloan_silver_to_gold_unified"
        }
      },
      "job_cluster_key": "shared_cluster"
    },
    {
      "task_key": "export_gold_to_tableau",
      "depends_on": [
        { "task_key": "silver_to_gold_unified" }
      ],
      "notebook_task": {
        "notebook_path": "/Projects/HomeLoanIQ/nb_06_export_gold_to_tableau",
        "base_parameters": {
          "job_name": "homeloan_export_gold_to_tableau"
        }
      },
      "job_cluster_key": "shared_cluster"
    }
  ],
  "format": "MULTI_TASK"
}
```

---

## 🧠 Key Highlights

* **Metadata-Driven**: Every notebook uses `job_name` to look up parameters from your `Process_Metadata` and `Process_Parameter_Metadata` tables.
* **Modular DAG**: You can run each task independently or as a full chain.
* **Parallel**:

  * Stream and batch ingestion run in parallel.
  * Downstream dependencies wait for respective parents.
* **Cluster Reuse**: `shared_cluster` minimizes cost and boosts efficiency.
* **Scheduling**: Can be configured via UI or `schedule` block in JSON for daily/hourly/triggered.

---

## 📍 How to Use

1. Save this JSON in a file called `home_loaniq_workflow.json`.
2. Upload or create via:

   * Databricks UI → Jobs → Create Job → Import JSON.
   * Or REST API / Terraform / Databricks CLI.

---
