
-- 1. Upsert into `graph_modeling.referral_edges`

```sql
MERGE INTO graph_modeling.referral_edges AS target
USING delta.`/mnt/home_loaniq/tmp/referral_edges_update` AS source
  ON target.referrer_id = source.referrer_id
  AND target.customer_id = source.customer_id
  AND target.application_date = source.application_date
WHEN MATCHED THEN
  UPDATE SET
    target.region = source.region
WHEN NOT MATCHED THEN
  INSERT (referrer_id, customer_id, application_date, region)
  VALUES (source.referrer_id, source.customer_id, source.application_date, source.region);
```

---

-- 2. Upsert into `graph_modeling.customer_influence_scores`

```sql
MERGE INTO graph_modeling.customer_influence_scores AS target
USING delta.`/mnt/home_loaniq/tmp/influence_scores_update` AS source
  ON target.customer_id = source.customer_id
  AND target.application_date = source.application_date
WHEN MATCHED THEN
  UPDATE SET
    target.region = source.region,
    target.pagerank = source.pagerank,
    target.in_degree = source.in_degree,
    target.out_degree = source.out_degree
WHEN NOT MATCHED THEN
  INSERT (customer_id, application_date, region, pagerank, in_degree, out_degree)
  VALUES (source.customer_id, source.application_date, source.region, source.pagerank, source.in_degree, source.out_degree);
```

---

----- Explanation

-- `source` is your staging Delta table (a temporary or incremental update location).
---The `ON` clause defines the keys used to find matching rows.
-- If a row exists, update the target with new values.
-- If no match, insert the new row.

---You can run these MERGE statements directly in Databricks SQL or use the SQL API in PySpark.

