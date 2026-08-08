import streamlit as st
import plotly.express as px

from utils.analytics import (
    get_dashboard_stats,
    get_category_expenses,
    get_monthly_spending,
    get_income_vs_expenses,
    get_recent_transactions
)

st.title("🏠 FinSight Dashboard")
st.caption("Your personal financial overview")

stats = get_dashboard_stats()
category_data = get_category_expenses()
monthly_data = get_monthly_spending()
income_expense_data = get_income_vs_expenses()
recent_transactions = get_recent_transactions()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Income", f"£{stats['income']:,.2f}")

with col2:
    st.metric("💸 Total Expenses", f"£{stats['expenses']:,.2f}")

with col3:
    st.metric("💵 Balance", f"£{stats['balance']:,.2f}")

with col4:
    st.metric("📄 Transactions", stats["transactions"])

st.divider()

st.subheader("📈 Spending Over Time")

if not monthly_data.empty:
    fig = px.line(
        monthly_data,
        x="Month",
        y="Amount",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Spending (£)",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Add some expense transactions to see your spending trend.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🥧 Spending by Category")

    if not category_data.empty:
        fig = px.pie(
            category_data,
            names="Category",
            values="Amount",
            hole=0.4
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No expense data available yet.")

with col2:
    st.subheader("⚖️ Income vs Expenses")

    if not income_expense_data.empty:
        fig = px.bar(
            income_expense_data,
            x="Type",
            y="Amount",
            text="Amount"
        )

        fig.update_traces(
            texttemplate="£%{text:.2f}",
            textposition="outside"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No financial data available yet.")

st.divider()

st.subheader("🕒 Recent Transactions")

if not recent_transactions.empty:
    display_df = recent_transactions.copy()

    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

    display_df["Amount"] = display_df["Amount"].map(
        lambda x: f"£{x:,.2f}"
    )

    st.dataframe(
        display_df[
            [
                "Date",
                "Merchant",
                "Category",
                "Amount",
                "Type",
                "Description"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No transactions available yet.")

st.divider()

st.subheader("💡 Financial Insight")

if stats["expenses"] > stats["income"]:
    st.warning(
        "⚠️ Your expenses are currently higher than your income."
    )

elif stats["income"] > 0:
    spending_percentage = (
        stats["expenses"] / stats["income"]
    ) * 100

    if spending_percentage < 50:
        st.success(
            f"You're currently spending {spending_percentage:.1f}% "
            "of your income. Good job keeping spending under control! 💪"
        )

    elif spending_percentage < 80:
        st.info(
            f"You're currently spending {spending_percentage:.1f}% "
            "of your income."
        )

    else:
        st.warning(
            f"You're currently spending {spending_percentage:.1f}% "
            "of your income. Consider reviewing your expenses."
        )

else:
    st.info(
        "Add some income and expense transactions "
        "to receive financial insights."
    )