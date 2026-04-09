from typing import Literal

from sqlmodel import SQLModel


class ConvertResponse(SQLModel):
    source: Literal["file", "url"]
    filename: str | None = None
    title: str | None = None
    content: str
    content_type: str | None = None
