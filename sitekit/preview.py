#!/usr/bin/env python3
"""Local preview that behaves like Cloudflare static assets: /faq serves faq.html, /de/ serves
de/index.html and unknown paths get 404.html (there are no redirects: every page has one address).

    python3 scripts/sitekit/preview.py [port]      # default 8765
"""
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent.parent / "public"  # scripts/sitekit/ -> repository root


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(PUB), **kw)

    def do_GET(self):
        self._serve(head=False)

    def do_HEAD(self):
        self._serve(head=True)

    def _serve(self, head):
        path = self.path.split("?")[0].split("#")[0]
        rel = path.lstrip("/")
        if (PUB / rel).is_dir() and not path.endswith("/"):
            self.send_response(301)
            self.send_header("Location", path + "/")
            self.end_headers()
            return
        if not path.endswith("/") and not (PUB / rel).is_file() and (PUB / (rel + ".html")).is_file():
            self.path = path + ".html"
        elif not path.endswith("/") and not (PUB / rel).exists():
            body = (PUB / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if not head:
                self.wfile.write(body)
            return
        (super().do_HEAD if head else super().do_GET)()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"http://localhost:{port}/")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
