
This module exposes **governed, real-time APIs** using **FastAPI** to deliver business-ready, Gold-layer metrics—like **customer KPIs**, **influence networks**, and **risk scores**—to digital banking platforms, Salesforce, internal portals, and fraud analytics tools.

---

## 📁 Directory Structure

```plaintext
extraction/
└── application_apis/
    ├── main.py                       # FastAPI app entry point
    ├── api/
    │   ├── endpoints/
    │   │   ├── kpi.py                # Customer KPI endpoints
    │   │   └── influence_scores.py   # Customer influence graph endpoints
    │   └── dependencies.py           # Auth, SparkSession, config loaders
    ├── models/                       # API request/response schemas
    ├── utils/
    │   ├── spark_session.py          # Delta SparkSession loader
    │   └── logger.py                 # Structured logging setup
    ├── configs/
    │   └── api_config.yaml           # Metadata-driven routing config
    ├── requirements.txt              # Python dependencies
    └── Dockerfile                    # Containerization for deployment
```

---

## 🚀 Capabilities at a Glance

| Feature                | Details                                                             |
| ---------------------- | ------------------------------------------------------------------- |
| **Framework**          | FastAPI with automatic OpenAPI docs & async handlers                |
| **Data Source**        | Reads Delta tables (`gold_customer_kpi`, `gold_customer_influence`) |
| **Execution Engine**   | Uses PySpark in a Databricks runtime or Spark-on-K8s                |
| **Security**           | OAuth2, Azure AD tokens, Unity Catalog role-based masking           |
| **Metadata-Driven**    | YAML config to define endpoints, masking, and RBAC                  |
| **Logging & Auditing** | API access logs tracked by request ID, sent to Azure Monitor        |

---

## 🧪 Example: Influence Graph Endpoint (`influence_scores.py`)

```python
from fastapi import APIRouter, Depends
from utils.spark_session import get_spark
from api.dependencies import authorize_user

router = APIRouter()

@router.get("/influence/top_customers", tags=["Influence Scores"])
def get_top_influencers(limit: int = 10, user=Depends(authorize_user)):
    spark = get_spark()
    df = spark.table("gold_customer_influence")
    top_df = df.orderBy("page_rank", ascending=False).limit(limit)
    return top_df.toPandas().to_dict(orient="records")
```

---

## 🔐 Enterprise-Grade Security

| Layer              | Description                                                          |
| ------------------ | -------------------------------------------------------------------- |
| Authentication     | OAuth2 / Azure AD + JWT token validation                             |
| Authorization      | Role-based access via Unity Catalog or external RBAC engine          |
| PII Protection     | Configurable masking on sensitive fields (phone, email, DOB, etc.)   |
| Secrets Management | Secure token handling using Azure Key Vault or environment variables |
| Audit Logging      | Logs stored per endpoint with timestamps and user IDs                |

---

## 📂 Example Metadata Config (`configs/api_config.yaml`)

```yaml
endpoints:
  - path: /kpis/customer_summary
    source: gold_customer_kpi
    auth_required: true
    masking: true
    limit: 100

  - path: /influence/top_customers
    source: gold_customer_influence
    auth_required: true
    limit: 50

roles:
  analyst:
    access:
      - /kpis/customer_summary

  fraud_investigator:
    access:
      - /influence/top_customers
```

---

## 🔁 Platform Integration

| Component               | Role                                                       |
| ----------------------- | ---------------------------------------------------------- |
| **Delta Lake**          | Gold-layer data source, versioned & ACID-compliant         |
| **SparkSession**        | All APIs run Spark SQL via shared `spark_session.py`       |
| **Unity Catalog**       | Secure access control and field-level masking              |
| **Airflow / Workflows** | Trigger FastAPI deployment or refresh Gold layer if needed |
| **Docker**              | Deployment-ready container (`Dockerfile`)                  |

---

## 🧪 Unit Test: `tests/test_influence_scores.py`

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

