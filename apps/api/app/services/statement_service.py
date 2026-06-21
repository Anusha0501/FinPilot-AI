from __future__ import annotations

from datetime import date
from pathlib import Path
from uuid import UUID

from fastapi import UploadFile
from sqlmodel import Session, select

from app.agents.finance_graph import FinanceAuditGraph
from app.core.config import settings
from app.domain.models import Insight, Statement, StatementStatus, Subscription, Transaction, TransactionClassification
from app.infrastructure.pdf_parser import parse_pdf_transactions
from app.services.normalization import direction_for_amount, merchant_from_description, normalize_description


class StatementService:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def upload_statement(self, file: UploadFile) -> Statement:
        if file.content_type != "application/pdf" and not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are supported.")
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)
        statement = Statement(file_name=file.filename, storage_path="pending")
        self.session.add(statement)
        self.session.commit()
        self.session.refresh(statement)
        path = upload_dir / f"{statement.id}.pdf"
        content = await file.read()
        if len(content) > settings.max_upload_mb * 1024 * 1024:
            raise ValueError(f"PDF exceeds {settings.max_upload_mb}MB limit.")
        path.write_bytes(content)
        statement.storage_path = str(path)
        self.session.add(statement)
        self.session.commit()
        self.session.refresh(statement)
        return statement

    def process_statement(self, statement_id: UUID) -> Statement:
        statement = self.session.get(Statement, statement_id)
        if statement is None:
            raise LookupError("Statement not found.")
        statement.status = StatementStatus.PROCESSING
        self.session.add(statement)
        self.session.commit()
        try:
            parsed_rows = parse_pdf_transactions(Path(statement.storage_path))
            if not parsed_rows:
                raise ValueError("No transactions found. Scanned PDFs may require OCR.")
            for row in parsed_rows:
                normalized = normalize_description(row.description_raw)
                tx = Transaction(
                    statement_id=statement.id,
                    posted_date=row.posted_date,
                    description_raw=row.description_raw,
                    description_normalized=normalized,
                    merchant_name=merchant_from_description(normalized),
                    amount=row.amount,
                    direction=direction_for_amount(row.amount),
                    balance_after=row.balance_after,
                    source_page=row.source_page,
                    extraction_confidence=row.confidence,
                )
                self.session.add(tx)
            statement.period_start = min(row.posted_date for row in parsed_rows)
            statement.period_end = max(row.posted_date for row in parsed_rows)
            statement.status = StatementStatus.COMPLETED
            statement.error_message = None
        except Exception as exc:  # service boundary records processing failure
            statement.status = StatementStatus.FAILED
            statement.error_message = str(exc)
        self.session.add(statement)
        self.session.commit()
        self.session.refresh(statement)
        return statement

    def run_audit(self) -> dict:
        transactions = list(self.session.exec(select(Transaction)).all())
        result = FinanceAuditGraph().run(transactions)
        for item in result.classifications:
            self.session.add(
                TransactionClassification(
                    transaction_id=UUID(item.transaction_id),
                    category=item.category,
                    confidence=item.confidence,
                    method=item.method,
                    rationale=item.rationale,
                )
            )
        for item in result.subscriptions:
            self.session.add(
                Subscription(
                    merchant_name=item["merchant_name"],
                    typical_amount=item["typical_amount"],
                    cadence=item["cadence"],
                    confidence=item["confidence"],
                    first_seen=date.fromisoformat(item["first_seen"]),
                    last_seen=date.fromisoformat(item["last_seen"]),
                )
            )
        for item in result.insights:
            self.session.add(
                Insight(
                    title=item["title"], body=item["body"], insight_type=item["type"], estimated_impact=item["estimated_impact"]
                )
            )
        self.session.commit()
        return result.report
