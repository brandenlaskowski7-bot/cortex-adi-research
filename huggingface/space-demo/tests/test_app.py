import importlib.util
import pathlib
import sys
import types
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


class _Widget:
    def click(self, *args, **kwargs):
        return None


class _Blocks(_Widget):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def launch(self):
        return None


sys.modules["gradio"] = types.SimpleNamespace(
    Blocks=lambda **kwargs: _Blocks(), State=lambda **kwargs: _Widget(),
    Markdown=lambda *args, **kwargs: _Widget(), Dropdown=lambda *args, **kwargs: _Widget(),
    Button=lambda *args, **kwargs: _Widget(), Code=lambda *args, **kwargs: _Widget(),
)

APP = pathlib.Path(__file__).parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("space_app", APP)
app = importlib.util.module_from_spec(SPEC)
sys.modules["space_app"] = app
SPEC.loader.exec_module(app)


class FakeApi:
    def __init__(self):
        self.created = 0
        self.calls = []

    def create_session(self):
        self.created += 1
        return 201, {"session_id": f"session-{self.created}", "token": f"token-{self.created}", "scopes": ["synthetic-scope-1"]}

    def call(self, method, path, body=None, session=None):
        self.calls.append((method, path, body, session.token if session else None))
        if path == "/v1/challenge/reset":
            return 200, {"decision": "RETURN", "reason_category": "RESET", "receipt_id": "receipt-reset"}
        return 200, {"decision": "RETURN", "reason_category": "ADMITTED", "record_id": "synthetic-record-1", "receipt_id": "receipt-1", "token": "must-not-display"}


class SpaceSafetyTests(unittest.TestCase):
    def setUp(self):
        self.previous_api, self.previous_store = app.API, app.STORE
        app.API, app.STORE = FakeApi(), app.VisitorStore()

    def tearDown(self):
        app.API, app.STORE = self.previous_api, self.previous_store

    def test_two_visitors_receive_distinct_server_only_credentials(self):
        app.run_scenario("Temporal expiry", "visitor-a")
        app.run_scenario("Temporal expiry", "visitor-b")
        self.assertEqual(app.API.created, 2)
        self.assertNotEqual(app.STORE.get("visitor-a").token, app.STORE.get("visitor-b").token)

    def test_safe_view_does_not_return_token(self):
        _, rendered = app.run_scenario("Temporal expiry", "visitor-a")
        self.assertNotIn("must-not-display", rendered)
        self.assertNotIn("token", rendered)

    def test_reset_uses_only_current_visitor_session(self):
        app.run_scenario("Temporal expiry", "visitor-a")
        app.run_scenario("Temporal expiry", "visitor-b")
        app.reset_session("visitor-a")
        self.assertEqual(app.API.calls[-1][3], "token-1")

    def test_local_http_smoke_uses_documented_headers_and_safe_output(self):
        observed = {}

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                observed["path"] = self.path
                observed["agent"] = self.headers.get("User-Agent")
                observed["content_type"] = self.headers.get("Content-Type")
                observed["body"] = self.rfile.read(int(self.headers["Content-Length"])).decode()
                body = b'{"session_id":"local-session","token":"local-secret","scopes":["synthetic-scope-1"]}'
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        server.timeout = 2
        thread = Thread(target=server.handle_request)
        thread.start()
        try:
            status, response = app.ChallengeApi(f"http://127.0.0.1:{server.server_port}").create_session()
        finally:
            thread.join(timeout=2)
            server.server_close()
        self.assertEqual(status, 201)
        self.assertEqual(response["session_id"], "local-session")
        self.assertEqual(observed["path"], "/v1/challenge/session")
        self.assertEqual(observed["agent"], "CortexGovernedMemoryChallenge/0.1")
        self.assertEqual(observed["content_type"], "application/json")
        self.assertEqual(observed["body"], '{"synthetic":true,"scopes":["synthetic-scope-1","synthetic-scope-2"]}')


if __name__ == "__main__":
    unittest.main()
