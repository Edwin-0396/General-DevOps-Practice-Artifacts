"""Lightweight HTTP application exposing health and greeting endpoints."""

from __future__ import annotations

import json
import logging
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, Tuple

LOGGER = logging.getLogger(__name__)

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000


def handle_request(path: str) -> Tuple[int, Dict[str, str]]:
    """Return an HTTP status code and JSON payload for the provided path."""
    if path == "/healthz":
        return 200, {"status": "ok"}

    if path == "/":
        return 200, {"message": "Welcome to the Parameta DevOps MVP"}

    return 404, {"error": "not found"}


def resolve_bind_host(custom_host: str | None = None) -> str:
    """Determine the bind host, honoring optional overrides."""
    if custom_host is not None:
        return custom_host
    return os.getenv("APP_HOST", DEFAULT_HOST)


def resolve_bind_port(custom_port: int | None = None) -> int:
    """Determine the bind port from configuration or environment variables."""
    if custom_port is not None:
        return _validate_port(custom_port)

    raw_port = os.getenv("APP_PORT", str(DEFAULT_PORT))
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise ValueError("APP_PORT must be an integer") from exc

    return _validate_port(port)


def _validate_port(port: int) -> int:
    if not 0 <= port <= 65535:
        raise ValueError("Port must be between 0 and 65535")
    return port


def create_server(host: str | None = None, port: int | None = None) -> ThreadingHTTPServer:
    """Create a configured HTTP server instance without starting it."""
    bind_host = resolve_bind_host(host)
    bind_port = resolve_bind_port(port)
    server = ThreadingHTTPServer((bind_host, bind_port), DevOpsMVPRequestHandler)
    server.daemon_threads = True
    return server


class DevOpsMVPRequestHandler(BaseHTTPRequestHandler):
    """Minimal request handler to serve JSON responses."""

    server_version = "ParametaDevOpsMVP/1.0"

    def do_GET(self) -> None:  # noqa: N802 - http.server interface
        status_code, payload = handle_request(self.path)
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003 - third-party signature
        """Route request logs through the application logger."""
        LOGGER.info("%s - - %s", self.address_string(), format % args)


def run_server() -> None:
    """Start the HTTP server and handle graceful shutdown."""
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    server = create_server()
    host, port = server.server_address
    LOGGER.info("Starting HTTP server on %s:%s", host, port)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info("Received shutdown signal. Stopping server...")
    finally:
        server.server_close()
        LOGGER.info("Server stopped")


if __name__ == "__main__":
    run_server()
