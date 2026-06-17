"""Custom application exceptions and FastAPI exception handlers."""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class IngestError(Exception):
    """Raised when PDF ingestion fails."""


class QueryError(Exception):
    """Raised when a RAG query fails."""


class VectorStoreError(Exception):
    """Raised on ChromaDB errors."""


class LLMError(Exception):
    """Raised when the LLM API call fails after retries."""


async def ingest_error_handler(request: Request, exc: IngestError) -> JSONResponse:
    logger.error("IngestError: %s", exc)
    return JSONResponse(status_code=422, content={"detail": str(exc)})


async def query_error_handler(request: Request, exc: QueryError) -> JSONResponse:
    logger.error("QueryError: %s", exc)
    return JSONResponse(status_code=500, content={"detail": str(exc)})


async def vector_store_error_handler(
    request: Request, exc: VectorStoreError
) -> JSONResponse:
    logger.error("VectorStoreError: %s", exc)
    return JSONResponse(
        status_code=503,
        content={"detail": "Vector store unavailable. Please re-ingest the document."},
    )


async def llm_error_handler(request: Request, exc: LLMError) -> JSONResponse:
    logger.error("LLMError: %s", exc)
    return JSONResponse(
        status_code=503,
        content={"detail": "LLM service unavailable. Please try again later."},
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred."},
    )
