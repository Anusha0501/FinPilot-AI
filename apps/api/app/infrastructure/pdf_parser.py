from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

import fitz
import pdfplumber


@dataclass(frozen=True)
class ParsedTransaction:
    posted_date: date
    description_raw: str
    amount: Decimal
    balance_after: Decimal | None
    source_page: int
    confidence: float


_AMOUNT_RE = re.compile(r"-?\$?\(?\d{1,3}(?:,\d{3})*(?:\.\d{2})\)?|-?\$?\d+\.\d{2}")
_DATE_RE = re.compile(r"(?P<date>\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)")


def _parse_date(value: str, default_year: int) -> date | None:
    value = value.strip()
    for fmt in ("%m/%d/%Y", "%m/%d/%y", "%m-%d-%Y", "%m-%d-%y", "%m/%d", "%m-%d"):
        try:
            parsed = datetime.strptime(value, fmt)
            if fmt in {"%m/%d", "%m-%d"}:
                return parsed.date().replace(year=default_year)
            return parsed.date()
        except ValueError:
            continue
    return None


def _parse_amount(value: str) -> Decimal | None:
    cleaned = value.replace("$", "").replace(",", "").strip()
    negative = cleaned.startswith("(") and cleaned.endswith(")")
    cleaned = cleaned.strip("()")
    try:
        amount = Decimal(cleaned).quantize(Decimal("0.01"))
    except InvalidOperation:
        return None
    return -amount if negative else amount


def _transaction_from_line(line: str, page: int, default_year: int) -> ParsedTransaction | None:
    date_match = _DATE_RE.search(line)
    amounts = _AMOUNT_RE.findall(line)
    if not date_match or not amounts:
        return None
    posted = _parse_date(date_match.group("date"), default_year)
    amount = _parse_amount(amounts[-2] if len(amounts) > 1 else amounts[-1])
    balance = _parse_amount(amounts[-1]) if len(amounts) > 1 else None
    if posted is None or amount is None:
        return None
    description = line[date_match.end() :].replace(amounts[-1], "")
    if len(amounts) > 1:
        description = description.replace(amounts[-2], "")
    description = re.sub(r"\s+", " ", description).strip(" -|•\t")
    if not description:
        return None
    confidence = 0.82 if balance is not None else 0.68
    return ParsedTransaction(posted, description, amount, balance, page, confidence)


def parse_pdf_transactions(path: Path) -> list[ParsedTransaction]:
    default_year = date.today().year
    parsed: list[ParsedTransaction] = []

    with pdfplumber.open(path) as pdf:
        for page_index, page in enumerate(pdf.pages, start=1):
            for table in page.extract_tables() or []:
                for row in table:
                    line = " ".join(cell or "" for cell in row)
                    tx = _transaction_from_line(line, page_index, default_year)
                    if tx:
                        parsed.append(tx)
            text = page.extract_text() or ""
            for line in text.splitlines():
                tx = _transaction_from_line(line, page_index, default_year)
                if tx:
                    parsed.append(tx)

    if parsed:
        return _dedupe(parsed)

    # PyMuPDF fallback handles PDFs where pdfplumber text extraction is weak.
    document = fitz.open(path)
    for page_index, page in enumerate(document, start=1):
        for line in page.get_text().splitlines():
            tx = _transaction_from_line(line, page_index, default_year)
            if tx:
                parsed.append(tx)
    return _dedupe(parsed)


def _dedupe(items: list[ParsedTransaction]) -> list[ParsedTransaction]:
    seen: set[tuple[date, str, Decimal]] = set()
    unique: list[ParsedTransaction] = []
    for item in items:
        key = (item.posted_date, item.description_raw.lower(), item.amount)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique
