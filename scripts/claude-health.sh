#!/bin/bash
CLAUDE=/root/.npm-global/bin/claude
echo "Version: $($CLAUDE --version 2>&1)"
echo ""
echo "Sending test prompt..."
RESP=$($CLAUDE -p "respond with only the word: ONLINE" --print 2>&1)
echo "Response: $RESP"
if echo "$RESP" | grep -qi "online"; then
  echo ""
  echo "OK - Claude CLI is healthy"
else
  echo ""
  echo "FAIL - unexpected response"
  exit 1
fi
