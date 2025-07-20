-- Table to store raw referral edges (from gold layer)
-- Purpose: Store directed edges representing referral relationships between customers.
CREATE TABLE IF NOT EXISTS graph_modeling.referral_edges (
    referrer_id STRING NOT NULL,
    customer_id STRING NOT NULL,
    application_date DATE NOT NULL,
    region STRING,
    PRIMARY KEY (referrer_id, customer_id, application_date)
)
USING DELTA
PARTITIONED BY (application_date)
LOCATION '/mnt/home_loaniq/gold/referral_edges';

-- Table to store computed influence scores (pagerank, degree centrality)
-- Purpose: Persist graph analytics results for customer influence.
CREATE TABLE IF NOT EXISTS graph_modeling.customer_influence_scores (
    customer_id STRING NOT NULL,
    application_date DATE NOT NULL,
    region STRING,
    pagerank DOUBLE,
    in_degree INT,
    out_degree INT,
    PRIMARY KEY (customer_id, application_date)
)
USING DELTA
PARTITIONED BY (application_date)
LOCATION '/mnt/home_loaniq/gold/customer_influence_scores';

-- View for easier querying of customer influence scores
-- Purpose: Provide a simplified interface to query customer influence scores without masking.
CREATE OR REPLACE VIEW graph_modeling.v_customer_influence_scores AS
SELECT
    customer_id,
    application_date,
    region,
    pagerank,
    in_degree,
    out_degree
FROM
    graph_modeling.customer_influence_scores;
