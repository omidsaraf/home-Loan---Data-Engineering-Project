import streamlit as st
from pyspark.sql import SparkSession
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import tempfile

# Initialize Spark session
spark = SparkSession.builder.appName("HomeLoanIQDashboard").getOrCreate()

@st.cache_data(ttl=3600)
def load_data(sql_view):
    df = spark.sql(f"SELECT * FROM {sql_view}")
    return df.toPandas()

# Load data
loan_kpis = load_data("gold.vw_loan_performance_kpis")
loan_trends = load_data("gold.vw_loan_volume_default_trend")
influence_summary = load_data("gold.vw_customer_influence_summary")

st.title("🏦 HomeLoanIQ Dashboard with Seaborn")

# Date filter for loan KPIs
min_date = pd.to_datetime(loan_kpis['processing_date']).min()
max_date = pd.to_datetime(loan_kpis['processing_date']).max()
date_range = st.slider("Select date range",
                       min_value=min_date,
                       max_value=max_date,
                       value=(min_date, max_date),
                       format="YYYY-MM-DD")

filtered_kpis = loan_kpis[
    (pd.to_datetime(loan_kpis['processing_date']) >= date_range[0]) &
    (pd.to_datetime(loan_kpis['processing_date']) <= date_range[1])
]

st.subheader("Loan Performance KPIs Over Time")

plt.figure(figsize=(10,5))
sns.lineplot(data=filtered_kpis, x='processing_date', y='approval_rate_pct', label='Approval Rate %')
sns.lineplot(data=filtered_kpis, x='processing_date', y='default_rate_pct', label='Default Rate %')
plt.xticks(rotation=45)
plt.ylabel("Percentage")
plt.xlabel("Date")
plt.title("Loan Approval & Default Rates Over Time")
plt.tight_layout()
st.pyplot(plt.gcf())
plt.clf()

st.subheader("Loan Volume & Default Trend (Monthly)")

plt.figure(figsize=(10,5))
loan_trends_melted = loan_trends.melt(id_vars='month', value_vars=['total_applied', 'total_defaulted'],
                                     var_name='Loan Status', value_name='Count')
sns.barplot(data=loan_trends_melted, x='month', y='Count', hue='Loan Status')
plt.xticks(rotation=45)
plt.title("Monthly Loan Volume and Defaults")
plt.tight_layout()
st.pyplot(plt.gcf())
plt.clf()

st.subheader("Top Customer Influencers")

top_n = st.slider("Select number of top influencers", min_value=5, max_value=50, value=10)
top_influencers = influence_summary.sort_values('influence_score', ascending=False).head(top_n)

plt.figure(figsize=(10,5))
sns.barplot(data=top_influencers, x='customer_id', y='influence_score', palette='viridis')
plt.xticks(rotation=45)
plt.title(f"Top {top_n} Customer Influencers by Influence Score")
plt.tight_layout()
st.pyplot(plt.gcf())
plt.clf()

# Customer Influence Network Visualization

st.subheader("Customer Influence Network")

vertices_df = load_data("silver_customers")
edges_df = load_data("silver_customer_relationships")

G = nx.from_pandas_edgelist(edges_df, source='src_customer_id', target='dst_customer_id', edge_attr=True)

def draw_pyvis_graph(graph, notebook=True):
    net = Network(height='600px', width='100%', notebook=notebook)
    for node in graph.nodes:
        net.add_node(node, label=str(node))
    for src, dst in graph.edges:
        net.add_edge(src, dst)
    return net

net = draw_pyvis_graph(G)
tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
net.save_graph(tmp_file.name)
st.components.v1.html(open(tmp_file.name, 'r', encoding='utf-8').read(), height=650)
