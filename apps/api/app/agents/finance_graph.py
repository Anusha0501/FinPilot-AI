from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from decimal import Decimal
from statistics import mean

from app.domain.models import Category, Transaction

KEYWORDS: dict[Category, tuple[str, ...]] = {
    Category.FOOD: ("restaurant", "coffee", "cafe", "grocery", "doordash", "uber eats", "starbucks"),
    Category.TRANSPORT: ("uber", "lyft", "fuel", "gas", "metro", "parking", "shell"),
    Category.SHOPPING: ("amazon", "walmart", "target", "store", "shop"),
    Category.HEALTHCARE: ("pharmacy", "clinic", "hospital", "doctor", "cvs"),
    Category.EDUCATION: ("course", "school", "udemy", "coursera", "book"),
    Category.RENT: ("rent", "apartment", "lease"),
    Category.UTILITIES: ("electric", "water", "internet", "phone", "utility"),
    Category.ENTERTAINMENT: ("netflix", "spotify", "movie", "hulu", "disney"),
    Category.TRAVEL: ("hotel", "airlines", "flight", "airbnb", "booking"),
    Category.INVESTMENTS: ("brokerage", "mutual fund", "vanguard", "fidelity"),
    Category.EMI: ("loan", "emi", "mortgage", "installment"),
}


@dataclass
class ClassificationResult:
    transaction_id: str
    category: Category
    confidence: float
    method: str
    rationale: str


@dataclass
class AgentResult:
    classifications: list[ClassificationResult] = field(default_factory=list)
    subscriptions: list[dict] = field(default_factory=list)
    insights: list[dict] = field(default_factory=list)
    report: dict = field(default_factory=dict)


class FinanceAuditGraph:
    """Demo-ready LangGraph-shaped workflow with deterministic fallbacks.

    The class mirrors the requested LangGraph nodes while staying runnable without paid API keys.
    In production, each method can be wrapped as a LangGraph node and the classifier can call
    Gemini 2.5 Flash when rule confidence is low.
    """

    def run(self, transactions: list[Transaction]) -> AgentResult:
        cleaned = self.transaction_cleaner(transactions)
        classifications = self.category_classifier(cleaned)
        subscriptions = self.subscription_detector(cleaned)
        budget = self.budget_analyzer(cleaned, classifications)
        insights = self.insight_generator(budget, subscriptions)
        report = self.report_generator(cleaned, classifications, subscriptions, insights)
        return AgentResult(classifications, subscriptions, insights, report)

    def transaction_cleaner(self, transactions: list[Transaction]) -> list[Transaction]:
        return sorted(transactions, key=lambda tx: (tx.posted_date, tx.description_normalized))

    def category_classifier(self, transactions: list[Transaction]) -> list[ClassificationResult]:
        results: list[ClassificationResult] = []
        for tx in transactions:
            text = tx.description_normalized.lower()
            match = Category.MISC
            confidence = 0.52
            rationale = "No strong keyword matched; assigned Misc for review."
            for category, keywords in KEYWORDS.items():
                if any(keyword in text for keyword in keywords):
                    match = category
                    confidence = 0.88
                    rationale = f"Matched merchant text to {category} spending keywords."
                    break
            results.append(ClassificationResult(str(tx.id), match, confidence, "rules", rationale))
        return results

    def subscription_detector(self, transactions: list[Transaction]) -> list[dict]:
        by_merchant: dict[str, list[Transaction]] = defaultdict(list)
        for tx in transactions:
            if tx.amount < 0:
                by_merchant[tx.merchant_name].append(tx)
        candidates: list[dict] = []
        for merchant, rows in by_merchant.items():
            if len(rows) < 2:
                continue
            amounts = [abs(float(row.amount)) for row in rows]
            if max(amounts) - min(amounts) <= max(3.0, mean(amounts) * 0.15):
                candidates.append(
                    {
                        "merchant_name": merchant,
                        "typical_amount": round(mean(amounts), 2),
                        "cadence": "monthly" if len(rows) <= 3 else "frequent",
                        "confidence": 0.76,
                        "first_seen": min(row.posted_date for row in rows).isoformat(),
                        "last_seen": max(row.posted_date for row in rows).isoformat(),
                    }
                )
        return candidates

    def budget_analyzer(
        self, transactions: list[Transaction], classifications: list[ClassificationResult]
    ) -> dict:
        category_by_id = {item.transaction_id: item.category for item in classifications}
        totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
        income = Decimal("0.00")
        expenses = Decimal("0.00")
        for tx in transactions:
            if tx.amount > 0:
                income += tx.amount
            else:
                expenses += abs(tx.amount)
                totals[str(category_by_id.get(str(tx.id), Category.MISC))] += abs(tx.amount)
        return {"income": income, "expenses": expenses, "category_totals": dict(totals)}

    def insight_generator(self, budget: dict, subscriptions: list[dict]) -> list[dict]:
        insights: list[dict] = []
        category_totals = budget["category_totals"]
        if category_totals:
            top_category, top_amount = max(category_totals.items(), key=lambda item: item[1])
            insights.append(
                {
                    "type": "spending_leak",
                    "title": f"Highest spend category: {top_category}",
                    "body": f"You spent ${top_amount:.2f} in {top_category}. Review the top merchants for possible savings.",
                    "estimated_impact": round(float(top_amount) * 0.1, 2),
                }
            )
        if subscriptions:
            monthly = sum(item["typical_amount"] for item in subscriptions)
            insights.append(
                {
                    "type": "subscription_audit",
                    "title": "Recurring payments detected",
                    "body": f"Detected {len(subscriptions)} recurring merchants totaling about ${monthly:.2f} per cycle.",
                    "estimated_impact": round(monthly * 0.2, 2),
                }
            )
        return insights

    def report_generator(
        self,
        transactions: list[Transaction],
        classifications: list[ClassificationResult],
        subscriptions: list[dict],
        insights: list[dict],
    ) -> dict:
        return {
            "transaction_count": len(transactions),
            "classified_count": len(classifications),
            "subscription_count": len(subscriptions),
            "insight_count": len(insights),
        }
