from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.models import Category, Direction, StatementStatus


class StatementRead(BaseModel):
    id: UUID
    file_name: str
    status: StatementStatus
    period_start: date | None
    period_end: date | None
    error_message: str | None
    created_at: datetime


class TransactionRead(BaseModel):
    id: UUID
    statement_id: UUID
    posted_date: date
    description_raw: str
    description_normalized: str
    merchant_name: str
    amount: Decimal
    direction: Direction
    balance_after: Decimal | None
    source_page: int
    extraction_confidence: float
    category: Category | None = None
    classification_confidence: float | None = None


class UploadResponse(BaseModel):
    statement_id: UUID
    status: StatementStatus
    file_name: str
    created_at: datetime


class DashboardSummary(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    net_savings: Decimal
    savings_rate: float
    transaction_count: int
    top_merchants: list[dict[str, Any]]
    category_breakdown: list[dict[str, Any]]
    insights: list[dict[str, Any]]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    answer: str
    evidence: list[dict[str, Any]]
    disclaimer: str = "Educational financial analysis only, not regulated financial advice."
