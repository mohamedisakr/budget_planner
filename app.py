import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Budget Planner", layout="centered")
st.title("💸 Budget Planner with CSV Upload")

st.markdown("Track your monthly expenses, analyze spending by category, and monitor your savings goals.")

# --- Sidebar Inputs ---
st.sidebar.header("Client Inputs")
monthly_income = st.sidebar.number_input("Monthly Income (£)", min_value=0.0, value=4500.0, step=100.0)
monthly_savings_goal = st.sidebar.number_input("Monthly Savings Goal (£)", min_value=0.0, value=417.0, step=50.0)

# --- CSV Upload ---
st.sidebar.header("Upload Expenses CSV")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# --- Manual Entry (Optional) ---
st.sidebar.header("Manual Entry")
manual_amount = st.sidebar.number_input("Amount (£)", min_value=0.0, value=0.0, step=1.0)
manual_category = st.sidebar.selectbox("Category", ["Housing", "Food", "Transport", "Entertainment", "Subscriptions", "Miscellaneous"])
manual_description = st.sidebar.text_input("Description")
manual_date = st.sidebar.date_input("Date")

if st.sidebar.button("Add Manual Entry"):
    manual_entry = pd.DataFrame({
        "Date": [manual_date],
        "Amount": [manual_amount],
        "Category": [manual_category],
        "Description": [manual_description]
    })
else:
    manual_entry = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

# --- Load & Combine Data ---
if uploaded_file:
    try:
        csv_data = pd.read_csv(uploaded_file, parse_dates=["Date"])
        df = pd.concat([csv_data, manual_entry], ignore_index=True)
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        df = manual_entry.copy()
else:
    df = manual_entry.copy()

# --- Clean & Analyze ---
if not df.empty:
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df.dropna(subset=["Amount", "Category"], inplace=True)

    total_expenses = df["Amount"].sum()
    net_savings = monthly_income - total_expenses
    savings_progress = min(net_savings / monthly_savings_goal, 1.0) if monthly_savings_goal > 0 else 0.0

    # --- Summary Metrics ---
    st.subheader("📊 Summary")
    st.metric("Total Income", f"£{monthly_income:,.0f}")
    st.metric("Total Expenses", f"£{total_expenses:,.0f}")
    st.metric("Net Savings", f"£{net_savings:,.0f}")

    st.progress(savings_progress, text=f"Savings Goal Progress: {savings_progress*100:.1f}%")

    # --- Category Breakdown ---
    st.subheader("📂 Spending by Category")
    category_totals = df.groupby("Category")["Amount"].sum().reset_index()

    fig_pie = px.pie(category_totals, names="Category", values="Amount", title="Spending Breakdown")
    st.plotly_chart(fig_pie, use_container_width=True)

    fig_bar = px.bar(category_totals, x="Category", y="Amount", title="Total Spent per Category", text_auto=True)
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- Raw Data Table ---
    st.subheader("📄 Expense Records")
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

else:
    st.info("Upload a CSV or add manual entries to begin tracking your budget.")

# --- Footer ---
st.markdown("---")
st.caption("Built by Mohamed • Budget Planner for Paraplanner Portfolio")
