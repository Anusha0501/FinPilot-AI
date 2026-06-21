# FinPilot-AI User Stories

## Epic 1: Statement Upload

### Story 1.1: Upload a PDF Statement
As a user, I want to upload a PDF bank statement so that FinPilot-AI can analyze my spending without requiring bank login credentials.

**Acceptance Criteria**
- Only PDF files are accepted.
- The system rejects files over the configured size limit.
- The user sees upload status: uploaded, processing, completed, or failed.
- The backend stores upload metadata with user ownership.

### Story 1.2: Review Extraction Quality
As a user, I want to see whether transactions were extracted confidently so that I can trust the report.

**Acceptance Criteria**
- Each transaction has an extraction confidence score.
- Low-confidence rows are flagged.
- The source statement and page number are retained for auditability.

## Epic 2: Transaction Intelligence

### Story 2.1: Categorize Spending
As a user, I want transactions grouped into clear categories so that I can understand my spending patterns.

**Acceptance Criteria**
- Supported categories are Food, Transport, Shopping, Healthcare, Education, Rent, Utilities, Entertainment, Travel, Investments, EMI, and Misc.
- Each AI classification includes confidence and rationale.
- Low-confidence classifications can be reviewed later.

### Story 2.2: Detect Subscriptions
As a user, I want recurring payments identified so that I can cancel unwanted subscriptions.

**Acceptance Criteria**
- Recurring payments are detected by merchant similarity, amount similarity, and cadence.
- The system shows estimated monthly cost.
- The system distinguishes confirmed, likely, and possible subscriptions.

## Epic 3: Financial Reports

### Story 3.1: View Monthly Summary
As a user, I want a monthly financial report so that I can quickly understand income, expenses, savings rate, and top categories.

**Acceptance Criteria**
- Report includes total income, total expenses, net savings, top merchants, and category breakdown.
- Report includes plain-English insights.
- Report can be regenerated after categorization changes.

### Story 3.2: Find Spending Leaks
As a user, I want the system to identify avoidable spending leaks so that I can save money.

**Acceptance Criteria**
- Leaks include frequent small purchases, duplicate subscriptions, spikes, and high discretionary categories.
- Each recommendation includes reasoning and estimated impact.
- Recommendations are not presented as regulated financial advice.

## Epic 4: Conversational Assistant

### Story 4.1: Ask About Spending
As a user, I want to ask questions like "Why did my food spending increase?" so that I can understand my finances conversationally.

**Acceptance Criteria**
- Assistant answers using transaction data and report summaries.
- Assistant cites the time window and categories used.
- Assistant refuses or qualifies regulated financial advice.

## Epic 5: Learning Experience

### Story 5.1: Learn the Architecture
As a learner, I want every module explained with what, why, how, alternatives, and best practices so that I can discuss the system in interviews.

**Acceptance Criteria**
- Each phase has documentation before or alongside code.
- Each module includes conceptual questions.
- Each module includes exercises.
