from database.database import get_transactions


def get_dashboard_stats():
    transactions = get_transactions()

    income = 0
    expenses = 0

    for transaction in transactions:
        amount = transaction[4]
        transaction_type = transaction[5]

        if transaction_type == "Income":
            income += amount
        else:
            expenses += amount

    balance = income - expenses

    return {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "transactions": len(transactions)
    }