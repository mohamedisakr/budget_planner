
import plotly.express as px


def plot_spending_pie(category_totals):
    fig = px.pie(category_totals, names="Category",
                 values="Amount", title="Spending Breakdown")
    return fig


def plot_spending_bar(category_totals):
    fig = px.bar(category_totals, x="Category", y="Amount",
                 title="Total Spent per Category", text_auto=True)
    return fig
