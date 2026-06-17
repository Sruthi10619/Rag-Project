"""POST /ingest — ingest the AWS Customer Agreement PDF."""

import logging
import os
import shutil
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.core.config import Settings, get_settings
from app.schemas.ingest import IngestResponse
from app.services.ingest_service import run_ingestion

router = APIRouter(tags=["Ingestion"])
logger = logging.getLogger(__name__)


@router.post("/ingest", response_model=IngestResponse, summary="Ingest PDF document")
async def ingest_pdf(
    file: UploadFile | None = File(default=None),
    force_reingest: bool = Query(default=False, description="Delete existing data and re-process"),
    settings: Settings = Depends(get_settings),
) -> IngestResponse:
    """
    Ingest the AWS Customer Agreement PDF into the vector store.

    - Upload a file via multipart/form-data, **or**
    - Omit the file to use the PDF_PATH configured in the environment.

    Set `force_reingest=true` to delete existing vectors and re-process from scratch.
    """
    tmp_path: str | None = None
    try:
        if file is not None:
            suffix = os.path.splitext(file.filename or "")[1] or ".pdf"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = tmp.name
            result = run_ingestion(pdf_path=tmp_path, force_reingest=force_reingest)
        else:
            try:
                result = run_ingestion(force_reingest=force_reingest)
            except FileNotFoundError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Ingestion failed.")
        raise HTTPException(status_code=500, detail=f"Ingestion error: {exc}") from exc
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    return IngestResponse(**result)
