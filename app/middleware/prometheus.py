import time
from starlette.requests import Request
import logging

from app.metrics.http import (
    http_requests_total,
    http_request_duration_seconds,
    http_requests_in_progress,
)

logger = logging.getLogger("goods-api")

async def prometheus_middleware(request: Request, call_next):
    method = request.method
    path = request.scope.get("route").path if request.scope.get("route") else request.url.path
    
    http_requests_in_progress.inc()
    start_time = time.time()
    
    status_code = 500
    response = None

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception as e:
        status_code = 500
        logger.error(f"Error processing request {method} {path}: {e}", exc_info=True)
        raise
    finally:
        duration = time.time() - start_time
        http_requests_in_progress.dec()

        # Всегда инкрементируем счетчик
        http_requests_total.labels(
            method=method,
            path=path,
            status=status_code,
        ).inc()

        # Измеряем длительность
        http_request_duration_seconds.labels(
            method=method,
            path=path,
            status=status_code,
        ).observe(duration)
        
        # Логируем метрики
        if duration > 1.0:  # Логируем медленные запросы
            logger.warning(
                f"Slow request detected: {method} {path} "
                f"took {duration:.2f}s, status: {status_code}"
            )
