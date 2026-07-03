#!/bin/bash
SESSION="claude-remote"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux kill-session -t "$SESSION"
  echo "Remote session '$SESSION' stopped."
else
  echo "No active remote session."
fi
