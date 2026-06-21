from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from enum import StrEnum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Category(StrEnum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    SHOPPING = "Shopping"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    RENT = "Rent"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"
    TRAVEL = "Travel"
    INVESTMENTS = "Investments"
    EMI = "EMI"
    MISC = "Misc"


class StatementStatus(StrEnum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Direction(StrEnum):
    DEBIT = "debit"
    CREDIT = "credit"


class Statement(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, default="demo-user")
    file_name: str
    storage_path: str
    status: StatementStatus = Field(default=StatementStatus.UPLOADED)
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)


class Transaction(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    statement_id: UUID = Field(index=True)
    user_id: str = Field(index=True, default="demo-user")
    posted_date: date = Field(index=True)
    description_raw: str
    description_normalized: str
    merchant_name: str
    amount: Decimal = Field(decimal_places=2, max_digits=14)
    direction: Direction
    balance_after: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=14)
    source_page: int = 1
    extraction_confidence: float = 0.8
    created_at: datetime = Field(default_factory=utc_now)


class TransactionClassification(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    transaction_id: UUID = Field(index=True)
    category: Category
    confidence: float
    method: str
    rationale: str
    created_at: datetime = Field(default_factory=utc_now)


class Subscription(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, default="demo-user")
    merchant_name: str = Field(index=True)
    typical_amount: Decimal = Field(decimal_places=2, max_digits=14)
    cadence: str
    status: str = "likely"
    confidence: float = 0.7
    first_seen: date
    last_seen: date
    created_at: datetime = Field(default_factory=utc_now)


class Insight(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, default="demo-user")
    title: str
    body: str
    insight_type: str
    estimated_impact: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=14)
    created_at: datetime = Field(default_factory=utc_now)
