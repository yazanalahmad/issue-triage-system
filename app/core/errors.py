from typing import Any, cast

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.issue import ErrorResponse


class APIError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


def _error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    payload = ErrorResponse(code=code, message=message, details=details).model_dump()
    return JSONResponse(status_code=status_code, content=payload)


async def api_error_handler(_: Request, exc: Exception) -> JSONResponse:
    api_exc = cast(APIError, exc)
    return _error_response(
        status_code=api_exc.status_code,
        code=api_exc.code,
        message=api_exc.message,
        details=api_exc.details,
    )


async def http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    http_exc = cast(StarletteHTTPException, exc)
    if (
        isinstance(http_exc.detail, dict)
        and "code" in http_exc.detail
        and "message" in http_exc.detail
    ):
        detail = cast(dict[str, Any], http_exc.detail)
        return _error_response(
            status_code=http_exc.status_code,
            code=detail["code"],
            message=detail["message"],
            details=detail.get("details"),
        )

    return _error_response(
        status_code=http_exc.status_code,
        code="http_error",
        message=str(http_exc.detail),
        details={"status_code": http_exc.status_code},
    )


async def validation_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    validation_exc = cast(RequestValidationError, exc)
    return _error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="validation_error",
        message="Request validation failed.",
        details={"errors": validation_exc.errors()},
    )
