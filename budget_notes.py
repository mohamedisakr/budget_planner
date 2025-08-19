def generate_budget_notes(category_totals, monthly_income, net_savings, savings_goal, profile, category_goals):
    notes = []

    # Profile-based thresholds
    if profile == "Young Couple":
        sub_limit = 0.10
        ent_limit = 0.15
    elif profile == "Solo Professional":
        sub_limit = 0.15
        ent_limit = 0.20
    else:  # Family Planner
        sub_limit = 0.08
        ent_limit = 0.12

    # Savings logic
    if net_savings < 0:
        notes.append(
            "You're spending more than your income—consider revisiting discretionary categories.")
    elif net_savings < savings_goal:
        notes.append(
            "You're under your savings goal—small adjustments in entertainment or subscriptions could help.")

    # Category-specific insights
    for _, row in category_totals.iterrows():
        category = row["Category"]
        amount = row["Amount"]
        pct = amount / monthly_income
        if category == "Subscriptions" and pct > sub_limit:
            notes.append(
                f"Subscriptions exceed {int(sub_limit*100)}% of income—consider reviewing recurring charges.")
        if category == "Entertainment" and pct > ent_limit:
            notes.append(
                f"Entertainment spending is high for a {profile.lower()}—consider setting a monthly cap.")

    if net_savings > savings_goal:
        notes.append(
            "Great job! You're exceeding your savings goal this month.")

    # Existing profile logic...

    # Category goal comparison
    for _, row in category_totals.iterrows():
        cat = row["Category"]
        spent = row["Amount"]
        goal = category_goals.get(cat, None)
        if goal and spent > goal:
            notes.append(
                f"⚠️ Spending in {cat} exceeded the goal by EGP {spent - goal:,.0f}.")

    # Existing savings logic...

    return notes


def generate_planners_notes(df, monthly_income, savings_goal):
    notes = []
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly_summary = df.groupby("Month")["Amount"].sum().reset_index()
    monthly_summary["Net Savings"] = monthly_income - monthly_summary["Amount"]

    for _, row in monthly_summary.iterrows():
        month = row["Month"]
        spent = row["Amount"]
        net = row["Net Savings"]

        if net < 0:
            notes.append(
                f"⚠️ In {month}, spending exceeded income by EGP {abs(net):,.0f}. Consider reviewing discretionary categories.")
        elif net < savings_goal:
            notes.append(
                f"📉 In {month}, savings of EGP {net:,.0f} fell short of the goal (EGP {savings_goal:,.0f}).")
        else:
            notes.append(
                f"✅ In {month}, savings of EGP {net:,.0f} met or exceeded the goal.")

    # Optional: Add category-level observations
    category_summary = df.groupby(
        "Category")["Amount"].sum().sort_values(ascending=False)
    top_category = category_summary.idxmax()
    top_amount = category_summary.max()
    notes.append(
        f"💡 Highest spending category overall: {top_category} (EGP {top_amount:,.0f})")

    return notes

# before adding profile
# def generate_budget_notes(category_totals, monthly_income, net_savings, savings_goal):
#     notes = []

#     if net_savings < 0:
#         notes.append(
#             "You're spending more than your income—consider revisiting discretionary categories.")
#     elif net_savings < savings_goal:
#         notes.append(
#             "You're under your savings goal—small adjustments in entertainment or subscriptions could help.")

#     for _, row in category_totals.iterrows():
#         category = row["Category"]
#         amount = row["Amount"]
#         pct = amount / monthly_income
#         if category == "Subscriptions" and pct > 0.1:
#             notes.append(
#                 "Subscriptions exceed 10% of income—consider reviewing recurring charges.")
#         if category == "Entertainment" and pct > 0.15:
#             notes.append(
#                 "Entertainment spending is high—consider setting a monthly cap.")

#     if net_savings > savings_goal:
#         notes.append(
#             "Great job! You're exceeding your savings goal this month.")

#     return notes
