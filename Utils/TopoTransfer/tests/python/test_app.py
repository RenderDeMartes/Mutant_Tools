"""
Tests for maya/tt_app.py: finding, starting and opening the TopoTransfer app from Maya.

    python -m unittest discover -s tests/python -v
"""

import http.server
import os
import socket
import sys
import tempfile
import threading
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "maya"))

import tt_app  # noqa: E402


class TestAppAutostart(unittest.TestCase):
    def test_app_is_up_against_a_real_local_server(self):
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), http.server.SimpleHTTPRequestHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            self.assertTrue(tt_app.app_is_up(f"http://127.0.0.1:{server.server_address[1]}/"))
        finally:
            server.shutdown()
            server.server_close()
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        free = s.getsockname()[1]
        s.close()
        self.assertFalse(tt_app.app_is_up(f"http://127.0.0.1:{free}/", timeout=0.3))

    def test_start_command_pins_the_port(self):
        self.assertEqual(tt_app.app_start_command("http://localhost:5180/", npm="npm"), ["npm", "run", "dev", "--", "--port", "5180", "--strictPort"])

    def test_ensure_app_running(self):
        url = "http://localhost:5173/"
        with tempfile.TemporaryDirectory() as repo:
            # already running: nothing started
            starter = mock.MagicMock()
            self.assertEqual(tt_app.ensure_app_running(url, repo, is_up=lambda u: True, starter=starter)[0], True)
            starter.assert_not_called()
            # hosted URL that does not answer: cannot start it
            ok, msg = tt_app.ensure_app_running("https://tt.example.com/", repo, is_up=lambda u: False, starter=starter)
            self.assertFalse(ok)
            self.assertIn("not on this machine", msg)
            # not installed yet
            open(os.path.join(repo, "package.json"), "w").close()
            ok, msg = tt_app.ensure_app_running(url, repo, is_up=lambda u: False, starter=starter)
            self.assertFalse(ok)
            self.assertIn("npm install", msg)
            # installed: started, then answers on the 3rd poll
            os.mkdir(os.path.join(repo, "node_modules"))
            answers = iter([False, False, False, True])
            ok, msg = tt_app.ensure_app_running(url, repo, is_up=lambda u: next(answers), starter=starter, sleep=lambda s: None)
            self.assertTrue(ok)
            starter.assert_called_once_with(repo, url)
            self.assertIn("started TopoTransfer", msg)
            # never answers: reported after the wait
            ok, msg = tt_app.ensure_app_running(url, repo, wait_seconds=2, is_up=lambda u: False, starter=mock.MagicMock(), sleep=lambda s: None)
            self.assertFalse(ok)
            self.assertIn("did not answer", msg)

    def test_root_is_the_topotransfer_folder(self):
        self.assertTrue(os.path.isfile(os.path.join(tt_app.ROOT, "package.json")))


if __name__ == "__main__":
    unittest.main()
