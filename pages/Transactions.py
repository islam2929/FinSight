import pandas as pd
import streamlit as st
from database.database import add_transaction, get_transactions
from datetime import date

st.title("💳 Transactions")

with st.form("transaction_form"):

    amount = st.number_input("Amount", min_value=0.0, step=0.01)

    transaction_type = st.selectbox(
        "Type",
        ["Expense", "Income"]
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Bills",
            "Shopping",
            "Entertainment",
            "Salary",
            "Other"
        ]
    )

    merchant = st.text_input("Merchant")

    transaction_date = st.date_input("Date", value=date.today())

    description = st.text_area("Description")

    submitted = st.form_submit_button("💾 Save Transaction")

    if submitted:

        add_transaction(
            str(transaction_date),
            merchant,
            category,
            amount,
            transaction_type,
            description
        )

        st.success("Transaction saved successfully!")

st.divider()

st.subheader("Saved Transactions")

transactions = get_transactions()

if transactions:
    st.dataframe(
        transactions,
        use_container_width=True
    )
else:
    st.info("No transactions found.")

st.divider()
st.subheader("📋 Transaction History")

transactions = get_transactions()

if transactions:
    df = pd.DataFrame(
        transactions,
        columns=[
            "ID",
            "Date",
            "Merchant",
            "Category",
            "Amount",
            "Type",
            "Description"
        ]
    )

    st.dataframe(df, use_container_width=True)
else:
    st.info("No transactions yet.")