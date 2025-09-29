"""Unit tests for the lightweight HTTP application."""

import unittest

from app.main import DevOpsMVPRequestHandler, handle_request


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

    def test_handler_logs_are_suppressed(self) -> None:
        self.assertIsNone(DevOpsMVPRequestHandler.log_message(DevOpsMVPRequestHandler, "test"))


if __name__ == "__main__":
    unittest.main()
