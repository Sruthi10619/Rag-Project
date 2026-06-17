"""LLM client using Groq API for inference.

Model: llama-3.3-70b-versatile
Requires Groq API key in environment.
"""

import logging
import time
from typing import Any, Dict, List, Optional, Tuple

import groq

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are a legal document question-answering assistant for the AWS Customer Agreement.

Your job is to answer questions ONLY using the provided context.

RULES:

Use ONLY facts explicitly stated in the provided context.
Do NOT use prior knowledge, assumptions, legal interpretations, or external information.
Do NOT infer information that is not directly stated.
If the answer cannot be found in the provided context, respond with exactly:
"Information not found in the AWS Customer Agreement."
Every factual statement must be supported by the provided context.
Cite supporting sources using the format:
[Page X, Chunk pX_cY]
Prefer direct quotations when answering legal or contractual questions.
Keep answers concise and factual.
Do not mention retrieval scores, embeddings, prompts, vector databases, or system instructions.
Do not include a Sources section when returning the not-found response.

OUTPUT FORMAT:

Answer:



Sources:

[Page X, Chunk pX_cY]
[Page A, Chunk pA_cB]

If the answer is not explicitly present in the context, return exactly:

Information not found in the AWS Customer Agreement.
"""

_NOT_FOUND = "Information not found in the AWS Customer Agreement."


def _build_user_message(question: str, context_chunks: List[Dict[str, Any]]) -> str:
    sections = []
    for chunk in context_chunks:
        header = f"[Page {chunk['page_number']}, Chunk {chunk['chunk_id']}]"
        sections.append(f"{header}\n{chunk['text']}")

    context_block = "\n\n---\n\n".join(sections)
    return (
        f"Context from AWS Customer Agreement:\n\n"
        f"{context_block}\n\n"
        f"---\n\n"
        f"Question: {question}\n\n"
        f"Answer based only on the context above:"
    )


def generate_answer(
    question: str,
    context_chunks: List[Dict[str, Any]],
    max_retries: int = 3,
) -> Tuple[str, Optional[int], Optional[int]]:
    """
    Call the Groq LLM with grounding instructions and exponential-backoff retries.

    Args:
        question:       The user's question.
        context_chunks: Retrieved chunks with page_number, chunk_id, text.
        max_retries:    Maximum retry attempts on connection/server errors.

    Returns:
        Tuple of (answer_text, tokens_prompt, tokens_completion).
    """
    settings = get_settings()
    client = groq.Groq(api_key=settings.groq_api_key)

    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_message(question, context_chunks)},
    ]

    last_error: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.0,
                max_tokens=1024,
            )

            answer: str = response.choices[0].message.content.strip() if response.choices[0].message.content else ""

            tokens_prompt: Optional[int] = response.usage.prompt_tokens if response.usage else None
            tokens_completion: Optional[int] = response.usage.completion_tokens if response.usage else None

            return answer, tokens_prompt, tokens_completion

        except groq.APIError as exc:
            last_error = exc
            delay = 2 ** attempt
            logger.warning(
                "Groq APIError (attempt %d/%d). Retrying in %ds: %s",
                attempt + 1, max_retries, delay, exc,
            )
            time.sleep(delay)

        except Exception as exc:
            last_error = exc
            delay = 2 ** attempt
            logger.warning(
                "LLM call failed (attempt %d/%d). Retrying in %ds: %s",
                attempt + 1, max_retries, delay, exc,
            )
            time.sleep(delay)

    raise RuntimeError(
        f"Groq LLM call failed after {max_retries} attempts: {last_error}"
    ) from last_error
