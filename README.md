# FinPilot-AI

FinPilot-AI is a production-oriented learning project for building an AI Personal Finance Audit Agent. It will accept PDF bank statements, extract and normalize transactions, categorize spending, detect subscriptions, identify spending leaks, generate reports, and provide conversational financial insights.

## Current Status

Phase 1 documentation is complete:

- Product Requirements Document
- User Stories
- Architecture Diagram
- Database Design
- API Design
- Folder Structure

Implementation will proceed progressively so each module can be explained, tested, and understood before the next layer is added.

## Planned Stack

- Frontend: Next.js 15, TypeScript, Tailwind, shadcn/ui, Recharts, Plotly
- Backend: FastAPI, PostgreSQL, SQLModel
- AI: LangGraph, LangChain, Gemini 2.5 Flash
- Document Processing: pdfplumber, PyMuPDF
- Storage: Supabase Free
- Deployment: Vercel, Railway
- Monitoring: LangSmith Free

## Documentation

- [PRD](docs/product/prd.md)
- [User Stories](docs/product/user-stories.md)
- [Architecture](docs/architecture/architecture.md)
- [Database Design](docs/database/schema.md)
- [API Design](docs/api/api-design.md)
- [Folder Structure](docs/architecture/folder-structure.md)
