#!/bin/sh
echo "=== Combind Chat Logs (last 100 lines) ==="
LOG=$(grep -rl '"Name":"/combind-chat"' /var/lib/docker/containers/*/config.v2.json 2>/dev/null | head -1 | sed 's|/config.v2.json||')
if [ -n "$LOG" ]; then
  ID=$(basename "$LOG")
  tail -100 "${LOG}/${ID}-json.log" 2>/dev/null | awk -F'"' '{for(i=1;i<=NF;i++){if($i=="log"){printf "%s", $(i+2); break}}}'
else
  echo "Container not found or logs unavailable"
fi
