"""Mutant Tools MCP server — model-independent, standard stdio transport."""

from __future__ import annotations

import json
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

from mcp.server.mcpserver import MCPServer, Image
from mcp.types import ToolAnnotations

try:
    from . import bridge_transport as client
except ImportError:
    import bridge_transport as client

_bridge_call = client.bridge_call


def _ann(read_only, destructive, idempotent):
    """Shorthand for the risk annotations MCP clients use to gate confirmation."""
    return ToolAnnotations(
        readOnlyHint=read_only,
        destructiveHint=destructive,
        idempotentHint=idempotent,
        openWorldHint=False,
    )

# Jobs live in this sidecar process. Use durable jobs only if restart recovery is needed.
_EXECUTOR = ThreadPoolExecutor(max_workers=4, thread_name_prefix="mutant-mcp")
_JOBS = {}
_JOBS_LOCK = threading.Lock()


def _execute(code, port, timeout, background):
    if not background:
        return _bridge_call("exec", port=port, timeout=timeout, code=code)
    try:
        client.validate_timeout(timeout)
        port = client.resolve_port(port)
    except (OSError, ValueError) as exc:
        return {"success": False, "status": "not_sent", "error": str(exc)}
    with _JOBS_LOCK:
        # Bound memory; never discard a pending job.
        for job_id, job in list(_JOBS.items()):
            if job["future"].done() and time.monotonic() - job["created"] > 3600:
                del _JOBS[job_id]
        if len(_JOBS) >= 100:
            return {
                "success": False,
                "status": "not_sent",
                "error": "Job limit reached; forget completed jobs.",
            }
        job_id = uuid.uuid4().hex
        future = _EXECUTOR.submit(
            _bridge_call, "exec", port=port, timeout=timeout, code=code
        )
        _JOBS[job_id] = {"future": future, "port": port, "created": time.monotonic()}
    return {"success": True, "status": "submitted", "job_id": job_id, "port": port}


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = MCPServer(
    "mutant-maya",
    log_level="WARNING",
    instructions=(
        "Mutant Tools Maya bridge — provides tools to interact with a running "
        "Autodesk Maya session running Mutant Tools rigging. Prefer the typed "
        "tools over maya_execute/maya_query/maya_execute_mel, which run "
        "arbitrary code and should be reserved for anything a typed tool does "
        "not cover. For rig-building specifically, prefer the Mutant Tools "
        "commands (maya_create_control, maya_add_root_group, maya_assign_color* "
        "maya_hide_attr, maya_match_transform, maya_create_ikfk_switch, "
        "maya_add_attr, maya_connect_rotate_order, maya_lock_node, "
        "maya_mirror_group) over the generic node/attribute/joint/constraint "
        "tools when both could do the job — they call Mutant Tools' own "
        "Utils/Rigging commands, so naming and conventions stay consistent "
        "with the rest of the rig instead of being reimplemented ad hoc. Use "
        "the generic tools for anything Mutant Tools' commands don't cover. "
        "Use these tools to inspect scene objects and query Mutant Tools rig "
        "blocks/controllers. The bridge communicates with Maya's commandPort "
        "over localhost TCP. List sessions first; when several are open, pass "
        "port on every scene tool. Use maya_capture for visual checks. For "
        "long Python/MEL work use background=True and poll maya_job_status. A "
        "timeout does not cancel execution; never automatically retry a "
        "mutation. A failed call carries error_type: 'validation' for bad "
        "input caught before Maya was touched, 'maya_command' for an "
        "exception Maya itself raised."
    ),
)


# --- Core Execution ---


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_job_status(job_id: str, forget: bool = False) -> str:
    """Poll a background job without calling Maya, even while its UI is busy.

    Completed jobs become eligible for cleanup after an hour. A sidecar restart
    loses tracking, not necessarily Maya execution. `forget` removes only a
    finished job after returning its result. No tool forcibly cancels Maya.
    """
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
        if job is None:
            return json.dumps(
                {
                    "success": False,
                    "status": "unknown",
                    "error": "Unknown or expired job; do not automatically resubmit.",
                }
            )
        future = job["future"]
        result = {"success": True, "job_id": job_id, "port": job["port"]}
        if not future.done():
            result["status"] = "waiting_for_maya" if future.running() else "queued"
        else:
            try:
                response = future.result()
            except Exception as exc:
                response = {"success": False, "status": "unknown", "error": str(exc)}
            result.update(
                success=response.get("success", False),
                status=response.get(
                    "status", "completed" if response.get("success") else "failed"
                ),
                response=response,
            )
            if forget:
                del _JOBS[job_id]
        return json.dumps(result)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_capture(
    target: Literal["viewport", "window"] = "viewport",
    width: int = 1280,
    height: int = 720,
    panel: str = "",
    window: str = "",
    port: int | None = None,
) -> Image:
    """Return a PNG image for visual inspection (not a base64 text dump).

    target=viewport captures the current frame, optionally from a named model
    panel. target=window captures Maya's main window, or a visible Qt window
    identified by its exact objectName/title. Floating windows need their own
    capture. Width/height bound image size (64..4096). No scene save is performed.
    """
    response = _bridge_call(
        "capture",
        port=port,
        target=target,
        width=width,
        height=height,
        panel=panel,
        window=window,
    )
    if not response.get("success"):
        raise RuntimeError(json.dumps(response))
    path = Path(response["result"]["path"])
    try:
        return Image(data=path.read_bytes(), format="png")
    finally:
        path.unlink(missing_ok=True)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_list_sessions() -> str:
    """List all running Maya sessions discovered from lockfiles.

    Returns:
        JSON with the list of sessions (port, pid, started, scene).
    """
    return json.dumps({"success": True, "sessions": client.list_sessions()})


@mcp.tool(annotations=_ann(read_only=False, destructive=True, idempotent=False))
def maya_execute(
    code: str, port: int | None = None, timeout: float = 30, background: bool = False
) -> str:
    """Execute arbitrary Python code in Maya and return structured results.

    The code has access to `cmds` (maya.cmds), `mel` (maya.mel), and `om`
    (maya.OpenMaya) in the execution namespace. Assign `result` to return data.
    For long work use background=True, timeout up to 3600, then maya_job_status.
    A timeout does not cancel Maya execution; never blindly retry a mutation.

    Args:
        code: Python code to execute in Maya.
        port: Optional specific port/session to target (e.g., 7501).
        timeout: Maximum reply wait in seconds, up to 3600.
        background: Return a job ID immediately instead of waiting for Maya.

    Returns:
        JSON with: success, result, stdout (captured prints), stderr, traceback.
    """
    result = _execute(code, port, timeout, background)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_query(code: str, port: int | None = None, timeout: float = 30) -> str:
    """Execute a Python expression in Maya and return its value.

    Use this for simple queries like `cmds.ls(sl=True)` or `cmds.getAttr('node.attr')`.
    The expression is eval'd so it must return a value.

    Args:
        code: Python expression to evaluate in Maya.
        port: Optional specific port/session to target (e.g., 7501).
        timeout: Maximum reply wait in seconds; use background execution for long work.

    Returns:
        JSON with: success, result (the evaluated value), stdout, stderr, traceback.
    """
    result = _bridge_call("query", port=port, code=code, timeout=timeout)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=True, idempotent=False))
def maya_execute_mel(
    mel_command: str,
    port: int | None = None,
    timeout: float = 30,
    background: bool = False,
) -> str:
    """Execute MEL; use background=True and maya_job_status for long operations.

    Args:
        mel_command: MEL command string to execute.
        port: Optional specific port/session to target (e.g., 7501).
        timeout: Maximum reply wait in seconds, up to 3600.
        background: Return a job ID immediately instead of waiting for Maya.

    Returns:
        JSON with: success, result, stdout, stderr, traceback.
    """
    code = "mel.eval({})".format(json.dumps(mel_command))
    result = _execute(code, port, timeout, background)
    return json.dumps(result, indent=2)


# --- Scene Inspection ---


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_scene_info(port: int | None = None) -> str:
    """Get scene metadata: filename, path, FPS, frame range, units, modified state.

    Args:
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with scene information.
    """
    result = _bridge_call("scene_info", port=port)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_list_nodes(
    type: str = "", pattern: str = "", limit: int = 500, port: int | None = None
) -> str:
    """List Maya nodes filtered by type and/or name pattern.

    Args:
        type: Node type filter (e.g., 'transform', 'mesh', 'joint').
        pattern: Name pattern with wildcards (e.g., 'L_*_Ctrl').
        limit: Maximum number of nodes to return (default 500).
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with node list, count, and truncation status.
    """
    params = {"limit": limit}
    if type:
        params["type"] = type
    if pattern:
        params["pattern"] = pattern
    result = _bridge_call("list_nodes", port=port, **params)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_node_info(node: str, port: int | None = None) -> str:
    """Get detailed information about a specific Maya node.

    Returns the node's type, parent, children, shapes, and all user-defined
    attributes with their values, types, lock state, and connections.

    Args:
        node: Name of the node to inspect.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with full node details.
    """
    result = _bridge_call("node_info", port=port, node=node)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_selection(select: str | None = None, port: int | None = None) -> str:
    """Get or set the current Maya selection.

    Call with no arguments to get the current selection.
    Pass a node name or comma-separated list to set selection.
    Pass empty string '' to clear selection.

    Args:
        select: Omit to query; empty string clears selection.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with current selection list and count.
    """
    params = {}
    if select is not None:
        if "," in select:
            params["select"] = [s.strip() for s in select.split(",")]
        else:
            params["select"] = select
    result = _bridge_call("selection", port=port, **params)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_scene_tree(root: str = "", depth: int = 4, port: int | None = None) -> str:
    """Get the scene hierarchy as a tree structure.

    Args:
        root: Root node to start from (empty = all top-level transforms).
        depth: Maximum tree depth to traverse (default 4).

    Returns:
        JSON tree with node names, types, and children.
    """
    params = {"depth": depth}
    if root:
        params["root"] = root
    result = _bridge_call("scene_tree", port=port, **params)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_list_references(port: int | None = None) -> str:
    """List all file references in the scene.

    Returns:
        JSON with reference paths, namespaces, and load status.
    """
    result = _bridge_call("list_references", port=port)
    return json.dumps(result, indent=2)


# --- Rigging / Mutant Tools Awareness ---


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_list_blocks(port: int | None = None) -> str:
    """List all Mutant Tools rig blocks in the scene, with their config attributes.

    Block/controller naming comes from Mutant Tools' own
    Config/name_conventions.json, not a hardcoded suffix.

    Returns:
        JSON with block names and their configuration values.
    """
    result = _bridge_call("list_blocks", port=port)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_block_info(block: str, port: int | None = None) -> str:
    """Get full configuration for a specific Mutant Tools rig block.

    Args:
        block: Name of the block node (e.g., 'L_Arm_Block').

    Returns:
        JSON with block config, children, and config node details.
    """
    result = _bridge_call("block_info", port=port, block=block)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_list_controllers(
    pattern: str = "", limit: int = 200, port: int | None = None
) -> str:
    """List all rig controllers with color and parent info.

    Args:
        pattern: Optional regex or substring filter for controller names.
        limit: Maximum controllers to return (default 200).

    Returns:
        JSON with controller list, colors, and parents.
    """
    params = {"limit": limit}
    if pattern:
        params["pattern"] = pattern
    result = _bridge_call("list_controllers", port=port, **params)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_rig_structure(root: str = "", depth: int = 4, port: int | None = None) -> str:
    """Get one or more rig hierarchy trees.

    With no root, finds top-level assemblies that contain at least one rig
    block and returns a tree per assembly (Mutant Tools does not fix a single
    rig-root group name).

    Args:
        root: Root transform to start from (empty = auto-detect rig roots).
        depth: Maximum tree depth (default 4).

    Returns:
        JSON tree (or list of trees) of the rig structure.
    """
    params = {"depth": depth}
    if root:
        params["root"] = root
    result = _bridge_call("rig_structure", port=port, **params)
    return json.dumps(result, indent=2)


# --- Attributes ---


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_get_attr(node: str, attr: str, port: int | None = None) -> str:
    """Get the value of a single attribute.

    Args:
        node: Name of the node.
        attr: Short attribute name (e.g., 'translateX').
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: value, type, locked, source (incoming connection, if any).
    """
    result = _bridge_call("get_attr", port=port, node=node, attr=attr)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_set_attr(
    node: str,
    attr: str,
    value: float | int | str | bool | list[float],
    port: int | None = None,
) -> str:
    """Set the value of a single attribute.

    The value is coerced to the attribute's existing type (numeric, string,
    bool, or a 3-number compound like translate/rotate/scale). Locked or
    connected attributes fail with a validation error rather than silently
    breaking the connection.

    Args:
        node: Name of the node.
        attr: Short attribute name (e.g., 'translateX').
        value: New value — number, string, bool, or a 3-item list for compound attrs.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: value (as read back after the set).
    """
    result = _bridge_call("set_attr", port=port, node=node, attr=attr, value=value)
    return json.dumps(result, indent=2)


# --- Connections ---


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_list_connections(
    node: str,
    attr: str = "",
    source: bool = True,
    destination: bool = True,
    port: int | None = None,
) -> str:
    """List DG connections into and/or out of a node or plug.

    Args:
        node: Node name, or 'node.attr' to scope to one plug.
        attr: Optional attribute name (alternative to 'node.attr' in node).
        source: Include incoming connections.
        destination: Include outgoing connections.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with a list of {plug, connected_to, direction}.
    """
    result = _bridge_call(
        "list_connections",
        port=port,
        node=node,
        attr=attr,
        source=source,
        destination=destination,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_connection_history(node: str, limit: int = 500, port: int | None = None) -> str:
    """List a node's construction history (upstream DG nodes).

    Args:
        node: Name of the node.
        limit: Maximum history nodes to return (default 500).
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with node list, count, and truncation status.
    """
    result = _bridge_call("connection_history", port=port, node=node, limit=limit)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_connect_attrs(
    source: str, destination: str, force: bool = False, port: int | None = None
) -> str:
    """Connect one attribute plug to another.

    Args:
        source: Source plug, e.g. 'L_Arm_Ctrl.rotateX'.
        destination: Destination plug, e.g. 'L_Arm_Jnt.rotateX'.
        force: Break an existing connection into destination if one exists.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: source, destination.
    """
    result = _bridge_call(
        "connect_attrs", port=port, source=source, destination=destination, force=force
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_disconnect_attrs(source: str, destination: str, port: int | None = None) -> str:
    """Disconnect one attribute plug from another.

    Args:
        source: Source plug, e.g. 'L_Arm_Ctrl.rotateX'.
        destination: Destination plug, e.g. 'L_Arm_Jnt.rotateX'.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: source, destination.
    """
    result = _bridge_call(
        "disconnect_attrs", port=port, source=source, destination=destination
    )
    return json.dumps(result, indent=2)


# --- Nodes (typed CRUD) ---


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_create_node(
    node_type: str, name: str = "", parent: str = "", port: int | None = None
) -> str:
    """Create a new dependency-graph or DAG node.

    Args:
        node_type: Maya node type, e.g. 'joint', 'transform', 'multiplyDivide'.
        name: Optional name for the new node.
        parent: Optional transform to parent a DAG node under.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: node (the resulting node name).
    """
    result = _bridge_call(
        "create_node", port=port, node_type=node_type, name=name, parent=parent
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=True, idempotent=False))
def maya_delete_node(node: str, port: int | None = None) -> str:
    """Delete one or more nodes. Comma-separate for more than one.

    Args:
        node: Node name, or comma-separated list of node names.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: deleted (the list of node names that were removed).
    """
    result = _bridge_call("delete_node", port=port, node=node)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_rename_node(node: str, new_name: str, port: int | None = None) -> str:
    """Rename a node.

    Args:
        node: Current name of the node.
        new_name: New name for the node.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: node (the new name, which may differ if Maya deduplicated it).
    """
    result = _bridge_call("rename_node", port=port, node=node, new_name=new_name)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_parent_node(
    node: str, parent: str = "", world: bool = False, port: int | None = None
) -> str:
    """Reparent a transform under another transform, or to world.

    Args:
        node: Node name, or comma-separated list of node names.
        parent: Transform to parent under. Ignored if world=True.
        world: Parent to world space instead.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: node (resulting full path(s)).
    """
    result = _bridge_call(
        "parent_node", port=port, node=node, parent=parent, world=world
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_duplicate_node(node: str, name: str = "", port: int | None = None) -> str:
    """Duplicate a node (shallow — no input connections).

    Args:
        node: Name of the node to duplicate.
        name: Optional name for the duplicate.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: node (the new node's name).
    """
    result = _bridge_call("duplicate_node", port=port, node=node, name=name)
    return json.dumps(result, indent=2)


# --- Components ---


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_convert_components(
    components: str,
    to: Literal["vertex", "edge", "face", "uv"] = "vertex",
    port: int | None = None,
) -> str:
    """Convert a component selection to another component type, and select it.

    Args:
        components: Component name(s), e.g. 'pCube1.f[0]' or comma-separated list.
        to: Target component type.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: selection (converted component names), count.
    """
    comps = [c.strip() for c in components.split(",")] if "," in components else components
    result = _bridge_call("convert_components", port=port, components=comps, to=to)
    return json.dumps(result, indent=2)


# --- Skinning ---


@mcp.tool(annotations=_ann(read_only=False, destructive=True, idempotent=False))
def maya_skin_bind(
    mesh: str,
    joints: str,
    bind_method: Literal[
        "closestDistance", "closestInHierarchy", "heatMap", "geodesicVoxel"
    ] = "closestDistance",
    skin_method: Literal["classicLinear", "dualQuaternion", "blend"] = "classicLinear",
    max_influences: int = 4,
    name: str = "",
    port: int | None = None,
) -> str:
    """Bind a mesh to a joint chain with a new skinCluster.

    Args:
        mesh: Name of the mesh (or transform) to bind.
        joints: Comma-separated list of joint names to use as influences.
        bind_method: Initial-weight algorithm.
        skin_method: Skinning deformation algorithm.
        max_influences: Maximum influences per vertex.
        name: Optional name for the skinCluster node.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: skin_cluster, influences, influence_count.
    """
    joint_list = [j.strip() for j in joints.split(",")]
    result = _bridge_call(
        "skin_bind",
        port=port,
        mesh=mesh,
        joints=joint_list,
        bind_method=bind_method,
        skin_method=skin_method,
        max_influences=max_influences,
        name=name,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=True, idempotent=False))
def maya_skin_unbind(mesh: str, port: int | None = None) -> str:
    """Remove the skinCluster from a mesh.

    Args:
        mesh: Name of the bound mesh.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: skin_cluster (the removed node's name).
    """
    result = _bridge_call("skin_unbind", port=port, mesh=mesh)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_skin_influences(mesh: str, port: int | None = None) -> str:
    """List the influence joints on a mesh's skinCluster.

    Args:
        mesh: Name of the bound mesh.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: skin_cluster, influences (list of joint names).
    """
    result = _bridge_call("skin_influences", port=port, mesh=mesh)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_skin_weights_get(
    mesh: str, vertices: str = "", limit: int = 100, port: int | None = None
) -> str:
    """Get per-vertex skin weights.

    Args:
        mesh: Name of the bound mesh.
        vertices: Comma-separated vertex component names (e.g. 'pCube1.vtx[0]').
            Empty means all vertices, bounded by limit.
        limit: Maximum vertices to return (default 100).
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: skin_cluster, weights ({vertex: {joint: weight}}), truncated.
    """
    vertex_list = [v.strip() for v in vertices.split(",")] if vertices else []
    result = _bridge_call(
        "skin_weights_get", port=port, mesh=mesh, vertices=vertex_list, limit=limit
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_skin_weights_set(
    mesh: str,
    vertex: str,
    weights: dict[str, float],
    normalize: bool = True,
    port: int | None = None,
) -> str:
    """Set skin weights for a single vertex.

    Args:
        mesh: Name of the bound mesh.
        vertex: Single vertex component name, e.g. 'pCube1.vtx[0]'.
        weights: Map of joint name to weight value.
        normalize: Let Maya rebalance the remaining influences to sum to 1.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: vertex, weights (as read back after the set).
    """
    result = _bridge_call(
        "skin_weights_set",
        port=port,
        mesh=mesh,
        vertex=vertex,
        weights=weights,
        normalize=normalize,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_skin_copy_weights(
    source_mesh: str,
    dest_mesh: str,
    surface_association: Literal[
        "closestPoint", "rayCast", "closestComponent"
    ] = "closestPoint",
    influence_association: Literal[
        "oneToOne", "name", "closestJoint"
    ] = "oneToOne",
    port: int | None = None,
) -> str:
    """Copy skin weights from one bound mesh to another bound mesh.

    Both meshes must already have a skinCluster (bind dest_mesh first, e.g.
    to the same joints, if it has none).

    Args:
        source_mesh: Name of the bound source mesh.
        dest_mesh: Name of the bound destination mesh.
        surface_association: How source points map to destination points.
        influence_association: How source influences map to destination influences.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: source_skin_cluster, dest_skin_cluster.
    """
    result = _bridge_call(
        "skin_copy_weights",
        port=port,
        source_mesh=source_mesh,
        dest_mesh=dest_mesh,
        surface_association=surface_association,
        influence_association=influence_association,
    )
    return json.dumps(result, indent=2)


# --- Joints & Constraints ---


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_create_joint(
    name: str = "",
    position: list[float] | None = None,
    parent: str = "",
    radius: float = 1.0,
    port: int | None = None,
) -> str:
    """Create a single joint.

    Selection is cleared first, so the joint never auto-parents onto whatever
    happened to be selected in Maya. Pass parent explicitly to place it in a chain.

    Args:
        name: Optional name for the joint.
        position: Optional [x, y, z] world-space position (default origin).
        parent: Optional transform/joint to parent this joint under.
        radius: Joint display radius.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: joint (the resulting node name).
    """
    result = _bridge_call(
        "create_joint",
        port=port,
        name=name,
        position=position or [0.0, 0.0, 0.0],
        parent=parent,
        radius=radius,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_orient_joint(
    joints: str,
    aim_axis: str = "xyz",
    up_axis: str = "yup",
    zero_scale_orient: bool = True,
    port: int | None = None,
) -> str:
    """Orient one or more joints using Maya's standard joint-orient algorithm.

    Args:
        joints: Comma-separated list of joint names, in the order to orient.
        aim_axis: Primary (aim) axis order, e.g. 'xyz'.
        up_axis: Secondary axis orientation, e.g. 'yup', 'zup', 'none'.
        zero_scale_orient: Zero out scale orient after orienting.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: joints (the list that was oriented).
    """
    joint_list = [j.strip() for j in joints.split(",")]
    result = _bridge_call(
        "orient_joint",
        port=port,
        joints=joint_list,
        aim_axis=aim_axis,
        up_axis=up_axis,
        zero_scale_orient=zero_scale_orient,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_create_ik_handle(
    start_joint: str,
    end_joint: str,
    solver: Literal["ikRPsolver", "ikSCsolver", "ikSplineSolver"] = "ikRPsolver",
    name: str = "",
    port: int | None = None,
) -> str:
    """Create an IK handle across a joint chain.

    Args:
        start_joint: First joint in the chain.
        end_joint: Last joint (effector) in the chain.
        solver: IK solver type.
        name: Optional name for the IK handle.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: ik_handle, effector.
    """
    result = _bridge_call(
        "create_ik_handle",
        port=port,
        start_joint=start_joint,
        end_joint=end_joint,
        solver=solver,
        name=name,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_create_constraint(
    type: Literal["parent", "point", "orient", "scale", "aim"],
    drivers: str,
    driven: str,
    maintain_offset: bool = True,
    name: str = "",
    port: int | None = None,
) -> str:
    """Create a constraint driving one transform from one or more others.

    Args:
        type: Constraint type.
        drivers: Comma-separated list of driver (target) transform names.
        driven: Transform to be constrained.
        maintain_offset: Preserve driven's current position/orientation as an offset.
        name: Optional name for the constraint node.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: constraint (the resulting node name).
    """
    driver_list = [d.strip() for d in drivers.split(",")]
    result = _bridge_call(
        "create_constraint",
        port=port,
        type=type,
        drivers=driver_list,
        driven=driven,
        maintain_offset=maintain_offset,
        name=name,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_list_constraints(node: str, port: int | None = None) -> str:
    """List constraint nodes driving a transform.

    Args:
        node: Name of the constrained transform.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: constraints (list of {name, type, drivers}).
    """
    result = _bridge_call("list_constraints", port=port, node=node)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=True, idempotent=False))
def maya_delete_constraint(constraint: str, port: int | None = None) -> str:
    """Delete a constraint node.

    Args:
        constraint: Name of the constraint node (must be a *Constraint node type).
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: deleted (the constraint node name).
    """
    result = _bridge_call("delete_constraint", port=port, constraint=constraint)
    return json.dumps(result, indent=2)


# --- Mutant Tools' own rig-building commands (Utils/Rigging) ---
#
# These call mt.<method>() from tools.py/kinematics.py rather than
# reimplementing the same operation with raw cmds, so naming, color, and
# control-building stay driven by Mutant Tools' own conventions.


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_create_control(
    name: str,
    node: str = "",
    shape: str = "cube",
    color: str = "",
    size: float = 1.0,
    gimbal: bool = True,
    world: bool = True,
    port: int | None = None,
) -> str:
    """Create a rig controller via Mutant Tools' mt.controller().

    Builds a curve-shape control (see maya_list_control_shapes), snapped onto
    node if given, with an offset root group and optional world/gimbal sub-controls.

    Args:
        name: Name for the controller (suffixed with the ctrl naming convention).
        node: Optional transform to snap the controller onto (default: world origin).
        shape: Curve shape name from Config/curves.json.
        color: Override color name (default: Mutant Tools' configured main_color).
        size: Uniform scale for the control curve.
        gimbal: Create a gimbal sub-controller.
        world: Create a world-oriented sub-controller.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: ctrl, root, world, gimbal (node names; world/gimbal False if not created).
    """
    result = _bridge_call(
        "create_control",
        port=port,
        node=node,
        name=name,
        shape=shape,
        color=color,
        size=size,
        gimbal=gimbal,
        world=world,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_list_control_shapes(port: int | None = None) -> str:
    """List curve shape names available to maya_create_control (Config/curves.json).

    Args:
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: shapes (list of shape names).
    """
    result = _bridge_call("list_control_shapes", port=port)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_add_root_group(
    node: str,
    custom_name: str = "",
    auto_root: bool = False,
    replace_naming: bool = False,
    port: int | None = None,
) -> str:
    """Create an offset (or root+auto) group above a node via mt.root_grp().

    Args:
        node: Transform to add the group(s) above.
        custom_name: Use this name instead of the offset naming convention.
        auto_root: Create two groups (root + auto) instead of one offset group.
        replace_naming: Strip ctrl/joint naming-convention suffixes from the new group's name.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: groups (list of new group names, in parent-to-child order).
    """
    result = _bridge_call(
        "root_group",
        port=port,
        node=node,
        custom_name=custom_name,
        auto_root=auto_root,
        replace_naming=replace_naming,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_assign_color(
    nodes: str, color: str = "", smart: bool = False, port: int | None = None
) -> str:
    """Assign a named override color via mt.assign_color() or mt.smart_assign_color().

    Args:
        nodes: Comma-separated node names.
        color: Color name (red, blue, white, purple, green, lightBlue, yellow,
            pink, grey, orange). Ignored if smart=True.
        smart: Auto-pick color from the node's L_/R_/C_ naming prefix instead.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: nodes.
    """
    node_list = [n.strip() for n in nodes.split(",")]
    result = _bridge_call(
        "assign_color", port=port, nodes=node_list, color=color, smart=smart
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_assign_color_rgb(
    nodes: str, color: list[float], hsv: bool = False, port: int | None = None
) -> str:
    """Assign an exact RGB (or HSV) override color via mt.assign_color_rgb().

    Args:
        nodes: Comma-separated node names.
        color: [r, g, b] in 0..1 (or [h, s, v] in 0..1 if hsv=True).
        hsv: Treat color as HSV instead of RGB.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: nodes.
    """
    node_list = [n.strip() for n in nodes.split(",")]
    result = _bridge_call(
        "assign_color_rgb", port=port, nodes=node_list, color=color, hsv=hsv
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_hide_attr(
    nodes: str,
    translate: bool = False,
    rotate: bool = False,
    scale: bool = False,
    visibility: bool = False,
    rotate_order: bool = False,
    show: bool = False,
    port: int | None = None,
) -> str:
    """Hide and lock channel-box attributes via mt.hide_attr().

    Args:
        nodes: Comma-separated node names.
        translate: Hide/lock translateX/Y/Z.
        rotate: Hide/lock rotateX/Y/Z (and RotateOrder, if present).
        scale: Hide/lock scaleX/Y/Z.
        visibility: Hide/lock visibility.
        rotate_order: Hide/lock RotateOrder specifically.
        show: Show and unlock every standard transform attribute instead.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: nodes.
    """
    node_list = [n.strip() for n in nodes.split(",")]
    result = _bridge_call(
        "hide_attr",
        port=port,
        nodes=node_list,
        translate=translate,
        rotate=rotate,
        scale=scale,
        visibility=visibility,
        rotate_order=rotate_order,
        show=show,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_match_transform(
    this: str,
    that: str,
    translate: bool = True,
    rotate: bool = True,
    scale: bool = True,
    port: int | None = None,
) -> str:
    """Snap one transform onto another via mt.match() (constrain, then delete).

    Args:
        this: Transform to move.
        that: Transform with the desired position/rotation/scale.
        translate: Match translation.
        rotate: Match rotation.
        scale: Match scale.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: this, that.
    """
    result = _bridge_call(
        "match_transform",
        port=port,
        this=this,
        that=that,
        translate=translate,
        rotate=rotate,
        scale=scale,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_create_ikfk_switch(
    ik: str,
    fk: str,
    main: str,
    attr: str,
    mode: Literal["constraint", "blend"] = "constraint",
    port: int | None = None,
) -> str:
    """Wire an IK/FK switch onto a main joint via Mutant Tools' switch commands.

    mode="constraint" uses mt.switch_constraints() (parent+scale constraint pair
    driven by a reverse node). mode="blend" uses mt.switch_blend_colors()
    (blendColors nodes per translate/rotate/scale). Either way, attr=0 favors
    ik/that... check the resulting node's weight connections if the direction
    matters for your rig.

    Args:
        ik: IK transform (driver 1).
        fk: FK transform (driver 2).
        main: Transform actually driven — typically the bind joint.
        attr: Existing 0..1 attribute to use as the switch (create with maya_add_attr first).
        mode: 'constraint' or 'blend'.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: ik, fk, main, attr, mode.
    """
    result = _bridge_call(
        "ikfk_switch", port=port, ik=ik, fk=fk, main=main, attr=attr, mode=mode
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_add_attr(
    node: str,
    name: str,
    kind: Literal["float", "int", "enum", "bool"] = "float",
    min: float = 0,
    max: float = 1,
    default: float = 0,
    enums: str = "",
    keyable: bool = True,
    port: int | None = None,
) -> str:
    """Add a custom attribute via Mutant Tools' new_attr/new_attr_interger/new_enum/new_boolean.

    Args:
        node: Transform to add the attribute to.
        name: Name of the new attribute.
        kind: 'float' (double), 'int' (long), 'enum', or 'bool'.
        min: Minimum value (float/int kinds only).
        max: Maximum value (float/int kinds only).
        default: Default value. For kind='enum' this is the default option's index.
        enums: Colon-separated option names, required for kind='enum' (e.g. 'IK:FK').
        keyable: Keyable in the channel box (float/enum kinds only).
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: attr (the new 'node.attr' name).
    """
    result = _bridge_call(
        "add_attr",
        port=port,
        node=node,
        name=name,
        kind=kind,
        min=min,
        max=max,
        default=default,
        enums=enums,
        keyable=keyable,
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_connect_rotate_order(nodes: str, driver: str, port: int | None = None) -> str:
    """Connect nodes' rotateOrder to a shared driver attribute via mt.connect_rotate_order().

    Creates a RotateOrder enum attribute on driver if it doesn't already have one.

    Args:
        nodes: Comma-separated node names whose rotateOrder should follow driver.
        driver: Node to hold the shared RotateOrder attribute (often a controller).
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: attr (the driver's 'node.RotateOrder' plug), nodes.
    """
    node_list = [n.strip() for n in nodes.split(",")]
    result = _bridge_call(
        "connect_rotate_order", port=port, nodes=node_list, driver=driver
    )
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=True))
def maya_lock_node(nodes: str, unlock: bool = False, port: int | None = None) -> str:
    """Lock or unlock nodes (Maya's node-level lock, not attribute lock) via mt.lock_node().

    Args:
        nodes: Comma-separated node names.
        unlock: Unlock instead of lock.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: nodes, unlock.
    """
    node_list = [n.strip() for n in nodes.split(",")]
    result = _bridge_call("lock_node", port=port, nodes=node_list, unlock=unlock)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_mirror_group(node: str, world: bool = True, port: int | None = None) -> str:
    """Create a negative-scale mirror group above a node via mt.mirror_group().

    Parents node under a new group with scale -1/-1/-1 and rotateX 180 — the
    classic Maya mirror-by-negative-scale trick, not a mirrored duplicate.

    Args:
        node: Transform to mirror.
        world: Align the mirror group to the world origin instead of node's current position.
        port: Optional specific port/session to target (e.g., 7501).

    Returns:
        JSON with: mirror_group (the new group's name).
    """
    result = _bridge_call("mirror_group", port=port, node=node, world=world)
    return json.dumps(result, indent=2)


# --- Debugging ---


@mcp.tool(annotations=_ann(read_only=False, destructive=False, idempotent=False))
def maya_inspect_variable(expression: str, port: int | None = None) -> str:
    """Evaluate a Python expression in Maya and return its value, type, and repr.

    Use this to inspect variables, check attribute values, or evaluate
    conditions in the running Maya session.

    Args:
        expression: Python expression to evaluate (e.g., 'cmds.ls(sl=True)').

    Returns:
        JSON with value, type, and repr of the result.
    """
    result = _bridge_call("inspect_variable", port=port, expression=expression)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_check_errors(port: int | None = None) -> str:
    """Check the Maya scene for common problems.

    Scans for: duplicate node names, unknown nodes, unknown plugins,
    and broken references.

    Returns:
        JSON with issue list, severity levels, and health status.
    """
    result = _bridge_call("check_errors", port=port)
    return json.dumps(result, indent=2)


@mcp.tool(annotations=_ann(read_only=True, destructive=False, idempotent=True))
def maya_ping(port: int | None = None) -> str:
    """Check if Maya is running and the bridge is connected.

    Returns:
        JSON with Maya version, scene name, port, and PID.
    """
    try:
        result = _bridge_call("ping", port=port)
        return json.dumps(result, indent=2)
    except ConnectionError as e:
        return json.dumps({"success": False, "error": str(e)}, indent=2)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(
        "Mutant MCP: {} registered session(s).".format(len(client.list_sessions())),
        file=sys.stderr,
    )
    mcp.run(transport="stdio")
