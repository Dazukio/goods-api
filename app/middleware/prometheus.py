
import time
from starlette.requests import Request

from app.metrics.http import (
    http_requests_total,
    http_request_duration_seconds,
    http_requests_in_progress,
)


async def prometheus_middleware(request: Request, call_next):
    method = request.method

    # ⚠️ ВАЖНО: path без id
    path = request.scope.get("route").path if request.scope.get("route") else request.url.path

    http_requests_in_progress.inc()
    start_time = time.time()

    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        duration = time.time() - start_time
        http_requests_in_progress.dec()

        http_requests_total.labels(
            method=method,
            path=path,
            status=status,
        ).inc()

        http_request_duration_seconds.labels(
            method=method,
            path=path,
        ).observe(duration)
