"""
Loopback link between a Maya tool (e.g. Meta Mutant's mm_controller.py) and the TopoTransfer
browser app, so the Base / Reference OBJs and the wrapped result do not have to be dragged around by hand.

    bridge = Bridge(work_dir, "http://localhost:5173/", {"base": base_obj, "reference": ref_obj},
                    result_path=wrapped_obj, on_result=callback)
    bridge.start()
    webbrowser.open(bridge.app_launch_url())   # app fetches the files, Export POSTs the OBJ back
    ...
    bridge.stop()

The app is opened as `<app>?base=<url>&reference=<url>&return=<url>` (src/state/launch.ts).

Bundled app: with `app_dir` (a prebuilt copy of the web app, `npm run build:maya`) the bridge
also serves the app itself under `/<token>/app/`, so no Node.js / dev server is needed; the
page and the meshes then share one origin. `static_dirs` are extra read-only roots searched
after `app_dir` (e.g. `public/` for the example meshes, so they are not copied twice).

Security:
* binds 127.0.0.1 on a random free port only;
* every URL carries a random per-start token (`/<token>/...`); anything else is 404;
* serves only the files it was given (by name, inside the work folder), never a directory;
  app files only from inside `app_dir` / `static_dirs` (no `..`, no absolute paths, real paths checked);
* requests from a browser page must come from the app's origin (Origin header), and the Host
  header must be the loopback address (DNS rebinding); CORS is granted to the app origin only;
* the result is written under a fixed name, size-limited, checked by `validate` before it
  replaces the previous result.

Claude link: with "Claude" on in the app's Guides step, the page asks the bridge for commands
(`GET /<token>/claude/next`, long poll) and answers them (`POST /<token>/claude/reply`). Commands
come from Claude Code, without Maya in between: `POST /<token>/claude/call` with
{"command", "args"} (maya/tt_claude.py finds the open bridges through a file per bridge in
CLAUDE_DIR, written on start, removed on stop), or from Maya-side Python with `claude_call`:

    claude_call("state")                                   # guides, positions, mirror
    claude_call("capture", view="front", mesh="reference") # PNG of a view, guides drawn on it
    claude_call("set_guides", points=[{"label": "Nose tip", "view": "front", "x": 512, "y": 480}])

Standard library only (Maya's Python has no extra packages).
"""

from __future__ import annotations

import atexit
import json
import mimetypes
import os
import secrets
import sys
import tempfile
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable, Dict, Mapping, Optional, Sequence
from urllib.parse import quote, unquote, urlencode, urlsplit, urlunsplit

HOST = "127.0.0.1"
MAX_RESULT_BYTES = 512 * 1024 * 1024
_CHUNK = 1 << 20
REQUEST_TIMEOUT = 15  # seconds a request may stall before its thread gives up
CLAUDE_WAIT = 8  # seconds the app's Claude link waits for the next command (long poll)
MAX_REPLY_BYTES = 64 * 1024 * 1024
#: one JSON file per running bridge ({"root": ...}), so Claude Code can find the open page
CLAUDE_DIR = os.path.join(tempfile.gettempdir(), "topotransfer_claude")

# Every running bridge, so all can be stopped before Maya quits. A server thread still polling
# while Maya finalizes Python aborts Maya on exit ("PyThreadState_Get: ... the GIL is released").
# Kept across importlib.reload (the tools reload this module), so no bridge is forgotten.
_LIVE: "set[Bridge]" = globals().get("_LIVE", set())


def claude_call(command: str, timeout: float = 60.0, **args):
    """Run a Claude-link command in the open TopoTransfer page (the latest bridge whose page is linked)."""
    linked = [b for b in _LIVE if b.claude_linked]
    if not linked:
        raise RuntimeError(
            "TopoTransfer is not linked: open it from Mutant Tools (Misc > TopoTransfer or Meta Mutant), "
            "then turn on Claude in its Guides step.")
    return max(linked, key=lambda b: b.started_at).call_app(command, timeout, **args)


def stop_all() -> None:
    for bridge in list(_LIVE):
        try:
            bridge.stop()
        except Exception:  # never stop Maya from quitting
            traceback.print_exc()


def _stop_when_maya_quits() -> None:
    """Stop the bridges on Maya's quitApplication event, and at interpreter exit."""
    if getattr(sys.modules[__name__], "_quit_hooked", False):  # once per session, even across reloads
        return
    sys.modules[__name__]._quit_hooked = True
    atexit.register(stop_all)
    try:
        import maya.cmds as cmds  # type: ignore

        cmds.scriptJob(event=["quitApplication", stop_all], protected=True)
    except Exception:  # outside Maya, or Maya without its UI
        pass


def app_origin(app_url: str) -> str:
    """`scheme://host[:port]` of the app URL, as browsers send it in the Origin header."""
    u = urlsplit(app_url.strip())
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError(f"not an http(s) URL: {app_url!r}")
    default = {"http": 80, "https": 443}[u.scheme]
    host = u.hostname.lower()
    if ":" in host:  # IPv6 literal
        host = f"[{host}]"
    port = u.port if u.port not in (None, default) else None
    return f"{u.scheme}://{host}" + (f":{port}" if port else "")


def with_query(url: str, params: Mapping[str, str]) -> str:
    """`url` with `params` added to its query string (existing parameters are kept)."""
    u = urlsplit(url)
    query = u.query + ("&" if u.query else "") + urlencode(params, quote_via=quote)
    return urlunsplit((u.scheme, u.netloc, u.path or "/", query, u.fragment))


#: explicit types for app files (module scripts and workers must be served as JavaScript)
_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
    ".wasm": "application/wasm",
    ".txt": "text/plain; charset=utf-8",
    ".obj": "text/plain; charset=utf-8",
    ".ply": "application/octet-stream",
    ".stl": "application/octet-stream",
}


def content_type(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    return _TYPES.get(ext) or mimetypes.guess_type(path)[0] or "application/octet-stream"


def safe_static_path(roots, rel: str) -> Optional[str]:
    """
    The file `rel` (URL path, already unquoted) inside one of `roots`, or None. Rejects
    absolute paths, drive letters, backslashes and `..`; the real path must stay inside the root.
    """
    if not rel or rel.endswith("/"):
        rel = rel + "index.html"
    if "\\" in rel or "\0" in rel or rel.startswith("/") or ":" in rel:
        return None
    parts = rel.split("/")
    if any(p in ("", ".", "..") for p in parts):
        return None
    for root in roots:
        full = os.path.realpath(os.path.join(root, *parts))
        if full.startswith(root + os.sep) and os.path.isfile(full):
            return full
    return None


class Bridge:
    def __init__(
        self,
        work_dir: str,
        app_url: str,
        files: Mapping[str, str],
        result_path: Optional[str] = None,
        on_result: Optional[Callable[[str], None]] = None,
        validate: Optional[Callable[[str], Optional[str]]] = None,
        max_result_bytes: int = MAX_RESULT_BYTES,
        app_dir: Optional[str] = None,
        static_dirs: Sequence[str] = (),
    ):
        """
        files       role -> path ('base', 'reference'); each must be a file inside `work_dir`
        result_path where a received result is stored (inside `work_dir`); None = no upload route
        app_dir     prebuilt web app to serve under /<token>/app/ (then `app_url` is not used)
        on_result   called with `result_path` after a result was stored (on the server thread)
        validate    called with the received temporary file; returns an error message to reject it
        """
        self.work_dir = os.path.realpath(work_dir)
        self.app_url = app_url
        self.app_dirs = [os.path.realpath(d) for d in ([app_dir] if app_dir else []) + list(static_dirs) if d]
        if app_dir and not os.path.isfile(os.path.join(app_dir, "index.html")):
            raise FileNotFoundError(f"no index.html in the app folder {app_dir}")
        self.serves_app = bool(app_dir)
        self._origin = None if self.serves_app else app_origin(app_url)
        self.files: Dict[str, str] = {}
        for role, path in files.items():
            real = self._inside_work(path)
            if not os.path.isfile(real):
                raise FileNotFoundError(real)
            self.files[role] = real
        self.result_path = self._inside_work(result_path) if result_path else None
        self.on_result = on_result
        self.validate = validate
        self.max_result_bytes = max_result_bytes
        self.token = secrets.token_urlsafe(24)
        self.received = 0
        self._lock = threading.Lock()
        self._server: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[threading.Thread] = None
        self.started_at = 0.0
        # Claude link: commands waiting for the page, its replies by id, when it last asked
        self._claude = threading.Condition()
        self._commands: list = []
        self._replies: Dict[str, dict] = {}
        self._polled = 0.0

    def _inside_work(self, path: str) -> str:
        real = os.path.realpath(path)
        if os.path.dirname(real) != self.work_dir:
            raise ValueError(f"{path} is not directly inside the work folder {self.work_dir}")
        return real

    # ------------------------------------------------------------------ lifecycle

    def start(self) -> "Bridge":
        if self._server:
            return self
        bridge = self

        class Handler(_Handler):
            pass

        Handler.bridge = bridge
        self._server = ThreadingHTTPServer((HOST, 0), Handler)
        # request threads are joined on stop (each has a socket timeout), so none is left running
        # Python code while Maya shuts its interpreter down
        self._server.daemon_threads = False
        self._server.block_on_close = True
        self._thread = threading.Thread(target=self._server.serve_forever, kwargs={"poll_interval": 0.2}, name="topotransfer-bridge", daemon=True)
        self._thread.start()
        self.started_at = time.monotonic()
        _LIVE.add(self)
        self._announce()
        _stop_when_maya_quits()
        return self

    def stop(self) -> None:
        _LIVE.discard(self)
        if self._server:
            try:
                os.remove(self._announce_path())
            except OSError:
                pass
        with self._claude:  # wake a waiting long poll so the server can close
            self._claude.notify_all()
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
            self._thread = None

    @property
    def running(self) -> bool:
        return self._server is not None

    @property
    def port(self) -> int:
        if not self._server:
            raise RuntimeError("bridge is not running")
        return self._server.server_address[1]

    # ------------------------------------------------------------------ URLs

    @property
    def origin(self) -> str:
        """Origin allowed to use this bridge: the bundled app's own (this server) or the external app's."""
        return f"http://{HOST}:{self.port}" if self.serves_app else self._origin

    @property
    def root(self) -> str:
        return f"http://{HOST}:{self.port}/{self.token}"

    def file_url(self, role: str) -> str:
        return f"{self.root}/files/{quote(os.path.basename(self.files[role]))}"

    @property
    def result_url(self) -> str:
        return f"{self.root}/result"

    @property
    def app_page_url(self) -> str:
        """Where the app is loaded from: this bridge (bundled app) or the configured app URL."""
        return f"{self.root}/app/" if self.serves_app else self.app_url

    def app_launch_url(self) -> str:
        """The app URL with ?base=&reference=&return= pointing at this bridge."""
        params = {role: self.file_url(role) for role in ("base", "reference") if role in self.files}
        if self.result_path:
            params["return"] = self.result_url
        return with_query(self.app_page_url, params) if params else self.app_page_url

    # ------------------------------------------------------------------ Claude link

    def _announce_path(self) -> str:
        return os.path.join(CLAUDE_DIR, f"{self.port}.json")

    def _announce(self) -> None:
        """Let Claude Code find this bridge (only the current user's temp folder holds the token)."""
        try:
            os.makedirs(CLAUDE_DIR, exist_ok=True)
            with open(self._announce_path(), "w", encoding="utf-8") as f:
                json.dump({"root": self.root, "pid": os.getpid(), "started": time.time()}, f)
        except OSError:  # the link still works with the URL
            traceback.print_exc()

    @property
    def claude_linked(self) -> bool:
        """The page's Claude link asked for a command recently."""
        return self.running and time.monotonic() - self._polled < CLAUDE_WAIT + 5

    def call_app(self, command: str, timeout: float = 60.0, **args):
        """Send `command` to the page and wait for its answer (raises its error message)."""
        cid = secrets.token_hex(8)
        deadline = time.monotonic() + timeout
        with self._claude:
            self._commands.append({"id": cid, "command": command, "args": args})
            self._claude.notify_all()
            while cid not in self._replies:
                left = deadline - time.monotonic()
                if left <= 0 or not self.running:
                    self._commands = [c for c in self._commands if c["id"] != cid]
                    raise TimeoutError(f"TopoTransfer did not answer {command!r} in {timeout:.0f} s")
                self._claude.wait(left)
            reply = self._replies.pop(cid)
        if not reply.get("ok"):
            raise RuntimeError(reply.get("message") or f"{command} failed")
        return reply.get("result")

    def _next_command(self) -> Optional[dict]:
        with self._claude:
            self._polled = time.monotonic()
            if not self._commands and self.running:
                self._claude.wait(CLAUDE_WAIT)
            self._polled = time.monotonic()
            return self._commands.pop(0) if self._commands else None

    def _reply(self, reply: dict) -> None:
        with self._claude:
            if isinstance(reply.get("id"), str):
                self._replies[reply["id"]] = reply
                self._claude.notify_all()

    # ------------------------------------------------------------------ result

    def _store_result(self, rfile, length: int) -> str:
        """Copy `length` bytes into a temporary file next to the result, validate, then replace."""
        fd, tmp = tempfile.mkstemp(prefix=".tt_upload_", suffix=".obj", dir=self.work_dir)
        try:
            with os.fdopen(fd, "wb") as f:
                left = length
                while left > 0:
                    chunk = rfile.read(min(_CHUNK, left))
                    if not chunk:
                        raise _HttpError(400, "connection closed before the whole file arrived")
                    f.write(chunk)
                    left -= len(chunk)
            problem = self.validate(tmp) if self.validate else None
            if problem:
                raise _HttpError(422, problem)
            with self._lock:
                os.replace(tmp, self.result_path)
                self.received += 1
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
        if self.on_result:
            try:
                self.on_result(self.result_path)
            except Exception:  # the file is stored; a failing UI callback must not fail the upload
                traceback.print_exc()
        return self.result_path


class _HttpError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


class _Handler(BaseHTTPRequestHandler):
    bridge: Bridge
    server_version = "TopoTransferBridge/1"
    sys_version = ""

    timeout = REQUEST_TIMEOUT  # a stalled browser connection cannot hold a thread (or Maya's exit) forever

    def log_message(self, format, *args):  # noqa: A002 - keep Maya's script editor quiet
        pass

    # ------------------------------------------------------------------ checks

    def _route(self) -> str:
        """Path after `/<token>`; raises 403/404 for foreign hosts, origins or tokens."""
        host = (self.headers.get("Host") or "").lower()
        port = self.bridge.port
        if host not in (f"{HOST}:{port}", f"localhost:{port}"):
            raise _HttpError(403, "bad Host header")
        origin = self.headers.get("Origin")
        if origin is not None and origin != self.bridge.origin:
            raise _HttpError(403, "origin not allowed")
        parts = urlsplit(self.path).path.split("/", 2)
        if len(parts) < 3 or parts[0] or not secrets.compare_digest(parts[1], self.bridge.token):
            raise _HttpError(404, "not found")
        return parts[2]

    def _cors(self) -> None:
        if self.headers.get("Origin") == self.bridge.origin:
            self.send_header("Access-Control-Allow-Origin", self.bridge.origin)
        self.send_header("Vary", "Origin")

    def _send(self, status: int, body: bytes, content_type: str, extra: Optional[Dict[str, str]] = None) -> None:
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, status: int, ok: bool, message: str, **extra) -> None:
        self._send(status, json.dumps(dict(ok=ok, message=message, **extra)).encode("utf-8"), "application/json")

    def _guard(self, fn) -> None:
        try:
            fn(self._route())
        except _HttpError as e:
            self.close_connection = True
            self._json(e.status, False, e.message)
        except Exception as e:  # never leave the browser hanging
            self.close_connection = True
            self._json(500, False, f"{type(e).__name__}: {e}")

    # ------------------------------------------------------------------ verbs

    def do_OPTIONS(self):
        def run(route):
            if route not in ("result", "claude/next", "claude/reply", "claude/call") and not route.startswith("files/"):
                raise _HttpError(404, "not found")
            extra = {
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "600",
            }
            if self.headers.get("Access-Control-Request-Private-Network") == "true":
                extra["Access-Control-Allow-Private-Network"] = "true"
            self._send(204, b"", "text/plain", extra)

        self._guard(run)

    def do_GET(self):
        def run(route):
            if route == "claude/next":
                command = self.bridge._next_command()
                if command is None:
                    self._send(204, b"", "text/plain")
                else:
                    self._json(200, True, "command", **command)
                return
            if route == "app" and self.bridge.serves_app:
                self._send(302, b"", "text/plain", {"Location": f"/{self.bridge.token}/app/"})
                return
            if route.startswith("app/") and self.bridge.app_dirs:
                path = safe_static_path(self.bridge.app_dirs, unquote(route[len("app/"):]))
                if path is None:
                    raise _HttpError(404, "not found")
                with open(path, "rb") as f:
                    body = f.read()
                self._send(200, body, content_type(path))
                return
            if not route.startswith("files/"):
                raise _HttpError(404, "not found")
            # only the registered files, matched by exact basename: no path is ever built from the URL
            name = unquote(route[len("files/"):])
            path = next((p for p in self.bridge.files.values() if os.path.basename(p) == name), None)
            if path is None:
                raise _HttpError(404, "not found")
            with open(path, "rb") as f:
                body = f.read()
            self._send(200, body, "text/plain; charset=utf-8")

        self._guard(run)

    do_HEAD = do_GET

    def do_POST(self):
        def run(route):
            if route == "claude/call":
                # from Claude Code (no browser page: pages are refused by their Origin in _route)
                if self.headers.get("Origin") is not None:
                    raise _HttpError(403, "not for browser pages")
                length = int(self.headers.get("Content-Length") or 0)
                if not 0 < length <= 1024 * 1024:
                    raise _HttpError(413, "bad request size")
                try:
                    call = json.loads(self.rfile.read(length).decode("utf-8"))
                    command, args = str(call["command"]), dict(call.get("args") or {})
                    timeout = float(call.get("timeout", 60))
                except (ValueError, KeyError, TypeError):
                    raise _HttpError(400, "expected {\"command\": ..., \"args\": {...}}")
                if not self.bridge.claude_linked:
                    raise _HttpError(409, "TopoTransfer is not listening: turn on Claude in its Guides step")
                try:
                    result = self.bridge.call_app(command, timeout, **args)
                except TimeoutError as e:
                    raise _HttpError(504, str(e))
                except RuntimeError as e:
                    raise _HttpError(422, str(e))
                self._json(200, True, "ok", result=result)
                return
            if route == "claude/reply":
                length = int(self.headers.get("Content-Length") or 0)
                if not 0 < length <= MAX_REPLY_BYTES:
                    raise _HttpError(413, "bad reply size")
                try:
                    reply = json.loads(self.rfile.read(length).decode("utf-8"))
                except ValueError:
                    raise _HttpError(400, "reply is not JSON")
                self.bridge._reply(reply if isinstance(reply, dict) else {})
                self._json(200, True, "ok")
                return
            if route != "result" or not self.bridge.result_path:
                raise _HttpError(404, "not found")
            raw = self.headers.get("Content-Length")
            if raw is None:
                raise _HttpError(411, "Content-Length required")
            try:
                length = int(raw)
            except ValueError:
                raise _HttpError(400, "bad Content-Length")
            if length <= 0:
                raise _HttpError(400, "empty upload")
            if length > self.bridge.max_result_bytes:
                raise _HttpError(413, f"upload larger than {self.bridge.max_result_bytes} bytes")
            path = self.bridge._store_result(self.rfile, length)
            self._json(200, True, f"saved as {os.path.basename(path)} in the Maya work folder", path=path)

        self._guard(run)
