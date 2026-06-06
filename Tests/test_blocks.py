"""
Static analysis tests for all Mutant Tools blocks.
Runs outside Maya — no cmds import required.

Run from the Mutant_Tools root:
    python -m pytest Tests/test_blocks.py -v
    python Tests/test_blocks.py
"""
import ast
import json
import os
import re
import unittest
from pathlib import Path

MUTANT_TOOLS_ROOT = Path(__file__).resolve().parents[1]
BLOCKS_DIR = MUTANT_TOOLS_ROOT / 'Blocks'
CONFIG_DIR = MUTANT_TOOLS_ROOT / 'config'
GUIDE_DATA_DIR = MUTANT_TOOLS_ROOT / 'Utils' / 'IO' / 'Guide_Data'

BLOCK_JSON_REQUIRED_KEYS = {'Name', 'Description', 'Icon', 'Enable',
                             'python_file', 'exec_command', 'build_command'}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _all_block_jsons():
    """All per-block JSON files — skips category-level files like order.json."""
    results = []
    for path in BLOCKS_DIR.rglob('*.json'):
        if path.name == 'order.json':
            continue
        # Block JSONs live exactly 2 levels under BLOCKS_DIR: Category/Block/file.json
        rel = path.relative_to(BLOCKS_DIR)
        if len(rel.parts) >= 2:
            results.append(path)
    return results


def _all_exec_files():
    """All exec_*.py files under Blocks/."""
    return list(BLOCKS_DIR.rglob('exec_*.py'))


def _parsed_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _parsed_ast(path):
    # utf-8-sig strips a leading BOM if present
    return ast.parse(path.read_text(encoding='utf-8-sig'))


def _func_name_from_command(command):
    """Extract bare function name from 'module.func_name()' style string."""
    try:
        return command.split('.')[-1].split('(')[0].strip()
    except Exception:
        return ''


def _defined_functions(tree):
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}


# ---------------------------------------------------------------------------
# JSON integrity
# ---------------------------------------------------------------------------

class TestBlockJSON(unittest.TestCase):

    def test_all_json_parse(self):
        """Every block JSON must be valid JSON."""
        errors = []
        for path in _all_block_jsons():
            try:
                _parsed_json(path)
            except json.JSONDecodeError as exc:
                errors.append('{}: {}'.format(path.relative_to(MUTANT_TOOLS_ROOT), exc))
        self.assertFalse(errors, '\n'.join(errors))

    def test_required_keys_present(self):
        """Every block JSON must contain all required top-level keys."""
        errors = []
        for path in _all_block_jsons():
            try:
                data = _parsed_json(path)
            except Exception:
                continue
            missing = BLOCK_JSON_REQUIRED_KEYS - set(data.keys())
            if missing:
                errors.append('{}: missing {}'.format(
                    path.relative_to(MUTANT_TOOLS_ROOT), sorted(missing)))
        self.assertFalse(errors, '\n'.join(errors))

    def test_python_file_field_exists(self):
        """The python_file named in each block JSON must exist alongside it."""
        errors = []
        for path in _all_block_jsons():
            try:
                data = _parsed_json(path)
            except Exception:
                continue
            py_name = data.get('python_file', '')
            if not py_name:
                errors.append('{}: python_file field is empty'.format(
                    path.relative_to(MUTANT_TOOLS_ROOT)))
                continue
            target = path.parent / py_name
            if not target.exists():
                errors.append('{}: python_file "{}" not found'.format(
                    path.relative_to(MUTANT_TOOLS_ROOT), py_name))
        self.assertFalse(errors, '\n'.join(errors))

    def test_enable_is_valid(self):
        """Enable field must be 'True' or 'False'."""
        errors = []
        for path in _all_block_jsons():
            try:
                data = _parsed_json(path)
            except Exception:
                continue
            val = data.get('Enable', '')
            if val not in ('True', 'False'):
                errors.append('{}: Enable="{}"'.format(
                    path.relative_to(MUTANT_TOOLS_ROOT), val))
        self.assertFalse(errors, '\n'.join(errors))


# ---------------------------------------------------------------------------
# Exec file syntax and structure
# ---------------------------------------------------------------------------

class TestExecFileSyntax(unittest.TestCase):

    def test_all_exec_files_parse(self):
        """Every exec_*.py must have valid Python 3 syntax."""
        errors = []
        for path in _all_exec_files():
            try:
                _parsed_ast(path)
            except SyntaxError as exc:
                errors.append('{}: {}'.format(path.relative_to(MUTANT_TOOLS_ROOT), exc))
        self.assertFalse(errors, '\n'.join(errors))

    def test_no_parts_minus2_path_computation(self):
        """No exec file may use parts[:-2] — all must use parts[:-3] to reach root."""
        pattern = re.compile(r'parts\[:-2\]')
        errors = []
        for path in _all_exec_files():
            try:
                source = path.read_text(encoding='utf-8-sig')
            except Exception:
                continue
            if pattern.search(source):
                errors.append(str(path.relative_to(MUTANT_TOOLS_ROOT)))
        self.assertFalse(
            errors,
            'Files still using parts[:-2] (should be [:-3]):\n' + '\n'.join(errors))

    def test_exec_files_are_at_correct_depth(self):
        """Each exec file must live exactly at Blocks/Category/Block/ (depth=2 under BLOCKS_DIR)."""
        errors = []
        for path in _all_exec_files():
            rel = path.relative_to(BLOCKS_DIR)
            depth = len(rel.parts) - 1  # subtract the filename itself
            if depth != 2:
                errors.append('{}: depth={} (expected 2)'.format(
                    path.relative_to(MUTANT_TOOLS_ROOT), depth))
        self.assertFalse(errors, '\n'.join(errors))

    def test_computed_folder_reaches_root(self):
        """parts[:-3] from each exec file must resolve to MUTANT_TOOLS_ROOT."""
        errors = []
        for path in _all_exec_files():
            parent = path.parent  # the directory containing the exec file
            # parent has parts: .../Mutant_Tools/Blocks/Category/Block
            # [:-3] removes Block, Category, Blocks → leaves Mutant_Tools
            computed = Path(*parent.parts[:-3])
            if computed != MUTANT_TOOLS_ROOT:
                errors.append('{}: computed={}'.format(
                    path.relative_to(MUTANT_TOOLS_ROOT), computed))
        self.assertFalse(errors, '\n'.join(errors))


# ---------------------------------------------------------------------------
# Cross-reference: JSON commands vs exec function definitions
# ---------------------------------------------------------------------------

class TestCommandFunctionCrossRef(unittest.TestCase):

    def _check_command_key(self, key):
        errors = []
        for json_path in _all_block_jsons():
            try:
                data = _parsed_json(json_path)
            except Exception:
                continue
            py_name = data.get('python_file', '')
            command = data.get(key, '')
            if not py_name or not command:
                continue
            exec_path = json_path.parent / py_name
            if not exec_path.exists():
                continue
            func = _func_name_from_command(command)
            if not func:
                continue
            try:
                tree = _parsed_ast(exec_path)
            except SyntaxError:
                continue
            if func not in _defined_functions(tree):
                errors.append('{}: {}="{}" — function "{}" not in {}'.format(
                    json_path.relative_to(MUTANT_TOOLS_ROOT),
                    key, command, func, py_name))
        return errors

    def test_exec_command_function_defined(self):
        """The function named in exec_command must be defined in python_file."""
        errors = self._check_command_key('exec_command')
        self.assertFalse(errors, '\n'.join(errors))

    def test_build_command_function_defined(self):
        """The function named in build_command must be defined in python_file."""
        errors = self._check_command_key('build_command')
        self.assertFalse(errors, '\n'.join(errors))


# ---------------------------------------------------------------------------
# Config files
# ---------------------------------------------------------------------------

class TestConfigFiles(unittest.TestCase):

    CONFIG_FILES = ['name_conventions.json', 'curves.json', 'rig_setup.json', 'version.json']

    def test_config_files_exist(self):
        """All config files referenced by exec blocks must exist."""
        errors = []
        for name in self.CONFIG_FILES:
            path = CONFIG_DIR / name
            if not path.exists():
                errors.append('Missing: {}'.format(path))
        self.assertFalse(errors, '\n'.join(errors))

    def test_config_files_parse(self):
        """All config files must be valid JSON."""
        errors = []
        for name in self.CONFIG_FILES:
            path = CONFIG_DIR / name
            if not path.exists():
                continue
            try:
                _parsed_json(path)
            except json.JSONDecodeError as exc:
                errors.append('{}: {}'.format(name, exc))
        self.assertFalse(errors, '\n'.join(errors))


# ---------------------------------------------------------------------------
# Guide .ma files referenced by preset exec files
# ---------------------------------------------------------------------------

class TestGuideDataFiles(unittest.TestCase):

    _MA_PATTERN = re.compile(r"Guide_Data['\",\s]*,\s*['\"]([^'\"]+\.ma)['\"]")

    def test_referenced_ma_files_exist(self):
        """Every .ma file referenced via Guide_Data in exec files must exist."""
        errors = []
        for exec_path in _all_exec_files():
            try:
                source = exec_path.read_text(encoding='utf-8-sig')
            except Exception:
                continue
            for ma_name in self._MA_PATTERN.findall(source):
                ma_path = GUIDE_DATA_DIR / ma_name
                if not ma_path.exists():
                    errors.append('{}: references missing "{}"'.format(
                        exec_path.relative_to(MUTANT_TOOLS_ROOT), ma_name))
        self.assertFalse(errors, '\n'.join(errors))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main(verbosity=2)
