
This module contains **RESTful Python APIs** built using **FastAPI** (or Flask), which expose curated Gold-layer datasets—like KPIs, customer influence scores, and default risk metrics—to operational apps, portals, and external systems. It enables **secure**, **governed**, and **real-time data access** from the HomeLoanIQ platform.

---

## 📁 Directory Structure

```plaintext
src/
└── extraction/
    └── application_apis/
        ├── main.py                      # API entrypoint
        ├── routers/
        │   ├── kpi_metrics.py           # Endpoints for KPIs
        │   ├── influence_scores.py      # Endpoints for graph-based metrics
        │   └── customer_profiles.py     # Customer profile exposure
        ├── services/
        │   ├── data_loader.py           # Functions to query Delta tables via Spark SQL
        │   └── security.py              # OAuth2, RBAC, masking utilities
        ├── configs/
        │   └── api_config.yaml          # Metadata for endpoints and auth
        └── utils/
            └── logger.py                # Logging and tracing helpers
```

---

## 🚀 Key Capabilities

| Feature                 | Description                                                               |
| ----------------------- | ------------------------------------------------------------------------- |
| **FastAPI Framework**   | Fully async, OpenAPI-documented, highly performant API base               |
| **Spark SQL Backend**   | APIs query gold-layer Delta tables using Spark SQL from within Databricks |
| **RBAC & OAuth2**       | Auth & authorization via Azure AD or Keycloak tokens                      |
| **Metadata-Driven**     | Endpoints, parameters, roles defined in external YAML config              |
| **Secure PII Exposure** | Masking logic (phone, email, names) applied via metadata or view logic    |
| **Logging & Tracing**   | API usage monitored with request IDs and alerts via Azure Monitor         |

---

## ✨ Example: `/routers/influence_scores.py`

```python
from fastapi import APIRouter, Depends
from services.data_loader import load_gold_table
from services.security import authorize_user

router = APIRouter()

@router.get("/influence/top_customers", tags=["Influence Scores"])
def get_top_influencers(limit: int = 10, user=Depends(authorize_user)):
    df = load_gold_table("gold_customer_influence_scores")
    top = df.orderBy("page_rank", ascending=False).limit(limit).toPandas()
    return top.to_dict(orient="records")
```

---

## 🔐 Security Best Practices

| Layer              | Mechanism                                        |
| ------------------ | ------------------------------------------------ |
| Authentication     | OAuth2 / Azure AD                                |
| Authorization      | Role-based logic via Unity Catalog roles         |
| PII Masking        | Masking by view (`with_mask`, `no_mask`) or code |
| Secrets Management | Azure Key Vault for DB tokens and API keys       |
| Audit Logging      | Logged via `utils/logger.py` and sent to Azure   |

---

## ⚙️ Metadata Config Example (`configs/api_config.yaml`)

```yaml
endpoints:
  - path: /kpis/daily
    source: gold_kpi_daily
    auth_required: true
    masking: true
  - path: /influence/top_customers
    source: gold_customer_influence_scores
    auth_required: true
    limit: 100

roles:
  analyst:
    access:
      - /kpis/daily
  fraud_analyst:
    access:
      - /influence/top_customers
```

---

## 🔁 Integration with Data Platform

* Reads from **Delta tables** in the Gold layer via **SparkSession** or SQL endpoints.
* API access is **token-based** and governed using **Unity Catalog roles**.
* Triggered and monitored via **Airflow DAGs** or **Databricks Workflows** with metadata-driven job parameters.

---

## 🧪 Test Example (`tests/test_influence_scores.py`)

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_top_influencers():
    response = client.get("/influence/top_customers?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "page_rank" in response.json()[0]
```

---

