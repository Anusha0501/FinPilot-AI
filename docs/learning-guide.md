# Progressive Learning Guide

## Backend API Module
- **What:** FastAPI routes expose upload, processing, analytics, subscriptions, audit, chat, and health endpoints.
- **Why:** A typed API boundary keeps the frontend independent from PDF parsing and AI orchestration details.
- **How:** Routes delegate to services instead of embedding business logic in handlers.
- **Alternatives:** Django REST Framework, Flask, or serverless functions.
- **Best Practices:** Keep route handlers thin, validate inputs, return stable IDs, and avoid logging financial PII.

## PDF Processing Module
- **What:** `pdfplumber` extracts tables/text first; PyMuPDF is the fallback text extractor.
- **Why:** Bank PDFs vary widely. A two-engine approach improves coverage while remaining free-tier compatible.
- **How:** Lines are scanned for date and money patterns, converted into parsed transaction records, deduplicated, normalized, and stored.
- **Alternatives:** Tesseract OCR for scanned PDFs, bank-specific parsers, or paid document AI APIs.
- **Best Practices:** Store source page and confidence, make parsers pluggable, and flag low-confidence rows for review.

## Finance Agent Module
- **What:** A LangGraph-shaped workflow cleans transactions, classifies categories, detects subscriptions, analyzes budgets, generates insights, and builds a report.
- **Why:** Agent workflows are easier to test and explain when each node has one responsibility.
- **How:** The current implementation uses deterministic fallbacks for demo reliability and can add Gemini 2.5 Flash for low-confidence classification.
- **Alternatives:** Single LLM prompt, batch classifier only, or fully deterministic rules.
- **Best Practices:** Use rules before LLMs, keep evidence with insights, trace model calls with LangSmith, and unit test non-LLM nodes.

## Frontend Module
- **What:** Next.js pages provide a SaaS-style dashboard, upload center, analytics, subscriptions, trends, planner, and chat assistant.
- **Why:** Recruiters and demo viewers understand the system faster through polished workflows and visuals.
- **How:** Server components fetch dashboard data, client components handle upload/chat interactions, and Recharts renders visuals.
- **Alternatives:** Streamlit for speed, React Router SPA, or a mobile-first app.
- **Best Practices:** Keep business logic in the backend, design empty states, and never expose secrets in client code.

## Concept Questions
1. Which parts of this project are deterministic analytics, and which parts benefit from AI?
2. Why is a confidence score important for extracted transactions and classifications?
3. How would you explain the difference between a PDF parser and a finance agent in an interview?

## Exercises
1. Add a bank-specific parser for a sample statement format.
2. Add a user correction endpoint for transaction categories.
3. Replace the rule classifier with Gemini only when confidence is below 0.7.
4. Add a screenshot to the README after running the frontend locally.
