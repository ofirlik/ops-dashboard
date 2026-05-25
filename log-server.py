#!/usr/bin/env python3
import http.server
import subprocess
import urllib.parse

CONTAINERS = {
    'combind-logs': 'combind-chat',
    'anime-logs': 'anime-downloader',
}

class LogHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress access logs
    def do_GET(self):
        path = self.path.lstrip('/')
        if path in CONTAINERS:
            try:
                result = subprocess.run(
                    ['docker', 'logs', '--tail', '100', CONTAINERS[path]],
                    capture_output=True, text=True, timeout=10
                )
                out = result.stdout + result.stderr
                body = out.encode()
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', 9002), LogHandler)
    print('Log server on 127.0.0.1:9002')
    server.serve_forever()
