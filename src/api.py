from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel

from src.markitdown.router import router as markitdown_router


class ErrorMessage(SQLModel):
    """Represents a single error message."""

    msg: str


class ErrorResponse(SQLModel):
    """Defines the structure for API error responses."""

    detail: list[ErrorMessage] | None = None


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

public_api_router = APIRouter()

public_api_router.include_router(
    markitdown_router, prefix="/markitdown", tags=["markitdown"]
)


@api_router.get("/health-check", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    """Simple healthcheck endpoint."""
    return {"status": "ok"}


api_router.include_router(public_api_router)
