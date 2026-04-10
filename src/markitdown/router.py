import asyncio
import logging
import tempfile
from typing import Annotated, Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from markitdown import MarkItDown, StreamInfo
from src.markitdown.models import ExtractResponse

router = APIRouter()
md = MarkItDown()


def perform_conversion(
    md_instance: MarkItDown, source: str | bytes, **kwargs: Any
) -> Any:
    """
    Synchronous wrapper to be run in a thread pool.
    """
    return md_instance.convert(source, **kwargs)  # ty: ignore[invalid-argument-type]


async def process_url(url: str) -> ExtractResponse:
    try:
        result = await run_in_threadpool(perform_conversion, md, url)
        return ExtractResponse(
            source="url",
            filename=None,
            title=result.title,
            markdown=result.markdown,
            content_type="text/html",
        )
    except Exception as e:
        logging.error(f"Error converting URL {url}: {e}")
        raise e


async def process_file(file: UploadFile) -> ExtractResponse:
    try:
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp.flush()

            result = await run_in_threadpool(
                perform_conversion,
                md,
                tmp.name,
                stream_info=StreamInfo(
                    filename=file.filename,
                    mimetype=file.content_type,
                ),
            )

            return ExtractResponse(
                source="file",
                filename=file.filename,
                title=result.title,
                markdown=result.markdown,
                content_type=file.content_type,
            )
    except Exception as e:
        logging.error(f"Error converting file {file.filename}: {e}")
        raise e


@router.post("/extract", response_model=list[ExtractResponse])
async def extract_multiple(
    file: Annotated[list[UploadFile] | None, File()] = None,
    url: Annotated[list[str] | None, Form()] = None,
) -> Any:
    if not file and not url:
        raise HTTPException(status_code=400, detail="Provide at least one file or url")

    tasks = []

    if url:
        for url_item in url:
            tasks.append(process_url(url_item))

    if file:
        for file_item in file:
            tasks.append(process_file(file_item))

    try:
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results
    except Exception as e:
        logging.exception("Batch conversion failed")
        raise HTTPException(status_code=500, detail=str(e))
