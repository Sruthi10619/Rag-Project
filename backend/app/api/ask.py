"""POST /ask — ask a question about the AWS Customer Agreement."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.ask import AskRequest, AskResponse
from app.services.query_service import ask

router = APIRouter(tags=["Query"])
logger = logging.getLogger(__name__)


@router.post("/ask", response_model=AskResponse, summary="Ask a question")
async def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db),
) -> AskResponse:
    """
    Ask a question and receive a grounded answer with citations.

    The RAG pipeline:
    1. Embeds the question using BAAI/bge-small-en-v1.5.
    2. Retrieves top-K relevant chunks from ChromaDB.
    3. Applies a relevance threshold — returns "not found" if no chunk qualifies.
    4. Passes retrieved context to llama-3.3-70b-versatile on Groq.
    5. Returns the answer with page/chunk citations.
    """
    try:
        return ask(question=request.question, db=db)
    except Exception as exc:
        logger.exception("Query pipeline failed for: '%s'", request.question[:80])
        raise HTTPException(status_code=500, detail=f"Query error: {exc}") from exc
