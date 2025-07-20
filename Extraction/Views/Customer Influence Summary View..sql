CREATE OR REPLACE VIEW gold.vw_customer_influence_summary AS
SELECT
    customer_id,
    influence_score,
    degree_centrality,
    betweenness_centrality,
    closeness_centrality,
    community_cluster
FROM gold.customer_influence;
