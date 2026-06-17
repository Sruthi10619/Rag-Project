"""Singleton embedding model wrapper for BAAI/bge-small-en-v1.5."""

import logging
from typing import List

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_model: SentenceTransformer | None = None

# BGE asymmetric retrieval: queries need this prefix; documents do not.
_BGE_QUERY_PREFIX = "Represent this sentence: "


def _get_model() -> SentenceTransformer:
    """Load the embedding model once and cache it in the module-level variable."""
    global _model
    if _model is None:
        model_name = get_settings().embedding_model
        logger.info("Loading embedding model: %s", model_name)
        _model = SentenceTransformer(model_name)
        logger.info("Embedding model ready.")
    return _model


def embed_documents(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of document chunks.

    Note: No prefix is added — BGE models embed passages without instruction.
    """
    model = _get_model()
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return embeddings.tolist()


def embed_query(query: str) -> List[float]:
    """
    Generate embedding for a single query string.

    BGE models require the instruction prefix on the *query side only* for
    asymmetric retrieval (query vs. passage). Omitting it silently degrades
    retrieval quality.
    """
    model = _get_model()
    embedding = model.encode(
        _BGE_QUERY_PREFIX + query,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return embedding.tolist()
