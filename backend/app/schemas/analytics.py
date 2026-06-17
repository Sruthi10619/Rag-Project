"""Pydantic schemas for the /analytics endpoint."""

from typing import List, Optional

from pydantic import BaseModel


class TopQuestion(BaseModel):
    query: str
    count: int


class FailedQuery(BaseModel):
    query: str
    count: int


class DailyQueryCount(BaseModel):
    date: str
    count: int


class RecentQuery(BaseModel):
    id: int
    query: str
    answer_found: bool
    latency_ms: float
    top_score: Optional[float] = None
    created_at: str


class AnalyticsResponse(BaseModel):
    total_requests: int
    success_rate: float
    avg_latency_ms: float
    avg_retrieval_score: Optional[float] = None
    top_questions: List[TopQuestion]
    failed_queries: List[FailedQuery]
    daily_query_counts: List[DailyQueryCount]
    recent_queries: List[RecentQuery]
