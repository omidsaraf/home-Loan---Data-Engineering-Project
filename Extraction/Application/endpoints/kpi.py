# 1. 
from fastapi import APIRouter, Depends
from utils.spark_session import get_spark_session
from utils.security import authorize_user

router = APIRouter()

@router.get("/kpi/daily", tags=["KPIs"])
def get_daily_kpis(user=Depends(authorize_user)):
    spark = get_spark_session()
    df = spark.sql("SELECT * FROM gold_kpi_daily")
    return df.limit(100).toPandas().to_dict(orient="records")
