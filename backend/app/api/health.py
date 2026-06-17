"""GET /health — liveness and readiness probe."""

import logging
from datetime import datetime, timezone

import groq
from fastapi import APIRouter

from app.core.config import get_settings
from app.rag.vector_store import collection_count

router = APIRouter(tags=["Health"])
logger = logging.getLogger(__name__)


@router.get("/health", summary="Health check")
async def health_check() -> dict:
    """
    Returns system status including vector store chunk count,
    and Groq API connectivity status.
    """
    settings = get_settings()

    # Check ChromaDB
    try:
        chunks = collection_count()
        vs_status = "ok"
    except Exception as exc:
        chunks = 0
        vs_status = f"error: {exc}"
        logger.warning("Vector store health check failed: %s", exc)

    # Check Groq reachability
    try:
        client = groq.Groq(api_key=settings.groq_api_key)
        client.models.list()
        groq_status = "ok"
    except Exception as exc:
        groq_status = f"unreachable: {exc}"
        logger.warning("Groq health check failed: %s", exc)

    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "embedding_model": settings.embedding_model,
        "llm_model": "llama-3.3-70b-versatile",
        "groq_status": groq_status,
        "vector_store": vs_status,
        "chunks_indexed": chunks,
    }
