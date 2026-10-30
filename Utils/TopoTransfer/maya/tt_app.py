"""
The TopoTransfer app from Maya: where it is, whether it answers, and opening it.

The bundled copy (`app/`, `npm run build:maya`) is served by Maya itself through
tt_bridge, so no Node.js is needed; a development checkout without `app/` is
started with `npm run dev`. Used by Meta Mutant (Utils/MetaMutant) and open to
any other Mutant tool:

    import tt_app
    tt_app.open_app()                       # the app on its own
    tt_app.bundled_app(tt_app.ROOT)         # (app_dir, static_dirs) or None
"""

from __future__ import annotations

import os
import sys
import webbrowser
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tt_bridge  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # the TopoTransfer folder
DEFAULT_URL = "http://localhost:5173/"


LOCAL_HOSTS = ("localhost", "127.0.0.1", "::1")


def is_local_url(url: str) -> bool:
    from urllib.parse import urlsplit

    return (urlsplit(url).hostname or "").lower() in LOCAL_HOSTS


def app_is_up(url: str, timeout: float = 1.0) -> bool:
    """True when something answers HTTP at `url` (any status)."""
    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=timeout):
            return True
    except urllib.error.HTTPError:
        return True
    except (OSError, ValueError):
        return False


def app_start_command(url: str, npm: Optional[str] = None) -> List[str]:
    """`npm run dev` on the URL's port, failing instead of silently moving to another port."""
    import shutil
    from urllib.parse import urlsplit

    npm = npm or shutil.which("npm.cmd" if sys.platform.startswith("win") else "npm") or shutil.which("npm") or ""
    port = urlsplit(url).port or 5173
    return [npm, "run", "dev", "--", "--port", str(port), "--strictPort"]


def start_app(repo: str, url: str):
    """Start the TopoTransfer dev server in its own console window (closing it stops the app)."""
    import subprocess

    cmd = app_start_command(url)
    kw = {"cwd": repo}
    if sys.platform.startswith("win"):
        kw["creationflags"] = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    else:
        kw["start_new_session"] = True
    return subprocess.Popen(cmd, **kw)


def ensure_app_running(url: str, repo: str, wait_seconds: float = 40.0, is_up=app_is_up, starter=start_app, sleep=None) -> "tuple[bool, str]":
    """
    Make sure TopoTransfer answers at `url`. A local URL that does not answer is started from
    `repo` with `npm run dev`; returns (ok, message for the log).
    """
    import shutil
    import time

    sleep = sleep or time.sleep
    if is_up(url):
        return True, f"TopoTransfer is running at {url}"
    if not is_local_url(url):
        return False, f"{url} does not answer; it is not on this machine, so it cannot be started from Maya"
    if not os.path.isfile(os.path.join(repo, "package.json")):
        return False, f"no TopoTransfer checkout at {repo}"
    if not os.path.isdir(os.path.join(repo, "node_modules")):
        return False, f"TopoTransfer is not installed yet: run `npm install` once in {repo}"
    if not app_start_command(url)[0] and starter is start_app and not shutil.which("npm"):
        return False, "Node.js (npm) was not found on PATH; install Node.js 20+ and restart Maya"
    starter(repo, url)
    waited = 0.0
    while waited < wait_seconds:
        sleep(0.5)
        waited += 0.5
        if is_up(url):
            return True, f"started TopoTransfer at {url} (its console window keeps it running; close it to stop the app)"
    return False, f"started `npm run dev` in {repo} but {url} did not answer within {wait_seconds:.0f} s; check its console window"


def bundled_app(repo: str) -> "Optional[tuple[str, List[str]]]":
    """(app_dir, static_dirs) when the prebuilt app (`npm run build:maya`) is present, else None."""
    app_dir = os.path.join(repo, "app")
    if not os.path.isfile(os.path.join(app_dir, "index.html")):
        return None
    public = os.path.join(repo, "public")
    return app_dir, ([public] if os.path.isdir(public) else [])


_APP_SERVER = globals().get("_APP_SERVER")  # bridge serving the bundled app for open_app(); kept across reloads


def open_app() -> Optional[str]:
    """Open the TopoTransfer app on its own (no files): served by Maya when app/ is bundled."""
    global _APP_SERVER
    bundled = bundled_app(ROOT)
    if bundled:
        import tempfile

        if _APP_SERVER is None or not _APP_SERVER.running:
            app_dir, static = bundled
            _APP_SERVER = tt_bridge.Bridge(tempfile.gettempdir(), DEFAULT_URL, {}, app_dir=app_dir, static_dirs=static).start()
        url = _APP_SERVER.app_page_url
        webbrowser.open(url)
        return url
    ok, message = ensure_app_running(DEFAULT_URL, ROOT)
    print(f"[TopoTransfer] {message}")
    if not ok:
        raise RuntimeError(message)
    webbrowser.open(DEFAULT_URL)
    return DEFAULT_URL
