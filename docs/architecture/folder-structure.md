# FinPilot-AI Folder Structure

## 1. Proposed Repository Layout

```text
FinPilot-AI/
├── apps/
│   ├── web/                         # Next.js 15 frontend
│   │   ├── app/                     # App Router pages and layouts
│   │   ├── components/              # Reusable UI components
│   │   ├── features/                # Feature-specific UI modules
│   │   ├── lib/                     # Frontend utilities and API client
│   │   └── tests/                   # Frontend tests
│   └── api/                         # FastAPI backend
│       ├── app/
│       │   ├── api/                 # Route handlers
│       │   ├── core/                # Settings, logging, security
│       │   ├── domain/              # Business entities and rules
│       │   ├── services/            # Application use cases
│       │   ├── infrastructure/      # DB, PDF, storage, LLM integrations
│       │   ├── agents/              # LangGraph workflows and nodes
│       │   └── main.py              # FastAPI application factory
│       └── tests/                   # Backend tests
├── packages/
│   └── shared/                      # Shared schemas or generated clients if needed
├── docs/
│   ├── api/                         # API design docs
│   ├── architecture/                # Architecture and diagrams
│   ├── database/                    # Database design
│   └── product/                     # PRD and user stories
├── infra/                           # Deployment notes and config templates
├── .github/
│   ├── ISSUE_TEMPLATE/              # Future issue templates
│   └── pull_request_template.md     # Future PR template
├── README.md
└── .env.example
```

## 2. What
This layout separates deployable applications, reusable packages, documentation, and infrastructure assets.

## 3. Why
A finance AI assistant has multiple layers: web UI, API, document processing, AI workflows, database models, and deployment config. Separating them prevents route handlers, UI components, and AI prompts from becoming tangled.

## 4. How
- `apps/web` owns all frontend code.
- `apps/api` owns all backend code.
- `apps/api/app/domain` contains rules that should not know about FastAPI or LangChain.
- `apps/api/app/infrastructure` contains adapters for external systems.
- `apps/api/app/agents` contains LangGraph state, nodes, prompts, and graph assembly.
- `docs` captures decisions before code is written.

## 5. Alternatives

### Single `frontend/` and `backend/` folders
Simpler for beginners, but less scalable if shared packages or deployment tooling grow.

### Full monorepo tooling immediately
Tools like Turborepo or Nx are powerful, but unnecessary until both apps have real build pipelines.

### Backend-only first
Good for API-first learning, but the project goal includes a polished SaaS-style UI.

## 6. Best Practices

- Keep imports pointing inward: routes call services, services call domain and infrastructure.
- Do not put business logic in React components.
- Do not put LLM prompts directly inside route handlers.
- Keep diagrams and decisions updated as architecture changes.
- Add tests near the app they validate.

## 7. Phase 1 Concept Check

1. Why should `domain` not import from `infrastructure`?
2. Where should a PDF parser implementation live?
3. Where should category labels be defined so frontend and backend stay consistent?

## 8. Exercises

1. Create the future empty folders from this structure.
2. Add a `docs/decisions` folder for Architecture Decision Records.
3. Propose where mock bank statements should live for tests.
