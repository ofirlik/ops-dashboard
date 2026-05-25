#!/usr/bin/env python3
import http.server, subprocess, json, os

ACTIONS = {
    'combind-update':  ['sh', '/opt/ops-dashboard/scripts/combind-update.sh'],
    'combind-restart': ['sh', '/opt/ops-dashboard/scripts/combind-restart.sh'],
    'anime-update':    ['sh', '/opt/ops-dashboard/scripts/anime-update.sh'],
    'anime-restart':   ['sh', '/opt/ops-dashboard/scripts/anime-restart.sh'],
}
LOGS = {
    'combind-logs': 'combind-chat',
    'anime-logs':   'anime-downloader',
}

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send_text(self, code, body):
        b = body.encode()
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(b)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b)
    def do_GET(self):
        path = self.path.strip('/')
        if path in ACTIONS:
            try:
                r = subprocess.run(ACTIONS[path], capture_output=True, text=True, timeout=120)
                out = r.stdout + r.stderr
                self.send_text(200, out or '(no output)')
            except Exception as e:
                self.send_text(500, str(e))
        elif path in LOGS:
            try:
                r = subprocess.run(['docker','logs','--tail','100',LOGS[path]], capture_output=True, text=True, timeout=10)
                self.send_text(200, r.stdout + r.stderr)
            except Exception as e:
                self.send_text(500, str(e))
        else:
            self.send_text(404, 'not found')

if __name__ == '__main__':
    s = http.server.HTTPServer(('0.0.0.0', 9002), Handler)
    print('ops-server on :9002')
    s.serve_forever()
