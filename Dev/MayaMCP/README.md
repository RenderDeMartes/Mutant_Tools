# Mutant MCP Bridge

Lets an MCP client (Claude Code, Claude Desktop, Codex, etc.) see and drive a
live Maya session running Mutant Tools: read the scene, run Python/MEL,
inspect rig blocks and controllers. Independent of any other repo or studio
pipeline — nothing here depends on anything outside Mutant Tools.

Three pieces:
- `maya_listener.py` — runs **inside Maya**. Opens a Maya `commandPort` and
  executes incoming requests on Maya's main thread. Only the standard library
  plus Maya/Qt modules; no `pip install` needed inside Maya.
- `bridge_transport.py` — stdlib-only transport shared by the listener and
  the server (session discovery, socket framing, timeouts).
- `mcp_server.py` — runs **outside Maya**, in a regular system Python. Speaks
  MCP over stdio to the client, forwards tool calls to the listener over a
  loopback TCP socket.

Only binds to `127.0.0.1`. `maya_execute`/`maya_query`/`maya_execute_mel` run
arbitrary Python or MEL in the Maya session — treat them like a local
debugger, not something to expose off-box. Everything else is a typed,
validated tool (see "Typed scene-editing tools" below), in the spirit of
[GimbalGoats/GG_MayaMCP](https://github.com/GimbalGoats/GG_MayaMCP), an
open-source Maya MCP server this bridge takes inspiration from.

## 1. Install the MCP SDK (system Python, not mayapy)

```
pip install "mcp>=2.0,<3"
```

## 2. Start the listener inside Maya

Use the **MCP** menu on the Mutant Tools main window (Start Bridge / Stop
Bridge). A status pill appears in Maya's main window while the bridge is
active; click its close button, or use Stop Bridge, to shut it down.

Equivalently, from the Script Editor (Python tab):

```python
from Mutant_Tools.Dev.MayaMCP import maya_listener
maya_listener.start_bridge()       # auto-detects a free port
maya_listener.stop_bridge()

maya_listener.port_report()        # see what is holding which port
```

The connection starts only when launched manually — no `userSetup.py` hook
or startup module is required.

## 3. Register the server with your MCP client

From this folder, use "Copy Claude Code Setup Command" in the main window's
MCP menu. If the bridge isn't running yet, it offers to start it first so the
copied command can pin the session's port — otherwise the server falls back
to auto-discovery, which only works while exactly one Maya session is
registered. Or run manually:

```
claude mcp add mutant-maya -- python "Dev/MayaMCP/mcp_server.py"
```

To pin a specific Maya session instead of relying on auto-discovery (needed
once more than one Maya is running), set `MUTANT_MCP_PORT` — this is what the
menu's copy does automatically:

```
claude mcp add mutant-maya -e MUTANT_MCP_PORT=7501 -- python "Dev/MayaMCP/mcp_server.py"
```

`MUTANT_MCP_PORT` is only a *default*: any tool call that passes `port=`
explicitly still overrides it.

For Claude Desktop, add to `claude_desktop_config.json` (use the absolute
path to this repo):

```json
{
  "mcpServers": {
    "mutant-maya": {
      "command": "python",
      "args": ["C:\\path\\to\\Mutant_Tools\\Dev\\MayaMCP\\mcp_server.py"],
      "env": {"MUTANT_MCP_PORT": "7501"}
    }
  }
}
```

Restart the client (or reconnect MCP) and the `maya_*` tools become
available whenever the listener is running in Maya.

## Tools and sessions

Start with `maya_list_sessions`, then `maya_ping(port=...)`. Discovery uses
a per-machine temp lockfile directory and ignores registrations from dead
processes. Scene metadata refreshes on open/new/save; `maya_scene_info`
queries current state. When multiple sessions exist, scene tools require an
explicit `port`. Every scene tool accepts it; `maya_job_status` uses the
session fixed at submission.

`maya_capture(target="viewport", port=...)` returns a PNG image of the
current frame. Use `target="window"` for Maya's UI. Floating tool windows can
be selected by their exact Qt `objectName` or window title via `window=...`.
Images fit within the requested width/height (default 1280x720; 64..4096).
Temporary images are removed after the sidecar reads them. No scene save
occurs.

Python execution shares one namespace within each call, including functions
and comprehensions. Calls are independent; assign `result` to return data
from a multi-line script. Python and MEL retain captured stdout/stderr/tracebacks.

### Rigging tools

`maya_list_blocks`, `maya_block_info`, `maya_list_controllers`, and
`maya_rig_structure` read Mutant Tools' own rig-block and controller naming
from `Config/name_conventions.json` (`nc['module']`, `nc['ctrl']`) — they are
not hardcoded suffixes, so an edited convention file still works.
`maya_rig_structure` with no `root` auto-detects rig roots as the top-level
assemblies that contain at least one block.

### Mutant Tools commands

These call `mt.<method>()` from `Utils/Rigging/tools.py` and `kinematics.py`
directly — the same rig-building API the Blocks templates use — instead of
reimplementing the same operation with raw `cmds`. Prefer these over the
generic typed tools below when both could do the job; naming, color, and
control-building conventions then stay driven by Mutant Tools itself:

- `maya_create_control` — `mt.controller()`: curve-shape control with an
  offset root and optional world/gimbal sub-controls.
- `maya_list_control_shapes` — available shape names (`Config/curves.json`).
- `maya_add_root_group` — `mt.root_grp()`: offset group, or root+auto pair.
- `maya_assign_color` / `maya_assign_color_rgb` — `mt.assign_color()` /
  `mt.smart_assign_color()` / `mt.assign_color_rgb()`.
- `maya_hide_attr` — `mt.hide_attr()`: hide/lock channel-box attributes.
- `maya_match_transform` — `mt.match()`: snap one transform onto another.
- `maya_create_ikfk_switch` — `mt.switch_constraints()` /
  `mt.switch_blend_colors()`: wire an IK/FK switch onto a main joint.
- `maya_add_attr` — `mt.new_attr()` / `new_attr_interger()` / `new_enum()` /
  `new_boolean()`: custom float/int/enum/bool attributes.
- `maya_connect_rotate_order` — `mt.connect_rotate_order()`.
- `maya_lock_node` — `mt.lock_node()`: node-level lock, not attribute lock.
- `maya_mirror_group` — `mt.mirror_group()`: negative-scale mirror group.

Joints, IK handles, and constraints have no Mutant Tools wrapper to prefer —
`kinematics.py` itself builds those with raw `cmds.joint`/`cmds.ikHandle`/
`cmds.*Constraint`, so `maya_create_joint`/`maya_create_ik_handle`/
`maya_create_constraint` below are already at that level.

### Typed scene-editing tools

Beyond `maya_execute`/`maya_query`, the bridge exposes typed tools for common
rig-building operations, each validated before it touches Maya rather than
relying on a raw script:

- **Attributes**: `maya_get_attr`, `maya_set_attr` (locked/connected/wrong-type
  attributes fail with a clear validation error, not a Python traceback).
- **Connections**: `maya_list_connections`, `maya_connection_history`,
  `maya_connect_attrs`, `maya_disconnect_attrs`.
- **Nodes**: `maya_create_node`, `maya_delete_node`, `maya_rename_node`,
  `maya_parent_node`, `maya_duplicate_node`.
- **Components**: `maya_convert_components` (vertex/edge/face/UV, selects the result).
- **Skinning**: `maya_skin_bind`, `maya_skin_unbind`, `maya_skin_influences`,
  `maya_skin_weights_get`, `maya_skin_weights_set`, `maya_skin_copy_weights`.
- **Joints & constraints**: `maya_create_joint`, `maya_orient_joint`,
  `maya_create_ik_handle`, `maya_create_constraint` (parent/point/orient/scale/aim),
  `maya_list_constraints`, `maya_delete_constraint`.

Every tool carries MCP annotations (`readOnlyHint`/`destructiveHint`/
`idempotentHint`) so a client can decide when to ask for confirmation —
`maya_delete_node`, `maya_skin_bind/unbind`, and `maya_delete_constraint` are
marked destructive. Failed calls carry `error_type`: `"validation"` for bad
input caught before Maya was touched, `"maya_command"` for an exception Maya
itself raised.

## Long work

Normal calls have a 30-second response deadline. Python/MEL execution accepts
`timeout` up to 3600 seconds. For anything likely to exceed the MCP client's
tool deadline, use `background=True` and poll `maya_job_status(job_id=...)`:

```text
maya_execute(code="result = build_rig()", port=7501, timeout=600, background=True)
maya_job_status(job_id="<returned id>")
```

The sidecar waits on a worker thread; Maya work still executes on Maya's main
thread. Polling works while Maya is busy. Jobs are scoped to this sidecar,
limited to 100, and completed jobs become eligible for cleanup after an hour.
`forget=True` removes a completed job after returning its result.

Timeout/disconnection after sending returns `status="unknown"`: the operation
may still be running or may have completed. **Do not automatically retry.**
Connection failure before sending returns `status="not_sent"`. No operation is
forcibly cancelled. Restarting the sidecar loses job tracking and does not stop
Maya execution. Keep it running until jobs finish.

## Changing the port range

The listener scans ports starting at 7501 (see `_DEFAULT_PORT` in
`maya_listener.py`). Multiple Maya sessions each get their own port
automatically; pass `port=` explicitly to any tool once more than one
session is registered.
