# FinPilot-AI Product Requirements Document

## 1. Product Vision

FinPilot-AI is an AI-powered personal finance audit agent that turns PDF bank statements into clear, actionable financial intelligence. It helps users understand where money goes, identify waste, detect recurring subscriptions, and receive practical savings recommendations through dashboards and conversational insights.

## 2. Learning Goal

This project is intentionally built in phases so an AI Engineering learner can understand each architectural layer before writing production code. Phase 1 defines the product, system boundaries, and technical design before implementation begins.

## 3. Target Users

### Primary User: Individual Budget Optimizer
- Uploads monthly bank statements.
- Wants spending summaries, leaks, and savings ideas.
- Needs simple language, charts, and trustworthy calculations.

### Secondary User: AI Engineering Learner
- Wants to understand document processing, LangGraph workflows, FastAPI APIs, and finance analytics.
- Needs explanations, tradeoffs, exercises, and interview-ready system design knowledge.

## 4. Problems to Solve

1. Bank statements are hard to analyze manually.
2. Transaction descriptions are noisy and inconsistent.
3. Subscriptions and small recurring charges are easy to forget.
4. Generic budgeting apps often require live bank integrations that may not be free or privacy-friendly.
5. Users need explanations, not just charts.

## 5. Goals

### Product Goals
- Accept PDF bank statements.
- Extract, clean, and normalize transactions.
- Categorize transactions into personal finance categories.
- Detect subscriptions and recurring payments.
- Identify spending spikes, anomalies, and leaks.
- Generate weekly/monthly insights and savings recommendations.
- Provide interactive dashboards and AI chat.

### Engineering Goals
- Use clean architecture and modular boundaries.
- Keep free-tier deployment compatibility.
- Make AI workflows explainable and testable.
- Avoid vendor lock-in where reasonable.
- Build in phases with strong documentation.

## 6. Non-Goals for Initial Version

- Direct bank account linking through Plaid or open banking.
- Investment advice or regulated financial advisory decisions.
- Tax filing, credit underwriting, or loan recommendations.
- Multi-currency accounting beyond basic normalization hooks.
- Full OCR for scanned statements in Phase 2. OCR is documented as a limitation and future enhancement.

## 7. Functional Requirements

### PDF Statement Upload
- User uploads one or more PDF bank statements.
- System validates file type, size, and ownership.
- Backend stores upload metadata and extraction status.

### Transaction Extraction
- System parses statement text and tables using pdfplumber and PyMuPDF.
- System extracts transaction date, description, amount, debit/credit direction, balance when available, and source page.
- System flags low-confidence or incomplete rows for review.

### Categorization
- AI classifies normalized transactions into the configured category taxonomy.
- Deterministic rules handle obvious patterns before model calls to reduce cost.
- Classifier returns category, confidence, and rationale.

### Subscription Detection
- System detects recurring merchant patterns by amount, cadence, and description similarity.
- System labels likely subscriptions and exposes them to the dashboard.

### Spending Intelligence
- System calculates category totals, monthly trends, anomalies, and budget risk indicators.
- System generates recommendations with estimated monthly savings impact.

### Conversational Assistant
- User can ask finance questions grounded in their extracted transaction data.
- Assistant must not provide regulated financial advice.

## 8. Non-Functional Requirements

### Privacy and Security
- Uploaded statements contain sensitive financial data and must be treated as private.
- Use authenticated access before production deployment.
- Store secrets only in environment variables.
- Minimize raw PDF retention and allow deletion.

### Reliability
- Extraction pipeline should be idempotent by statement ID.
- Failed extraction steps should be retryable.
- Persist processing status for long-running jobs.

### Observability
- Backend logs structured events with request IDs.
- LangGraph runs are observable through LangSmith free tier.
- Store extraction confidence and AI classification confidence for debugging.

### Performance
- Keep initial PDF processing synchronous only for small files.
- Design for future background jobs when files are larger.
- Avoid unnecessary LLM calls by batching and using rules first.

## 9. Success Metrics

- Transaction extraction precision for supported statement formats: target 90%+ after format tuning.
- Categorization accuracy on manually labeled sample set: target 85%+.
- Subscription detection recall on sample data: target 80%+.
- Time from upload to dashboard for a typical statement: under 30 seconds in MVP.
- User can explain system architecture and LangGraph node responsibilities after completing phases.

## 10. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---:|---|
| PDF formats vary by bank | High | Create pluggable parsers and confidence flags |
| Scanned PDFs need OCR | Medium | Document limitation; add OCR later with Tesseract or cloud OCR |
| LLM misclassification | Medium | Use deterministic rules, confidence thresholds, review queue |
| Sensitive data leakage | High | Redact logs, store secrets securely, avoid sending unnecessary PII |
| Free-tier constraints | Medium | Batch model calls, limit file size, design efficient schemas |

## 11. Phase 1 Concept Check

1. Why do we define non-goals before coding?
2. Which requirements should be deterministic instead of AI-driven?
3. What sensitive fields should never appear in logs?

## 12. Exercises

1. Write three acceptance criteria for the PDF upload feature.
2. Add one new user persona and explain how it changes the product scope.
3. List five banks whose PDF formats you may want to test later.
