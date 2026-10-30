"""
The Maya bridge serving the bundled web app (no Node.js): static files, MIME types,
path safety, same-origin result upload. Uses a real loopback server.

    python -m unittest discover -s tests/python -v
"""

import http.client
import json
import os
import sys
import tempfile
import unittest

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

OBJ = "# Exported by TopoTransfer\n# space: original base coordinates\nv 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n"


class TestBundledApp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = self.tmp.name
        self.work = os.path.join(t, "work")
        self.app = os.path.join(t, "app")
        self.public = os.path.join(t, "public")
        for d in (self.work, os.path.join(self.app, "assets"), os.path.join(self.public, "examples")):
            os.makedirs(d)
        files = {
            os.path.join(self.app, "index.html"): "<!doctype html><title>TopoTransfer</title>",
            os.path.join(self.app, "assets", "index.js"): "export {}",
            os.path.join(self.app, "assets", "engine.worker.js"): "self.onmessage = () => {}",
            os.path.join(self.public, "examples", "head.obj"): "v 0 0 0\n",
            os.path.join(t, "secret.txt"): "do not serve",
            os.path.join(self.work, "mh_head_lod0.obj"): OBJ,
            os.path.join(self.work, "custom_head.obj"): OBJ,
        }
        for path, text in files.items():
            with open(path, "w", newline="") as f:
                f.write(text)
        self.bridge = tt_bridge.Bridge(
            self.work, "http://localhost:5173/",
            {"base": os.path.join(self.work, "mh_head_lod0.obj"), "reference": os.path.join(self.work, "custom_head.obj")},
            result_path=os.path.join(self.work, "mh_head_lod0_wrapped.obj"),
            validate=lambda tmp: obj_problem(tmp, 3),
            app_dir=self.app, static_dirs=[self.public],
        ).start()

    def tearDown(self):
        self.bridge.stop()
        self.tmp.cleanup()

    def request(self, method, path, body=None, headers=None):
        c = http.client.HTTPConnection("127.0.0.1", self.bridge.port, timeout=5)
        h = {"Host": f"127.0.0.1:{self.bridge.port}"}
        h.update(headers or {})
        c.request(method, path, body=body, headers=h)
        r = c.getresponse()
        data = r.read()
        c.close()
        return r.status, r.getheader("Content-Type"), data

    def p(self, rest):
        return f"/{self.bridge.token}/{rest}"

    def test_serves_the_app_with_correct_types(self):
        status, ctype, body = self.request("GET", self.p("app/"))
        self.assertEqual(status, 200)
        self.assertTrue(ctype.startswith("text/html"))
        self.assertIn(b"TopoTransfer", body)
        for asset in ("app/assets/index.js", "app/assets/engine.worker.js"):
            status, ctype, _ = self.request("GET", self.p(asset))
            self.assertEqual(status, 200)
            self.assertTrue(ctype.startswith("text/javascript"), ctype)  # module scripts and workers need a JS type
        # example meshes come from public/ (not copied into app/)
        status, _, body = self.request("GET", self.p("app/examples/head.obj"))
        self.assertEqual((status, body), (200, b"v 0 0 0\n"))
        # /app redirects to /app/
        status, _, _ = self.request("GET", self.p("app"))
        self.assertEqual(status, 302)

    def test_never_serves_files_outside_the_app_folders(self):
        for evil in ("app/../secret.txt", "app/%2e%2e/secret.txt", "app/..%2fsecret.txt", "app/assets/..%5c..%5csecret.txt",
                     "app/C:/Windows/win.ini", "app//etc/passwd", "app/assets/", "app/nothing.js"):
            status, _, body = self.request("GET", self.p(evil))
            self.assertEqual(status, 404, evil)
            self.assertNotIn(b"do not serve", body)
        # wrong token: nothing at all
        status, _, _ = self.request("GET", "/wrongtoken/app/")
        self.assertEqual(status, 404)
        self.assertIsNone(tt_bridge.safe_static_path([self.app], "../secret.txt"))

    def test_launch_url_points_at_the_bundled_app_and_upload_is_same_origin(self):
        url = self.bridge.app_launch_url()
        self.assertTrue(url.startswith(f"http://127.0.0.1:{self.bridge.port}/{self.bridge.token}/app/?"), url)
        self.assertIn("base=", url)
        self.assertIn("return=", url)
        own = {"Origin": self.bridge.origin, "Content-Type": "text/plain"}
        status, _, body = self.request("POST", self.p("result"), OBJ.encode(), own)
        self.assertEqual(status, 200, body)
        self.assertTrue(json.loads(body)["ok"])
        self.assertTrue(os.path.isfile(os.path.join(self.work, "mh_head_lod0_wrapped.obj")))
        # the external dev-server origin is not accepted when the bundled app is used
        status, _, _ = self.request("POST", self.p("result"), OBJ.encode(), {"Origin": "http://localhost:5173", "Content-Type": "text/plain"})
        self.assertEqual(status, 403)

    def test_app_only_server_without_files_or_upload(self):
        b = tt_bridge.Bridge(self.work, "http://localhost:5173/", {}, app_dir=self.app).start()
        try:
            self.assertEqual(b.app_launch_url(), f"http://127.0.0.1:{b.port}/{b.token}/app/")
            c = http.client.HTTPConnection("127.0.0.1", b.port, timeout=5)
            c.request("POST", f"/{b.token}/result", body=b"x", headers={"Host": f"127.0.0.1:{b.port}", "Content-Type": "text/plain"})
            self.assertEqual(c.getresponse().status, 404)
            c.close()
        finally:
            b.stop()

    def test_bundled_app_detection(self):
        repo = self.tmp.name
        self.assertEqual(tt_app.bundled_app(repo), (self.app, [self.public]))
        os.remove(os.path.join(self.app, "index.html"))
        self.assertIsNone(tt_app.bundled_app(repo))
        with self.assertRaises(FileNotFoundError):
            tt_bridge.Bridge(self.work, "http://localhost:5173/", {}, app_dir=self.app)


if __name__ == "__main__":
    unittest.main()
