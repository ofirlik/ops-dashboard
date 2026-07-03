#!/bin/sh
# Restart the ttyd web terminal (systemd service, port 7681).
echo "Restarting ttyd..."
systemctl restart ttyd || { echo "systemctl restart failed"; exit 1; }
sleep 1
active=$(systemctl is-active ttyd 2>/dev/null)
echo "active: $active"
if command -v ss >/dev/null 2>&1; then
  ss -ltn 2>/dev/null | grep -q ':7681' && echo "listening on :7681: YES" || echo "listening on :7681: NO"
fi
[ "$active" = "active" ] || exit 1
echo "ttyd restarted successfully."
