# Deployment Guide

## Backend: Railway
1. Create a Railway project from the repository.
2. Set root directory to `apps/api`.
3. Configure environment variables from `.env.example`.
4. Use Supabase PostgreSQL as `DATABASE_URL` for production.
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

## Frontend: Vercel
1. Import the repository in Vercel.
2. Set root directory to `apps/web`.
3. Set `NEXT_PUBLIC_API_BASE_URL` to the Railway API URL plus `/api/v1`.
4. Deploy with the default Next.js build command.

## Database: Supabase
1. Create a free Supabase project.
2. Copy the pooled PostgreSQL connection string.
3. Enable Row Level Security before real users upload statements.
4. Keep uploaded PDFs private and scoped by user ID.

## Monitoring: LangSmith
1. Create a free LangSmith account.
2. Set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY`.
3. Trace LangGraph nodes once Gemini-backed classification is enabled.
