# 2.
from fastapi import APIRouter, Depends
from utils.spark_session import get_spark_session
from utils.security import authorize_user

router = APIRouter()

@router.get("/influence/top_customers", tags=["Influence Scores"])
def get_top_influencers(limit: int = 10, user=Depends(authorize_user)):
    spark = get_spark_session()
    df = spark.sql("SELECT * FROM gold_customer_influence_scores")
    top = df.orderBy("page_rank", ascending=False).limit(limit).toPandas()
    return top.to_dict(orient="records")
