import time
from starlette.requests import Request

from app.metrics.http import (
    http_requests_total,
    http_request_duration_seconds,
    http_requests_in_progress,
)


async def prometheus_middleware(request: Request, call_next):
    method = request.method

    path = request.scope.get("route").path if request.scope.get("route") else request.url.path

    http_requests_in_progress.inc()
    start_time = time.time()
    
    status = "500"  
    response = None

    try:
        response = await call_next(request)
        status = str(response.status_code)
        return response
    except Exception as e:
        status = "500"
        raise  
    finally:
        duration = time.time() - start_time
        http_requests_in_progress.dec()

        # Всегда инкрементируем счетчик
        http_requests_total.labels(
            method=method,
            path=path,
            status=status,
        ).inc()

        # Измеряем длительность
        http_request_duration_seconds.labels(
            method=method,
            path=path,
            status=status,  
        ).observe(duration)
