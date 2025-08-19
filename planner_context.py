from dataclasses import dataclass
from typing import Dict


@dataclass
class PlannerContext:
    monthly_income: float
    savings_goal: float
    profile: str
    category_goals: Dict[str, float]
