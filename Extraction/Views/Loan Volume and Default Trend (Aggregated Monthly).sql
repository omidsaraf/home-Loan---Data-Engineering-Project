CREATE OR REPLACE VIEW gold.vw_loan_volume_default_trend AS
SELECT
    DATE_TRUNC('month', processing_date) AS month,
    SUM(application_count) AS total_applied,
    SUM(default_count) AS total_defaulted,
    CASE WHEN SUM(application_count) > 0
        THEN (SUM(default_count)*1.0 / SUM(application_count)) * 100 ELSE 0 END AS default_rate_pct
FROM gold.loan_performance
GROUP BY month
ORDER BY month;
