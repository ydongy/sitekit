#!/usr/bin/env python3
"""Local preview that behaves like Cloudflare static assets: /faq serves faq.html, /de/ serves
de/index.html and unknown paths get 404.html (there are no redirects: every page has one address).

    python3 scripts/sitekit/preview.py [port]      # default 8765
"""
import posixpath
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

PUB = Path(__file__).resolve().parent.parent.parent / "public"  # scripts/sitekit/ -> repository root


def resolve(url_path: str):
    """The request path as (clean URL path, file under public/), or None when it leaves public/ or is malformed."""
    path = unquote(urlsplit(url_path).path)
    if not path.startswith("/") or any(c in path for c in "\r\n\0\\"):
        return None
    clean = posixpath.normpath(path)
    if path.endswith("/") and clean != "/":
        clean += "/"
    target = (PUB / clean.lstrip("/")).resolve()
    if target != PUB and PUB not in target.parents:
        return None
    return clean, target


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(PUB), **kw)

    def do_GET(self):
        self._serve(head=False)

    def do_HEAD(self):
        self._serve(head=True)

    def _not_found(self, head):
        body = (PUB / "404.html").read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def _serve(self, head):
        resolved = resolve(self.path)
        if resolved is None:
            self._not_found(head)
            return
        path, target = resolved
        if target.is_dir() and not path.endswith("/"):
            self.send_response(301)
            self.send_header("Location", path + "/")  # normalized, inside public/, no control characters
            self.end_headers()
            return
        page = target.with_name(target.name + ".html")
        if not path.endswith("/") and not target.is_file() and page.is_file():
            self.path = path + ".html"
        elif not path.endswith("/") and not target.exists():
            self._not_found(head)
            return
        else:
            self.path = path
        (super().do_HEAD if head else super().do_GET)()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"http://localhost:{port}/")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
