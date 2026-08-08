from database.database import get_transactions
import pandas as pd


def get_transactions_dataframe():
    transactions = get_transactions()

    if not transactions:
        return pd.DataFrame(
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

    df["Date"] = pd.to_datetime(df["Date"])

    return df


def get_dashboard_stats():
    df = get_transactions_dataframe()

    if df.empty:
        return {
            "income": 0,
            "expenses": 0,
            "balance": 0,
            "transactions": 0
        }

    income = df.loc[
        df["Type"] == "Income",
        "Amount"
    ].sum()

    expenses = df.loc[
        df["Type"] == "Expense",
        "Amount"
    ].sum()

    balance = income - expenses

    return {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "transactions": len(df)
    }


def get_category_expenses():
    df = get_transactions_dataframe()

    if df.empty:
        return pd.DataFrame(
            columns=["Category", "Amount"]
        )

    expenses = df[
        df["Type"] == "Expense"
    ]

    category_data = (
        expenses
        .groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Amount", ascending=False)
    )

    return category_data


def get_monthly_spending():
    df = get_transactions_dataframe()

    if df.empty:
        return pd.DataFrame(
            columns=["Month", "Amount"]
        )

    expenses = df[
        df["Type"] == "Expense"
    ].copy()

    expenses["Month"] = (
        expenses["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_data = (
        expenses
        .groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    return monthly_data.sort_values("Month")


def get_income_vs_expenses():
    df = get_transactions_dataframe()

    if df.empty:
        return pd.DataFrame(
            columns=["Type", "Amount"]
        )

    return (
        df
        .groupby("Type")["Amount"]
        .sum()
        .reset_index()
    )


def get_recent_transactions(limit=5):
    df = get_transactions_dataframe()

    if df.empty:
        return df

    return (
        df
        .sort_values("Date", ascending=False)
        .head(limit)
    )