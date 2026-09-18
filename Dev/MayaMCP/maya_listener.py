"""Mutant MCP Bridge — Maya-Side Listener
=========================================
Opens a Maya commandPort with a JSON-based protocol layer that captures
stdout, stderr and full tracebacks.

Picks a port that can actually be bound and writes a lockfile so
`mcp_server.py` can discover the running Maya session.

Usage (inside Maya, or via the Mutant Tools main window's MCP menu):
    from Mutant_Tools.Dev.MayaMCP import maya_listener
    maya_listener.start_bridge()       # auto-detect port
    maya_listener.stop_bridge()

    maya_listener.port_report()        # what is holding which port

Uses OS bind checks to avoid ports held by other Maya sessions.
"""

from __future__ import annotations

import io
import atexit
import uuid
import json
import os
import sys
import socket
import tempfile
import time
import traceback

import maya.cmds as cmds
import maya.OpenMayaUI as omui

try:
    from . import bridge_transport as client
except ImportError:
    import bridge_transport as client

try:
    from shiboken6 import wrapInstance
    from PySide6 import QtWidgets, QtCore, QtGui
except ImportError:
    from shiboken2 import wrapInstance
    from PySide2 import QtWidgets, QtCore, QtGui

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_DEFAULT_PORT = 7501
_PORT_RANGE = (_DEFAULT_PORT, _DEFAULT_PORT + 50)  # scan up to 50 ports
_LOCKFILE_DIR = client.LOCKFILE_DIR
_ACTIVE_PORT = None
_STATUS_WIDGET = None
_SCENE_JOBS = []


def _maya_main_window():
    pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(pointer), QtWidgets.QWidget) if pointer else None


# ---------------------------------------------------------------------------
# Rigging naming conventions (Mutant Tools' own config, not hardcoded)
# ---------------------------------------------------------------------------


def _name_conventions():
    """Read Mutant Tools' own suffix conventions (Config/name_conventions.json)."""
    try:
        import Mutant_Tools.Utils.Rigging.tools as mt_tools

        nc, _curves, _setup = mt_tools.import_configs(curves=False, setup=False)
        return nc or {}
    except Exception:
        return {}


_MT = None

# Keys of the `colors` dict in Tools_class.assign_color — not derived from
# config, so kept in sync by hand if that dict ever changes.
_COLOR_NAMES = {
    "red", "blue", "white", "purple", "green",
    "lightBlue", "yellow", "pink", "grey", "orange",
}


def _mt():
    """Mutant Tools' own rig-building API (Utils/Rigging), cached after first use.

    Prefer this over raw cmds for anything it already covers: naming,
    color, offset groups, controllers, custom attrs, and IK/FK switching
    all come from here rather than being reimplemented in the bridge.
    """
    global _MT
    if _MT is None:
        import Mutant_Tools.Utils.Rigging.main_mutant as main_mutant

        _MT = main_mutant.Mutant()
    return _MT


# ---------------------------------------------------------------------------
# Port & Lockfile Management
# ---------------------------------------------------------------------------


def _can_bind(port):
    """True if this process could actually take *port*.

    Binding is the only test that answers the question we care about.
    connect() does not: a wedged Maya holds its port bound while refusing
    connections, so a connect failure means "nobody answered", never "the
    port is free". SO_REUSEADDR is deliberately NOT set -- it would let the
    bind succeed against a socket in TIME_WAIT and put us right back to
    guessing.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def _port_responds(port, timeout=0.25):
    """True if something on *port* completes a TCP handshake."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        return sock.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False
    finally:
        sock.close()


def _port_state(port):
    """One of "free", "live" or "wedged".

    "wedged" is the case worth naming: bound by somebody, but refusing
    connections. Usually a Maya whose main thread is stuck, and the reason a
    later session cannot get the port.
    """
    if _can_bind(port):
        return "free"
    return "live" if _port_responds(port) else "wedged"


def _find_free_port(start=_PORT_RANGE[0], end=_PORT_RANGE[1]):
    """First port in the range this process can bind, or None.

    Skips ports held by anything else -- including a wedged Maya -- and warns
    about those rather than letting the caller fail mysteriously later.
    """
    blocked = []
    for port in range(start, end):
        state = _port_state(port)
        if state == "free":
            if blocked:
                print(
                    "Mutant MCP: skipped {} -- already held ({}).".format(
                        ", ".join("{} [{}]".format(p, s) for p, s in blocked),
                        "another Maya or tool",
                    )
                )
            return port
        blocked.append((port, state))
    return None


def _lockfile_path(port):
    """Return the lockfile path for a given port."""
    return os.path.join(_LOCKFILE_DIR, "maya_{}.json".format(port))


def _write_lockfile(port):
    """Write a lockfile so the MCP sidecar can discover this Maya session."""
    os.makedirs(_LOCKFILE_DIR, exist_ok=True)
    data = {
        "port": port,
        "pid": os.getpid(),
        "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "maya_version": str(cmds.about(version=True)),
        "bridge_version": 1,
    }
    # Include scene name if available
    try:
        scene = cmds.file(q=True, sceneName=True)
        if scene:
            data["scene"] = scene
    except Exception:
        pass

    path = _lockfile_path(port)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(path + ".tmp", path)
    return path


def _remove_lockfile(port):
    """Remove the lockfile for a given port."""
    path = _lockfile_path(port)
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def _cleanup_stale_lockfiles():
    """Remove lockfiles for Maya sessions that are no longer running."""
    if not os.path.isdir(_LOCKFILE_DIR):
        return
    for filename in os.listdir(_LOCKFILE_DIR):
        if not filename.startswith("maya_") or not filename.endswith(".json"):
            continue
        filepath = os.path.join(_LOCKFILE_DIR, filename)
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            pid = data.get("pid")
            if pid and not _is_pid_running(pid):
                os.remove(filepath)
        except Exception:
            # Corrupted lockfile — remove it
            try:
                os.remove(filepath)
            except Exception:
                pass


_is_pid_running = client.is_pid_running


# ---------------------------------------------------------------------------
# Status GUI
# ---------------------------------------------------------------------------


class _BridgeStatusWidget(QtWidgets.QWidget):
    """Small floating pill that indicates the Mutant MCP bridge is active."""

    def __init__(self, port, parent=None):
        super().__init__(parent)
        self.setObjectName("MutantMCPStatus")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.port = port

        # --- Layout ---
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Container frame
        frame = QtWidgets.QFrame()
        frame.setObjectName("bridgeFrame")
        frame.setStyleSheet("""
            QFrame#bridgeFrame {
                background-color: rgba(30, 30, 30, 220);
                border: 1px solid #5c6bc0;
                border-radius: 12px;
            }
        """)
        frame_layout = QtWidgets.QHBoxLayout(frame)
        frame_layout.setContentsMargins(12, 6, 8, 6)
        frame_layout.setSpacing(8)

        # Dot indicator
        dot = QtWidgets.QLabel("●")
        dot.setStyleSheet("color: #66bb6a; font-size: 10px;")
        frame_layout.addWidget(dot)

        # Label
        label = QtWidgets.QLabel("Mutant MCP  ·  port {}".format(port))
        label.setStyleSheet("""
            color: #e0e0e0;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            font-size: 11px;
            font-weight: 500;
        """)
        frame_layout.addWidget(label)

        # Close button
        close_btn = QtWidgets.QPushButton("✕")
        close_btn.setFixedSize(18, 18)
        close_btn.setCursor(QtCore.Qt.PointingHandCursor)
        close_btn.setToolTip("Stop the Mutant MCP connection")
        close_btn.setAccessibleName("Close Bridge")
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #999;
                border: none;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ef5350;
            }
        """)
        close_btn.clicked.connect(self._on_close)
        frame_layout.addWidget(close_btn)

        layout.addWidget(frame)
        self.adjustSize()

    def _on_close(self):
        """Close the bridge when the user clicks X."""
        stop_bridge(self.port)

    def showEvent(self, event):
        """Position at bottom-right of Maya's main window."""
        super().showEvent(event)
        parent = self.parentWidget()
        if parent:
            pw = parent.width()
            ph = parent.height()
            self.move(pw - self.width() - 20, ph - self.height() - 40)


def _show_status_widget(port):
    """Show the bridge status pill."""
    global _STATUS_WIDGET
    _hide_status_widget()

    maya_win = _maya_main_window()
    _STATUS_WIDGET = _BridgeStatusWidget(port, parent=maya_win)
    _STATUS_WIDGET.show()


def _hide_status_widget():
    """Hide and destroy the status pill."""
    global _STATUS_WIDGET
    if _STATUS_WIDGET is not None:
        try:
            _STATUS_WIDGET.close()
            _STATUS_WIDGET.deleteLater()
        except Exception:
            pass
        _STATUS_WIDGET = None


# ---------------------------------------------------------------------------
# Start / Stop
# ---------------------------------------------------------------------------


def start_bridge(port=None):
    """Open a command port in Maya with auto port detection and lockfile.

    Args:
        port (int, optional): Specific port to use. If None, auto-detects.

    Returns:
        int: The port number that was opened, or None on failure.
    """
    global _ACTIVE_PORT

    _cleanup_stale_lockfiles()

    if _ACTIVE_PORT is not None:
        if port is not None and port != _ACTIVE_PORT:
            raise ValueError(
                "Stop the current bridge before opening another port in this Maya."
            )
        if cmds.commandPort("127.0.0.1:{}".format(_ACTIVE_PORT), query=True):
            _write_lockfile(_ACTIVE_PORT)
            return _ACTIVE_PORT
        _remove_lockfile(_ACTIVE_PORT)
        _ACTIVE_PORT = None

    if port is None:
        port = _find_free_port()
        if port is None:
            cmds.warning(
                "Mutant MCP: no bindable port in range {}-{}. Run "
                "maya_listener.port_report() to see what is holding "
                "them.".format(_PORT_RANGE[0], _PORT_RANGE[1])
            )
            return None
    else:
        # An explicit port still gets checked: silently failing to bind is
        # what made this confusing in the first place.
        if (
            not isinstance(port, int)
            or isinstance(port, bool)
            or not 1 <= port <= 65535
        ):
            raise ValueError("port must be an integer from 1 to 65535")
        if not cmds.commandPort("127.0.0.1:{}".format(port), query=True):
            state = _port_state(port)
            if state != "free":
                cmds.warning(
                    "Mutant MCP: port {} is already held by another process "
                    "({}){}. Call start_bridge() with no argument to take the "
                    "next free one.".format(
                        port,
                        state,
                        (
                            " -- it is bound but not answering, so it is probably a "
                            "wedged Maya"
                            if state == "wedged"
                            else ""
                        ),
                    )
                )
                return None

    port_name = "127.0.0.1:{}".format(port)

    try:
        if not cmds.commandPort(port_name, query=True):
            # Maya 2023's echo handler writes str to a binary socket and drops
            # connections. The bridge returns JSON as the command result.
            cmds.commandPort(
                name=port_name,
                sourceType="python",
                echoOutput=False,
                bufferSize=client.MAX_MESSAGE_BYTES,
            )
            _ACTIVE_PORT = port
            lockfile = _write_lockfile(port)
            print(
                "Mutant MCP: listening on {} (pid {}, lockfile: {})".format(
                    port, os.getpid(), lockfile
                )
            )
            _register_lifecycle()
            return port
        else:
            _ACTIVE_PORT = port
            _write_lockfile(port)
            print("Mutant MCP: already listening on port {}.".format(port))
            _register_lifecycle()
            return port
    except Exception as e:
        cmds.warning("Mutant MCP: failed to open port {}: {}".format(port, e))
        return None


def _refresh_registration():
    if _ACTIVE_PORT is not None:
        _write_lockfile(_ACTIVE_PORT)


def _register_lifecycle():
    atexit.unregister(_refresh_registration_on_exit)
    atexit.register(_refresh_registration_on_exit)
    if not cmds.about(batch=True):
        if not _SCENE_JOBS:
            for event in ("SceneOpened", "NewSceneOpened", "SceneSaved"):
                _SCENE_JOBS.append(cmds.scriptJob(event=[event, _refresh_registration]))
        try:
            _show_status_widget(_ACTIVE_PORT)
        except Exception as exc:
            cmds.warning(
                "Mutant MCP connected; status widget unavailable: {}".format(exc)
            )


def _refresh_registration_on_exit():
    if _ACTIVE_PORT is not None:
        _remove_lockfile(_ACTIVE_PORT)


def port_report(start=_PORT_RANGE[0], end=None):
    """Print who holds each port in the range. Prints, and returns, the rows.

    Written for exactly one situation: the port looks open (netstat says
    LISTENING) but nothing can talk to it. A "wedged" row is that -- a bound
    socket whose owner is not servicing it.
    """
    if end is None:
        end = min(start + 10, _PORT_RANGE[1])
    lockfiles = {}
    if os.path.isdir(_LOCKFILE_DIR):
        for filename in os.listdir(_LOCKFILE_DIR):
            try:
                with open(os.path.join(_LOCKFILE_DIR, filename), "r") as f:
                    data = json.load(f)
                lockfiles[data.get("port")] = data
            except Exception:
                continue

    rows = []
    for port in range(start, end):
        state = _port_state(port)
        owner = ""
        info = lockfiles.get(port)
        if info:
            pid = info.get("pid")
            alive = _is_pid_running(pid) if pid else False
            owner = "maya pid {}{}".format(pid, "" if alive else " (GONE)")
            if info.get("scene"):
                owner += " -- {}".format(os.path.basename(info["scene"]))
        elif state != "free":
            owner = "not ours (no lockfile)"
        rows.append((port, state, owner))
        marker = {"free": "  ", "live": "->", "wedged": "!!"}[state]
        print("{} {}  {:6}  {}".format(marker, port, state, owner))
    if any(state == "wedged" for _p, state, _o in rows):
        print(
            "\n!! wedged = bound but refusing connections. That is usually a "
            "Maya whose main thread is stuck; quit it (or use another port) "
            "before expecting this one to answer."
        )
    return rows


def stop_bridge(port=None):
    """Close the command port, remove the lockfile, and dismiss the status GUI.

    Args:
        port (int, optional): Port to close. Defaults to the active port.
    """
    global _ACTIVE_PORT

    _hide_status_widget()

    if port is None:
        port = _ACTIVE_PORT
    if port is None:
        print("Mutant MCP: No active port to close.")
        return

    port_name = "127.0.0.1:{}".format(port)
    try:
        if cmds.commandPort(port_name, query=True):
            cmds.commandPort(name=port_name, close=True)
            print("Mutant MCP closed on port {}.".format(port))
        else:
            print("Mutant MCP not open on port {}.".format(port))
    except Exception as e:
        print("Mutant MCP: Error closing port {}: {}".format(port, e))

    _remove_lockfile(port)
    if _ACTIVE_PORT == port:
        _ACTIVE_PORT = None
        for job in _SCENE_JOBS:
            if cmds.scriptJob(exists=job):
                cmds.scriptJob(kill=job, force=True)
        _SCENE_JOBS[:] = []


def get_active_port():
    """Return the currently active bridge port, or None."""
    return _ACTIVE_PORT


# ---------------------------------------------------------------------------
# JSON Protocol — Dispatch
# ---------------------------------------------------------------------------


def bridge_dispatch(json_str):
    """Main entry point called by the MCP sidecar over commandPort.

    Receives a JSON request string, executes the action, and returns a
    JSON response string with captured stdout, stderr, result, and errors.

    Args:
        json_str (str): JSON-encoded request.

    Returns:
        str: JSON-encoded response.
    """
    try:
        request = json.loads(json_str)
    except (json.JSONDecodeError, TypeError) as e:
        return json.dumps(
            {
                "success": False,
                "error": "Invalid JSON: {}".format(str(e)),
                "stdout": "",
                "stderr": "",
                "result": None,
                "traceback": None,
            }
        )

    if not isinstance(request, dict):
        return _make_response(False, error="Request must be a JSON object")
    action = request.get("action", "exec")

    dispatch_table = {
        "exec": _action_exec,
        "query": _action_query,
        "scene_info": _action_scene_info,
        "list_nodes": _action_list_nodes,
        "node_info": _action_node_info,
        "scene_tree": _action_scene_tree,
        "selection": _action_selection,
        "list_references": _action_list_references,
        "list_blocks": _action_list_blocks,
        "block_info": _action_block_info,
        "list_controllers": _action_list_controllers,
        "rig_structure": _action_rig_structure,
        "inspect_variable": _action_inspect_variable,
        "check_errors": _action_check_errors,
        "ping": _action_ping,
        "capture": _action_capture,
        "get_attr": _action_get_attr,
        "set_attr": _action_set_attr,
        "list_connections": _action_list_connections,
        "connection_history": _action_connection_history,
        "connect_attrs": _action_connect_attrs,
        "disconnect_attrs": _action_disconnect_attrs,
        "create_node": _action_create_node,
        "delete_node": _action_delete_node,
        "rename_node": _action_rename_node,
        "parent_node": _action_parent_node,
        "duplicate_node": _action_duplicate_node,
        "convert_components": _action_convert_components,
        "skin_bind": _action_skin_bind,
        "skin_unbind": _action_skin_unbind,
        "skin_influences": _action_skin_influences,
        "skin_weights_get": _action_skin_weights_get,
        "skin_weights_set": _action_skin_weights_set,
        "skin_copy_weights": _action_skin_copy_weights,
        "create_joint": _action_create_joint,
        "orient_joint": _action_orient_joint,
        "create_ik_handle": _action_create_ik_handle,
        "create_constraint": _action_create_constraint,
        "list_constraints": _action_list_constraints,
        "delete_constraint": _action_delete_constraint,
        "create_control": _action_create_control,
        "root_group": _action_root_group,
        "assign_color": _action_assign_color,
        "assign_color_rgb": _action_assign_color_rgb,
        "hide_attr": _action_hide_attr,
        "match_transform": _action_match_transform,
        "ikfk_switch": _action_ikfk_switch,
        "add_attr": _action_add_attr,
        "connect_rotate_order": _action_connect_rotate_order,
        "lock_node": _action_lock_node,
        "mirror_group": _action_mirror_group,
        "list_control_shapes": _action_list_control_shapes,
    }

    handler = dispatch_table.get(action)
    if handler is None:
        return json.dumps(
            {
                "success": False,
                "error": "Unknown action: {}".format(action),
                "stdout": "",
                "stderr": "",
                "result": None,
                "traceback": None,
            }
        )

    return handler(request)


# ---------------------------------------------------------------------------
# Output Capture Helper
# ---------------------------------------------------------------------------


def _action_capture(request):
    """Capture on Maya's main thread; pass only the temporary PNG path over TCP."""
    path = None
    try:
        if cmds.about(batch=True):
            raise ValueError("Capture requires an interactive Maya session")
        width, height = request.get("width", 1280), request.get("height", 720)
        if any(not isinstance(n, int) or not 64 <= n <= 4096 for n in (width, height)):
            raise ValueError("width and height must be integers from 64 to 4096")
        target = request.get("target", "viewport")
        if target not in ("viewport", "window"):
            raise ValueError("target must be viewport or window")
        folder = os.path.join(tempfile.gettempdir(), "mutant_mcp_captures")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, uuid.uuid4().hex + ".png")
        if target == "viewport":
            panel = request.get("panel") or cmds.getPanel(withFocus=True)
            panels = cmds.getPanel(type="modelPanel") or []
            if panel not in panels:
                if request.get("panel"):
                    raise ValueError("Not a model panel: {}".format(panel))
                visible = cmds.getPanel(visiblePanels=True) or []
                panel = next((p for p in panels if p in visible), None)
            if not panel:
                raise ValueError("No visible model panel to capture")
            cmds.playblast(
                completeFilename=path,
                format="image",
                compression="png",
                frame=cmds.currentTime(query=True),
                editorPanelName=panel,
                widthHeight=(width, height),
                percent=100,
                viewer=False,
                showOrnaments=False,
                offScreen=True,
                forceOverwrite=True,
            )
            picture = QtGui.QImage(path)
        else:
            name = request.get("window", "")
            widget = _maya_main_window()
            if name:
                matches = [
                    w
                    for w in QtWidgets.QApplication.topLevelWidgets()
                    if w.isVisible() and name in (w.objectName(), w.windowTitle())
                ]
                if len(matches) != 1:
                    raise ValueError(
                        "window must match exactly one visible Qt objectName or title"
                    )
                widget = matches[0]
            if widget is None or not widget.isVisible():
                raise ValueError("Maya window is not visible")
            # QWidget.grab() leaves Maya's native GPU viewport black.
            picture = widget.screen().grabWindow(int(widget.winId())).toImage()
        if picture.isNull():
            raise RuntimeError("Maya returned an empty capture")
        if picture.width() > width or picture.height() > height:
            picture = picture.scaled(
                width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
        if not picture.save(path, "PNG"):
            raise RuntimeError("Could not save capture")
        return _make_response(
            True,
            result={
                "path": path,
                "width": picture.width(),
                "height": picture.height(),
                "target": target,
            },
        )
    except Exception as exc:
        if path and os.path.exists(path):
            os.remove(path)
        return _make_response(False, error=str(exc), tb=traceback.format_exc())


def _capture_exec(code_str, local_vars=None):
    """Execute Python code and capture stdout, stderr, result, and exceptions.

    Args:
        code_str (str): Python code to execute.
        local_vars (dict, optional): Local variables for exec context.

    Returns:
        dict: {success, result, stdout, stderr, traceback}
    """
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    exec_globals = {"__builtins__": __builtins__}
    exec_globals.update(local_vars or {})
    exec_locals = exec_globals

    # Make common Maya modules available
    exec_globals["cmds"] = cmds
    try:
        import maya.mel as mel

        exec_globals["mel"] = mel
    except ImportError:
        pass
    try:
        import maya.OpenMaya as om

        exec_globals["om"] = om
    except ImportError:
        pass

    result = None
    success = True
    tb_str = None

    try:
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture

        # Python execution is intentional; the command port binds to loopback only.
        try:
            compiled = compile(code_str, "<mutant-mcp>", "eval")
        except SyntaxError:
            # Compile before executing, so a runtime SyntaxError cannot run code twice.
            compiled = compile(code_str, "<mutant-mcp>", "exec")
            exec(compiled, exec_globals, exec_locals)
            result = exec_locals.get("result")
        else:
            result = eval(compiled, exec_globals, exec_locals)

    except Exception as e:
        success = False
        result = str(e)
        tb_str = traceback.format_exc()
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    # Make result JSON-serializable
    try:
        json.dumps(result)
    except (TypeError, ValueError):
        result = repr(result)

    return {
        "success": success,
        "result": result,
        "stdout": stdout_capture.getvalue(),
        "stderr": stderr_capture.getvalue(),
        "traceback": tb_str,
    }


def _make_response(
    success, result=None, stdout="", stderr="", tb=None, error=None, error_type=None
):
    """Build a standard response dict.

    error_type distinguishes bad input caught before touching Maya
    ("validation") from an exception raised by the Maya command itself
    ("maya_command"), so clients can tell "fix your call" from "Maya refused".
    """
    resp = {
        "success": success,
        "result": result,
        "stdout": stdout,
        "stderr": stderr,
        "traceback": tb,
    }
    if error:
        resp["error"] = error
        resp["error_type"] = error_type or "maya_command"
    return json.dumps(resp)


def _missing(node):
    """True if node is falsy or does not exist — the check every typed action starts with."""
    return not node or not cmds.objExists(node)


# ---------------------------------------------------------------------------
# Actions — Core Execution
# ---------------------------------------------------------------------------


def _action_exec(request):
    """Execute arbitrary Python code in Maya."""
    code = request.get("code", "")
    if not code:
        return _make_response(False, error="No code provided")

    result = _capture_exec(code)
    return json.dumps(result)


def _action_query(request):
    """Execute Python and return the evaluated result as structured data."""
    code = request.get("code", "")
    if not code:
        return _make_response(False, error="No code provided")

    result = _capture_exec(code)
    return json.dumps(result)


def _action_ping(request):
    """Health check — verify Maya is alive."""
    return _make_response(
        True,
        result={
            "status": "alive",
            "maya_version": str(cmds.about(version=True)),
            "scene": cmds.file(q=True, sceneName=True) or "(untitled)",
            "port": _ACTIVE_PORT,
            "pid": os.getpid(),
        },
    )


# ---------------------------------------------------------------------------
# Actions — Scene Inspection
# ---------------------------------------------------------------------------


def _action_scene_info(request):
    """Get scene metadata."""
    try:
        scene_name = cmds.file(q=True, sceneName=True) or "(untitled)"
        fps_mapping = {
            "game": 15,
            "film": 24,
            "pal": 25,
            "ntsc": 30,
            "show": 48,
            "palf": 50,
            "ntscf": 60,
        }
        time_unit = cmds.currentUnit(q=True, time=True)
        fps = fps_mapping.get(time_unit, time_unit)

        info = {
            "scene_name": os.path.basename(scene_name),
            "scene_path": scene_name,
            "project_path": cmds.workspace(q=True, rd=True),
            "fps": fps,
            "time_unit": time_unit,
            "frame_range": [
                cmds.playbackOptions(q=True, min=True),
                cmds.playbackOptions(q=True, max=True),
            ],
            "animation_range": [
                cmds.playbackOptions(q=True, ast=True),
                cmds.playbackOptions(q=True, aet=True),
            ],
            "linear_unit": cmds.currentUnit(q=True, linear=True),
            "up_axis": cmds.upAxis(q=True, axis=True),
            "modified": cmds.file(q=True, modified=True),
        }
        return _make_response(True, result=info)
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_list_nodes(request):
    """List nodes by type and/or pattern."""
    try:
        node_type = request.get("type")
        pattern = request.get("pattern")
        long_names = request.get("long", False)
        limit = request.get("limit", 500)

        kwargs = {}
        if node_type:
            kwargs["type"] = node_type
        if long_names:
            kwargs["long"] = True

        if pattern:
            nodes = cmds.ls(pattern, **kwargs) or []
        else:
            nodes = cmds.ls(**kwargs) or []

        if limit and len(nodes) > limit:
            nodes = nodes[:limit]
            truncated = True
        else:
            truncated = False

        return _make_response(
            True,
            result={
                "nodes": nodes,
                "count": len(nodes),
                "truncated": truncated,
            },
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_node_info(request):
    """Get detailed info about a specific node."""
    try:
        node = request.get("node")
        if not node or not cmds.objExists(node):
            return _make_response(False, error="Node '{}' does not exist".format(node))

        info = {
            "name": node,
            "type": cmds.nodeType(node),
            "parent": None,
            "children": [],
            "shapes": [],
            "attributes": {},
        }

        # Parent
        parents = cmds.listRelatives(node, parent=True, fullPath=True)
        if parents:
            info["parent"] = parents[0]

        # Children
        children = cmds.listRelatives(node, children=True, type="transform") or []
        info["children"] = children

        # Shapes
        shapes = cmds.listRelatives(node, shapes=True) or []
        info["shapes"] = shapes

        # Key attributes (user-defined + common)
        include_attrs = request.get("attrs")
        if include_attrs:
            attr_list = include_attrs
        else:
            attr_list = cmds.listAttr(node, userDefined=True) or []
            # Add common transform attrs
            for a in [
                "translateX",
                "translateY",
                "translateZ",
                "rotateX",
                "rotateY",
                "rotateZ",
                "scaleX",
                "scaleY",
                "scaleZ",
                "visibility",
            ]:
                if cmds.attributeQuery(a, node=node, exists=True):
                    attr_list.append(a)

        for attr in attr_list:
            try:
                full_attr = "{}.{}".format(node, attr)
                if not cmds.objExists(full_attr):
                    continue
                val = cmds.getAttr(full_attr)
                attr_type = cmds.getAttr(full_attr, type=True)
                locked = cmds.getAttr(full_attr, lock=True)
                # Check connections
                conns = (
                    cmds.listConnections(
                        full_attr, plugs=True, source=True, destination=False
                    )
                    or []
                )
                info["attributes"][attr] = {
                    "value": val,
                    "type": attr_type,
                    "locked": locked,
                    "source": conns[0] if conns else None,
                }
            except Exception:
                info["attributes"][attr] = {"value": "(unreadable)", "type": "unknown"}

        return _make_response(True, result=info)
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_scene_tree(request):
    """Get the DAG hierarchy as a tree."""
    try:
        root_node = request.get("root")
        max_depth = request.get("depth", 5)

        def build_tree(node, depth=0):
            if depth >= max_depth:
                return {"name": node, "type": cmds.nodeType(node), "children": ["..."]}

            children = cmds.listRelatives(node, children=True, type="transform") or []
            return {
                "name": node,
                "type": cmds.nodeType(node),
                "children": [build_tree(c, depth + 1) for c in children],
            }

        if root_node:
            if not cmds.objExists(root_node):
                return _make_response(
                    False, error="Root node '{}' not found".format(root_node)
                )
            tree = build_tree(root_node)
        else:
            # Get top-level transforms
            assemblies = cmds.ls(assemblies=True) or []
            # Filter out cameras
            assemblies = [
                a
                for a in assemblies
                if cmds.nodeType(a) == "transform"
                and not (cmds.listRelatives(a, shapes=True, type="camera"))
            ]
            tree = [build_tree(a) for a in assemblies]

        return _make_response(True, result=tree)
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_selection(request):
    """Get or set the current selection."""
    try:
        set_sel = request.get("select")
        if set_sel is not None:
            if isinstance(set_sel, list):
                cmds.select(set_sel, replace=True)
            elif set_sel == "":
                cmds.select(clear=True)
            else:
                cmds.select(set_sel, replace=True)

        sel = cmds.ls(selection=True, long=True) or []
        return _make_response(
            True,
            result={
                "selection": sel,
                "count": len(sel),
            },
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_list_references(request):
    """List all file references in the scene."""
    try:
        refs = cmds.file(q=True, reference=True) or []
        result = []
        for ref in refs:
            try:
                ref_node = cmds.referenceQuery(ref, referenceNode=True)
                namespace = cmds.referenceQuery(ref, namespace=True)
                loaded = cmds.referenceQuery(ref, isLoaded=True)
                result.append(
                    {
                        "path": ref,
                        "node": ref_node,
                        "namespace": namespace,
                        "loaded": loaded,
                    }
                )
            except Exception:
                result.append(
                    {"path": ref, "node": None, "namespace": None, "loaded": False}
                )

        return _make_response(True, result=result)
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


# ---------------------------------------------------------------------------
# Actions — Rigging / Mutant Tools Awareness
#
# Block/controller suffixes come from Mutant Tools' own
# Config/name_conventions.json (nc['module'], nc['ctrl']) rather than being
# hardcoded, so a studio that edits that file does not silently break these.
# ---------------------------------------------------------------------------


def _action_list_blocks(request):
    """List all Mutant Tools rig blocks (nc['module'] suffix) and their config."""
    try:
        nc = _name_conventions()
        block_suffix = nc.get("module", "_Block")
        blocks = cmds.ls("*" + block_suffix, type="transform") or []
        result = []
        for block in blocks:
            entry = {"name": block, "config": {}}
            conns = cmds.listConnections(block) or []
            # Config node is typically the second connection
            for conn in conns:
                user_attrs = cmds.listAttr(conn, userDefined=True) or []
                if user_attrs:
                    for attr in user_attrs:
                        try:
                            full = "{}.{}".format(conn, attr)
                            val = cmds.getAttr(full)
                            # Try getting enum as string
                            if cmds.getAttr(full, type=True) == "enum":
                                val = cmds.getAttr(full, asString=True)
                            entry["config"][attr] = val
                        except Exception:
                            entry["config"][attr] = "(unreadable)"
                    entry["config_node"] = conn
                    break
            result.append(entry)

        return _make_response(True, result=result)
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_block_info(request):
    """Get full config for a specific block."""
    try:
        block = request.get("block")
        if not block:
            return _make_response(False, error="No block name provided")
        if not cmds.objExists(block):
            return _make_response(False, error="Block '{}' not found".format(block))

        conns = cmds.listConnections(block) or []
        config_data = {}
        config_node = None

        for conn in conns:
            user_attrs = cmds.listAttr(conn, userDefined=True) or []
            if user_attrs:
                config_node = conn
                for attr in user_attrs:
                    try:
                        full = "{}.{}".format(conn, attr)
                        val = cmds.getAttr(full)
                        if cmds.getAttr(full, type=True) == "enum":
                            val = cmds.getAttr(full, asString=True)
                        config_data[attr] = val
                    except Exception:
                        config_data[attr] = "(unreadable)"
                break

        children = cmds.listRelatives(block, children=True, allDescendents=True) or []

        return _make_response(
            True,
            result={
                "block": block,
                "config_node": config_node,
                "config": config_data,
                "children": children,
            },
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_list_controllers(request):
    """List all rig controllers (nc['ctrl'] suffix)."""
    try:
        nc = _name_conventions()
        ctrl_suffix = nc.get("ctrl", "_Ctrl")
        ctrls = cmds.ls("*" + ctrl_suffix, type="transform") or []
        limit = request.get("limit", 200)
        pattern = request.get("pattern")

        if pattern:
            import re

            try:
                regex = re.compile(pattern, re.IGNORECASE)
                ctrls = [c for c in ctrls if regex.search(c)]
            except re.error:
                ctrls = [c for c in ctrls if pattern.lower() in c.lower()]

        truncated = False
        if limit and len(ctrls) > limit:
            ctrls = ctrls[:limit]
            truncated = True

        result = []
        for ctrl in ctrls:
            entry = {"name": ctrl}
            # Get color
            shapes = cmds.listRelatives(ctrl, shapes=True) or []
            if shapes:
                try:
                    override = cmds.getAttr("{}.overrideEnabled".format(shapes[0]))
                    if override:
                        entry["color_index"] = cmds.getAttr(
                            "{}.overrideColor".format(shapes[0])
                        )
                except Exception:
                    pass
            # Get parent
            parents = cmds.listRelatives(ctrl, parent=True)
            if parents:
                entry["parent"] = parents[0]
            result.append(entry)

        return _make_response(
            True,
            result={
                "controllers": result,
                "count": len(result),
                "truncated": truncated,
            },
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_rig_structure(request):
    """Dump a rig hierarchy tree.

    With no root, finds top-level assemblies that contain at least one rig
    block (nc['module'] suffix) and returns one tree per assembly, since
    Mutant Tools does not fix a single rig-root group name.
    """
    try:
        nc = _name_conventions()
        block_suffix = nc.get("module", "_Block")
        depth = request.get("depth", 4)

        def build_tree(node, d=0):
            if d >= depth:
                child_count = len(cmds.listRelatives(node, children=True) or [])
                return {
                    "name": node,
                    "type": cmds.nodeType(node),
                    "children_count": child_count,
                }

            children = cmds.listRelatives(node, children=True, type="transform") or []
            return {
                "name": node,
                "type": cmds.nodeType(node),
                "children": [build_tree(c, d + 1) for c in children],
            }

        root = request.get("root")
        if root:
            if not cmds.objExists(root):
                return _make_response(False, error="Root node '{}' not found".format(root))
            return _make_response(True, result=build_tree(root))

        assemblies = cmds.ls(assemblies=True) or []
        roots = []
        for a in assemblies:
            descendents = cmds.listRelatives(a, allDescendents=True, fullPath=True) or []
            if any(d.split("|")[-1].endswith(block_suffix) for d in descendents):
                roots.append(a)
        if not roots:
            # Fall back to top-level block nodes themselves.
            roots = cmds.ls("*" + block_suffix, type="transform", assemblies=True) or []
        if not roots:
            return _make_response(
                False,
                error="No rig blocks ('*{}') found in the scene.".format(block_suffix),
            )

        tree = [build_tree(r) for r in roots]
        return _make_response(True, result=tree)
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


# ---------------------------------------------------------------------------
# Actions — Debugging
# ---------------------------------------------------------------------------


def _action_inspect_variable(request):
    """Evaluate an expression and return its repr, type, and value."""
    try:
        expr = request.get("expression")
        if not expr:
            return _make_response(False, error="No expression provided")

        result = _capture_exec(expr)
        if result["success"]:
            val = result["result"]
            return _make_response(
                True,
                result={
                    "expression": expr,
                    "value": val,
                    "repr": repr(val) if val is not None else "None",
                    "type": type(val).__name__ if val is not None else "NoneType",
                },
            )
        else:
            return json.dumps(result)
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_check_errors(request):
    """Check for common scene problems."""
    try:
        issues = []

        # Duplicate node names
        all_nodes = cmds.ls() or []
        seen = {}
        for node in all_nodes:
            base_name = node.split("|")[-1]
            seen.setdefault(base_name, []).append(node)
        duplicates = {k: v for k, v in seen.items() if len(v) > 1}
        if duplicates:
            issues.append(
                {
                    "type": "duplicate_names",
                    "severity": "warning",
                    "count": len(duplicates),
                    "examples": list(duplicates.keys())[:10],
                }
            )

        # Unknown nodes
        unknown_nodes = cmds.ls(type="unknown") or []
        if unknown_nodes:
            issues.append(
                {
                    "type": "unknown_nodes",
                    "severity": "warning",
                    "count": len(unknown_nodes),
                    "nodes": unknown_nodes[:10],
                }
            )

        # Unknown plugins
        try:
            unknown_plugins = cmds.unknownPlugin(q=True, l=True) or []
            if unknown_plugins:
                issues.append(
                    {
                        "type": "unknown_plugins",
                        "severity": "warning",
                        "count": len(unknown_plugins),
                        "plugins": unknown_plugins,
                    }
                )
        except Exception:
            pass

        # Broken references
        refs = cmds.file(q=True, reference=True) or []
        broken_refs = []
        for ref in refs:
            try:
                if not cmds.referenceQuery(ref, isLoaded=True):
                    broken_refs.append(ref)
            except Exception:
                broken_refs.append(ref)
        if broken_refs:
            issues.append(
                {
                    "type": "broken_references",
                    "severity": "error",
                    "count": len(broken_refs),
                    "references": broken_refs,
                }
            )

        return _make_response(
            True,
            result={
                "issues": issues,
                "issue_count": len(issues),
                "healthy": len(issues) == 0,
            },
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


# ---------------------------------------------------------------------------
# Actions — Attributes / Connections
# ---------------------------------------------------------------------------


def _action_get_attr(request):
    """Get a single attribute's value, type, lock state, and incoming connection."""
    try:
        node = request.get("node")
        attr = request.get("attr")
        if _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        full = "{}.{}".format(node, attr)
        if not cmds.objExists(full):
            return _make_response(
                False,
                error="Attribute '{}' does not exist".format(full),
                error_type="validation",
            )
        conns = (
            cmds.listConnections(full, plugs=True, source=True, destination=False) or []
        )
        return _make_response(
            True,
            result={
                "value": cmds.getAttr(full),
                "type": cmds.getAttr(full, type=True),
                "locked": cmds.getAttr(full, lock=True),
                "source": conns[0] if conns else None,
            },
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_set_attr(request):
    """Set a single attribute, coercing the value to the attribute's existing type."""
    try:
        node = request.get("node")
        attr = request.get("attr")
        if _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        full = "{}.{}".format(node, attr)
        if not cmds.objExists(full):
            return _make_response(
                False,
                error="Attribute '{}' does not exist".format(full),
                error_type="validation",
            )
        if cmds.getAttr(full, lock=True):
            return _make_response(
                False,
                error="Attribute '{}' is locked".format(full),
                error_type="validation",
            )
        value = request.get("value")
        attr_type = cmds.getAttr(full, type=True)
        if attr_type == "string":
            cmds.setAttr(full, value, type="string")
        elif attr_type in ("double3", "float3", "long3", "short3"):
            if not isinstance(value, (list, tuple)) or len(value) != 3:
                return _make_response(
                    False,
                    error="'{}' expects 3 numbers, got {!r}".format(attr_type, value),
                    error_type="validation",
                )
            cmds.setAttr(full, *value, type=attr_type)
        elif isinstance(value, (bool, int, float)):
            cmds.setAttr(full, value)
        else:
            return _make_response(
                False,
                error="Unsupported value {!r} for attribute type '{}'".format(
                    value, attr_type
                ),
                error_type="validation",
            )
        return _make_response(True, result={"value": cmds.getAttr(full)})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_list_connections(request):
    """List connections into and/or out of a node or plug, tagged by direction."""
    try:
        node = request.get("node")
        attr = request.get("attr", "")
        base = node.split(".")[0] if node else node
        if _missing(base):
            return _make_response(
                False, error="Node '{}' does not exist".format(base), error_type="validation"
            )
        plug = "{}.{}".format(node, attr) if attr else node
        results = []
        if request.get("source", True):
            pairs = (
                cmds.listConnections(
                    plug, plugs=True, connections=True, source=True, destination=False
                )
                or []
            )
            for i in range(0, len(pairs), 2):
                results.append(
                    {"plug": pairs[i], "connected_to": pairs[i + 1], "direction": "incoming"}
                )
        if request.get("destination", True):
            pairs = (
                cmds.listConnections(
                    plug, plugs=True, connections=True, source=False, destination=True
                )
                or []
            )
            for i in range(0, len(pairs), 2):
                results.append(
                    {"plug": pairs[i], "connected_to": pairs[i + 1], "direction": "outgoing"}
                )
        return _make_response(
            True, result={"connections": results, "count": len(results)}
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_connection_history(request):
    """List a node's upstream construction history."""
    try:
        node = request.get("node")
        if _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        limit = request.get("limit", 500)
        history = cmds.listHistory(node) or []
        truncated = False
        if limit and len(history) > limit:
            history = history[:limit]
            truncated = True
        return _make_response(
            True, result={"nodes": history, "count": len(history), "truncated": truncated}
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_connect_attrs(request):
    """Connect one plug to another."""
    try:
        source = request.get("source")
        destination = request.get("destination")
        if not source or not cmds.objExists(source):
            return _make_response(
                False,
                error="Plug '{}' does not exist".format(source),
                error_type="validation",
            )
        if not destination or not cmds.objExists(destination):
            return _make_response(
                False,
                error="Plug '{}' does not exist".format(destination),
                error_type="validation",
            )
        cmds.connectAttr(source, destination, force=request.get("force", False))
        return _make_response(True, result={"source": source, "destination": destination})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_disconnect_attrs(request):
    """Disconnect one plug from another."""
    try:
        source = request.get("source")
        destination = request.get("destination")
        if not source or not cmds.objExists(source):
            return _make_response(
                False,
                error="Plug '{}' does not exist".format(source),
                error_type="validation",
            )
        if not destination or not cmds.objExists(destination):
            return _make_response(
                False,
                error="Plug '{}' does not exist".format(destination),
                error_type="validation",
            )
        cmds.disconnectAttr(source, destination)
        return _make_response(True, result={"source": source, "destination": destination})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


# ---------------------------------------------------------------------------
# Actions — Nodes (typed CRUD) / Components
# ---------------------------------------------------------------------------


def _action_create_node(request):
    """Create a dependency-graph or DAG node."""
    try:
        node_type = request.get("node_type")
        if not node_type:
            return _make_response(False, error="No node_type provided", error_type="validation")
        parent = request.get("parent")
        if parent and _missing(parent):
            return _make_response(
                False,
                error="Parent '{}' does not exist".format(parent),
                error_type="validation",
            )
        kwargs = {}
        if request.get("name"):
            kwargs["name"] = request["name"]
        if parent:
            kwargs["parent"] = parent
        node = cmds.createNode(node_type, **kwargs)
        return _make_response(True, result={"node": node})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_delete_node(request):
    """Delete one or more nodes."""
    try:
        node = request.get("node")
        if not node:
            return _make_response(False, error="No node provided", error_type="validation")
        names = [n.strip() for n in node.split(",")] if isinstance(node, str) else list(node)
        missing = [n for n in names if _missing(n)]
        if missing:
            return _make_response(
                False,
                error="Node(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        cmds.delete(names)
        return _make_response(True, result={"deleted": names})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_rename_node(request):
    """Rename a node."""
    try:
        node = request.get("node")
        new_name = request.get("new_name")
        if _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        if not new_name:
            return _make_response(False, error="No new_name provided", error_type="validation")
        return _make_response(True, result={"node": cmds.rename(node, new_name)})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_parent_node(request):
    """Reparent one or more transforms under another, or to world."""
    try:
        node = request.get("node")
        if not node:
            return _make_response(False, error="No node provided", error_type="validation")
        names = [n.strip() for n in node.split(",")] if isinstance(node, str) else list(node)
        missing = [n for n in names if _missing(n)]
        if missing:
            return _make_response(
                False,
                error="Node(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        if request.get("world", False):
            result = cmds.parent(names, world=True)
        else:
            parent = request.get("parent")
            if _missing(parent):
                return _make_response(
                    False,
                    error="Parent '{}' does not exist".format(parent),
                    error_type="validation",
                )
            result = cmds.parent(names, parent)
        return _make_response(True, result={"node": result})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_duplicate_node(request):
    """Duplicate a node."""
    try:
        node = request.get("node")
        if _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        kwargs = {}
        if request.get("name"):
            kwargs["name"] = request["name"]
        result = cmds.duplicate(node, **kwargs)
        return _make_response(True, result={"node": result[0]})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_convert_components(request):
    """Convert a component selection to another component type, and select it."""
    try:
        components = request.get("components")
        if not components:
            return _make_response(
                False, error="No components provided", error_type="validation"
            )
        to = request.get("to", "vertex")
        flag = {
            "vertex": "toVertex",
            "edge": "toEdge",
            "face": "toFace",
            "uv": "toUV",
        }.get(to)
        if flag is None:
            return _make_response(
                False, error="Unknown component type '{}'".format(to), error_type="validation"
            )
        converted = cmds.polyListComponentConversion(components, **{flag: True}) or []
        cmds.select(converted, replace=True)
        return _make_response(
            True, result={"selection": converted, "count": len(converted)}
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


# ---------------------------------------------------------------------------
# Actions — Skinning
# ---------------------------------------------------------------------------

_BIND_METHODS = {"closestDistance": 0, "closestInHierarchy": 1, "heatMap": 2, "geodesicVoxel": 3}
_SKIN_METHODS = {"classicLinear": 0, "dualQuaternion": 1, "blend": 2}


def _find_skin_cluster(mesh):
    """Return the skinCluster upstream of mesh, or None."""
    history = cmds.listHistory(mesh) or []
    skins = cmds.ls(history, type="skinCluster") or []
    return skins[0] if skins else None


def _action_skin_bind(request):
    """Bind a mesh to a joint chain with a new skinCluster."""
    try:
        mesh = request.get("mesh")
        if _missing(mesh):
            return _make_response(
                False, error="Mesh '{}' does not exist".format(mesh), error_type="validation"
            )
        joints = request.get("joints") or []
        if not joints:
            return _make_response(False, error="No joints provided", error_type="validation")
        missing = [j for j in joints if _missing(j)]
        if missing:
            return _make_response(
                False,
                error="Joint(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        bind_method = _BIND_METHODS.get(request.get("bind_method", "closestDistance"))
        skin_method = _SKIN_METHODS.get(request.get("skin_method", "classicLinear"))
        if bind_method is None or skin_method is None:
            return _make_response(
                False, error="Unknown bind_method or skin_method", error_type="validation"
            )
        kwargs = {
            "bindMethod": bind_method,
            "skinMethod": skin_method,
            "maximumInfluences": request.get("max_influences", 4),
            "obeyMaxInfluences": True,
        }
        if request.get("name"):
            kwargs["name"] = request["name"]
        skin_node = cmds.skinCluster(joints + [mesh], **kwargs)[0]
        influences = cmds.skinCluster(skin_node, query=True, influence=True) or []
        return _make_response(
            True,
            result={
                "skin_cluster": skin_node,
                "influences": influences,
                "influence_count": len(influences),
            },
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_skin_unbind(request):
    """Remove the skinCluster from a mesh."""
    try:
        mesh = request.get("mesh")
        if _missing(mesh):
            return _make_response(
                False, error="Mesh '{}' does not exist".format(mesh), error_type="validation"
            )
        skin_node = _find_skin_cluster(mesh)
        if not skin_node:
            return _make_response(
                False,
                error="No skinCluster found on '{}'".format(mesh),
                error_type="validation",
            )
        cmds.skinCluster(skin_node, edit=True, unbind=True)
        return _make_response(True, result={"skin_cluster": skin_node})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_skin_influences(request):
    """List the influence joints on a mesh's skinCluster."""
    try:
        mesh = request.get("mesh")
        if _missing(mesh):
            return _make_response(
                False, error="Mesh '{}' does not exist".format(mesh), error_type="validation"
            )
        skin_node = _find_skin_cluster(mesh)
        if not skin_node:
            return _make_response(
                False,
                error="No skinCluster found on '{}'".format(mesh),
                error_type="validation",
            )
        influences = cmds.skinCluster(skin_node, query=True, influence=True) or []
        return _make_response(
            True, result={"skin_cluster": skin_node, "influences": influences}
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_skin_weights_get(request):
    """Get per-vertex skin weights, bounded by limit."""
    try:
        mesh = request.get("mesh")
        if _missing(mesh):
            return _make_response(
                False, error="Mesh '{}' does not exist".format(mesh), error_type="validation"
            )
        skin_node = _find_skin_cluster(mesh)
        if not skin_node:
            return _make_response(
                False,
                error="No skinCluster found on '{}'".format(mesh),
                error_type="validation",
            )
        vertices = request.get("vertices") or []
        limit = request.get("limit", 100)
        if not vertices:
            shapes = cmds.listRelatives(mesh, shapes=True, type="mesh") or []
            if not shapes:
                return _make_response(
                    False,
                    error="'{}' has no mesh shape".format(mesh),
                    error_type="validation",
                )
            count = cmds.polyEvaluate(shapes[0], vertex=True) or 0
            vertices = ["{}.vtx[{}]".format(mesh, i) for i in range(count)]
        truncated = False
        if limit and len(vertices) > limit:
            vertices = vertices[:limit]
            truncated = True
        influences = cmds.skinCluster(skin_node, query=True, influence=True) or []
        weights = {}
        for vtx in vertices:
            values = cmds.skinPercent(skin_node, vtx, query=True, value=True) or []
            weights[vtx] = {
                inf: w for inf, w in zip(influences, values) if w > 0.0001
            }
        return _make_response(
            True,
            result={"skin_cluster": skin_node, "weights": weights, "truncated": truncated},
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_skin_weights_set(request):
    """Set skin weights for a single vertex."""
    try:
        mesh = request.get("mesh")
        if _missing(mesh):
            return _make_response(
                False, error="Mesh '{}' does not exist".format(mesh), error_type="validation"
            )
        skin_node = _find_skin_cluster(mesh)
        if not skin_node:
            return _make_response(
                False,
                error="No skinCluster found on '{}'".format(mesh),
                error_type="validation",
            )
        vertex = request.get("vertex")
        if not vertex or not cmds.objExists(vertex):
            return _make_response(
                False,
                error="Component '{}' does not exist".format(vertex),
                error_type="validation",
            )
        weights = request.get("weights") or {}
        if not weights:
            return _make_response(False, error="No weights provided", error_type="validation")
        influences = set(cmds.skinCluster(skin_node, query=True, influence=True) or [])
        unknown = [j for j in weights if j not in influences]
        if unknown:
            return _make_response(
                False,
                error="Not influences on '{}': {}".format(skin_node, ", ".join(unknown)),
                error_type="validation",
            )
        cmds.skinPercent(
            skin_node,
            vertex,
            transformValue=list(weights.items()),
            normalize=request.get("normalize", True),
        )
        all_influences = cmds.skinCluster(skin_node, query=True, influence=True) or []
        result_values = cmds.skinPercent(skin_node, vertex, query=True, value=True) or []
        readback = {
            inf: w for inf, w in zip(all_influences, result_values) if w > 0.0001
        }
        return _make_response(True, result={"vertex": vertex, "weights": readback})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_skin_copy_weights(request):
    """Copy skin weights from one bound mesh to another bound mesh."""
    try:
        source_mesh = request.get("source_mesh")
        dest_mesh = request.get("dest_mesh")
        if _missing(source_mesh):
            return _make_response(
                False,
                error="Mesh '{}' does not exist".format(source_mesh),
                error_type="validation",
            )
        if _missing(dest_mesh):
            return _make_response(
                False,
                error="Mesh '{}' does not exist".format(dest_mesh),
                error_type="validation",
            )
        source_skin = _find_skin_cluster(source_mesh)
        if not source_skin:
            return _make_response(
                False,
                error="No skinCluster found on '{}'".format(source_mesh),
                error_type="validation",
            )
        dest_skin = _find_skin_cluster(dest_mesh)
        if not dest_skin:
            return _make_response(
                False,
                error="'{}' has no skinCluster; bind it first".format(dest_mesh),
                error_type="validation",
            )
        cmds.copySkinWeights(
            sourceSkin=source_skin,
            destinationSkin=dest_skin,
            surfaceAssociation=request.get("surface_association", "closestPoint"),
            influenceAssociation=request.get("influence_association", "oneToOne"),
            noMirror=True,
        )
        return _make_response(
            True,
            result={"source_skin_cluster": source_skin, "dest_skin_cluster": dest_skin},
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


# ---------------------------------------------------------------------------
# Actions — Joints & Constraints
# ---------------------------------------------------------------------------


def _action_create_joint(request):
    """Create a single joint. Selection is cleared first so it never auto-parents."""
    try:
        position = request.get("position") or [0.0, 0.0, 0.0]
        if not isinstance(position, (list, tuple)) or len(position) != 3:
            return _make_response(
                False, error="position must be [x, y, z]", error_type="validation"
            )
        parent = request.get("parent")
        if parent and _missing(parent):
            return _make_response(
                False,
                error="Parent '{}' does not exist".format(parent),
                error_type="validation",
            )
        cmds.select(clear=True)
        kwargs = {"position": tuple(position), "radius": request.get("radius", 1.0)}
        if request.get("name"):
            kwargs["name"] = request["name"]
        joint = cmds.joint(**kwargs)
        if parent:
            joint = cmds.parent(joint, parent)[0]
        return _make_response(True, result={"joint": joint})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_orient_joint(request):
    """Orient one or more joints using Maya's standard joint-orient algorithm."""
    try:
        joints = request.get("joints") or []
        if not joints:
            return _make_response(False, error="No joints provided", error_type="validation")
        missing = [j for j in joints if _missing(j)]
        if missing:
            return _make_response(
                False,
                error="Joint(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        not_joints = [j for j in joints if cmds.nodeType(j) != "joint"]
        if not_joints:
            return _make_response(
                False,
                error="Not joints: {}".format(", ".join(not_joints)),
                error_type="validation",
            )
        for j in joints:
            cmds.joint(
                j,
                edit=True,
                orientJoint=request.get("aim_axis", "xyz"),
                secondaryAxisOrient=request.get("up_axis", "yup"),
                zeroScaleOrient=request.get("zero_scale_orient", True),
            )
        return _make_response(True, result={"joints": joints})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_create_ik_handle(request):
    """Create an IK handle across a joint chain."""
    try:
        start_joint = request.get("start_joint")
        end_joint = request.get("end_joint")
        if _missing(start_joint):
            return _make_response(
                False,
                error="Joint '{}' does not exist".format(start_joint),
                error_type="validation",
            )
        if _missing(end_joint):
            return _make_response(
                False,
                error="Joint '{}' does not exist".format(end_joint),
                error_type="validation",
            )
        kwargs = {
            "startJoint": start_joint,
            "endEffector": end_joint,
            "solver": request.get("solver", "ikRPsolver"),
        }
        if request.get("name"):
            kwargs["name"] = request["name"]
        handle, effector = cmds.ikHandle(**kwargs)
        return _make_response(True, result={"ik_handle": handle, "effector": effector})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _constraint_funcs():
    """Lazily bound so this module still imports if a constraint command is unavailable."""
    return {
        "parent": cmds.parentConstraint,
        "point": cmds.pointConstraint,
        "orient": cmds.orientConstraint,
        "scale": cmds.scaleConstraint,
        "aim": cmds.aimConstraint,
    }


def _action_create_constraint(request):
    """Create a constraint driving one transform from one or more others."""
    try:
        fn = _constraint_funcs().get(request.get("type"))
        if fn is None:
            return _make_response(
                False,
                error="Unknown constraint type '{}'".format(request.get("type")),
                error_type="validation",
            )
        drivers = request.get("drivers") or []
        driven = request.get("driven")
        if not drivers or not driven:
            return _make_response(
                False, error="drivers and driven are required", error_type="validation"
            )
        missing = [n for n in drivers + [driven] if _missing(n)]
        if missing:
            return _make_response(
                False,
                error="Node(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        kwargs = {"maintainOffset": request.get("maintain_offset", True)}
        if request.get("name"):
            kwargs["name"] = request["name"]
        result = fn(*(drivers + [driven]), **kwargs)
        return _make_response(True, result={"constraint": result[0]})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_list_constraints(request):
    """List constraint nodes driving a transform."""
    try:
        node = request.get("node")
        if _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        constraints = cmds.listRelatives(node, type="constraint") or []
        result = []
        for c in constraints:
            drivers = cmds.ls(cmds.listConnections(c, source=True, destination=False) or [], type="transform")
            result.append(
                {"name": c, "type": cmds.nodeType(c), "drivers": sorted(set(drivers))}
            )
        return _make_response(True, result={"constraints": result})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_delete_constraint(request):
    """Delete a constraint node."""
    try:
        constraint = request.get("constraint")
        if _missing(constraint):
            return _make_response(
                False,
                error="Node '{}' does not exist".format(constraint),
                error_type="validation",
            )
        if not cmds.nodeType(constraint).endswith("Constraint"):
            return _make_response(
                False,
                error="'{}' is not a constraint node".format(constraint),
                error_type="validation",
            )
        cmds.delete(constraint)
        return _make_response(True, result={"deleted": constraint})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


# ---------------------------------------------------------------------------
# Actions — Mutant Tools' own rig-building commands (Utils/Rigging)
#
# These call mt.<method>() from tools.py/kinematics.py instead of
# reimplementing the same thing with raw cmds, so naming, color, and
# control-building conventions stay in exactly one place.
# ---------------------------------------------------------------------------


def _action_create_control(request):
    """Create a rig controller via mt.controller() (curve shape + root + gimbal/world)."""
    try:
        node = request.get("node") or ""
        if node and _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        name = request.get("name")
        if not name:
            return _make_response(False, error="No name provided", error_type="validation")
        mt = _mt()
        shape = request.get("shape", "cube")
        if shape not in mt.curve_data:
            return _make_response(
                False,
                error="Unknown shape '{}'; see list_control_shapes".format(shape),
                error_type="validation",
            )
        color = request.get("color") or mt.setup["main_color"]
        if color not in _COLOR_NAMES:
            return _make_response(
                False,
                error="Unknown color '{}'; choices: {}".format(
                    color, ", ".join(sorted(_COLOR_NAMES))
                ),
                error_type="validation",
            )
        result = mt.controller(
            input=node,
            name=name,
            shape=shape,
            color=color,
            size=request.get("size", 1),
            gimbal=request.get("gimbal", True),
            world=request.get("world", True),
        )
        return _make_response(True, result=result)
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_root_group(request):
    """Create offset/root group(s) above a node via mt.root_grp()."""
    try:
        node = request.get("node")
        if _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        custom_name = request.get("custom_name", "")
        groups = _mt().root_grp(
            input=node,
            custom=bool(custom_name),
            custom_name=custom_name or "customName",
            autoRoot=request.get("auto_root", False),
            replace_nc=request.get("replace_naming", False),
        )
        return _make_response(True, result={"groups": groups})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_assign_color(request):
    """Assign a named override color via mt.assign_color()/mt.smart_assign_color()."""
    try:
        nodes = request.get("nodes") or []
        if not nodes:
            return _make_response(False, error="No nodes provided", error_type="validation")
        missing = [n for n in nodes if _missing(n)]
        if missing:
            return _make_response(
                False,
                error="Node(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        mt = _mt()
        if request.get("smart", False):
            for n in nodes:
                mt.smart_assign_color(input=n)
        else:
            color = request.get("color")
            if color not in _COLOR_NAMES:
                return _make_response(
                    False,
                    error="Unknown color '{}'; choices: {}".format(
                        color, ", ".join(sorted(_COLOR_NAMES))
                    ),
                    error_type="validation",
                )
            for n in nodes:
                mt.assign_color(input=n, color=color)
        return _make_response(True, result={"nodes": nodes})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_assign_color_rgb(request):
    """Assign an RGB/HSV override color via mt.assign_color_rgb()."""
    try:
        nodes = request.get("nodes") or []
        if not nodes:
            return _make_response(False, error="No nodes provided", error_type="validation")
        missing = [n for n in nodes if _missing(n)]
        if missing:
            return _make_response(
                False,
                error="Node(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        color = request.get("color")
        if not isinstance(color, (list, tuple)) or len(color) != 3:
            return _make_response(
                False,
                error="color must be [r, g, b] (or [h, s, v] with hsv=True)",
                error_type="validation",
            )
        _mt().assign_color_rgb(input=list(nodes), color=list(color), hsv=request.get("hsv", False))
        return _make_response(True, result={"nodes": nodes})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_hide_attr(request):
    """Hide/lock channel-box attributes via mt.hide_attr()."""
    try:
        nodes = request.get("nodes") or []
        if not nodes:
            return _make_response(False, error="No nodes provided", error_type="validation")
        missing = [n for n in nodes if _missing(n)]
        if missing:
            return _make_response(
                False,
                error="Node(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        mt = _mt()
        for n in nodes:
            mt.hide_attr(
                input=n,
                t=request.get("translate", False),
                r=request.get("rotate", False),
                s=request.get("scale", False),
                v=request.get("visibility", False),
                rotate_order=request.get("rotate_order", False),
                show=request.get("show", False),
            )
        return _make_response(True, result={"nodes": nodes})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_match_transform(request):
    """Snap one transform onto another via mt.match() (constrain then delete)."""
    try:
        this = request.get("this")
        that = request.get("that")
        if _missing(this):
            return _make_response(
                False, error="Node '{}' does not exist".format(this), error_type="validation"
            )
        if _missing(that):
            return _make_response(
                False, error="Node '{}' does not exist".format(that), error_type="validation"
            )
        _mt().match(
            this=this,
            that=that,
            t=request.get("translate", True),
            r=request.get("rotate", True),
            s=request.get("scale", True),
        )
        return _make_response(True, result={"this": this, "that": that})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_ikfk_switch(request):
    """Wire an IK/FK switch onto a main joint via mt.switch_constraints()/switch_blend_colors()."""
    try:
        ik = request.get("ik")
        fk = request.get("fk")
        main = request.get("main")
        attr = request.get("attr")
        missing = [n for n in (ik, fk, main) if _missing(n)]
        if missing:
            return _make_response(
                False,
                error="Node(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        if not attr or not cmds.objExists(attr):
            return _make_response(
                False,
                error="Attribute '{}' does not exist".format(attr),
                error_type="validation",
            )
        mode = request.get("mode", "constraint")
        mt = _mt()
        if mode == "constraint":
            mt.switch_constraints(this=ik, that=fk, main=main, attr=attr)
        elif mode == "blend":
            mt.switch_blend_colors(this=ik, that=fk, main=main, attr=attr)
        else:
            return _make_response(
                False, error="mode must be 'constraint' or 'blend'", error_type="validation"
            )
        return _make_response(
            True, result={"ik": ik, "fk": fk, "main": main, "attr": attr, "mode": mode}
        )
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_add_attr(request):
    """Add a custom attribute via mt.new_attr()/new_attr_interger()/new_enum()/new_boolean()."""
    try:
        node = request.get("node")
        if _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        name = request.get("name")
        if not name:
            return _make_response(False, error="No name provided", error_type="validation")
        if cmds.attributeQuery(name, node=node, exists=True):
            return _make_response(
                False,
                error="Attribute '{}.{}' already exists".format(node, name),
                error_type="validation",
            )
        kind = request.get("kind", "float")
        mt = _mt()
        if kind == "float":
            attr = mt.new_attr(
                input=node,
                name=name,
                min=request.get("min", 0),
                max=request.get("max", 1),
                default=request.get("default", 0),
                keyable=request.get("keyable", True),
            )
        elif kind == "int":
            attr = mt.new_attr_interger(
                input=node,
                name=name,
                min=request.get("min", 0),
                max=request.get("max", 1),
                default=request.get("default", 0),
            )
        elif kind == "enum":
            enums = request.get("enums")
            if not enums:
                return _make_response(
                    False, error="enums is required for kind='enum'", error_type="validation"
                )
            attr = mt.new_enum(
                input=node,
                name=name,
                enums=enums,
                keyable=request.get("keyable", True),
                default=request.get("default", 0),
            )
        elif kind == "bool":
            # new_attr's `dv` is compared against the literal string 'True', not
            # a bool -- passing a real bool through would silently default false.
            attr = mt.new_boolean(
                input=node, name=name, dv="True" if request.get("default", True) else "False"
            )
        else:
            return _make_response(
                False, error="Unknown kind '{}'".format(kind), error_type="validation"
            )
        return _make_response(True, result={"attr": attr})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_connect_rotate_order(request):
    """Connect nodes' rotateOrder to a shared driver attr via mt.connect_rotate_order()."""
    try:
        nodes = request.get("nodes") or []
        driver = request.get("driver")
        if not nodes:
            return _make_response(False, error="No nodes provided", error_type="validation")
        missing = [n for n in nodes if _missing(n)]
        if _missing(driver):
            missing.append(driver)
        if missing:
            return _make_response(
                False,
                error="Node(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        mt = _mt()
        attr = None
        for n in nodes:
            attr = mt.connect_rotate_order(input=n, object=driver)
        return _make_response(True, result={"attr": attr, "nodes": nodes})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_lock_node(request):
    """Lock or unlock nodes via mt.lock_node()."""
    try:
        nodes = request.get("nodes") or []
        if not nodes:
            return _make_response(False, error="No nodes provided", error_type="validation")
        missing = [n for n in nodes if _missing(n)]
        if missing:
            return _make_response(
                False,
                error="Node(s) not found: {}".format(", ".join(missing)),
                error_type="validation",
            )
        unlock = request.get("unlock", False)
        _mt().lock_node(input=list(nodes), unlock=unlock)
        return _make_response(True, result={"nodes": nodes, "unlock": unlock})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_mirror_group(request):
    """Create a negative-scale mirror group above a node via mt.mirror_group()."""
    try:
        node = request.get("node")
        if _missing(node):
            return _make_response(
                False, error="Node '{}' does not exist".format(node), error_type="validation"
            )
        group = _mt().mirror_group(input=node, world=request.get("world", True))
        return _make_response(True, result={"mirror_group": group})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


def _action_list_control_shapes(request):
    """List curve shape names available to mt.controller() (Config/curves.json)."""
    try:
        shapes = sorted(_mt().curve_data.keys())
        return _make_response(True, result={"shapes": shapes})
    except Exception as e:
        return _make_response(False, error=str(e), tb=traceback.format_exc())


# ---------------------------------------------------------------------------
# Direct Python clients share the same transport as MCP (no SDK needed in Maya).
# ---------------------------------------------------------------------------

send_command = client.send_command
send_bridge_command = client.bridge_call
discover_maya_port = client.discover_maya_port

# Both package imports and the standalone Maya module share one bridge state.
sys.modules[__name__] = sys.modules.setdefault(
    "mutant_tools_mcp_bridge", sys.modules[__name__]
)
