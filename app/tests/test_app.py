"""Unit tests for the lightweight HTTP application."""

from __future__ import annotations

import os
import unittest
from unittest import mock

from app.main import (
    DevOpsMVPRequestHandler,
    create_server,
    handle_request,
    resolve_bind_host,
    resolve_bind_port,
)


class TestApp(unittest.TestCase):
    """Test suite for the request handlers."""

    def test_healthz_route_returns_ok_status(self) -> None:
        status_code, payload = handle_request("/healthz")
        self.assertEqual(status_code, 200)
        self.assertEqual(payload, {"status": "ok"})

    def test_index_returns_greeting_message(self) -> None:
        status_code, payload = handle_request("/")
        self.assertEqual(status_code, 200)
        self.assertEqual(payload, {"message": "Welcome to the Parameta DevOps MVP"})

    def test_unknown_path_returns_404(self) -> None:
        status_code, payload = handle_request("/unknown")
        self.assertEqual(status_code, 404)
        self.assertEqual(payload, {"error": "not found"})

    def test_resolve_bind_host_prefers_custom_value(self) -> None:
        self.assertEqual(resolve_bind_host("127.0.0.1"), "127.0.0.1")

    def test_resolve_bind_host_reads_environment(self) -> None:
        with mock.patch.dict(os.environ, {"APP_HOST": "192.168.1.10"}):
            self.assertEqual(resolve_bind_host(), "192.168.1.10")

    def test_resolve_bind_port_accepts_custom_value(self) -> None:
        self.assertEqual(resolve_bind_port(9000), 9000)

    def test_resolve_bind_port_reads_environment(self) -> None:
        with mock.patch.dict(os.environ, {"APP_PORT": "9001"}):
            self.assertEqual(resolve_bind_port(), 9001)

    def test_resolve_bind_port_rejects_out_of_range_values(self) -> None:
        with self.assertRaises(ValueError):
            resolve_bind_port(70000)
        with self.assertRaises(ValueError):
            resolve_bind_port(-1)

    def test_resolve_bind_port_rejects_invalid_environment_value(self) -> None:
        with mock.patch.dict(os.environ, {"APP_PORT": "invalid"}):
            with self.assertRaises(ValueError):
                resolve_bind_port()

    def test_create_server_binds_to_requested_address(self) -> None:
        server = create_server(host="127.0.0.1", port=0)
        try:
            host, port = server.server_address
            self.assertEqual(host, "127.0.0.1")
            self.assertGreater(port, 0)
        finally:
            server.server_close()

    def test_request_handler_logs_via_logger(self) -> None:
        handler = mock.MagicMock(spec=DevOpsMVPRequestHandler)
        handler.address_string.return_value = "127.0.0.1"
        with mock.patch("app.main.LOGGER") as logger:
            DevOpsMVPRequestHandler.log_message(handler, "%s", "log-test")
            logger.info.assert_called_once_with("%s - - %s", "127.0.0.1", "log-test")

    def test_run_server_handles_keyboard_interrupt(self) -> None:
        with mock.patch("app.main.create_server") as create_server_mock:
            fake_server = mock.MagicMock()
            fake_server.server_address = ("127.0.0.1", 8000)
            fake_server.serve_forever.side_effect = KeyboardInterrupt()
            create_server_mock.return_value = fake_server

            from app import main  # Local import to avoid circulars during patching

            main.run_server()

            fake_server.serve_forever.assert_called_once()
            fake_server.server_close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
