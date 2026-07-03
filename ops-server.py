#!/usr/bin/env python3
import http.server, subprocess, threading, json, os, queue, time

ACTIONS = {
    'combind-update':  ['sh', '/opt/ops-dashboard/scripts/combind-update.sh'],
    'combind-restart': ['sh', '/opt/ops-dashboard/scripts/combind-restart.sh'],
    'anime-update':    ['sh', '/opt/ops-dashboard/scripts/anime-update.sh'],
    'anime-restart':   ['sh', '/opt/ops-dashboard/scripts/anime-restart.sh'],
    'marinara-update':  ['sh', '/opt/ops-dashboard/scripts/marinara-update.sh'],
    'marinara-restart': ['sh', '/opt/ops-dashboard/scripts/marinara-restart.sh'],
    'spoolman-update':  ['sh', '/opt/ops-dashboard/scripts/spoolman-update.sh'],
    'spoolman-restart': ['sh', '/opt/ops-dashboard/scripts/spoolman-restart.sh'],
    'claude-health':        ['sh', '/opt/ops-dashboard/scripts/claude-health.sh'],
    'claude-remote-start':  ['sh', '/opt/ops-dashboard/scripts/claude-remote-start.sh'],
    'claude-remote-stop':   ['sh', '/opt/ops-dashboard/scripts/claude-remote-stop.sh'],
    'claude-remote-status': ['sh', '/opt/ops-dashboard/scripts/claude-remote-status.sh'],
    'ttyd-status':   ['sh', '/opt/ops-dashboard/scripts/ttyd-status.sh'],
    'ttyd-restart':  ['sh', '/opt/ops-dashboard/scripts/ttyd-restart.sh'],
}
LOGS = {
    'combind-logs':   'combind-chat',
    'anime-logs':     'anime-downloader',
    'marinara-logs':  'marinara-engine-marinara-1',
    'spoolman-logs':  'spoolman-spoolman-1',
}

# job_id -> {'status': running/done/error, 'output': str}
jobs = {}
jobs_lock = threading.Lock()

def run_job(job_id, cmd):
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        out = []
        for line in proc.stdout:
            out.append(line)
            with jobs_lock:
                jobs[job_id]['output'] = ''.join(out)
        proc.wait()
        with jobs_lock:
            jobs[job_id]['status'] = 'done' if proc.returncode == 0 else 'error'
            jobs[job_id]['output'] = ''.join(out)
    except Exception as e:
        with jobs_lock:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['output'] = str(e)

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send_json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(b)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b)

    def send_text(self, code, body):
        b = body.encode()
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(b)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        path = self.path.lstrip('/')

        # Start an action -> returns job_id immediately
        if path in ACTIONS:
            job_id = f"{path}-{int(time.time())}"
            with jobs_lock:
                jobs[job_id] = {'status': 'running', 'output': ''}
            t = threading.Thread(target=run_job, args=(job_id, ACTIONS[path]), daemon=True)
            t.start()
            self.send_json(200, {'job_id': job_id, 'status': 'running'})

        # Poll job status
        elif path.startswith('job/'):
            job_id = path[4:]
            with jobs_lock:
                job = jobs.get(job_id)
            if job:
                self.send_json(200, job)
            else:
                self.send_json(404, {'error': 'job not found'})

        # Logs
        elif path in LOGS:
            container = LOGS[path]
            r = subprocess.run(['docker', 'logs', '--tail', '100', container],
                               capture_output=True, text=True)
            self.send_text(200, r.stdout + r.stderr)

        else:
            self.send_text(404, 'not found')

http.server.HTTPServer(('0.0.0.0', 9002), Handler).serve_forever()
