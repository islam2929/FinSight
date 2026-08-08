import streamlit as st
from utils.analytics import get_dashboard_stats

st.title("🏠 Dashboard")

stats = get_dashboard_stats()

col1, col2 = st.columns(2)

with col1:
    st.metric("💰 Total Income", f"£{stats['income']:.2f}")

with col2:
    st.metric("💸 Total Expenses", f"£{stats['expenses']:.2f}")

col3, col4 = st.columns(2)

with col3:
    st.metric("💵 Balance", f"£{stats['balance']:.2f}")

with col4:
    st.metric("📄 Transactions", stats["transactions"]) 