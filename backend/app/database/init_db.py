"""Database initialisation — creates all tables on first run."""

from app.database.session import engine
from app.models.query_log import Base  # import triggers model registration


def init_db() -> None:
    """Create all tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)
