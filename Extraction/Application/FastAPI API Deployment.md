a complete production-ready `docker-compose.yaml` to run your **HomeLoanIQ API container** alongside optional supporting services (like Spark gateway, secrets, etc.).

---

## 📦 `docker-compose.yaml` for `application_apis/` FastAPI Service

```yaml
version: '3.9'

services:

  homeloniq-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: homeloniq-api
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      SPARK_MASTER_URL: "spark://spark-master:7077"       # optional, if used
      DELTA_STORAGE_PATH: "/mnt/gold/"
    volumes:
      - ./src/extraction/application_apis:/app
    depends_on:
      - spark-master
    restart: unless-stopped

  spark-master:
    image: bitnami/spark:3.5
    container_name: spark-master
    environment:
      - SPARK_MODE=master
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
    ports:
      - "7077:7077"
      - "8080:8080"

  spark-worker:
    image: bitnami/spark:3.5
    container_name: spark-worker
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
    depends_on:
      - spark-master

  # Optional: Azure CLI or Databricks CLI for integration
  databricks-cli:
    image: mcr.microsoft.com/azure-cli
    container_name: databricks-cli
    volumes:
      - ~/.azure:/root/.azure
    stdin_open: true
    tty: true

```

---

## 📁 Project Directory Structure (API Context)

```
project-root/
├── src/
│   └── extraction/
│       └── application_apis/
│           ├── main.py
│           ├── api_utils.py
│           ├── routes/
│           └── models/
├── Dockerfile
├── docker-compose.yaml
├── .env
└── requirements.txt
```

---

## 🔐 `.env` File Example

```env
DBX_TOKEN=your-databricks-token
SPARK_MASTER_URL=spark://spark-master:7077
AZURE_CLIENT_ID=xxx
AZURE_TENANT_ID=xxx
AZURE_CLIENT_SECRET=xxx
```

---

## 🧪 Run Everything

```bash
docker-compose up --build
```

---

## ✅ Benefits & Best Practices

| Feature                    | Status |
| -------------------------- | ------ |
| FastAPI + Spark            | ✅      |
| `.env` for secrets         | ✅      |
| Container dependency graph | ✅      |
| Local Delta access         | ✅      |
| Optional Databricks CLI    | ✅      |

---
