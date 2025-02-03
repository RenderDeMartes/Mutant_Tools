from __future__ import absolute_import
from functools import wraps
from six.moves import map
from maya import cmds, mel


def viewport_off(func):
    '''Turnoff Maya's display decorator'''

    @wraps(func)
    def wrap(*args, **kwargs):

        # set $gMainPane off
        if not cmds.about(batch=True):
            mel.eval("paneLayout -e -manage false $gMainPane")

        try:
            return func(*args, **kwargs)
        except Exception:
            raise  # will raise original error
        finally:
            if not cmds.about(batch=True):
                mel.eval("paneLayout -e -manage true $gMainPane")
    return wrap


def wait_cursor(func):
    '''Set wait cursor while function is running'''

    @wraps(func)
    def wrap(*args, **kwargs):

        from star.qt.Qt import QtCore, QtWidgets

        if not cmds.about(batch=True):
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        try:
            return func(*args, **kwargs)
        except Exception:
            raise
        finally:
            if not cmds.about(batch=True):
                QtWidgets.QApplication.restoreOverrideCursor()
    return wrap


def undo(func):
    '''Enable undo within Maya after function is run'''

    @wraps(func)
    def wrap(*args, **kwargs):
        result = None
        try:
            cmds.undoInfo(openChunk=True, chunkName=func.__name__)
            result = func(*args, **kwargs)
        except Exception:
            raise
        finally:
            cmds.undoInfo(closeChunk=True)
        return result
    return wrap


def keep_selection(func):
    '''Restore the original Maya selection when exiting the function.'''

    @wraps(func)
    def wrap(*args, **kwargs):
        sel = list(map(MayaNode, cmds.ls(selection=True)))
        try:
            return func(*args, **kwargs)
        finally:
            if sel:
                cmds.select([x for x in sel if cmds.objExists(x)])
            else:
                cmds.select(deselect=True)
    return wrap
