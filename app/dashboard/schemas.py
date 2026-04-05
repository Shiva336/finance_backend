from pydantic import BaseModel
from typing import List


class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float


class CategoryBreakdown(BaseModel):
    category: str
    total: float


class TrendPoint(BaseModel):
    month: str
    income: float
    expense: float


class RecentActivity(BaseModel):
    id: int
    amount: float
    type: str
    category: str