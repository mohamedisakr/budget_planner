
import plotly.express as px


def plot_spending_pie(category_totals):
    fig = px.pie(category_totals, names="Category",
                 values="Amount", title="Spending Breakdown")
    return fig


def plot_spending_bar(category_totals):
    fig = px.bar(category_totals, x="Category", y="Amount",
                 title="Total Spent per Category", text_auto=True)
    return fig


def plot_monthly_trends(monthly_totals):
    fig = px.line(monthly_totals, x="Month", y=["Amount", "Net Savings"],
                  title="Monthly Spending & Savings Trend",
                  markers=True)
    fig.update_layout(yaxis_title="EGP")
    return fig


def plot_category_trends(category_trends):
    fig = px.bar(category_trends, x="Month", y="Amount", color="Category",
                 title="Monthly Spending by Category", barmode="stack")
    return fig
