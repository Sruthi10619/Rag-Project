"""Query service — orchestrates retrieval, LLM generation, and DB logging."""

import logging
import time
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.models.query_log import QueryLog
from app.rag.llm_client import generate_answer
from app.rag.retriever import NOT_FOUND_ANSWER, retrieve
from app.schemas.ask import AskResponse, SourceCitation

logger = logging.getLogger(__name__)


def ask(question: str, db: Session) -> AskResponse:
    """
    Execute the full RAG pipeline for a single question.

    Steps:
      1. Retrieve relevant chunks (with threshold guard).
      2. If threshold not met, return not-found response immediately.
      3. Call LLM with grounding system prompt and retrieved context.
      4. Build citations from retrieved chunks.
      5. Log everything to SQLite.

    Args:
        question: User's question string.
        db:       SQLAlchemy session (injected by FastAPI).

    Returns:
        AskResponse with answer, sources, latency, and token counts.
    """
    t0 = time.perf_counter()

    chunks, best_score, answer_found = retrieve(question)

    tokens_prompt: int | None = None
    tokens_completion: int | None = None
    sources: list[SourceCitation] = []

    if not answer_found:
        answer = NOT_FOUND_ANSWER
    else:
        answer, tokens_prompt, tokens_completion = generate_answer(question, chunks)
        sources = [
            SourceCitation(
                page=c["page_number"],
                chunk_id=c["chunk_id"],
                snippet=c["text"][:200],
            )
            for c in chunks
        ]

    latency_ms = (time.perf_counter() - t0) * 1000

    _log_query(
        db=db,
        question=question,
        answer=answer,
        answer_found=answer_found,
        latency_ms=latency_ms,
        top_score=best_score,
        tokens_prompt=tokens_prompt,
        tokens_completion=tokens_completion,
    )

    return AskResponse(
        answer=answer,
        answer_found=answer_found,
        sources=sources,
        latency_ms=round(latency_ms, 2),
        top_score=best_score,
        tokens_prompt=tokens_prompt,
        tokens_completion=tokens_completion,
    )


def _log_query(
    db: Session,
    question: str,
    answer: str,
    answer_found: bool,
    latency_ms: float,
    top_score: float | None,
    tokens_prompt: int | None,
    tokens_completion: int | None,
) -> None:
    """Persist query result to the query_logs table."""
    entry = QueryLog(
        query=question,
        answer=answer,
        answer_found=answer_found,
        latency_ms=latency_ms,
        top_score=top_score,
        tokens_prompt=tokens_prompt,
        tokens_completion=tokens_completion,
    )
    db.add(entry)
    try:
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Failed to log query to database.")
