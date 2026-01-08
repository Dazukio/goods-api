
from prometheus_client import Counter

goods_created_total = Counter(
    "goods_created_total",
    "Total number of goods created"
)

goods_deleted_total = Counter(
    "goods_deleted_total",
    "Total number of goods deleted"
)
