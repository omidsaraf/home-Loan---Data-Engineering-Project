from pydantic import BaseModel
from typing import List

class CustomerInsight(BaseModel):
    customer_id: str
    kpi_score: float
    risk_segment: str

class GraphMetric(BaseModel):
    node_id: str
    degree_centrality: float
    betweenness: float
    influence_score: float
