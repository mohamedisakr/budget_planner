from dataclasses import dataclass
from typing import Dict


@dataclass
class PlannerContext:
    def __init__(self, monthly_income: float, savings_goal: float, profile: str, category_goals: Dict[str, float]):
        self.monthly_income = monthly_income
        self.savings_goal = savings_goal
        self.profile = profile
        self.category_goals = category_goals

    def __iter__(self):
        yield self.monthly_income
        yield self.savings_goal
        yield self.profile
        yield self.category_goals

        # class PlannerContext:
        #     monthly_income: float
        #     savings_goal: float
        #     profile: str
        #     category_goals: Dict[str, float]
