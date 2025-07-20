# Databricks notebook source
# MAGIC %md
# MAGIC ## Customer Influence Network - Graph Analytics Notebook
# MAGIC This notebook computes customer influence scores using referral relationships from the Gold layer.
# MAGIC
# MAGIC Parameters are injected via dbutils.widgets for dynamic, metadata-driven execution.

# COMMAND ----------

# Setup widgets for metadata-driven parameters
dbutils.widgets.text("region", "", "Region filter (optional)")
dbutils.widgets.text("start_date", "", "Start date (yyyy-MM-dd)")
dbutils.widgets.text("end_date", "", "End date (yyyy-MM-dd)")

region = dbutils.widgets.get("region")
start_date = dbutils.widgets.get("start_date")
end_date = dbutils.widgets.get("end_date")

print(f"Parameters: region={region}, start_date={start_date}, end_date={end_date}")

# COMMAND ----------

from pyspark.sql.functions import col
import networkx as nx
import matplotlib.pyplot as plt

# Load Gold customer transaction summary table
gold_path = "/mnt/home_loaniq/gold/customer_transaction_summary"
df = spark.read.format("delta").load(gold_path)

# Filter by date range and optionally by region if provided
if start_date and end_date:
    df = df.filter((col("application_date") >= start_date) & (col("application_date") <= end_date))
if region:
    df = df.filter(col("region") == region)

# Select referral edges where referrer_id is not null
edges_df = df.filter(col("referrer_id").isNotNull()) \
    .select(col("referrer_id").alias("src"), col("customer_id").alias("dst"))

# COMMAND ----------

# Convert edges to Pandas for networkx (ensure dataset is small enough, else sample or optimize)
edges_pd = edges_df.toPandas()

# Build directed graph
G = nx.DiGraph()
G.add_edges_from(edges_pd.values.tolist())

# COMMAND ----------

# Calculate centrality metrics
page_rank = nx.pagerank(G)
in_degree = dict(G.in_degree())
out_degree = dict(G.out_degree())

# Prepare scores for saving back to Delta
scores = [(node, page_rank.get(node, 0), in_degree.get(node, 0), out_degree.get(node, 0)) for node in G.nodes()]
scores_df = spark.createDataFrame(scores, ["customer_id", "pagerank", "in_degree", "out_degree"])

# COMMAND ----------

# Define output path for influence scores (can be parameterized if needed)
output_path = "/mnt/home_loaniq/gold/customer_influence_scores"

# Save scores to Delta Lake
scores_df.write.format("delta").mode("overwrite").save(output_path)

print(f"Saved influence scores to {output_path}")

# COMMAND ----------

# Display top influencers by pagerank
display(scores_df.orderBy(col("pagerank").desc()).limit(10))

# COMMAND ----------

# Optional: visualize small graphs within notebook (only if small)
if len(G.nodes) < 100:
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=50, arrows=True)
    plt.title("Customer Referral Network")
    plt.show()
else:
    print("Graph too large to visualize")

# COMMAND ----------

# MAGIC %md
# MAGIC ### End of notebook
