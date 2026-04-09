import logging
import tempfile
from typing import Annotated, Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from markitdown import MarkItDown, StreamInfo
from src.markitdown.models import ConvertResponse

router = APIRouter()

md = MarkItDown()


@router.post("/convert", response_model=ConvertResponse)
async def convert_file(
    file: Annotated[UploadFile | None, File()] = None,
    url: Annotated[str | None, Form()] = None,
) -> Any:
    if not file and not url:
        raise HTTPException(status_code=400, detail="Provide file or url")

    try:
        if url:
            result = md.convert(url)
            return ConvertResponse(
                source="url",
                filename=None,
                title=result.title,
                content=result.markdown,
                content_type="text/html",
            )
            return {"source": "url", "content": result.text_content}

        if file:
            with tempfile.NamedTemporaryFile(delete=True) as tmp:
                contents = await file.read()
                tmp.write(contents)
                tmp.flush()
                tmp.seek(0)

                result = md.convert(
                    tmp.name,
                    stream_info=StreamInfo(
                        filename=file.filename,
                        mimetype=file.content_type,
                    ),
                )

                return ConvertResponse(
                    source="file",
                    filename=file.filename,
                    title=result.title,
                    content=result.markdown,
                    content_type=file.content_type,
                )

    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
