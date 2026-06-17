"""Unit tests for the embedding module."""

import math

import pytest

from app.rag.embedder import embed_documents, embed_query


@pytest.mark.slow
def test_embed_query_returns_list_of_floats():
    vec = embed_query("What are the payment terms?")
    assert isinstance(vec, list)
    assert len(vec) > 0
    assert isinstance(vec[0], float)


@pytest.mark.slow
def test_embed_query_is_normalized():
    """BGE embeddings with normalize_embeddings=True should have L2 norm ≈ 1.0."""
    vec = embed_query("What are the payment terms?")
    norm = math.sqrt(sum(v * v for v in vec))
    assert abs(norm - 1.0) < 1e-4, f"Expected norm ~1.0, got {norm}"


@pytest.mark.slow
def test_embed_documents_batch():
    texts = ["AWS Customer Agreement", "Payment terms apply.", "Termination clause."]
    vecs = embed_documents(texts)
    assert len(vecs) == 3
    for v in vecs:
        assert isinstance(v, list)
        assert len(v) > 0


@pytest.mark.slow
def test_query_and_doc_same_dimension():
    q_vec = embed_query("What are the termination terms?")
    d_vecs = embed_documents(["AWS reserves the right to terminate."])
    assert len(q_vec) == len(d_vecs[0])
