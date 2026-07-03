#!/bin/bash
CLAUDE=/root/.npm-global/bin/claude
SESSION="claude-remote"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "Remote session '$SESSION' is already running."
  echo ""
  echo "Session name: $SESSION"
  echo "Connect from Claude Code: open the app and look for Remote Control sessions."
  exit 0
fi

echo "Starting Claude remote-control session in tmux..."
tmux new-session -d -s "$SESSION" "$CLAUDE --remote-control $SESSION --dangerously-skip-permissions"
sleep 2

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "Remote session started."
  echo ""
  echo "Session name: $SESSION"
  echo "Connect from Claude Code by selecting the remote session named '$SESSION'."
  echo ""
  echo "--- Initial output ---"
  tmux capture-pane -p -t "$SESSION" 2>/dev/null | head -20
else
  echo "FAIL - session did not start. Check if claude is authenticated."
  exit 1
fi
