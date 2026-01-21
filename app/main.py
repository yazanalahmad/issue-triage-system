from fastapi import FastAPI
from app.api.issues import router as issues_router

app = FastAPI(title="Issue Triage System")

app.include_router(issues_router)


@app.get("/health")
def health():
    return {"status": "ok"}