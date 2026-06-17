"""Analytics service — aggregated SQL queries over the query_logs table."""

import logging
from typing import List

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.query_log import QueryLog
from app.schemas.analytics import (
    AnalyticsResponse,
    DailyQueryCount,
    FailedQuery,
    RecentQuery,
    TopQuestion,
)

logger = logging.getLogger(__name__)


def get_analytics(db: Session) -> AnalyticsResponse:
    """
    Compute all analytics metrics in a single function.

    Queries performed:
      1.  Total request count.
      2.  Success rate (answer_found=True / total).
      3.  Average latency across all queries.
      4.  Average retrieval score for successful queries.
      5.  Top 10 most frequent questions.
      6.  Top 10 question patterns with no answer found.
      7.  Daily query counts for the last 30 days.
      8.  10 most recent queries.
    """
    # ── 1. Total requests ────────────────────────────────────────────────────
    total: int = db.query(func.count(QueryLog.id)).scalar() or 0

    # ── 2. Success rate ───────────────────────────────────────────────────────
    successful: int = (
        db.query(func.count(QueryLog.id))
        .filter(QueryLog.answer_found.is_(True))
        .scalar()
        or 0
    )
    success_rate: float = (successful / total) if total > 0 else 0.0

    # ── 3. Average latency ────────────────────────────────────────────────────
    avg_latency_raw = db.query(func.avg(QueryLog.latency_ms)).scalar()
    avg_latency_ms: float = float(avg_latency_raw) if avg_latency_raw is not None else 0.0

    # ── 4. Average retrieval score (successful only) ──────────────────────────
    avg_score_raw = (
        db.query(func.avg(QueryLog.top_score))
        .filter(QueryLog.answer_found.is_(True))
        .scalar()
    )
    avg_retrieval_score = float(avg_score_raw) if avg_score_raw is not None else None

    # ── 5. Top 10 most frequent questions ─────────────────────────────────────
    top_q_rows = (
        db.query(QueryLog.query, func.count(QueryLog.id).label("count"))
        .group_by(QueryLog.query)
        .order_by(desc("count"))
        .limit(10)
        .all()
    )
    top_questions: List[TopQuestion] = [
        TopQuestion(query=r.query, count=r.count) for r in top_q_rows
    ]

    # ── 6. Failed queries (no answer found) ───────────────────────────────────
    failed_rows = (
        db.query(QueryLog.query, func.count(QueryLog.id).label("count"))
        .filter(QueryLog.answer_found.is_(False))
        .group_by(QueryLog.query)
        .order_by(desc("count"))
        .limit(10)
        .all()
    )
    failed_queries: List[FailedQuery] = [
        FailedQuery(query=r.query, count=r.count) for r in failed_rows
    ]

    # ── 7. Daily query counts (last 30 days) ──────────────────────────────────
    # strftime is SQLite-specific — maps to DATE() in PostgreSQL if migrated.
    daily_rows = (
        db.query(
            func.strftime("%Y-%m-%d", QueryLog.created_at).label("date"),
            func.count(QueryLog.id).label("count"),
        )
        .group_by(func.strftime("%Y-%m-%d", QueryLog.created_at))
        .order_by("date")
        .limit(30)
        .all()
    )
    daily_query_counts: List[DailyQueryCount] = [
        DailyQueryCount(date=r.date, count=r.count) for r in daily_rows
    ]

    # ── 8. 10 most recent queries ─────────────────────────────────────────────
    recent_rows = (
        db.query(QueryLog).order_by(desc(QueryLog.created_at)).limit(10).all()
    )
    recent_queries: List[RecentQuery] = [
        RecentQuery(
            id=r.id,
            query=r.query,
            answer_found=r.answer_found,
            latency_ms=round(r.latency_ms, 2),
            top_score=round(r.top_score, 4) if r.top_score is not None else None,
            created_at=r.created_at.isoformat(),
        )
        for r in recent_rows
    ]

    return AnalyticsResponse(
        total_requests=total,
        success_rate=round(success_rate, 4),
        avg_latency_ms=round(avg_latency_ms, 2),
        avg_retrieval_score=(
            round(avg_retrieval_score, 4) if avg_retrieval_score is not None else None
        ),
        top_questions=top_questions,
        failed_queries=failed_queries,
        daily_query_counts=daily_query_counts,
        recent_queries=recent_queries,
    )
