from typing import Literal

from sqlmodel import SQLModel


class ExtractResponse(SQLModel):
    source: Literal["file", "url"]
    filename: str | None = None
    title: str | None = None
    markdown: str
    content_type: str | None = None
