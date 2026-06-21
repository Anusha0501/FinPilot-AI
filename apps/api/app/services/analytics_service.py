from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from sqlmodel import Session, select

from app.domain.models import Insight, Subscription, Transaction, TransactionClassification


class AnalyticsService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def summary(self) -> dict:
        transactions = list(self.session.exec(select(Transaction)).all())
        classifications = list(self.session.exec(select(TransactionClassification)).all())
        latest_category = {str(item.transaction_id): item.category for item in classifications}
        income = sum((tx.amount for tx in transactions if tx.amount > 0), Decimal("0.00"))
        expenses = sum((abs(tx.amount) for tx in transactions if tx.amount < 0), Decimal("0.00"))
        merchants: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
        categories: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
        for tx in transactions:
            if tx.amount < 0:
                merchants[tx.merchant_name] += abs(tx.amount)
                categories[str(latest_category.get(str(tx.id), "Misc"))] += abs(tx.amount)
        top_merchants = sorted(
            ({"merchant": key, "amount": value} for key, value in merchants.items()),
            key=lambda item: item["amount"],
            reverse=True,
        )[:5]
        category_breakdown = [
            {"category": key, "amount": value} for key, value in sorted(categories.items())
        ]
        insights = [item.model_dump() for item in self.session.exec(select(Insight)).all()]
        savings_rate = float((income - expenses) / income) if income else 0.0
        return {
            "total_income": income,
            "total_expenses": expenses,
            "net_savings": income - expenses,
            "savings_rate": round(savings_rate, 4),
            "transaction_count": len(transactions),
            "top_merchants": top_merchants,
            "category_breakdown": category_breakdown,
            "insights": insights,
        }

    def subscriptions(self) -> list[Subscription]:
        return list(self.session.exec(select(Subscription)).all())

    def chat(self, message: str) -> dict:
        summary = self.summary()
        evidence = [
            {"type": "summary", "total_expenses": summary["total_expenses"], "net_savings": summary["net_savings"]},
            {"type": "top_categories", "items": summary["category_breakdown"][:5]},
        ]
        lowered = message.lower()
        if "subscription" in lowered:
            subs = self.subscriptions()
            total = sum((item.typical_amount for item in subs), Decimal("0.00"))
            answer = f"I found {len(subs)} recurring payment candidates totaling about ${total:.2f} per cycle. Review anything you no longer use."
        elif "save" in lowered or "saving" in lowered:
            leaks = summary["insights"][:2]
            answer = "Your best savings opportunities are: " + "; ".join(item["title"] for item in leaks) if leaks else "Upload and audit a statement first so I can estimate savings opportunities."
        else:
            answer = f"You have ${summary['total_expenses']:.2f} in expenses and ${summary['net_savings']:.2f} net savings in the loaded data."
        return {"answer": answer, "evidence": evidence}
