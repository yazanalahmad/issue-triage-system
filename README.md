# Issue Triage System

Backend service for triaging incoming issues with a simple rule-based classifier. Designed to evolve from a clean, stable API into a full triage platform with a data layer, frontend, and ML-based classification.

## What this is
- A FastAPI backend that accepts issues and returns a triaged result.
- A foundation for a production-ready triage workflow.

## API
### Create issue
`POST /issues`

Request body:
```json
{
  "title": "Payments failing for EU users",
  "description": "Checkout returns 500 after submitting card details.",
  "service": "checkout",
  "environment": "prod"
}
```

Response:
```json
{
  "id": "b1c2f02e-7a8d-4a36-9dc1-8e5b3b6c5a8f",
  "title": "Payments failing for EU users",
  "description": "Checkout returns 500 after submitting card details.",
  "service": "checkout",
  "environment": "prod",
  "status": "new",
  "predicted_severity": "critical",
  "predicted_category": "outage",
  "created_at": "2025-01-01T12:00:00Z"
}
```

### Error responses
All error responses use a single envelope:
```json
{
  "code": "validation_error",
  "message": "Request validation failed.",
  "details": {
    "errors": []
  }
}
```

Health:
- `GET /health` -> `{"status": "ok"}`

## Local setup
1) Create and activate a virtual environment
2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Set environment variables (example)
```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/triage
DB_SCHEMA=issue_triage
```

4) Run the API
```bash
uvicorn app.main:app --reload
```

## Roadmap (planned improvements)
- Data layer discipline: SQLAlchemy models, Alembic migrations, DB constraints, and indexes
- API contract hardening: explicit response models, enums, and error shapes
- Tests: unit tests for triage rules + integration tests for the create issue flow
- Observability: structured logging and error tracking
- Frontend: dashboard for issue intake and triage visualization
- AI: replace rule-based triage with a model and add evaluation metrics

## Project status
- v0.1: API skeleton + rule-based triage + unified error responses

## Notes
Each milestone focuses on a specific engineering practice to mirror production-quality systems.
