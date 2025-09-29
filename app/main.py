"""Lightweight HTTP application exposing health and greeting endpoints."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, Tuple

HOST = "0.0.0.0"
PORT = 8000


def handle_request(path: str) -> Tuple[int, Dict[str, str]]:
    """Return an HTTP status code and JSON payload for the provided path."""
    if path == "/healthz":
        return 200, {"status": "ok"}

    if path == "/":
        return 200, {"message": "Welcome to the Parameta DevOps MVP"}

    return 404, {"error": "not found"}


class DevOpsMVPRequestHandler(BaseHTTPRequestHandler):
    """Minimal request handler to serve JSON responses."""

    def do_GET(self) -> None:  # noqa: N802 - http.server interface
        status_code, payload = handle_request(self.path)
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003 - third-party signature
        """Silence the default stdout logging to keep containers clean."""
        return


def run_server() -> None:
    """Start the HTTP server."""
    server = HTTPServer((HOST, PORT), DevOpsMVPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
