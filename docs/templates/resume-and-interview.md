# Resume Bullets and Interview Prep

## Resume Bullets
- Built a full-stack AI personal finance audit agent using Next.js, FastAPI, SQLModel, and a LangGraph-style workflow to extract, classify, and explain bank statement transactions.
- Designed a document-processing pipeline using pdfplumber and PyMuPDF with normalization, confidence scoring, and auditable source-page metadata.
- Implemented deterministic financial analytics for recurring payments, category spend, savings opportunities, and grounded conversational insights.
- Created a production-oriented architecture targeting Vercel, Railway, Supabase PostgreSQL, and LangSmith observability on free-tier services.

## Interview Questions
1. How do you handle inconsistent PDF statement formats?
2. Why use deterministic rules before calling an LLM?
3. How does LangGraph improve maintainability versus one large prompt?
4. How would you prevent hallucinated financial numbers in chat?
5. What data should be excluded from logs in a fintech application?
6. How would you scale PDF processing beyond synchronous requests?

## System Design Discussion
Start with the upload boundary, explain statement metadata, move into the parser, then transaction normalization, classification, subscription detection, analytics, and grounded chat. Emphasize privacy, auditability, deterministic calculations, confidence scoring, and observability.
