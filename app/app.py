from http.server import BaseHTTPRequestHandler, HTTPServer
import os


APP_VERSION = os.getenv("APP_VERSION", "v1")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        message = f"Hello from ECS task definition {APP_VERSION}\n"
        self.wfile.write(message.encode("utf-8"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "80"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving version {APP_VERSION} on port {port}", flush=True)
    server.serve_forever()
