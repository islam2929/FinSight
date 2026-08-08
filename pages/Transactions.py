import pandas as pd
import streamlit as st
from database.database import (
    add_transaction,
    get_transactions,
    update_transaction,
    delete_transaction
)
from datetime import date, timedelta


# ==========================================
# Page Title
# ==========================================

st.title("💳 Transactions")


# ==========================================
# Add Transaction
# ==========================================

with st.expander("➕ Add New Transaction", expanded=True):

    with st.form("transaction_form"):

        col1, col2 = st.columns(2)

        with col1:

            amount = st.number_input(
                "Amount",
                min_value=0.01,
                step=0.01
            )

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

        with col2:

            merchant = st.text_input(
                "Merchant",
                placeholder="e.g. Tesco"
            )

            transaction_date = st.date_input(
                "Date",
                value=date.today()
            )

            description = st.text_area(
                "Description",
                placeholder="Optional"
            )

        submitted = st.form_submit_button(
            "💾 Save Transaction"
        )

        if submitted:

            if not merchant.strip():
                st.error("Please enter a merchant.")

            else:

                add_transaction(
                    str(transaction_date),
                    merchant.strip(),
                    category,
                    amount,
                    transaction_type,
                    description.strip()
                )

                st.success(
                    "Transaction saved successfully!"
                )

                st.rerun()


# ==========================================
# Transaction History
# ==========================================

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

    # ======================================
    # Filters
    # ======================================

    st.markdown("### 🔎 Filters")

    col1, col2, col3 = st.columns(3)

    with col1:

        search = st.text_input(
            "Merchant",
            placeholder="Search merchant..."
        )

    with col2:

        category_filter = st.selectbox(
            "Category",
            [
                "All",
                "Food",
                "Transport",
                "Bills",
                "Shopping",
                "Entertainment",
                "Salary",
                "Other"
            ]
        )

    with col3:

        type_filter = st.selectbox(
            "Type",
            [
                "All",
                "Expense",
                "Income"
            ]
        )

    # ======================================
    # Date Filters
    # ======================================

    col4, col5 = st.columns(2)

    with col4:

        start_date = st.date_input(
            "From",
            value=date.today() - timedelta(days=30)
        )

    with col5:

        end_date = st.date_input(
            "To",
            value=date.today()
        )

    # ======================================
    # Apply Filters
    # ======================================

    if search:

        df = df[
            df["Merchant"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if category_filter != "All":

        df = df[
            df["Category"] == category_filter
        ]

    if type_filter != "All":

        df = df[
            df["Type"] == type_filter
        ]

    df["Date"] = pd.to_datetime(df["Date"])

    df = df[
        (df["Date"].dt.date >= start_date)
        &
        (df["Date"].dt.date <= end_date)
    ]

    # ======================================
    # Sorting
    # ======================================

    sort_option = st.selectbox(
        "↕️ Sort by",
        [
            "Newest",
            "Oldest",
            "Highest Amount",
            "Lowest Amount"
        ]
    )

    if sort_option == "Newest":

        df = df.sort_values(
            "Date",
            ascending=False
        )

    elif sort_option == "Oldest":

        df = df.sort_values(
            "Date",
            ascending=True
        )

    elif sort_option == "Highest Amount":

        df = df.sort_values(
            "Amount",
            ascending=False
        )

    elif sort_option == "Lowest Amount":

        df = df.sort_values(
            "Amount",
            ascending=True
        )

    # ======================================
    # Results
    # ======================================

    st.write(
        f"Showing **{len(df)}** transaction(s)"
    )

    display_df = df.copy()

    display_df["Date"] = display_df[
        "Date"
    ].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # Edit Transaction
    # ======================================

    st.divider()

    st.subheader("✏️ Edit Transaction")

    transaction_ids = df["ID"].tolist()

    if transaction_ids:

        selected_id = st.selectbox(
            "Select transaction",
            transaction_ids
        )

        selected_transaction = df[
            df["ID"] == selected_id
        ].iloc[0]

        with st.form("edit_transaction_form"):

            edit_date = st.date_input(
                "Date",
                value=selected_transaction["Date"].date()
            )

            edit_merchant = st.text_input(
                "Merchant",
                value=selected_transaction["Merchant"]
            )

            categories = [
                "Food",
                "Transport",
                "Bills",
                "Shopping",
                "Entertainment",
                "Salary",
                "Other"
            ]

            edit_category = st.selectbox(
                "Category",
                categories,
                index=categories.index(
                    selected_transaction["Category"]
                )
            )

            edit_amount = st.number_input(
                "Amount",
                min_value=0.01,
                value=float(
                    selected_transaction["Amount"]
                ),
                step=0.01
            )

            types = [
                "Expense",
                "Income"
            ]

            edit_type = st.selectbox(
                "Type",
                types,
                index=types.index(
                    selected_transaction["Type"]
                )
            )

            edit_description = st.text_area(
                "Description",
                value=selected_transaction["Description"]
                if pd.notna(
                    selected_transaction["Description"]
                )
                else ""
            )

            update_button = st.form_submit_button(
                "💾 Update Transaction"
            )

            if update_button:

                if not edit_merchant.strip():

                    st.error(
                        "Merchant cannot be empty."
                    )

                else:

                    update_transaction(
                        selected_id,
                        str(edit_date),
                        edit_merchant.strip(),
                        edit_category,
                        edit_amount,
                        edit_type,
                        edit_description.strip()
                    )

                    st.success(
                        "Transaction updated!"
                    )

                    st.rerun()


    # ======================================
    # Delete Transaction
    # ======================================

    st.divider()

    st.subheader("🗑️ Delete Transaction")

    if transaction_ids:

        delete_id = st.selectbox(
            "Select transaction to delete",
            transaction_ids,
            key="delete_transaction"
        )

        confirm_delete = st.checkbox(
            "I understand this transaction will be permanently deleted."
        )

        if st.button(
            "🗑️ Delete Transaction",
            type="primary"
        ):

            if confirm_delete:

                delete_transaction(
                    delete_id
                )

                st.success(
                    "Transaction deleted."
                )

                st.rerun()

            else:

                st.warning(
                    "Please confirm deletion first."
                )


else:

    st.info(
        "No transactions found."
    )