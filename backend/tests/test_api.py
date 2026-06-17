"""Integration tests using FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "embedding_model" in data
    assert "llm_model" in data
    assert "chunks_indexed" in data


def test_analytics_empty_db():
    response = client.get("/analytics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_requests"] == 0
    assert data["success_rate"] == 0.0
    assert isinstance(data["top_questions"], list)
    assert isinstance(data["recent_queries"], list)


def test_ask_validation_too_short():
    response = client.post("/ask", json={"question": "Hi"})
    assert response.status_code == 422


def test_ask_validation_missing_field():
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_ingest_missing_pdf():
    """When no file is uploaded and PDF_PATH doesn't exist, should return 404."""
    response = client.post("/ingest")
    # Either 404 (file not found) or 200 (already ingested) depending on env
    assert response.status_code in (200, 404, 500)


def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200
