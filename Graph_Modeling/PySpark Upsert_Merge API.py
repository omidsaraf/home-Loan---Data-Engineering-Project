from delta.tables import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("GraphModelUpsert").getOrCreate()

# Paths to Delta tables
referral_edges_path = "/mnt/home_loaniq/graph_modeling/referral_edges"
influence_scores_path = "/mnt/home_loaniq/graph_modeling/customer_influence_scores"

# Load incremental update data (this would be your PySpark computed DataFrame)
referral_edges_updates = spark.read.format("delta").load("/mnt/home_loaniq/tmp/referral_edges_update")
influence_scores_updates = spark.read.format("delta").load("/mnt/home_loaniq/tmp/influence_scores_update")

# Function to upsert referral edges
def upsert_referral_edges(target_path, updates_df):
    deltaTable = DeltaTable.forPath(spark, target_path)
    (
        deltaTable.alias("target")
        .merge(
            updates_df.alias("source"),
            "target.referrer_id = source.referrer_id AND target.customer_id = source.customer_id AND target.application_date = source.application_date"
        )
        .whenMatchedUpdate(set={
            "region": "source.region"
        })
        .whenNotMatchedInsert(values={
            "referrer_id": "source.referrer_id",
            "customer_id": "source.customer_id",
            "application_date": "source.application_date",
            "region": "source.region"
        })
        .execute()
    )

# Function to upsert influence scores
def upsert_influence_scores(target_path, updates_df):
    deltaTable = DeltaTable.forPath(spark, target_path)
    (
        deltaTable.alias("target")
        .merge(
            updates_df.alias("source"),
            "target.customer_id = source.customer_id AND target.application_date = source.application_date"
        )
        .whenMatchedUpdate(set={
            "region": "source.region",
            "pagerank": "source.pagerank",
            "in_degree": "source.in_degree",
            "out_degree": "source.out_degree"
        })
        .whenNotMatchedInsert(values={
            "customer_id": "source.customer_id",
            "application_date": "source.application_date",
            "region": "source.region",
            "pagerank": "source.pagerank",
            "in_degree": "source.in_degree",
            "out_degree": "source.out_degree"
        })
        .execute()
    )

# Run upserts
upsert_referral_edges(referral_edges_path, referral_edges_updates)
upsert_influence_scores(influence_scores_path, influence_scores_updates)
