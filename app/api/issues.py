from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.schemas.issue import IssueCreate, IssueRead, ErrorResponse
from app.schemas.enums import IssueStatus, Severity, Category
from app.services.triage import predict_severity_and_category

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post(
    "",
    status_code=201,
    response_model=IssueRead,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def create_issue(payload: IssueCreate, db: Session = Depends(get_db)):
    try:
        severity_str, category_str = predict_severity_and_category(
            payload.title, payload.description
        )
        severity = Severity(severity_str)
        category = Category(category_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "invalid_triage",
                "message": "Predicted values are not valid enums.",
            },
        )

    q = text(
        """
        insert into issues (
            title, description, service, environment, status,
            predicted_severity, predicted_category
        )
        values (
            :title, :description, :service, :environment, :status,
            :predicted_severity, :predicted_category
        )
        returning id, title, description, service, environment, status,
                  predicted_severity, predicted_category, created_at
        """
    )

    try:
        row = (
            db.execute(
                q,
                {
                    "title": payload.title,
                    "description": payload.description,
                    "service": payload.service,
                    "environment": payload.environment,
                    "status": IssueStatus.new,
                    "predicted_severity": severity,
                    "predicted_category": category,
                },
            )
            .mappings()
            .first()
        )
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "code": "insert_failed",
                    "message": "Issue insert returned no row.",
                },
            )
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "db_error",
                "message": "Database operation failed.",
            },
        )

    return row
