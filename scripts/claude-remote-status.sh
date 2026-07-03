#!/bin/bash
SESSION="claude-remote"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "Status: RUNNING"
  echo "Session name: $SESSION"
  echo ""
  echo "--- Current pane output ---"
  tmux capture-pane -p -t "$SESSION" 2>/dev/null | tail -30
else
  echo "Status: STOPPED"
  echo "No active remote session."
fi
