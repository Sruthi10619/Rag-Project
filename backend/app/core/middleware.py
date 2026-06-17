"""HTTP middleware: request timing and structured logging."""

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every incoming request and its response status."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())[:8]
        logger.info("[%s] %s %s", request_id, request.method, request.url.path)
        response = await call_next(request)
        logger.info("[%s] -> %s", request_id, response.status_code)
        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """Adds X-Process-Time-Ms header to every response."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
        return response
