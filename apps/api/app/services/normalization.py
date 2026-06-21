from __future__ import annotations

import re
from decimal import Decimal

from app.domain.models import Direction

_NOISE = [r"\bPOS\b", r"\bACH\b", r"\bDEBIT\b", r"\bCREDIT\b", r"\d{4,}", r"\*+"]


def normalize_description(raw: str) -> str:
    value = raw.upper()
    for pattern in _NOISE:
        value = re.sub(pattern, " ", value)
    value = re.sub(r"[^A-Z0-9&. ]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value.title() or "Unknown Merchant"


def merchant_from_description(description: str) -> str:
    tokens = description.split()
    if not tokens:
        return "Unknown Merchant"
    return " ".join(tokens[:3])


def direction_for_amount(amount: Decimal) -> Direction:
    return Direction.CREDIT if amount > 0 else Direction.DEBIT
