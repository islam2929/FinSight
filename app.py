from database.database import create_database
import streamlit as st

st.set_page_config(
    page_title="FinSight",
    page_icon="💰",
    layout="wide"
)

create_database()

st.title("💰 FinSight")

st.markdown("""
## Welcome!

Welcome to **FinSight**.

This application helps users:

- Track expenses
- Analyze spending
- Visualize financial habits
- Predict future spending

Choose a page from the sidebar to begin.
""")