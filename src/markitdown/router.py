import os
import tempfile
from typing import Annotated, Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from markitdown import MarkItDown
from src.markitdown.models import ConvertResponse

router = APIRouter()

md = MarkItDown()


@router.post("/convert", response_model=ConvertResponse)
async def convert_file(
    file: Annotated[UploadFile | None, File()] = None,
    url: Annotated[str | None, Form()] = None,
) -> Any:
    try:
        if url:
            result = md.convert(url)
            return ConvertResponse(
                source="url",
                filename=None,
                content=result.text_content,
                metadata=getattr(result, "metadata", None),
            )
            return {"source": "url", "content": result.text_content}

        if file:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                contents = await file.read()
                tmp.write(contents)
                tmp_path = tmp.name

            try:
                result = md.convert(tmp_path)

                return ConvertResponse(
                    source="file",
                    filename=file.filename,
                    content=result.text_content,
                    metadata=getattr(result, "metadata", None),
                )
            finally:
                os.remove(tmp_path)

        raise HTTPException(status_code=400, detail="Provide file or url")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
