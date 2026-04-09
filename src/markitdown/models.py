from typing import Any, Literal

from sqlmodel import SQLModel


class ConvertResponse(SQLModel):
    source: Literal["file", "url"]
    filename: str | None = None
    content: str
    metadata: dict[str, Any] | None = None
