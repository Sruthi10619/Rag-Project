"""ORM model for the query_logs table."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class QueryLog(Base):
    """Records every question asked and its RAG pipeline result."""

    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    answer_found = Column(Boolean, nullable=False, default=False)
    latency_ms = Column(Float, nullable=False)
    top_score = Column(Float, nullable=True)
    tokens_prompt = Column(Integer, nullable=True)
    tokens_completion = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
