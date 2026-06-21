from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session, select

from app.domain.models import Statement, Transaction
from app.domain.schemas import ChatRequest, ChatResponse, DashboardSummary, StatementRead, TransactionRead, UploadResponse
from app.infrastructure.database import get_session
from app.services.analytics_service import AnalyticsService
from app.services.statement_service import StatementService

router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/statements", response_model=UploadResponse)
async def upload_statement(file: UploadFile = File(...), session: Session = Depends(get_session)):
    try:
        statement = await StatementService(session).upload_statement(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return UploadResponse(
        statement_id=statement.id,
        status=statement.status,
        file_name=statement.file_name,
        created_at=statement.created_at,
    )


@router.get("/statements", response_model=list[StatementRead])
def list_statements(session: Session = Depends(get_session)):
    return session.exec(select(Statement).order_by(Statement.created_at.desc())).all()


@router.post("/statements/{statement_id}/process", response_model=StatementRead)
def process_statement(statement_id: UUID, session: Session = Depends(get_session)):
    try:
        return StatementService(session).process_statement(statement_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/transactions", response_model=list[TransactionRead])
def list_transactions(session: Session = Depends(get_session)):
    rows = session.exec(select(Transaction).order_by(Transaction.posted_date.desc())).all()
    return [TransactionRead(**row.model_dump()) for row in rows]


@router.post("/agents/audit")
def run_audit(session: Session = Depends(get_session)):
    return StatementService(session).run_audit()


@router.get("/analytics/summary", response_model=DashboardSummary)
def dashboard_summary(session: Session = Depends(get_session)):
    return AnalyticsService(session).summary()


@router.get("/subscriptions")
def subscriptions(session: Session = Depends(get_session)):
    return AnalyticsService(session).subscriptions()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, session: Session = Depends(get_session)):
    return AnalyticsService(session).chat(request.message)
