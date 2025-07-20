import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(page_title="HomeLoanIQ Dashboard", layout="wide")

# ----- MOCK DATA CREATION -----

@st.cache_data
def load_mock_data():
    # Loan KPIs daily for 60 days
    dates = pd.date_range(end=pd.Timestamp.today(), periods=60)
    loan_performance_kpis = pd.DataFrame({
        'processing_date': dates,
        'approval_rate_pct': np.clip(np.random.normal(70, 5, 60), 50, 90),
        'default_rate_pct': np.clip(np.random.normal(5, 1.5, 60), 1, 10)
    })

    # Monthly loan volumes and defaults for 6 months
    months = pd.date_range(end=pd.Timestamp.today(), periods=6, freq='M').strftime('%Y-%m')
    loan_volume_default_trend = pd.DataFrame({
        'month': months,
        'total_applied': np.random.randint(800, 1200, 6),
        'total_defaulted': np.random.randint(20, 80, 6)
    })

    # Customer influence summary (top 50)
    customer_ids = [f"CUST{i:03d}" for i in range(1, 51)]
    influence_scores = np.random.uniform(0.1, 1.0, 50)
    customer_influence_summary = pd.DataFrame({
        'customer_id': customer_ids,
        'influence_score': influence_scores
    }).sort_values(by='influence_score', ascending=False)

    # Sample graph nodes (silver_customers)
    silver_customers = pd.DataFrame({
        'customer_id': customer_ids,
        'name': [f"Customer {i}" for i in range(1, 51)]
    })

    # Sample graph edges (silver_customer_relationships)
    edges = []
    np.random.seed(42)
    for i in range(50):
        connections = np.random.choice(customer_ids, np.random.randint(1,4), replace=False)
        for conn in connections:
            if conn != customer_ids[i]:
                edges.append({
                    'src_customer_id': customer_ids[i],
                    'dst_customer_id': conn,
                    'relationship_type': np.random.choice(['cosigner', 'referral', 'family'])
                })
    silver_customer_relationships = pd.DataFrame(edges)

    return (loan_performance_kpis, loan_volume_default_trend, customer_influence_summary,
            silver_customers, silver_customer_relationships)

# Load data
(loan_kpis, loan_trends, influence_summary,
 vertices_df, edges_df) = load_mock_data()

# ----- DASHBOARD LAYOUT -----

st.title("🏠 HomeLoanIQ Dashboard")
st.markdown("### Loan KPIs and Customer Influence Network")

# --- Loan Approval & Default Rate over Time ---

st.subheader("Loan Approval and Default Rates (Last 60 Days)")
fig1, ax1 = plt.subplots(figsize=(12,5))
sns.lineplot(data=loan_kpis, x='processing_date', y='approval_rate_pct', label='Approval Rate %', ax=ax1)
sns.lineplot(data=loan_kpis, x='processing_date', y='default_rate_pct', label='Default Rate %', ax=ax1)
ax1.set_ylabel("Percentage %")
ax1.set_xlabel("Date")
ax1.set_ylim(0, 100)
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# --- Monthly Loan Volume and Defaults ---

st.subheader("Monthly Loan Volume & Defaults (Last 6 Months)")
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.barplot(data=loan_trends, x='month', y='total_applied', color='skyblue', label='Total Applied', ax=ax2)
sns.barplot(data=loan_trends, x='month', y='total_defaulted', color='salmon', label='Total Defaulted', ax=ax2)
ax2.set_ylabel("Count")
ax2.set_xlabel("Month")
ax2.legend()
st.pyplot(fig2)

# --- Top 10 Influential Customers ---

st.subheader("Top 10 Customers by Influence Score")
top10 = influence_summary.head(10).copy()
fig3, ax3 = plt.subplots(figsize=(10,4))
sns.barplot(data=top10, y='customer_id', x='influence_score', palette='viridis', ax=ax3)
ax3.set_xlabel("Influence Score")
ax3.set_ylabel("Customer ID")
st.pyplot(fig3)

# --- Customer Influence Network Graph ---

st.subheader("Customer Influence Network Graph")

# Build graph
G = nx.from_pandas_edgelist(edges_df, 'src_customer_id', 'dst_customer_id', edge_attr='relationship_type', create_using=nx.DiGraph())

# Positions for all nodes
pos = nx.spring_layout(G, k=0.5, seed=42)

plt.figure(figsize=(14,10))
nx.draw_networkx_nodes(G, pos, node_size=100, node_color='cornflowerblue', alpha=0.8)
nx.draw_networkx_edges(G, pos, arrowsize=10, arrowstyle='-|>', alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.axis('off')
st.pyplot(plt.gcf())

# --- Footer ---

st.markdown("""
---
Data shown here is simulated for demonstration purposes only.  
""")
