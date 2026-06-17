"""Application configuration via pydantic-settings. Reads from .env file."""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Groq API Key
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")

    # Database
    database_url: str = Field("sqlite:///./rag_qa.db", alias="DATABASE_URL")

    # ChromaDB
    chroma_db_path: str = Field("./chroma_db", alias="CHROMA_DB_PATH")
    chroma_collection_name: str = "aws_agreement_chunks"

    # PDF document
    pdf_path: str = Field("./data/AWS Customer Agreement.pdf", alias="PDF_PATH")

    # Embedding
    embedding_model: str = Field("BAAI/bge-small-en-v1.5", alias="EMBEDDING_MODEL")

    # Chunking
    chunk_size: int = Field(800, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(150, alias="CHUNK_OVERLAP")

    # Retrieval
    top_k: int = Field(5, alias="TOP_K")
    relevance_threshold: float = Field(0.35, alias="RELEVANCE_THRESHOLD")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        alias="CORS_ORIGINS",
    )

    # Logging
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "populate_by_name": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """Return a cached singleton Settings instance."""
    return Settings()
