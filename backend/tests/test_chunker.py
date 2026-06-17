"""Unit tests for PDF chunking logic — no external dependencies required."""

import pytest

from app.rag.pdf_processor import chunk_page, process_pdf


def test_chunk_basic_size():
    text = "A" * 800
    chunks = chunk_page(text, page_number=1, source="test", chunk_size=800, chunk_overlap=150)
    assert len(chunks) >= 1
    assert len(chunks[0]["text"]) <= 800


def test_chunk_overlap_produces_correct_count():
    # step = chunk_size - overlap = 800 - 150 = 650
    # 2000 chars: starts at 0, 650, 1300, 1950 => 4 chunks
    text = "B" * 2000
    chunks = chunk_page(text, page_number=1, source="test", chunk_size=800, chunk_overlap=150)
    assert len(chunks) == 4


def test_chunk_empty_text_returns_nothing():
    chunks = chunk_page("", page_number=1, source="test", chunk_size=800, chunk_overlap=150)
    assert chunks == []


def test_chunk_metadata_fields():
    text = "Hello world " * 100
    chunks = chunk_page(text, page_number=3, source="aws_agreement", chunk_size=800, chunk_overlap=150)
    for chunk in chunks:
        assert "chunk_id" in chunk
        assert "page_number" in chunk
        assert "source" in chunk
        assert "text" in chunk
        assert chunk["page_number"] == 3
        assert chunk["source"] == "aws_agreement"


def test_chunk_id_format():
    text = "X" * 1600
    chunks = chunk_page(text, page_number=5, source="test", chunk_size=800, chunk_overlap=150)
    assert chunks[0]["chunk_id"] == "p5_c0"
    assert chunks[1]["chunk_id"] == "p5_c1"


def test_chunk_whitespace_only_skipped():
    text = "   \n\n   \t  "
    chunks = chunk_page(text, page_number=1, source="test", chunk_size=800, chunk_overlap=150)
    assert chunks == []
