#!/bin/bash

echo "Load test"
echo "Start: $(date '+%H:%M:%S')"
echo ""

# Endpoints to test
declare -A endpoints=(
  ["GET /goods"]="http://localhost:8000/goods/"
  ["GET /docs"]="http://localhost:8000/docs"
  ["GET /metrics"]="http://localhost:8000/metrics"
)

# Test each endpoint
for desc in "${!endpoints[@]}"; do
  url="${endpoints[$desc]}"

  echo "Testing: $desc"
  echo "URL: $url"
  echo "--------------------------------"

  # Run Apache Bench
  ab -n 1000 -c 10 -k -q "$url" 2>/dev/null |
    grep -E "(Requests per second:|Time per request:|Failed requests:|Transfer rate:)" |
    sed 's/^/  /'

  echo ""
  sleep 1
done

echo "Test completed"
echo "End: $(date '+%H:%M:%S')"

# (Optional) Check Prometheus metrics
echo ""
echo "Checking metrics..."
echo "Service status:"
curl -s "http://localhost:9090/api/v1/query?query=up{job='goods-api'}" |
  jq -r '.data.result[0].value[1] // "unknown"' 2>/dev/null
