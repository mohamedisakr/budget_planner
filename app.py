import streamlit as st
import pandas as pd

from budget_simulator import load_csv_and_manual, clean_expense_data, calculate_summary, get_category_totals, get_monthly_trends, get_category_trends
from budget_visuals import plot_spending_pie, plot_spending_bar, plot_monthly_trends, plot_category_trends
from budget_notes import generate_budget_notes


# --- Page Config ---
st.set_page_config(page_title="Budget Planner", layout="wide")
st.title("🧮 Monthly Budget Planner")

# --- Sidebar Inputs ---
st.sidebar.header("Client Profile")
profile = st.sidebar.selectbox("Select Profile", [
    "Young Couple",
    "Solo Professional",
    "Family Planner"
])

st.sidebar.header("Income & Goals")
monthly_income = st.sidebar.number_input(
    "Monthly Income (EGP)", min_value=0.0, value=15000.0, step=500.0)
monthly_savings_goal = st.sidebar.number_input(
    "Savings Goal (EGP)", min_value=0.0, value=3000.0, step=500.0)

st.sidebar.header("Upload or Enter Expenses")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
manual_entry = st.sidebar.data_editor(
    pd.DataFrame(columns=["Date", "Category", "Amount"]),
    num_rows="dynamic",
    use_container_width=True,
    key="manual_entry"
)

# --- Data Processing ---
df = load_csv_and_manual(uploaded_file, manual_entry)
df = clean_expense_data(df)

if df.empty:
    st.warning("Please upload a CSV or enter expenses manually.")
    st.stop()

# --- Summary Calculations ---
total_expenses, net_savings, savings_progress = calculate_summary(
    df, monthly_income, monthly_savings_goal)
category_totals = get_category_totals(df)

monthly_trends = get_monthly_trends(df, monthly_income)
category_trends = get_category_trends(df)

# --- Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Spending Overview")
    st.plotly_chart(plot_spending_bar(category_totals),
                    use_container_width=True)
    st.plotly_chart(plot_spending_pie(category_totals),
                    use_container_width=True)

    st.subheader("📆 Monthly Trend Analysis")
    st.plotly_chart(plot_monthly_trends(
        monthly_trends), use_container_width=True)
    st.plotly_chart(plot_category_trends(
        category_trends), use_container_width=True)

with col2:
    st.subheader("📋 Summary")
    st.metric("Total Expenses", f"{total_expenses:,.0f} EGP")
    st.metric("Net Savings", f"{net_savings:,.0f} EGP")
    st.progress(savings_progress,
                text=f"Savings Goal Progress: {savings_progress*100:.1f}%")


# --- Planner’s Notes ---
st.subheader("🧠 Planner’s Notes")
notes = generate_budget_notes(
    category_totals, monthly_income, net_savings, monthly_savings_goal, profile)

if notes:
    for note in notes:
        st.markdown(f"- {note}")
else:
    st.info("No specific notes this month. Keep tracking!")


# old version
# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # --- Page Config ---
# st.set_page_config(page_title="Budget Planner", layout="centered")
# st.title("💸 Budget Planner with CSV Upload")

# st.markdown("Track your monthly expenses, analyze spending by category, and monitor your savings goals.")

# # --- Sidebar Inputs ---
# st.sidebar.header("Client Inputs")
# monthly_income = st.sidebar.number_input("Monthly Income (£)", min_value=0.0, value=4500.0, step=100.0)
# monthly_savings_goal = st.sidebar.number_input("Monthly Savings Goal (£)", min_value=0.0, value=417.0, step=50.0)

# # --- CSV Upload ---
# st.sidebar.header("Upload Expenses CSV")
# uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# # --- Manual Entry (Optional) ---
# st.sidebar.header("Manual Entry")
# manual_amount = st.sidebar.number_input("Amount (£)", min_value=0.0, value=0.0, step=1.0)
# manual_category = st.sidebar.selectbox("Category", ["Housing", "Food", "Transport", "Entertainment", "Subscriptions", "Miscellaneous"])
# manual_description = st.sidebar.text_input("Description")
# manual_date = st.sidebar.date_input("Date")

# if st.sidebar.button("Add Manual Entry"):
#     manual_entry = pd.DataFrame({
#         "Date": [manual_date],
#         "Amount": [manual_amount],
#         "Category": [manual_category],
#         "Description": [manual_description]
#     })
# else:
#     manual_entry = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

# # --- Load & Combine Data ---
# if uploaded_file:
#     try:
#         csv_data = pd.read_csv(uploaded_file, parse_dates=["Date"])
#         df = pd.concat([csv_data, manual_entry], ignore_index=True)
#     except Exception as e:
#         st.error(f"Error loading CSV: {e}")
#         df = manual_entry.copy()
# else:
#     df = manual_entry.copy()

# # --- Clean & Analyze ---
# if not df.empty:
#     df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
#     df.dropna(subset=["Amount", "Category"], inplace=True)

#     total_expenses = df["Amount"].sum()
#     net_savings = monthly_income - total_expenses
#     savings_progress = min(net_savings / monthly_savings_goal, 1.0) if monthly_savings_goal > 0 else 0.0

#     # --- Summary Metrics ---
#     st.subheader("📊 Summary")
#     st.metric("Total Income", f"£{monthly_income:,.0f}")
#     st.metric("Total Expenses", f"£{total_expenses:,.0f}")
#     st.metric("Net Savings", f"£{net_savings:,.0f}")

#     st.progress(savings_progress, text=f"Savings Goal Progress: {savings_progress*100:.1f}%")

#     # --- Category Breakdown ---
#     st.subheader("📂 Spending by Category")
#     category_totals = df.groupby("Category")["Amount"].sum().reset_index()

#     fig_pie = px.pie(category_totals, names="Category", values="Amount", title="Spending Breakdown")
#     st.plotly_chart(fig_pie, use_container_width=True)

#     fig_bar = px.bar(category_totals, x="Category", y="Amount", title="Total Spent per Category", text_auto=True)
#     st.plotly_chart(fig_bar, use_container_width=True)

#     # --- Raw Data Table ---
#     st.subheader("📄 Expense Records")
#     st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

# else:
#     st.info("Upload a CSV or add manual entries to begin tracking your budget.")

# # --- Footer ---
# st.markdown("---")
# st.caption("Built by Mohamed • Budget Planner for Paraplanner Portfolio")
