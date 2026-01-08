
from prometheus_client import Counter, Histogram, Gauge

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
    buckets=(0.1, 0.3, 0.5, 1, 2, 5)
)

http_requests_in_progress = Gauge(
    "http_requests_in_progress",
    "HTTP requests in progress"
)
