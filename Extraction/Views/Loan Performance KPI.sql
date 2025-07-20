CREATE OR REPLACE VIEW gold.vw_loan_performance_kpis AS
SELECT
    processing_date,
    SUM(application_count) AS total_loans_applied,
    SUM(approved_count) AS total_loans_approved,
    SUM(default_count) AS total_loans_defaulted,
    AVG(avg_loan_amount) AS avg_loan_amount,
    AVG(avg_approval_time_days) AS avg_approval_time_days,
    CASE WHEN SUM(application_count) > 0
        THEN (SUM(approved_count)*1.0 / SUM(application_count)) * 100 ELSE 0 END AS approval_rate_pct,
    CASE WHEN SUM(application_count) > 0
        THEN (SUM(default_count)*1.0 / SUM(application_count)) * 100 ELSE 0 END AS default_rate_pct
FROM gold.loan_performance
GROUP BY processing_date
ORDER BY processing_date;
