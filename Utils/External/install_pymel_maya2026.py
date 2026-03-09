"""Install PyMEL for Maya 2026.

Usage inside Maya Script Editor (Python tab):

from Mutant_Tools.Utils.External import install_pymel_maya2026
install_pymel_maya2026.install_pymel()

If you get ModuleNotFoundError: No module named 'Mutant_Tools':

import sys
sys.path.insert(0, r"C:/Users/rodri/Documents/maya/2026/scripts")
from Mutant_Tools.Utils.External import install_pymel_maya2026
install_pymel_maya2026.install_pymel()

Usage from terminal with mayapy:

    "C:/Program Files/Autodesk/Maya2026/bin/mayapy.exe" \
        "C:/Users/rodri/Documents/maya/2026/scripts/Mutant_Tools/Utils/External/install_pymel_maya2026.py"

What it does:
- Finds the Maya Python interpreter (mayapy).
- Ensures pip exists in that interpreter.
- Installs/updates the `pymel` package (defaults to --user install).
- Validates install by printing the installed PyMEL package version.
- If Maya docs are missing, applies a cache fallback (2025 -> 2026).

How to test after install (restart Maya first):

import pymel.core as pm
print("PyMEL:", pm.__version__)
n = pm.polyCube(name="pymel_test_cube")[0]
print("Created:", n)

Expected result:
- No import error.
- PyMEL version prints.
- A cube named `pymel_test_cube` is created.

After install, restart Maya to ensure the new package path is loaded.
"""

from __future__ import absolute_import

import os
import shutil
import subprocess
import sys

try:
    from maya import cmds
except Exception:
    cmds = None


LOG_PREFIX = "[MutantTools][PyMELInstall]"


def _log(message):
    print("{} {}".format(LOG_PREFIX, message))


def _format_command(command):
    parts = []
    for arg in command:
        if " " in arg:
            parts.append('"{}"'.format(arg))
        else:
            parts.append(arg)
    return " ".join(parts)


def _run_command(command):
    _log("Running: {}".format(_format_command(command)))

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    output, _ = process.communicate()

    if output:
        print(output.rstrip())

    if process.returncode != 0:
        raise RuntimeError(
            "Command failed with exit code {}: {}".format(
                process.returncode, _format_command(command)
            )
        )

    return output or ""


def _find_mayapy():
    candidates = []

    executable = os.path.normpath(sys.executable)
    exe_name = os.path.basename(executable).lower()

    if exe_name.startswith("mayapy"):
        return executable

    exe_dir = os.path.dirname(executable)
    candidates.extend(
        [
        os.path.join(exe_dir, "mayapy.exe"),
        os.path.join(exe_dir, "mayapy"),
        ]
    )

    maya_location = os.environ.get("MAYA_LOCATION")
    if maya_location:
        candidates.insert(0, os.path.join(maya_location, "bin", "mayapy.exe"))
        candidates.insert(1, os.path.join(maya_location, "bin", "mayapy"))

    candidates.append(r"C:\Program Files\Autodesk\Maya2026\bin\mayapy.exe")

    for binary_name in ("mayapy.exe", "mayapy"):
        binary_path = shutil.which(binary_name)
        if binary_path:
            candidates.append(binary_path)

    for candidate in candidates:
        if os.path.exists(candidate):
            return os.path.normpath(candidate)

    return None


def _expected_maya_docs_dir(mayapy_path):
    maya_bin = os.path.dirname(os.path.normpath(mayapy_path))
    maya_root = os.path.dirname(maya_bin)
    return os.path.join(maya_root, "docs", "Maya2026", "en_US")


def _validate_pymel_package(mayapy_path):
    _run_command(
        [
            mayapy_path,
            "-c",
            "import importlib.metadata as m; print('PyMEL package version:', m.version('pymel'))",
        ]
    )


def _apply_pymel_cache_fallback(mayapy_path, source_version="2025", target_version="2026"):
    code = "\n".join(
        [
            "import importlib.util",
            "import os",
            "import shutil",
            "spec = importlib.util.find_spec('pymel')",
            "if not spec or not spec.origin:",
            "    raise RuntimeError('PyMEL package is not importable')",
            "cache_dir = os.path.join(os.path.dirname(spec.origin), 'cache')",
            "stems = ('mayaApi', 'mayaCmdsDocs', 'mayaCmdsExamples', 'mayaCmdsList')",
            "copied = []",
            "for stem in stems:",
            "    src = os.path.join(cache_dir, '{}{}.py'.format(stem, '" + source_version + "'))",
            "    dst = os.path.join(cache_dir, '{}{}.py'.format(stem, '" + target_version + "'))",
            "    if os.path.exists(src) and not os.path.exists(dst):",
            "        shutil.copy2(src, dst)",
            "        copied.append(os.path.basename(dst))",
            "print('PyMEL cache fallback copied:', copied if copied else 'none')",
        ]
    )

    _run_command([mayapy_path, "-c", code])


def apply_pymel_2026_cache_fallback(mayapy_path=None):
    """Apply PyMEL cache fallback files (2025 -> 2026).

    Use this when Maya docs are not installed and `import pymel.core` fails with
    "Cannot find maya documentation".
    """

    if mayapy_path:
        mayapy_path = os.path.normpath(mayapy_path)
    else:
        mayapy_path = _find_mayapy()

    if not mayapy_path or not os.path.exists(mayapy_path):
        raise RuntimeError("Could not find mayapy path.")

    if "mayapy" not in os.path.basename(mayapy_path).lower():
        raise RuntimeError("Resolved interpreter is not mayapy: {}".format(mayapy_path))

    _apply_pymel_cache_fallback(mayapy_path)
    return True


def _ensure_pip(mayapy_path):
    try:
        _run_command([mayapy_path, "-m", "pip", "--version"])
    except Exception:
        _log("pip was not found. Bootstrapping with ensurepip...")
        _run_command([mayapy_path, "-m", "ensurepip", "--upgrade"])


def install_pymel(package_spec="pymel", user_install=True, upgrade=True, mayapy_path=None):
    """Install PyMEL for Maya 2026.

    Args:
        package_spec (str): Pip package spec. Defaults to "pymel".
        user_install (bool): Install with --user to avoid admin permissions.
        upgrade (bool): Upgrade package if already present.
        mayapy_path (str): Optional full path to mayapy executable.

    Returns:
        bool: True if installation and validation completed.
    """

    if mayapy_path:
        mayapy_path = os.path.normpath(mayapy_path)
    else:
        mayapy_path = _find_mayapy()

    if not mayapy_path or not os.path.exists(mayapy_path):
        raise RuntimeError(
            "Could not find mayapy for Maya 2026. Pass mayapy_path explicitly, "
            "for example: C:/Program Files/Autodesk/Maya2026/bin/mayapy.exe"
        )

    if "mayapy" not in os.path.basename(mayapy_path).lower():
        raise RuntimeError("Resolved interpreter is not mayapy: {}".format(mayapy_path))

    _log("Using interpreter: {}".format(mayapy_path))

    _ensure_pip(mayapy_path)

    install_command = [mayapy_path, "-m", "pip", "install"]
    if upgrade:
        install_command.append("--upgrade")
    if user_install:
        install_command.append("--user")
    install_command.append(package_spec)

    _run_command(install_command)

    _validate_pymel_package(mayapy_path)

    docs_dir = _expected_maya_docs_dir(mayapy_path)
    if not os.path.isdir(docs_dir):
        _log("Warning: Maya docs folder not found: {}".format(docs_dir))
        _log("If pymel.core fails, install Maya Offline Help or set MAYA_DOC_DIR.")
        _log("Applying cache fallback 2025 -> 2026 for pymel...")
        _apply_pymel_cache_fallback(mayapy_path)

    _log("PyMEL installed successfully. Restart Maya to load new site-packages cleanly.")

    if cmds:
        try:
            cmds.confirmDialog(
                title="Mutant Tools",
                message="PyMEL installed successfully. Please restart Maya.",
                button=["OK"],
            )
        except Exception:
            pass

    return True


if __name__ == "__main__":
    install_pymel()
