# FinPilot-AI

FinPilot-AI is a production-oriented AI Personal Finance Audit Agent. It accepts PDF bank statements, extracts and normalizes transactions, categorizes spending, detects subscriptions, identifies leaks, generates reports, and powers a conversational finance assistant.

## Demo-Ready Features

- FastAPI backend with clean application, domain, infrastructure, service, and agent boundaries.
- PDF transaction extraction using `pdfplumber` with a PyMuPDF fallback.
- SQLModel persistence, defaulting to SQLite locally and designed for Supabase PostgreSQL in production.
- LangGraph-shaped finance audit workflow with deterministic fallback nodes for demo reliability.
- Categorization taxonomy for Food, Transport, Shopping, Healthcare, Education, Rent, Utilities, Entertainment, Travel, Investments, EMI, and Misc.
- Subscription detection, spending leak insights, dashboard analytics, and grounded chat endpoint.
- Next.js 15 SaaS-style frontend with dashboard, upload center, spending analysis, subscription tracker, trends, savings planner, and AI chat pages.
- Deployment guide for Vercel, Railway, Supabase, and LangSmith.

## Repository Structure

```text
apps/api     FastAPI backend
apps/web     Next.js frontend
docs         Product, architecture, database, API, and deployment docs
.github      PR and issue templates
```

## Local Development

### Backend

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

### Frontend

```bash
npm install
npm run dev:web
```

Open `http://localhost:3000` for the frontend and `http://localhost:8000/docs` for the API docs.

## Demo Flow

1. Start the FastAPI backend.
2. Start the Next.js frontend.
3. Upload a PDF through `POST /api/v1/statements`.
4. Process it with `POST /api/v1/statements/{statement_id}/process`.
5. Run the audit with `POST /api/v1/agents/audit`.
6. Refresh the dashboard and ask questions in AI Chat.

## Documentation

- [PRD](docs/product/prd.md)
- [User Stories](docs/product/user-stories.md)
- [Architecture](docs/architecture/architecture.md)
- [Database Design](docs/database/schema.md)
- [API Design](docs/api/api-design.md)
- [Folder Structure](docs/architecture/folder-structure.md)
- [Deployment Guide](docs/deployment/guide.md)
