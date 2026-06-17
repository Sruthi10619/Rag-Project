"""PDF text extraction and sliding-window chunking using PyMuPDF."""

import logging
from typing import Any, Dict, List

import fitz  # PyMuPDF

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def extract_pages(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Open a PDF and extract plain text from each page.

    Returns:
        List of dicts with keys: page_number (1-indexed), text.
    """
    doc = fitz.open(pdf_path)
    pages: List[Dict[str, Any]] = []
    for idx in range(len(doc)):
        page = doc[idx]
        raw = page.get_text("text")
        cleaned = " ".join(raw.split())  # collapse whitespace/newlines
        if cleaned.strip():
            pages.append({"page_number": idx + 1, "text": cleaned})
    doc.close()
    logger.info("Extracted %d non-empty pages from %s", len(pages), pdf_path)
    return pages


def chunk_page(
    text: str,
    page_number: int,
    source: str,
    chunk_size: int,
    chunk_overlap: int,
) -> List[Dict[str, Any]]:
    """
    Sliding-window character-level chunking for a single page.

    Chunk size: 800 chars (~150-200 words) fits one legal clause.
    Overlap: 150 chars preserves sentence context across boundaries.
    """
    chunks: List[Dict[str, Any]] = []
    start = 0
    idx = 0
    step = chunk_size - chunk_overlap

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]
        if chunk_text.strip():
            chunks.append(
                {
                    "chunk_id": f"p{page_number}_c{idx}",
                    "page_number": page_number,
                    "source": source,
                    "text": chunk_text,
                }
            )
            idx += 1
        start += step

    return chunks


def process_pdf(
    pdf_path: str,
    source_name: str = "aws_customer_agreement",
) -> List[Dict[str, Any]]:
    """
    Full ingestion pipeline: extract pages → chunk → return all chunks.

    Args:
        pdf_path:    Absolute or relative path to the PDF file.
        source_name: Value stored in chunk metadata 'source' field.

    Returns:
        Flat list of chunk dicts ready for embedding.
    """
    settings = get_settings()
    pages = extract_pages(pdf_path)
    all_chunks: List[Dict[str, Any]] = []

    for page in pages:
        page_chunks = chunk_page(
            text=page["text"],
            page_number=page["page_number"],
            source=source_name,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        all_chunks.extend(page_chunks)

    logger.info(
        "Produced %d chunks from %d pages", len(all_chunks), len(pages)
    )
    return all_chunks
