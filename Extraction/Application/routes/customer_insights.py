from fastapi import APIRouter
from models.response_models import CustomerInsight
from api_utils import get_spark_session, load_delta_table

router = APIRouter()
spark = get_spark_session()

@router.get("/insights", response_model=List[CustomerInsight])
def get_customer_insights(limit: int = 50):
    df = load_delta_table(spark, "/mnt/gold/customer_kpis").limit(limit)
    records = df.select("customer_id", "kpi_score", "risk_segment").toPandas()
    return records.to_dict(orient="records")
