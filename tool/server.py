# GET serves the files under a directory (404 where there is none); a POST answers 201 {"id": 7}.
import http.server, os, sys, json
port, root = int(sys.argv[1]), os.path.abspath(sys.argv[2])
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        path = os.path.join(root, self.path.lstrip('/'))
        if os.path.isfile(path):
            body = open(path, 'rb').read()
            self.send_response(200); self.send_header('Content-Type', 'application/json' if path.endswith('.json') else 'text/plain')
        else:
            body = b'not found'
            self.send_response(404); self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0)); self.rfile.read(n)
        body = json.dumps({"id": 7}).encode()
        self.send_response(201); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
