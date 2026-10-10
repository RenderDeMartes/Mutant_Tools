"""Send a Python file (or -c code) to the live Maya bridge and print the result.

    python Dev/MayaMCP/run_in_maya.py script.py [--port 7501]
    python Dev/MayaMCP/run_in_maya.py -c "import maya.cmds as mc; print(mc.ls(sl=1))"

Sending a file avoids quoting/backslash mangling of inline code.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge_transport import bridge_call  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file', nargs='?')
    ap.add_argument('-c', '--code')
    ap.add_argument('--port', type=int, default=7501)
    ap.add_argument('--timeout', type=float, default=600)
    a = ap.parse_args()
    if a.code is None and not a.file:
        ap.error('give a file or -c code')
    code = a.code if a.code is not None else open(a.file).read()
    r = bridge_call('exec', port=a.port, timeout=a.timeout, code=code)
    if r.get('stdout'):
        print(r['stdout'], end='')
    if r.get('stderr'):
        print('STDERR:', r['stderr'], file=sys.stderr)
    if r.get('traceback'):
        print(r['traceback'], file=sys.stderr)
        sys.exit(1)
    if not r.get('success', True):
        print(r, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
