"""Retrieval layer — embeds queries, searches ChromaDB, applies relevance threshold."""

import logging
from typing import Any, Dict, List, Optional, Tuple

from app.core.config import get_settings
from app.rag.embedder import embed_query
from app.rag.vector_store import similarity_search

logger = logging.getLogger(__name__)

NOT_FOUND_ANSWER = "Information not found in the AWS Customer Agreement."


def retrieve(
    question: str,
) -> Tuple[List[Dict[str, Any]], Optional[float], bool]:
    """
    Retrieve the most relevant chunks for the given question.

    Steps:
      1. Embed the question with BGE query prefix.
      2. Search ChromaDB (top-K cosine similarity).
      3. If the best similarity score < relevance_threshold, signal not-found.

    Returns:
        (chunks, best_score, answer_found)
        - chunks:        List of retrieved chunk dicts (empty if threshold not met).
        - best_score:    Highest similarity score among retrieved results (or None).
        - answer_found:  False if no results or score below threshold.
    """
    settings = get_settings()
    query_embedding = embed_query(question)
    chunks = similarity_search(query_embedding, top_k=settings.top_k)

    if not chunks:
        return [], None, False

    best_score: float = chunks[0]["similarity_score"]

    if best_score < settings.relevance_threshold:
        logger.info(
            "Best score %.4f below threshold %.2f for query: '%.60s...'",
            best_score,
            settings.relevance_threshold,
            question,
        )
        return [], best_score, False

    logger.info(
        "Retrieved %d chunks. Best score: %.4f for query: '%.60s...'",
        len(chunks),
        best_score,
        question,
    )
    return chunks, best_score, True
