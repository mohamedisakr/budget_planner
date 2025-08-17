def generate_budget_notes(category_totals, monthly_income, net_savings, savings_goal):
    notes = []

    if net_savings < 0:
        notes.append(
            "You're spending more than your income—consider revisiting discretionary categories.")
    elif net_savings < savings_goal:
        notes.append(
            "You're under your savings goal—small adjustments in entertainment or subscriptions could help.")

    for _, row in category_totals.iterrows():
        category = row["Category"]
        amount = row["Amount"]
        pct = amount / monthly_income
        if category == "Subscriptions" and pct > 0.1:
            notes.append(
                "Subscriptions exceed 10% of income—consider reviewing recurring charges.")
        if category == "Entertainment" and pct > 0.15:
            notes.append(
                "Entertainment spending is high—consider setting a monthly cap.")

    if net_savings > savings_goal:
        notes.append(
            "Great job! You're exceeding your savings goal this month.")

    return notes
