"""FastAPI application factory — wires all routers, middleware, and startup logic."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import analytics, ask, health, ingest
from app.core.config import get_settings
from app.core.exceptions import (
    IngestError,
    LLMError,
    QueryError,
    VectorStoreError,
    generic_error_handler,
    ingest_error_handler,
    llm_error_handler,
    query_error_handler,
    vector_store_error_handler,
)
from app.core.middleware import RequestLoggingMiddleware, TimingMiddleware
from app.database.init_db import init_db

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AWS Agreement RAG QA System...")
    init_db()
    logger.info("SQLite database ready.")
    yield
    logger.info("Shutting down.")


def create_app() -> FastAPI:
    app = FastAPI(
        title="AWS Customer Agreement — RAG QA System",
        description=(
            "Retrieval-Augmented Generation system for querying the "
            "AWS Customer Agreement PDF. Powered by BAAI/bge-small-en-v1.5 "
            "embeddings, ChromaDB vector storage, and llama-3.3-70b-versatile "
            "via the Groq API."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── CORS (must be registered before custom middleware) ──────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Custom middleware (LIFO — last added executes first) ─────────────────
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    # ── Exception handlers ──────────────────────────────────────────────────
    app.add_exception_handler(IngestError, ingest_error_handler)
    app.add_exception_handler(QueryError, query_error_handler)
    app.add_exception_handler(VectorStoreError, vector_store_error_handler)
    app.add_exception_handler(LLMError, llm_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)

    # ── Routers ─────────────────────────────────────────────────────────────
    app.include_router(health.router)
    app.include_router(ingest.router)
    app.include_router(ask.router)
    app.include_router(analytics.router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
