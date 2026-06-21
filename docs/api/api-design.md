# FinPilot-AI API Design

## 1. API Principles

- Use REST for predictable resource operations.
- Keep request and response schemas typed with Pydantic/SQLModel.
- Return stable IDs for asynchronous tracking.
- Separate upload, processing, analytics, and chat concerns.
- Avoid returning sensitive raw PDF content to the frontend.

## 2. Endpoint Overview

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/v1/statements` | Upload a PDF statement |
| `GET` | `/api/v1/statements` | List uploaded statements |
| `GET` | `/api/v1/statements/{statement_id}` | Get statement status and metadata |
| `POST` | `/api/v1/statements/{statement_id}/process` | Start or retry extraction |
| `GET` | `/api/v1/transactions` | List normalized transactions |
| `PATCH` | `/api/v1/transactions/{transaction_id}` | Correct merchant/category metadata |
| `POST` | `/api/v1/agents/categorize` | Run categorization workflow |
| `GET` | `/api/v1/analytics/summary` | Get dashboard summary |
| `GET` | `/api/v1/analytics/categories` | Get category breakdown |
| `GET` | `/api/v1/subscriptions` | List subscription candidates |
| `GET` | `/api/v1/reports/monthly` | Get monthly report |
| `POST` | `/api/v1/chat` | Ask grounded finance questions |
| `GET` | `/api/v1/health` | Health check |

## 3. Example Schemas

### Upload Statement Response

```json
{
  "statement_id": "c0f2d8f0-1b37-4a3c-a8d4-873b65b9e6d1",
  "status": "uploaded",
  "file_name": "checking-may-2026.pdf",
  "created_at": "2026-06-21T12:00:00Z"
}
```

### Transaction Response

```json
{
  "id": "9dd4b0cf-3f18-4a0c-a7fd-4e65c3a9d021",
  "posted_date": "2026-05-12",
  "description_raw": "UBER TRIP HELP.UBER.COM",
  "description_normalized": "Uber Trip",
  "merchant_name": "Uber",
  "amount": -18.42,
  "direction": "debit",
  "category": "Transport",
  "classification_confidence": 0.93,
  "source_page": 2
}
```

### Chat Request

```json
{
  "message": "Why did my food spending increase in May?",
  "period_start": "2026-05-01",
  "period_end": "2026-05-31"
}
```

### Chat Response

```json
{
  "answer": "Your food spending increased mainly because restaurant transactions rose by 32% compared with April.",
  "evidence": [
    {
      "type": "category_delta",
      "category": "Food",
      "current_period_total": 486.12,
      "previous_period_total": 368.40
    }
  ],
  "disclaimer": "This is educational financial analysis, not regulated financial advice."
}
```

## 4. API Design Decisions

### Upload and Process Are Separate
**What:** Upload stores the PDF, while processing extracts transactions.

**Why:** This makes failures retryable and prepares the system for background jobs.

**How:** `POST /statements` creates the record. `POST /statements/{id}/process` starts parsing.

**Alternatives:** Process during upload. Simpler for demos, but brittle for larger files.

**Best Practices:** Return a statement ID immediately and expose status polling.

### Analytics Endpoints Are Read Models
**What:** Dashboard endpoints return aggregated summaries rather than raw SQL-shaped records.

**Why:** Frontend charts should not duplicate business logic.

**How:** Backend computes totals, trends, and category breakdowns.

**Alternatives:** Let the frontend aggregate all transactions. This increases client complexity and data transfer.

**Best Practices:** Keep analytics deterministic and test with fixtures.

### Chat Is Grounded
**What:** Chat endpoint receives a user question and time window, then grounds answers in stored transactions and reports.

**Why:** Finance assistants must avoid hallucinated numbers.

**How:** Retrieve relevant metrics first, pass compact evidence to the LLM, and return evidence with the answer.

**Alternatives:** Let the LLM query the database directly. Powerful, but riskier and harder to secure.

**Best Practices:** Use tool/function boundaries and never expose unrestricted SQL generation to the model.

## 5. Error Model

```json
{
  "error": {
    "code": "INVALID_FILE_TYPE",
    "message": "Only PDF statements are supported.",
    "request_id": "req_01J..."
  }
}
```

## 6. Phase 1 Concept Check

1. Why is status polling useful for PDF processing?
2. Which endpoints should require authentication?
3. Why should chat responses include evidence?

## 7. Exercises

1. Design the request and response for correcting a transaction category.
2. Add pagination parameters to `GET /transactions`.
3. Define three API error codes for PDF extraction failures.
