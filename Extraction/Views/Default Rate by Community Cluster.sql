CREATE OR REPLACE VIEW gold.vw_default_rate_by_community AS
SELECT
    ci.community_cluster,
    COUNT(DISTINCT ci.customer_id) AS num_customers,
    AVG(lp.default_flag) AS avg_default_rate
FROM gold.customer_influence ci
JOIN gold.loan_performance lp ON ci.customer_id = lp.customer_id
GROUP BY ci.community_cluster
ORDER BY avg_default_rate DESC;
