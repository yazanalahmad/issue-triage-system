from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.issues import router as issues_router
from app.core.errors import (
    APIError,
    api_error_handler,
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI(title="Issue Triage System")

app.include_router(issues_router)
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/health")
def health():
    return {"status": "ok"}
