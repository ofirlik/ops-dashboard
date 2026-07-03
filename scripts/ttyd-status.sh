#!/bin/sh
# Health check for the ttyd web terminal (systemd service, port 7681).
echo "=== ttyd service ==="
echo "enabled: $(systemctl is-enabled ttyd 2>/dev/null || echo unknown)"
echo "active:  $(systemctl is-active ttyd 2>/dev/null || echo unknown)"
echo
echo "=== listening on :7681 ==="
if command -v ss >/dev/null 2>&1; then
  ss -ltn 2>/dev/null | grep -q ':7681' && echo "YES (0.0.0.0:7681)" || echo "NO"
else
  echo "(ss unavailable)"
fi
echo
echo "=== auth check (expect 401 without creds) ==="
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 http://localhost:7681/ 2>/dev/null)
echo "HTTP $code  ->  $( [ "$code" = "401" ] && echo 'OK (auth enforced)' || echo 'unexpected' )"
echo
echo "=== recent logs ==="
journalctl -u ttyd -n 8 --no-pager 2>/dev/null || echo "(journalctl unavailable)"
