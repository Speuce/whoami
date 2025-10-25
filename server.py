import os, json, socket, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "3000"))
HOSTNAME = socket.gethostname()

def get_outbound_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=3) as r:
            return json.loads(r.read().decode()).get("ip","unknown")
    except Exception:
        return "unknown"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            return
        payload = {
            "path": self.path,
            "hostname": HOSTNAME,
            "client_ip_seen_by_vm": self.client_address[0],
            "outbound_ip_seen_by_internet": get_outbound_ip(),
            "message": "Hello from the Server!"
        }
        body = f"""<!doctype html><html><head><meta charset="utf-8"><title>az-whoami</title></head>
<body><pre>{json.dumps(payload, indent=2)}</pre></body></html>"""
        self.send_response(200)
        self.send_header("Content-Type","text/html; charset=utf-8")
        self.send_header("Cache-Control","no-store")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))
    def log_message(self, *args, **kwargs):
        return  # quiet
if __name__ == "__main__":
    print(f"Starting server on port {PORT}...")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()
