"""Ingest service — orchestrates PDF processing and vector store population."""

import logging
import os
from typing import Any, Dict

from app.core.config import get_settings
from app.rag.embedder import embed_documents
from app.rag.pdf_processor import process_pdf
from app.rag.vector_store import collection_count, ingest_chunks, reset_collection

logger = logging.getLogger(__name__)


def run_ingestion(
    pdf_path: str | None = None,
    force_reingest: bool = False,
) -> Dict[str, Any]:
    """
    Full ingestion pipeline:
      1. Optionally reset the existing ChromaDB collection.
      2. Extract and chunk the PDF.
      3. Embed all chunks.
      4. Upsert into ChromaDB.

    Args:
        pdf_path:       Override the PDF path from settings.
        force_reingest: If True, deletes the existing collection first.

    Returns:
        Summary dict with message, chunks_created, pages_processed, collection_name.
    """
    settings = get_settings()
    path = pdf_path or settings.pdf_path

    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found: {path}")

    if force_reingest:
        logger.info("Force re-ingest requested — resetting collection.")
        reset_collection()

    existing = collection_count()
    if existing > 0 and not force_reingest:
        logger.info("Collection already contains %d chunks. Skipping.", existing)
        return {
            "message": "Document already ingested. Use force_reingest=true to re-process.",
            "chunks_created": existing,
            "pages_processed": 0,
            "collection_name": settings.chroma_collection_name,
        }

    chunks = process_pdf(path)
    pages_processed = len({c["page_number"] for c in chunks})

    logger.info("Embedding %d chunks...", len(chunks))
    embeddings = embed_documents([c["text"] for c in chunks])

    count = ingest_chunks(chunks, embeddings)

    return {
        "message": "Ingestion complete.",
        "chunks_created": count,
        "pages_processed": pages_processed,
        "collection_name": settings.chroma_collection_name,
    }
