"""Local preview server. Run via `uv run website` from the repo root."""

from __future__ import annotations

import argparse
import http.server
import socketserver
import sys
import webbrowser
from pathlib import Path

DEFAULT_PORT = 8000


class ReusableServer(socketserver.TCPServer):
    allow_reuse_address = True


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview the site locally.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-open", action="store_true", help="Don't open a browser.")
    args = parser.parse_args()

    root = Path.cwd()
    if not (root / "index.html").exists():
        print(f"error: no index.html in {root} — run from the repo root.", file=sys.stderr)
        return 1

    url = f"http://localhost:{args.port}"

    def factory(*a, **kw):
        return Handler(*a, directory=str(root), **kw)

    try:
        httpd = ReusableServer(("127.0.0.1", args.port), factory)
    except OSError as e:
        print(f"error: could not bind to port {args.port}: {e}", file=sys.stderr)
        print("tip: pass --port 8001 (or kill whatever is using the port).", file=sys.stderr)
        return 1

    print(f"serving {root} at {url}")
    print("press Ctrl-C to stop.")
    if not args.no_open:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping.")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
