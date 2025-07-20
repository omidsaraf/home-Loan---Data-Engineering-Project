from fastapi import APIRouter
from models.response_models import GraphMetric
from api_utils import get_spark_session, load_delta_table

router = APIRouter()
spark = get_spark_session()

@router.get("/graph-metrics", response_model=List[GraphMetric])
def get_graph_metrics(limit: int = 100):
    df = load_delta_table(spark, "/mnt/gold/customer_influence").limit(limit)
    df_selected = df.select("node_id", "degree", "betweenness", "influence_score")
    return df_selected.toPandas().to_dict(orient="records")
