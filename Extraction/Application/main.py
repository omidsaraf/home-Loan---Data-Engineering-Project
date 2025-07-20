from fastapi import FastAPI
from routes import customer_insights, graph_metrics

app = FastAPI(title="HomeLoanIQ API")

app.include_router(customer_insights.router, prefix="/api/v1/customers")
app.include_router(graph_metrics.router, prefix="/api/v1/graph")
