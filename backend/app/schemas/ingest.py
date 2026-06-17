"""Pydantic schemas for the /ingest endpoint."""

from pydantic import BaseModel


class IngestResponse(BaseModel):
    message: str
    chunks_created: int
    pages_processed: int
    collection_name: str
