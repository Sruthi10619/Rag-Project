"""GET /analytics — aggregated usage statistics."""

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics_service import get_analytics

router = APIRouter(tags=["Analytics"])
logger = logging.getLogger(__name__)


@router.get(
    "/analytics",
    response_model=AnalyticsResponse,
    summary="Get usage analytics",
)
async def analytics(db: Session = Depends(get_db)) -> AnalyticsResponse:
    """
    Returns aggregated analytics:
    - Total request count and success rate
    - Average latency and retrieval score
    - Top 10 most frequent questions
    - Failed queries (no answer found)
    - Daily query volume (last 30 days)
    - 10 most recent queries
    """
    return get_analytics(db)
