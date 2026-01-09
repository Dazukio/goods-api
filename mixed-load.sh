#!/bin/bash
# mixed-load.sh

# Разные эндпоинты
declare -A endpoints=(
  ["GET /goods"]="http://localhost:8000/goods/"
  ["GET /docs"]="http://localhost:8000/docs"
  ["GET /metrics"]="http://localhost:8000/metrics"
)

# Запускаем нагрузку на каждый эндпоинт
for desc in "${!endpoints[@]}"; do
  url="${endpoints[$desc]}"
  echo "Запуск нагрузки на: $desc"
  ab -n 1000 -c 10 -k "$url" >"results_${desc//\//_}.txt" 2>&1 &
done

# Ждем завершения всех
wait

# Сводка
echo -e "\n=== Сводка результатов ==="
for file in results_*.txt; do
  echo "--- $file ---"
  grep -E "(Requests per second:|Time per request:|Transfer rate:)" "$file"
done
