
import plotly.express as px

color_map = {
    "Housing": "#4CAF50",
    "Food": "#FF9800",
    "Transport": "#2196F3",
    "Entertainment": "#9C27B0",
    "Subscriptions": "#00BCD4",
    "Miscellaneous": "#607D8B"
}


# def plot_spending_pie(category_totals):
#     fig = px.pie(category_totals, names="Category",
#                  values="Amount", title="Spending Breakdown")
#     return fig
def plot_spending_pie(df):
    valid_categories = list(color_map.keys())
    df = df[df["Category"].isin(valid_categories)]

    fig = px.pie(
        df,
        names="Category",
        values="Amount",
        color="Category",
        color_discrete_map=color_map
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title="Spending Breakdown by Category")
    return fig


def plot_spending_bar(category_totals):
    fig = px.bar(category_totals, x="Category", y="Amount",
                 title="Total Spent per Category", text_auto=True)
    return fig


# def plot_monthly_trends(monthly_totals):
#     fig = px.line(monthly_totals, x="Month", y=["Amount", "Net Savings"],
#                   title="Monthly Spending & Savings Trend",
#                   markers=True)
#     fig.update_layout(yaxis_title="EGP")
#     return fig
def plot_monthly_trends(df):
    # valid_categories = list(color_map.keys())
    # df = df[df["Category"].isin(valid_categories)]

    fig = px.bar(
        df,
        x="Month",
        y="Amount",
        # color="Category",
        color_discrete_map=color_map,
        barmode="group"
    )
    fig.update_layout(title="Monthly Spending Trends")
    return fig


def plot_category_trends(category_trends):
    fig = px.bar(category_trends, x="Month", y="Amount", color="Category",
                 title="Monthly Spending by Category", barmode="stack")
    return fig


def plot_category_goals(category_totals, category_goals):
    df = category_totals.copy()
    df["Goal"] = df["Category"].map(category_goals)
    fig = px.bar(df, x="Category", y=["Amount", "Goal"], barmode="group",
                 title="Actual vs. Goal Spending by Category")
    return fig


def plot_cumulative_savings(cumulative_df):
    fig = px.line(cumulative_df, x="Month", y=["Cumulative Savings", "Cumulative Goal"],
                  title="Cumulative Savings vs. Goal", markers=True)
    fig.update_layout(yaxis_title="EGP")
    return fig
