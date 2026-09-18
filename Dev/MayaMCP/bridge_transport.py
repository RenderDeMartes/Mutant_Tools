"""Standard-library transport shared by the Mutant MCP bridge and direct Python clients."""

import ctypes
import json
import math
import os
import socket
import sys
import tempfile
import time

LOCKFILE_DIR = os.path.join(tempfile.gettempdir(), "mutant_tools_mcp_bridge")
SOCKET_TIMEOUT = 30.0
MAX_MESSAGE_BYTES = 16 * 1024 * 1024


def is_pid_running(pid):
    if not isinstance(pid, int) or pid <= 0:
        return False
    if sys.platform == "win32":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
        kernel32.OpenProcess.restype = ctypes.c_void_p
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = kernel32.OpenProcess(0x100000, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return True
        return False
    try:
        os.kill(pid, 0)
        return True
    except PermissionError:
        return True
    except OSError:
        return False


def list_sessions():
    """Return live-process registrations; scene is metadata from registration time."""
    sessions = []
    if not os.path.isdir(LOCKFILE_DIR):
        return sessions
    for name in sorted(os.listdir(LOCKFILE_DIR)):
        if not (name.startswith("maya_") and name.endswith(".json")):
            continue
        try:
            with open(os.path.join(LOCKFILE_DIR, name), encoding="utf-8") as stream:
                data = json.load(stream)
            if is_pid_running(data.get("pid")) and 1 <= int(data["port"]) <= 65535:
                sessions.append(data)
        except (OSError, ValueError, TypeError, KeyError, AttributeError):
            continue
    return sessions


def discover_maya_port():
    """Auto-select only an unambiguous session. Never silently change scenes."""
    sessions = list_sessions()
    if len(sessions) > 1:
        raise ValueError(
            "Multiple Maya sessions. Use maya_list_sessions and pass port explicitly."
        )
    return sessions[0]["port"] if sessions else None


def resolve_port(port=None):
    if port is None:
        env_port = os.environ.get("MUTANT_MCP_PORT")
        if env_port:
            try:
                port = int(env_port)
            except ValueError:
                raise ValueError(
                    "MUTANT_MCP_PORT must be an integer, got {!r}".format(env_port)
                )
    if port is None:
        port = discover_maya_port()
    if port is None:
        raise ConnectionError(
            "No Mutant MCP bridge found. Launch it from the Mutant Tools main "
            "window menu (MCP > Start Bridge)."
        )
    if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
        raise ValueError("port must be an integer from 1 to 65535")
    return port


def validate_timeout(timeout):
    if not math.isfinite(timeout) or not 0 < timeout <= 3600:
        raise ValueError("timeout must be greater than 0 and at most 3600 seconds")


class OutcomeUnknown(ConnectionError):
    """Request may have executed. Retrying could duplicate a mutation."""


def send_command(code, port=None, timeout=SOCKET_TIMEOUT):
    """One request, one complete NUL-terminated reply, no automatic retries."""
    validate_timeout(timeout)
    port = resolve_port(port)
    payload = code.encode("utf-8") + b"\n"
    if len(payload) >= MAX_MESSAGE_BYTES:
        raise ValueError("Maya command exceeds the 16 MiB transport limit")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.settimeout(min(timeout, 3.0))
        client.connect(("127.0.0.1", port))
        deadline = time.monotonic() + timeout
        try:
            client.settimeout(timeout)
            client.sendall(payload)
            data = bytearray()
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise socket.timeout()
                client.settimeout(remaining)
                chunk = client.recv(65536)
                if not chunk:
                    raise OSError(
                        "Maya closed the connection before completing its reply"
                    )
                data.extend(chunk)
                if len(data) > MAX_MESSAGE_BYTES:
                    raise OSError("Maya response exceeds the 16 MiB transport limit")
                if b"\x00" in chunk:
                    return bytes(data).split(b"\x00", 1)[0].decode("utf-8")
        except (OSError, UnicodeError) as exc:
            raise OutcomeUnknown(
                "Maya reply was interrupted or timed out. Execution may still be running "
                "or may have completed; do not automatically retry. {}".format(exc)
            ) from exc
    finally:
        client.close()


def bridge_call(action, port=None, timeout=SOCKET_TIMEOUT, **params):
    params["action"] = action
    code = "__import__('mutant_tools_mcp_bridge').bridge_dispatch({})".format(
        json.dumps(json.dumps(params))
    )
    try:
        port = resolve_port(port)
        raw = send_command(code, port=port, timeout=timeout)
    except OutcomeUnknown as exc:
        return {"success": False, "status": "unknown", "port": port, "error": str(exc)}
    except (OSError, ValueError) as exc:
        return {"success": False, "status": "not_sent", "port": port, "error": str(exc)}
    for line in raw.splitlines():
        try:
            result = json.loads(line)
            if isinstance(result, dict) and "success" in result:
                result["port"] = port
                return result
        except ValueError:
            pass
    return {
        "success": False,
        "status": "unknown",
        "port": port,
        "error": "Invalid Maya reply; do not automatically retry.",
        "raw": raw[:500],
    }
