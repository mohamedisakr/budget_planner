import pandas as pd


def load_csv_and_manual(uploaded_file, manual_entry):
    if uploaded_file:
        try:
            csv_data = pd.read_csv(uploaded_file, parse_dates=["Date"])
            df = pd.concat([csv_data, manual_entry], ignore_index=True)
        except Exception:
            df = manual_entry.copy()
    else:
        df = manual_entry.copy()
    return df


def clean_expense_data(df):
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df.dropna(subset=["Amount", "Category"], inplace=True)
    return df


def calculate_summary(df, monthly_income, monthly_savings_goal):
    total_expenses = df["Amount"].sum()
    net_savings = monthly_income - total_expenses
    savings_progress = min(net_savings / monthly_savings_goal,
                           1.0) if monthly_savings_goal > 0 else 0.0
    return total_expenses, net_savings, savings_progress


def get_category_totals(df):
    return df.groupby("Category")["Amount"].sum().reset_index()


def get_monthly_trends(df, monthly_income):
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly_totals = df.groupby("Month")["Amount"].sum().reset_index()
    monthly_totals["Net Savings"] = monthly_income - monthly_totals["Amount"]
    return monthly_totals


def get_category_trends(df):
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df.groupby(["Month", "Category"])["Amount"].sum().reset_index()


def get_cumulative_savings(df, monthly_income, savings_goal):
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly = df.groupby("Month")["Amount"].sum().reset_index()
    monthly["Net Savings"] = monthly_income - monthly["Amount"]
    monthly["Goal"] = savings_goal
    monthly["Cumulative Savings"] = monthly["Net Savings"].cumsum()
    monthly["Cumulative Goal"] = monthly["Goal"].cumsum()
    return monthly
