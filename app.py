"""Tiny web server used to demonstrate Docker images, ports, volumes and Compose."""

import html
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

TITLE = os.environ.get("APP_TITLE", "Docker Visitor Counter")
MESSAGE = os.environ.get(
    "APP_MESSAGE",
    "This application is running inside Docker."
)
PORT = int(os.environ.get("PORT", "5000"))
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
COUNTER_FILE = DATA_DIR / "visits.txt"


def record_visit():
    """Count one page view; store it outside the app in Docker's volume."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    visits = int(COUNTER_FILE.read_text()) if COUNTER_FILE.exists() else 0
    visits += 1
    COUNTER_FILE.write_text(str(visits))
    return visits


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            content = b"OK"
            content_type = "text/plain"
        elif self.path == "/":
            visits = record_visit()
            safe_title = html.escape(TITLE)
            safe_message = html.escape(MESSAGE)
            content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <style>
    body {{ font-family: Arial, sans-serif; display: grid; place-items: center;
           min-height: 90vh; background: #f4f7fb; color: #233044; }}
    main {{ background: white; padding: 36px; border-radius: 12px;
            box-shadow: 0 2px 18px #0001; text-align: center; }}
    strong {{ display: block; font-size: 54px; margin: 16px; color: #2366bc; }}
  </style>
</head>
<body>
  <main>
    <h1>{safe_title}</h1>
    <p>{safe_message}</p>
    <strong>{visits}</strong>
    <p>Total page visits (saved in a Docker volume)</p>
    <p>Refresh to increase the counter.</p>
  </main>
</body>
</html>""".encode("utf-8")
            content_type = "text/html; charset=utf-8"
        else:
            self.send_error(404, "Not found")
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    print(f"Serving on port {PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
