"""
Tests for maya/tt_bridge.py (loopback link between a Maya tool and the browser app).
Runs a real server on 127.0.0.1 and talks to it with http.client.

    python -m unittest discover -s tests/python -v
"""

import http.client
import json
import os
import sys
import tempfile
import threading
import types
import unittest
from unittest import mock
from urllib.parse import parse_qs, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "maya"))

import tt_app  # noqa: E402
import tt_bridge  # noqa: E402


def obj_problem(path, expected_vertices=None):
    """The validation a tool hands to the bridge: TopoTransfer header and vertex count."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if "Exported by TopoTransfer" not in text.split("\n", 1)[0]:
        return "not an OBJ exported by TopoTransfer"
    n = sum(1 for line in text.splitlines() if line.startswith("v "))
    if expected_vertices is not None and n != expected_vertices:
        return f"{n} vertices, expected {expected_vertices}"
    return None


APP = "http://localhost:5173/"
ORIGIN = "http://localhost:5173"
BASE_OBJ = "# MetaHuman LOD0\nv 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n"
WRAPPED_OBJ = "# Exported by TopoTransfer\n# space: reference coordinates\nv 0 0 1\nv 1 0 1\nv 0 1 1\nf 1 2 3\n"


class BridgeTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.work = self._tmp.name
        j = lambda name: os.path.join(self.work, name)  # noqa: E731
        self.p = types.SimpleNamespace(base_obj=j("base.obj"), reference_obj=j("reference.obj"), wrapped_obj=j("base_wrapped.obj"))
        with open(self.p.base_obj, "w", newline="") as f:
            f.write(BASE_OBJ)
        with open(self.p.reference_obj, "w", newline="") as f:
            f.write("v 5 5 5\nv 6 5 5\nv 5 6 5\nf 1 2 3\n")
        with open(os.path.join(self.work, "secret.txt"), "w", newline="") as f:
            f.write("not for the browser")
        self.results = []
        self.arrived = threading.Event()

        def on_result(path):
            self.results.append(path)
            self.arrived.set()

        self.bridge = tt_bridge.Bridge(
            self.work, APP, {"base": self.p.base_obj, "reference": self.p.reference_obj},
            result_path=self.p.wrapped_obj, on_result=on_result,
            validate=lambda tmp: obj_problem(tmp, 3), max_result_bytes=4096,
        ).start()
        self.addCleanup(self._tmp.cleanup)
        self.addCleanup(self.bridge.stop)

    def request(self, method, path, body=None, headers=None, host=None):
        conn = http.client.HTTPConnection(tt_bridge.HOST, self.bridge.port, timeout=10)
        try:
            h = {"Host": host or f"127.0.0.1:{self.bridge.port}"}
            h.update(headers or {})
            conn.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
            for k, v in h.items():
                conn.putheader(k, v)
            if body is not None and "Content-Length" not in h:
                conn.putheader("Content-Length", str(len(body)))
            conn.endheaders()
            if body:
                conn.send(body)
            r = conn.getresponse()
            return r.status, dict(r.getheaders()), r.read()
        finally:
            conn.close()

    def path(self, url):
        return urlsplit(url).path


class TestClaudeLink(BridgeTestCase):
    """The page's Claude link: it long-polls for commands and posts the answers back."""

    def page(self, answer):
        """Act as the app page for one command: fetch it, answer it with `answer(command)`."""
        root = f"/{self.bridge.token}"
        status, _, body = self.request("GET", f"{root}/claude/next", headers={"Origin": ORIGIN})
        self.assertEqual(status, 200)
        cmd = json.loads(body)
        reply = json.dumps(dict(id=cmd["id"], **answer(cmd))).encode()
        status, _, _ = self.request("POST", f"{root}/claude/reply", body=reply, headers={"Origin": ORIGIN, "Content-Type": "application/json"})
        self.assertEqual(status, 200)

    def test_call_reaches_the_page_and_returns_its_answer(self):
        self.assertFalse(self.bridge.claude_linked)
        with self.assertRaises(RuntimeError):
            tt_bridge.claude_call("state", timeout=1)
        self.bridge._polled = tt_bridge.time.monotonic()  # the page asked recently
        page = threading.Thread(target=self.page, args=(lambda c: {"ok": True, "result": {"echo": c["command"], "args": c["args"]}},))
        page.start()
        result = tt_bridge.claude_call("capture", timeout=5, view="left")
        page.join()
        self.assertEqual(result, {"echo": "capture", "args": {"view": "left"}})

    def test_page_errors_are_raised(self):
        page = threading.Thread(target=self.page, args=(lambda c: {"ok": False, "message": "no guide Chin"},))
        page.start()
        with self.assertRaisesRegex(RuntimeError, "no guide Chin"):
            self.bridge.call_app("set_guides", timeout=5)
        page.join()

    def test_no_answer_times_out_and_drops_the_command(self):
        with self.assertRaises(TimeoutError):
            self.bridge.call_app("state", timeout=0.2)
        self.assertEqual(self.bridge._commands, [])

    def test_claude_code_calls_the_page_directly(self):
        sys.path.insert(0, os.path.join(HERE, "..", "..", "maya"))
        import tt_claude  # noqa: E402

        root = f"/{self.bridge.token}"
        call = json.dumps({"command": "state", "args": {}, "timeout": 5}).encode()
        status, _, _ = self.request("POST", f"{root}/claude/call", body=call)
        self.assertEqual(status, 409)  # the page is not listening yet
        status, _, _ = self.request("POST", f"{root}/claude/call", body=call, headers={"Origin": ORIGIN})
        self.assertEqual(status, 403)  # never from a browser page
        self.bridge._polled = tt_bridge.time.monotonic()
        page = threading.Thread(target=self.page, args=(lambda c: {"ok": True, "result": {"guides": [], "cmd": c["command"]}},))
        page.start()
        with mock.patch.object(tt_claude, "CLAUDE_DIR", tt_bridge.CLAUDE_DIR):
            self.assertIn(self.bridge.root, tt_claude.bridge_roots())
            result = tt_claude.call("state", url=f"{self.bridge.root}/app/?base=x", timeout=5)  # the URL Maya opened
        page.join()
        self.assertEqual(result, {"guides": [], "cmd": "state"})
        path = self.bridge._announce_path()
        self.bridge.stop()
        self.assertFalse(os.path.exists(path))

    def test_foreign_origin_gets_no_commands(self):
        status, _, _ = self.request("GET", f"/{self.bridge.token}/claude/next", headers={"Origin": "https://evil.example"})
        self.assertEqual(status, 403)


class TestBridgeUrls(BridgeTestCase):
    def test_binds_loopback_on_random_port_with_token(self):
        self.assertEqual(self.bridge._server.server_address[0], "127.0.0.1")
        self.assertGreater(self.bridge.port, 0)
        self.assertGreaterEqual(len(self.bridge.token), 32)
        other = tt_bridge.Bridge(self.work, APP, {"base": self.p.base_obj}, self.p.wrapped_obj)
        self.assertNotEqual(other.token, self.bridge.token)

    def test_launch_url_points_the_app_at_the_bridge(self):
        url = self.bridge.app_launch_url()
        self.assertTrue(url.startswith("http://localhost:5173/?"))
        q = {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}
        root = f"http://127.0.0.1:{self.bridge.port}/{self.bridge.token}"
        self.assertEqual(q, {
            "base": f"{root}/files/base.obj",
            "reference": f"{root}/files/reference.obj",
            "return": f"{root}/result",
        })

    def test_app_origin_and_query_helpers(self):
        self.assertEqual(tt_bridge.app_origin("http://localhost:5173/"), "http://localhost:5173")
        self.assertEqual(tt_bridge.app_origin("HTTP://LocalHost:80/x?y"), "http://localhost")
        self.assertEqual(tt_bridge.app_origin("https://tt.example.com:443/app/"), "https://tt.example.com")
        self.assertEqual(tt_bridge.app_origin("http://[::1]:4173"), "http://[::1]:4173")
        with self.assertRaises(ValueError):
            tt_bridge.app_origin("file:///C:/app/index.html")
        self.assertEqual(tt_bridge.with_query("http://h/app/?x=1#f", {"a": "http://127.0.0.1:1/t/r"}),
                         "http://h/app/?x=1&a=http%3A%2F%2F127.0.0.1%3A1%2Ft%2Fr#f")

    def test_only_files_inside_the_work_folder(self):
        with tempfile.TemporaryDirectory() as other:
            outside = os.path.join(other, "x.obj")
            open(outside, "w").close()
            with self.assertRaises(ValueError):
                tt_bridge.Bridge(self.work, APP, {"base": outside}, self.p.wrapped_obj)
            with self.assertRaises(ValueError):
                tt_bridge.Bridge(self.work, APP, {"base": self.p.base_obj}, os.path.join(other, "r.obj"))
        with self.assertRaises(FileNotFoundError):
            tt_bridge.Bridge(self.work, APP, {"base": os.path.join(self.work, "missing.obj")}, self.p.wrapped_obj)


class TestBridgeServing(BridgeTestCase):
    def test_serves_registered_files_with_cors_for_the_app(self):
        status, headers, body = self.request("GET", self.path(self.bridge.file_url("base")), headers={"Origin": ORIGIN})
        self.assertEqual(status, 200)
        self.assertEqual(body.decode(), BASE_OBJ)
        self.assertEqual(headers["Access-Control-Allow-Origin"], ORIGIN)
        self.assertEqual(headers["Cache-Control"], "no-store")
        status, _, body = self.request("GET", self.path(self.bridge.file_url("reference")))
        self.assertEqual(status, 200)
        self.assertTrue(body.startswith(b"v 5 5 5"))

    def test_wrong_token_or_path_is_404(self):
        tok = self.bridge.token
        for path in [
            "/",
            "/files/base.obj",
            f"/{tok[:-1]}{'A' if tok[-1] != 'A' else 'B'}/files/base.obj",
            f"/{tok}",
            f"/{tok}/files/secret.txt",
            f"/{tok}/files/../secret.txt",
            f"/{tok}/files/..%2Fsecret.txt",
            f"/{tok}/files/%2E%2E%2F..%2Ftt_bridge.py",
            f"/{tok}/files/",
            f"/{tok}/files/sub/mh_head_lod0.obj",
            f"/{tok}/result",
        ]:
            status, headers, body = self.request("GET", path)
            self.assertEqual(status, 404, path)
            self.assertNotIn(b"not for the browser", body)

    def test_foreign_origin_is_403_without_cors(self):
        status, headers, _ = self.request("GET", self.path(self.bridge.file_url("base")), headers={"Origin": "https://evil.example"})
        self.assertEqual(status, 403)
        self.assertNotIn("Access-Control-Allow-Origin", headers)

    def test_foreign_host_header_is_403(self):
        # DNS rebinding: a page on evil.example resolved to 127.0.0.1 sends its own Host
        status, _, _ = self.request("GET", self.path(self.bridge.file_url("base")), host=f"evil.example:{self.bridge.port}")
        self.assertEqual(status, 403)
        status, _, _ = self.request("GET", self.path(self.bridge.file_url("base")), host=f"localhost:{self.bridge.port}")
        self.assertEqual(status, 200)

    def test_preflight(self):
        status, headers, _ = self.request("OPTIONS", self.path(self.bridge.result_url), headers={
            "Origin": ORIGIN, "Access-Control-Request-Method": "POST", "Access-Control-Request-Private-Network": "true"})
        self.assertEqual(status, 204)
        self.assertEqual(headers["Access-Control-Allow-Origin"], ORIGIN)
        self.assertIn("POST", headers["Access-Control-Allow-Methods"])
        self.assertEqual(headers["Access-Control-Allow-Private-Network"], "true")
        status, _, _ = self.request("OPTIONS", self.path(self.bridge.result_url), headers={"Origin": "https://evil.example"})
        self.assertEqual(status, 403)

    def test_stop_closes_the_port(self):
        port = self.bridge.port
        self.bridge.stop()
        self.assertFalse(self.bridge.running)
        conn = http.client.HTTPConnection(tt_bridge.HOST, port, timeout=2)
        with self.assertRaises(OSError):
            conn.request("GET", "/")
            conn.getresponse()
        conn.close()


class TestBridgeResult(BridgeTestCase):
    def post(self, body, origin=ORIGIN, **kw):
        headers = {"Content-Type": "text/plain"}
        if origin:
            headers["Origin"] = origin
        headers.update(kw.pop("headers", {}))
        return self.request("POST", self.path(self.bridge.result_url), body=body, headers=headers, **kw)

    def test_valid_result_is_saved_and_reported(self):
        status, headers, body = self.post(WRAPPED_OBJ.encode())
        self.assertEqual(status, 200, body)
        self.assertEqual(headers["Access-Control-Allow-Origin"], ORIGIN)
        answer = json.loads(body)
        self.assertTrue(answer["ok"])
        self.assertIn("base_wrapped.obj", answer["message"])
        self.assertTrue(self.arrived.wait(5))
        self.assertEqual(self.results, [self.p.wrapped_obj])
        with open(self.p.wrapped_obj, newline="") as f:
            self.assertEqual(f.read(), WRAPPED_OBJ)
        self.assertEqual(self.bridge.received, 1)
        self.assertEqual([n for n in os.listdir(self.work) if n.startswith(".tt_upload_")], [])

    def test_second_result_replaces_the_first(self):
        self.assertEqual(self.post(WRAPPED_OBJ.encode())[0], 200)
        second = WRAPPED_OBJ.replace("v 0 0 1", "v 0 0 2")
        self.assertEqual(self.post(second.encode())[0], 200)
        with open(self.p.wrapped_obj, newline="") as f:
            self.assertEqual(f.read(), second)
        self.assertEqual(self.bridge.received, 2)

    def test_invalid_results_are_rejected_and_keep_the_previous_file(self):
        self.assertEqual(self.post(WRAPPED_OBJ.encode())[0], 200)
        for bad, why in [
            (b"v 0 0 0\nv 1 0 0\nv 0 1 0\n", "not an OBJ exported by TopoTransfer"),
            ("# Exported by TopoTransfer\nv 0 0 0\n".encode(), "1 vertices, expected 3"),
        ]:
            status, _, body = self.post(bad)
            self.assertEqual(status, 422)
            self.assertIn(why, json.loads(body)["message"])
        with open(self.p.wrapped_obj, newline="") as f:
            self.assertEqual(f.read(), WRAPPED_OBJ)
        self.assertEqual(len(self.results), 1)
        self.assertEqual([n for n in os.listdir(self.work) if n.startswith(".tt_upload_")], [])

    def test_too_large_or_empty_is_rejected(self):
        status, _, _ = self.post(b"#" * 5000)
        self.assertEqual(status, 413)
        status, _, _ = self.post(b"")
        self.assertEqual(status, 400)
        self.assertFalse(os.path.exists(self.p.wrapped_obj))

    def test_post_needs_token_and_app_origin(self):
        status, _, _ = self.post(WRAPPED_OBJ.encode(), origin="https://evil.example")
        self.assertEqual(status, 403)
        status, _, _ = self.request("POST", f"/{'x' * 32}/result", body=WRAPPED_OBJ.encode(), headers={"Origin": ORIGIN})
        self.assertEqual(status, 404)
        status, _, _ = self.request("POST", self.path(self.bridge.file_url("base")), body=WRAPPED_OBJ.encode(), headers={"Origin": ORIGIN})
        self.assertEqual(status, 404)
        self.assertFalse(os.path.exists(self.p.wrapped_obj))
        with open(self.p.base_obj, newline="") as f:
            self.assertEqual(f.read(), BASE_OBJ)

    def test_failing_callback_does_not_fail_the_upload(self):
        def boom(path):
            raise RuntimeError("Maya UI is gone")

        self.bridge.on_result = boom
        with mock.patch("traceback.print_exc"):
            status, _, _ = self.post(WRAPPED_OBJ.encode())
        self.assertEqual(status, 200)
        self.assertTrue(os.path.isfile(self.p.wrapped_obj))


class TestStopAll(unittest.TestCase):
    def test_every_bridge_stops_before_exit_even_after_a_reload(self):
        import importlib

        with tempfile.TemporaryDirectory() as work:
            b = tt_bridge.Bridge(work, APP, {}).start()
            self.assertIn(b, tt_bridge._LIVE)
            importlib.reload(tt_bridge)  # the Maya tools reload it on every open
            self.assertIn(b, tt_bridge._LIVE)
            self.assertTrue(b.running)
            tt_bridge.stop_all()
            self.assertFalse(b.running)
            self.assertNotIn(b, tt_bridge._LIVE)
            self.assertNotIn("topotransfer-bridge", [t.name for t in threading.enumerate()])


if __name__ == "__main__":
    unittest.main()
