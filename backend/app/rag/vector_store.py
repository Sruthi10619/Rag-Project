"""ChromaDB vector store — collection management and similarity search."""

import logging
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_client: Optional[chromadb.PersistentClient] = None

_BATCH_SIZE = 100


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        path = get_settings().chroma_db_path
        _client = chromadb.PersistentClient(
            path=path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _client


def _get_collection(name: Optional[str] = None):
    """
    Return the ChromaDB collection, creating it if necessary.

    IMPORTANT: hnsw:space=cosine must be set at creation time.
    ChromaDB cosine distance is in [0, 2]; lower = more similar.
    Convert to similarity with: similarity = 1.0 - distance.
    """
    client = _get_client()
    col_name = name or get_settings().chroma_collection_name
    return client.get_or_create_collection(
        name=col_name,
        metadata={"hnsw:space": "cosine"},
    )


def ingest_chunks(chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> int:
    """
    Upsert document chunks into ChromaDB in batches.

    Args:
        chunks: List of `chunk dicts with keys: chunk_id, page_number, source, text.
        embeddings: Parallel list of embedding vectors.

    Returns:
        Number of chunks upserted.
    """
    collection = _get_collection()

    for i in range(0, len(chunks), _BATCH_SIZE):
        batch = chunks[i : i + _BATCH_SIZE]
        batch_embs = embeddings[i : i + _BATCH_SIZE]

        collection.upsert(
            ids=[c["chunk_id"] for c in batch],
            embeddings=batch_embs,
            documents=[c["text"] for c in batch],
            metadatas=[
                {
                    "page_number": c["page_number"],
                    "source": c["source"],
                    "chunk_id": c["chunk_id"],
                }
                for c in batch
            ],
        )
        logger.debug("Upserted batch %d-%d", i, i + len(batch))

    total = len(chunks)
    logger.info("Ingested %d chunks into ChromaDB", total)
    return total


def similarity_search(
    query_embedding: List[float],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Query ChromaDB and return top_k results with similarity scores.

    ChromaDB returns cosine *distances* (0 = identical, 2 = opposite).
    We convert: similarity = 1.0 - distance, giving [0, 1] where 1 = perfect match.
    Results are already ordered best-first by ChromaDB.
    """
    collection = _get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents: List[str] = results["documents"][0]
    metadatas: List[Dict] = results["metadatas"][0]
    distances: List[float] = results["distances"][0]

    retrieved = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        retrieved.append(
            {
                "text": doc,
                "page_number": meta.get("page_number", 0),
                "chunk_id": meta.get("chunk_id", ""),
                "source": meta.get("source", ""),
                "similarity_score": 1.0 - dist,  # distance → similarity
            }
        )

    return retrieved


def collection_count() -> int:
    """Return total number of documents in the active collection."""
    return _get_collection().count()


def reset_collection() -> None:
    """Delete and recreate the collection (used before re-ingestion)."""
    client = _get_client()
    name = get_settings().chroma_collection_name
    try:
        client.delete_collection(name)
        logger.info("Deleted collection '%s'", name)
    except Exception:
        pass
    # Recreate immediately so subsequent calls don't fail
    _get_collection(name)
