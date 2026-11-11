"""
Static checks for the Maya MCP bridge (runs outside Maya, no mcp package needed).

Every action the MCP server sends must have a handler in the Maya listener,
and every helper action must call a function that exists in its module.

Run from the Mutant_Tools root:
    python -m pytest Tests/test_maya_mcp_actions.py -v
    python Tests/test_maya_mcp_actions.py
"""
import ast
import unittest
from pathlib import Path

MCP_DIR = Path(__file__).resolve().parents[1] / 'Dev' / 'MayaMCP'


def _tree(name):
    return ast.parse((MCP_DIR / name).read_text())


def _server_actions():
    """Actions the server sends: first argument of every _bridge_call("...")."""
    found = set()
    for node in ast.walk(_tree('mcp_server.py')):
        if (isinstance(node, ast.Call) and getattr(node.func, 'id', None) == '_bridge_call'
                and node.args and isinstance(node.args[0], ast.Constant)):
            found.add(node.args[0].value)
    return found


def _dispatch_table():
    """{action: handler name} from bridge_dispatch's dispatch_table literal."""
    for node in ast.walk(_tree('maya_listener.py')):
        if (isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == 'dispatch_table' for t in node.targets)
                and isinstance(node.value, ast.Dict)):
            return {k.value: v.id for k, v in zip(node.value.keys, node.value.values)}
    raise AssertionError('dispatch_table not found')


def _functions(name):
    return {n.name for n in ast.walk(_tree(name)) if isinstance(n, ast.FunctionDef)}


class TestBridgeActions(unittest.TestCase):

    def test_every_server_action_has_a_handler(self):
        missing = _server_actions() - set(_dispatch_table())
        self.assertFalse(missing, 'server sends actions the listener does not handle: {}'.format(missing))

    def test_every_handler_is_defined(self):
        defined = _functions('maya_listener.py')
        missing = {a: h for a, h in _dispatch_table().items() if h not in defined}
        self.assertFalse(missing, 'dispatch_table points at missing functions: {}'.format(missing))

    def test_helper_calls_target_real_functions(self):
        """_helper_call(request, 'module', 'func', ...) -> module.py defines func."""
        bad = []
        for node in ast.walk(_tree('maya_listener.py')):
            if not (isinstance(node, ast.Call) and getattr(node.func, 'id', None) == '_helper_call'):
                continue
            module, func = node.args[1], node.args[2]
            if isinstance(module, ast.Constant) and isinstance(func, ast.Constant):
                if func.value not in _functions(module.value + '.py'):
                    bad.append('{}.{}'.format(module.value, func.value))
        # fit_ctrl_shape picks its function from a table of names
        for func in ('flat_shape', 'ring_around_bone', 'fit_fk_box'):
            if func not in _functions('ctrl_fit.py'):
                bad.append('ctrl_fit.' + func)
        self.assertFalse(bad, 'listener calls helpers that do not exist: {}'.format(bad))


if __name__ == '__main__':
    unittest.main()
