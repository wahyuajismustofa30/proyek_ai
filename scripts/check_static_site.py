#!/usr/bin/env python3
"""Smoke-test a static website's root index.html over a local HTTP server."""

from __future__ import annotations

import argparse
import functools
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen


class QuietHandler(SimpleHTTPRequestHandler):
    """Serve files without noisy request logs during CI."""

    def log_message(self, format: str, *args: object) -> None:
        pass


def check_static_site(project: Path, entrypoint: str = "index.html") -> None:
    """Require a regular root index.html and verify it is served over HTTP."""
    project = project.resolve()
    if not project.is_dir():
        raise ValueError(f"static website directory does not exist: {project}")

    relative_entrypoint = Path(entrypoint)
    if relative_entrypoint.is_absolute() or ".." in relative_entrypoint.parts:
        raise ValueError("static website entrypoint must stay inside the project directory")
    index = project / relative_entrypoint
    if index.is_symlink() or not index.is_file():
        raise ValueError(f"{project}: static website entrypoint is missing or is not a regular file: {entrypoint}")

    expected = index.read_bytes()
    handler = functools.partial(QuietHandler, directory=str(project))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/{quote(relative_entrypoint.as_posix(), safe="/")}"
        try:
            with urlopen(url, timeout=5) as response:
                body = response.read()
                if response.status != 200:
                    raise ValueError(f"{project}: static site returned HTTP {response.status}")
                if body != expected:
                    raise ValueError(f"{project}: HTTP root did not serve the project's index.html")
                if "text/html" not in response.headers.get("Content-Type", ""):
                    raise ValueError(f"{project}: root response is not served as HTML")
        except (URLError, TimeoutError, OSError) as exc:
            raise ValueError(f"{project}: static site HTTP smoke test failed: {exc}") from exc
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Static website project directory")
    parser.add_argument("--entrypoint", default="index.html", help="Root-relative HTML entrypoint (default: index.html)")
    args = parser.parse_args()
    try:
        check_static_site(args.project, args.entrypoint)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"PASS: static website smoke test passed: {args.project}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
