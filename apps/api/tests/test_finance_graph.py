from datetime import date
from decimal import Decimal
from uuid import uuid4

from app.agents.finance_graph import FinanceAuditGraph
from app.domain.models import Transaction


def make_tx(description: str, amount: str) -> Transaction:
    return Transaction(
        statement_id=uuid4(),
        posted_date=date(2026, 5, 1),
        description_raw=description,
        description_normalized=description,
        merchant_name=description.split()[0],
        amount=Decimal(amount),
        direction="debit" if Decimal(amount) < 0 else "credit",
    )


def test_graph_classifies_and_generates_insights():
    transactions = [make_tx("Uber Trip", "-18.00"), make_tx("Netflix", "-15.99")]
    result = FinanceAuditGraph().run(transactions)
    assert result.report["transaction_count"] == 2
    assert {item.category for item in result.classifications}
    assert result.insights
