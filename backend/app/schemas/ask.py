"""Pydantic schemas for the /ask endpoint."""

from typing import List, Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="The question to ask about the AWS Customer Agreement.",
    )


class SourceCitation(BaseModel):
    page: int
    chunk_id: str
    snippet: str = Field(..., description="First 200 characters of the source chunk.")


class AskResponse(BaseModel):
    answer: str
    answer_found: bool
    sources: List[SourceCitation]
    latency_ms: float
    top_score: Optional[float] = None
    tokens_prompt: Optional[int] = None
    tokens_completion: Optional[int] = None
