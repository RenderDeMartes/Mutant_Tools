"""
Talk to the open TopoTransfer page (its Guides step has "Claude" on) straight through its bridge,
no Maya in between. For Claude Code (Bash) and the Mutant Tools MCP server.

    python tt_claude.py state
    python tt_claude.py capture --view front --mesh reference [--focus "Nose tip" --zoom 4] --out shot.png
    python tt_claude.py set_guides '[{"label": "Nose tip", "view": "front", "x": 512, "y": 470}]'
    python tt_claude.py set_guides points.json

The bridge is found through tt_bridge.CLAUDE_DIR (newest first), or given with --url (the bridge
root, or the app URL Maya opened). Standard library only.
"""

from __future__ import annotations

import argparse
import base64
import glob
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request

CLAUDE_DIR = os.path.join(tempfile.gettempdir(), "topotransfer_claude")


def bridge_roots():
    """Roots of the announced bridges, newest first."""
    found = []
    for path in glob.glob(os.path.join(CLAUDE_DIR, "*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                info = json.load(f)
            found.append((info.get("started", 0), info["root"]))
        except (OSError, ValueError, KeyError):
            continue
    return [root for _, root in sorted(found, reverse=True)]


def root_of(url: str) -> str:
    """The bridge root from the root itself or the app URL (`<root>/app/...`)."""
    url = url.split("?", 1)[0].rstrip("/")
    return url[: url.index("/app")] if "/app" in url else url


def call(command: str, args=None, url: str | None = None, timeout: float = 60):
    """Run a command in the page; raises RuntimeError with the bridge's message."""
    roots = [root_of(url)] if url else bridge_roots()
    if not roots:
        raise RuntimeError("No TopoTransfer open: open it from Mutant Tools (Misc > TopoTransfer or Meta Mutant).")
    body = json.dumps({"command": command, "args": args or {}, "timeout": timeout}).encode("utf-8")
    last = None
    for root in roots:
        req = urllib.request.Request(f"{root}/claude/call", data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout + 10) as res:
                return json.loads(res.read().decode("utf-8"))["result"]
        except urllib.error.HTTPError as e:
            try:
                last = json.loads(e.read().decode("utf-8")).get("message")
            except ValueError:
                last = f"HTTP {e.code}"
            if e.code != 409:  # 409: that page is not listening; try the next bridge
                break
        except OSError as e:  # a stale file of a closed bridge
            last = str(e)
    raise RuntimeError(last or "TopoTransfer did not answer")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", help="bridge root or the app URL (default: the newest open bridge)")
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("state")
    cap = sub.add_parser("capture")
    cap.add_argument("--view", default="front", choices=["front", "left", "right"])
    cap.add_argument("--mesh", default="reference", choices=["reference", "base"])
    cap.add_argument("--focus", default="")
    cap.add_argument("--zoom", type=float, default=1.0)
    cap.add_argument("--out", required=True)
    sg = sub.add_parser("set_guides")
    sg.add_argument("points", help="JSON list, or a .json file")
    a = ap.parse_args(argv)
    try:
        if a.command == "state":
            print(json.dumps(call("state", url=a.url), indent=1))
        elif a.command == "capture":
            args = {"view": a.view, "mesh": a.mesh, "zoom": a.zoom}
            if a.focus:
                args["focus"] = a.focus
            shot = call("capture", args, url=a.url)
            with open(a.out, "wb") as f:
                f.write(base64.b64decode(shot.pop("png")))
            print(json.dumps(dict(shot, path=os.path.abspath(a.out))))
        else:
            text = a.points
            if os.path.isfile(text):
                with open(text, encoding="utf-8") as f:
                    text = f.read()
            print(json.dumps(call("set_guides", {"points": json.loads(text)}, url=a.url), indent=1))
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
