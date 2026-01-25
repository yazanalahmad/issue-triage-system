from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.enums import Environment, IssueStatus, Severity, Category


class IssueCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=5000)
    service: str = Field(min_length=2, max_length=100)
    environment: Environment


class IssueRead(BaseModel):
    id: UUID
    title: str
    description: str
    service: str
    environment: Environment
    status: IssueStatus
    predicted_severity: Severity | None
    predicted_category: Category | None
    created_at: datetime


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict[str, object] | None = None
