from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import kpi, influence_scores

app = FastAPI(
    title="HomeLoanIQ API",
    description="APIs for customer KPIs, influence scores, and risk insights",
    version="1.0.0",
    docs_url="/",
)

# CORS Middleware (for local testing or cross-origin apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(kpi.router, prefix="/kpis")
app.include_router(influence_scores.router, prefix="/influence")
