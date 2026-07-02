from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import CtrlUtils
reload(Mutant_Tools.Utils.IO.CtrlUtils)

ctrls = CtrlUtils.Ctrls()
ctrls.FUNC_NAME(argument = '')

#----------------
dependencies:

NG

#----------------
www.mutanttools.com
author:  Esteban Rodriguez <info@mutanttools.com>

'''
import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import json
from pathlib import Path

from maya import cmds as cmds
import maya.OpenMayaUI as omui
try:
    from maya.api import OpenMaya as om2
except:
    om2 = None
try:
    from shiboken6 import wrapInstance
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from shiboken2 import wrapInstance
    from PySide2 import QtCore, QtWidgets
from Mutant_Tools.Utils.Helpers.decorators import undo

import Mutant_Tools
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

# ---------------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)


def _maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class _CollapsibleSection(QtWidgets.QWidget):

    def __init__(self, title, color, parent=None):
        super(_CollapsibleSection, self).__init__(parent)

        self.toggle_button = QtWidgets.QToolButton(text=title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.setStyleSheet("QToolButton { border: none; font-weight: bold; color: %s; }" % color)
        self.toggle_button.clicked.connect(self._on_toggle)

        self.content = QtWidgets.QListWidget()
        self.content.setVisible(False)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.content)

    def _on_toggle(self):
        self.set_expanded(self.toggle_button.isChecked())

    def set_expanded(self, expanded):
        self.toggle_button.setChecked(expanded)
        self.toggle_button.setArrowType(QtCore.Qt.DownArrow if expanded else QtCore.Qt.RightArrow)
        self.content.setVisible(expanded)

    def add_entry(self, label, full_path):
        item = QtWidgets.QListWidgetItem(label)
        item.setData(QtCore.Qt.UserRole, full_path)
        self.content.addItem(item)


class SaveCtrlsReportDialog(QtWidgets.QDialog):

    def __init__(self, saved, warnings, failed, parent=None):
        super(SaveCtrlsReportDialog, self).__init__(parent)

        self.setWindowTitle("Save Ctrls Report")
        self.resize(560, 480)

        layout = QtWidgets.QVBoxLayout(self)

        summary = QtWidgets.QLabel("Saved: {}    Warnings: {}    Failed: {}".format(len(saved), len(warnings), len(failed)))
        layout.addWidget(summary)

        self.failed_section = _CollapsibleSection("Failed ({})".format(len(failed)), "#e05c4f")
        for full_path, err in failed:
            self.failed_section.add_entry("{} - {}".format(full_path.split('|')[-1], err), full_path)
        self.failed_section.set_expanded(bool(failed))
        layout.addWidget(self.failed_section)

        self.warning_section = _CollapsibleSection("Duplicate Names ({})".format(len(warnings)), "#e0b400")
        for full_path, msg in warnings:
            self.warning_section.add_entry("{} - {}".format(full_path.split('|')[-1], msg), full_path)
        self.warning_section.set_expanded(bool(warnings))
        layout.addWidget(self.warning_section)

        self.saved_section = _CollapsibleSection("Saved ({})".format(len(saved)), "#5cb85c")
        for full_path in saved:
            self.saved_section.add_entry(full_path.split('|')[-1], full_path)
        self.saved_section.set_expanded(False)
        layout.addWidget(self.saved_section)

        for section in (self.failed_section, self.warning_section, self.saved_section):
            section.content.itemClicked.connect(self._select_ctrl)

        layout.addStretch()

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def _select_ctrl(self, item):
        full_path = item.data(QtCore.Qt.UserRole)
        if full_path and cmds.objExists(full_path):
            cmds.select(full_path, replace=True)


# ---------------------------------------------------------------------------

class Ctrls(object):

    #Thanks to: https://github.com/vshotarov/controlShapeManager/blob/master/utils.py
    #Thanks To: https://bindpose.com/creating-maya-control-shape-manager/

    #---------------------------------------------------------------------------
    def __int__(self):

        self.to_delete = []


    #---------------------------------------------------------------------------

    def validateCurve(self, crv=None):
        if cmds.nodeType(crv) == "transform" or cmds.nodeType(cmds.listRelatives(crv, c=1, s=1)[0]) == "nurbsCurve":
            crvShapes = cmds.listRelatives(crv, c=1, s=1, fullPath=True)

        elif cmds.nodeType(crv) == "nurbsCurve":
            crvShapes = cmds.listRelatives(cmds.listRelatives(crv, p=1)[0], c=1, s=1, fullPath=True)
        if not crvShapes:
            return
        return_list = []
        for node in crvShapes:
            if cmds.nodeType(node) == 'nurbsCurve':
                return_list.append(node)

        return return_list

    #---------------------------------------------------------------------------

    def getShape(self, crv=None):
        crvShapes = self.validateCurve(crv)
        if not crvShapes:
            return
        crvShapeList = []

        for crvShape in crvShapes:
            crvShapeDict = {
                "points": [],
                "knots": [],
                "form": cmds.getAttr(crvShape + ".form"),
                "degree": cmds.getAttr(crvShape + ".degree"),
                "colour": cmds.getAttr(crvShape + ".overrideColor")
            }
            points = []

            for i in range(cmds.getAttr(crvShape + ".controlPoints", s=1)):
                points.append(cmds.getAttr(crvShape + ".controlPoints[%i]" % i)[0])

            crvShapeDict["points"] = points
            crvShapeDict["knots"] = self.getKnots(crvShape)

            crvShapeList.append(crvShapeDict)

        return crvShapeList

    #---------------------------------------------------------------------------

    def getKnots(self, crvShape=None):
        sel = om2.MSelectionList()
        sel.add(crvShape)
        dagPath = sel.getDagPath(0)

        fnCurve = om2.MFnNurbsCurve(dagPath)
        return list(fnCurve.knots())

    #---------------------------------------------------------------------------

    def setShape(self, crv, crvShapeList):
        crvShapes = self.validateCurve(crv)

        oldColour = cmds.getAttr(crvShapes[0] + ".overrideColor")
        cmds.delete(crvShapes)

        for i, crvShapeDict in enumerate(crvShapeList):
            tmpCrv = cmds.curve(p=crvShapeDict["points"], k=crvShapeDict["knots"], d=crvShapeDict["degree"], per=bool(crvShapeDict["form"]))
            newShape = cmds.listRelatives(tmpCrv, s=1)[0]
            cmds.parent(newShape, crv, r=1, s=1)
            cmds.setAttr(newShape + ".lineWidth", int(setup['line_width']))
            cmds.delete(tmpCrv)

        #newShape = cmds.rename(newShape, crv + "Shape" + str(i + 1).zfill(2))
        newShape = cmds.rename(newShape, crvShapes[0])

        #cmds.setAttr(newShape + ".overrideEnabled", 1)

        if "colour" in crvShapeDict.keys():
            self.setColour(newShape, crvShapeDict["colour"])
        else:
            self.setColour(newShape, oldColour)

    #---------------------------------------------------------------------------

    def setColour(self, crv, colour):
        if cmds.nodeType(crv) == "transform":
            crvShapes = mc.listRelatives(crv)

        else:
            crvShapes = [crv]
            for crv in crvShapes:
                cmds.setAttr(crv + ".overrideColor", colour)
    #---------------------------------------------------------------------------

    def getColour(self, crv):
        if cmds.nodeType(crv) == "transform":
            crv = cmds.listRelatives(crv)[0]

        return cmds.getAttr(crv + ".overrideColor")

    #---------------------------------------------------------------------------

    def assignColour(self):
        for each in cmds.ls(sl=1, fl=1):
            self.setColour(each, args[0])

    #---------------------------------------------------------------------------
    def loadData(self, path=None):
        if os.path.isfile(path):
            f = open(path, "r")
            data = json.loads(f.read())
            f.close()
            return data
        else:
            cmds.error("The file " + path + " doesn't exist")

    #---------------------------------------------------------------------------

    def saveData(self, path=None,data=None, force_validate=False):

        if self.validatePath(path, force_validate=force_validate):
            f = open(path, "w")
            f.write(json.dumps(data, sort_keys=1, indent=4, separators=(",", ":")))
            f.close()
            return 1
        return 0

    #---------------------------------------------------------------------------

    def validatePath(self, path=None, force_validate=False):
        '''Checks if the file already exists and provides a dialog to overwrite or not'''

        if force_validate:
            return 1

        if os.path.isfile(path):
            confirm = cmds.confirmDialog(title='Overwrite file?',
                                       message='The file ' + path + ' already exists.Do you want to overwrite it?',
                                       button=['Yes', 'No'],
                                       defaultButton='Yes',
                                       cancelButton='No',
                                       dismissString='No')
            if confirm == "No":
                cmds.warning("The file " + path + " was not saved")
                return 0
        return 1

    #---------------------------------------------------------------------------

    def mirrorCtlShapes(self):
        '''Mirrors the selected control's shape to the other control on the other side'''
        sel = cmds.ls(sl=1, fl=1)
        for ctl in sel:
            if ctl[0] not in ["L", "R"]:
                continue
            search = nc['right']
            replace = nc['left']
            if ctl[0] == nc['left'][0]:
                search = nc['left']
                replace = nc['right']
            shapes = self.getShape(ctl)
            for shape in shapes:
                shape.pop("colour")
            if cmds.objExists(ctl.replace(search, replace)):
                self.setShape(ctl.replace(search, replace), shapes)
                self._flipCtlShape(ctl.replace(search, replace))
                cmds.select(ctl.replace(search, replace))
                self.reparent_locators()
            else:
                print(ctl.replace(search, replace) + ': Doesnt Exists')

        cmds.select(sel)

    #---------------------------------------------------------------------------

    def _flipCtlShape(self, crv=None, axis=[1, 1, 1]):
        shapes = self.getShape(crv)

        newShapes = []
        for shape in shapes:
            for i, each in enumerate(shape["points"]):
                shape["points"][i] = [each[0] * axis[0], each[1] * axis[1], each[2] * axis[2]]
        newShapes.append(shape)
        self.setShape(crv, newShapes)
        cmds.select(crv)

    #---------------------------------------------------------------------------
    def save_all(self, ctrls='All', folder_path=None, force_validate=False):
        #ctrls.save_all('C:\\Users\\PC\\Desktop\\ctrls.json')
        if not folder_path:
            path = mh.export_window(extension = ".json")
            if not path:
                return
            path = path[0]
        else:
            path = folder_path
        if not path:
            return

        print("Mutant Tools: Saving Ctrls ...")

        all_ctrls = {}
        saved_ctrls = []
        failed_ctrls = []
        warning_ctrls = []
        seen_names = {}
        if ctrls == 'All':
            cmds.select('*{}'.format(nc['ctrl']))
        for ctrl in cmds.ls(sl=True, long=True):
            try:
                data = self.getShape(ctrl)
            except (RuntimeError, ValueError) as e:
                failed_ctrls.append((ctrl, str(e)))
                continue
            if not data:
                # Not an actual controller (no nurbsCurve shape) - skip.
                continue

            short = ctrl.split('|')[-1]
            if short in seen_names:
                self.tagFullPath(ctrl)
                self.tagFullPath(seen_names[short])
                warning_ctrls.append((ctrl, "duplicated name with '{}' - only one was saved".format(seen_names[short])))
                continue

            seen_names[short] = ctrl
            all_ctrls[short] = data
            saved_ctrls.append(ctrl)

        #Getting color information from ctrls
        colors_data = self.get_ctrl_colors(long_name=False)

        #Creating export dictionary with data.
        all_ctrl_data = {}
        all_ctrl_data["ctrl_shape_data"] = all_ctrls
        all_ctrl_data["ctrl_color_data"] = colors_data

        self.saveData(path=path, data=all_ctrl_data, force_validate=force_validate)
        print("Mutant Tools: Saved Ctrls -> {}".format(path))

        self.showSaveReport(saved_ctrls, warning_ctrls, failed_ctrls)

    #---------------------------------------------------------------------------

    def tagFullPath(self, ctrl):
        '''Stamps the ctrl's current full dag path onto itself so it can be identified later if its short name collides with another ctrl.'''
        attr = 'mutantFullPath'
        if not cmds.attributeQuery(attr, node=ctrl, exists=True):
            cmds.addAttr(ctrl, longName=attr, dataType='string')
        cmds.setAttr('{}.{}'.format(ctrl, attr), ctrl, type='string')

    #---------------------------------------------------------------------------

    def showSaveReport(self, saved_ctrls, warning_ctrls, failed_ctrls):
        if not warning_ctrls and not failed_ctrls:
            cmds.inViewMessage(amg="Mutant Tools: Ctrls Saved", pos='midCenter', fade=True)
            return
        self._report_dialog = SaveCtrlsReportDialog(saved_ctrls, warning_ctrls, failed_ctrls, parent=_maya_main_window())
        self._report_dialog.show()

    #---------------------------------------------------------------------------
    @undo
    def load_all(self, path=None):
        #ctrls.load_all('C:\\Users\\PC\\Desktop\\ctrls.json')
        if path is None:
            path = mh.import_window(extension = ".json")
            if not path:
                return False
            path = path[0]
        if not path:
            return False

        if not os.path.isfile(path):
            cmds.warning('Path doesnt exists', path)
            return False

        vis_data = self.save_all_vis_connections()

        all_data = self.loadData(path)

        color_info_presence = False

        #Check if the json file has color info or if it is the old version. 
        try:
            data = all_data["ctrl_shape_data"]
            color_info_presence = True
        
        except:
            data = all_data

        cmds.select('*{}'.format(nc['ctrl']))
        for ctrl in cmds.ls(sl=True):
            try:
                shape_data = data[ctrl]
                self.setShape(ctrl, shape_data)
                self.reparent_locators(ctrl)
            except Exception as e:
                print ('Error with load_all: {}, {}'.format(ctrl, e))

        self.load_all_vis_connections(vis_data)

        #Setting Colors from json info.
        if color_info_presence:
            color_data = all_data["ctrl_color_data"]    
            self.apply_ctrls_color_data(colors_data=color_data, selection=list(color_data.keys()))


    @undo
    def load_selected(self, path=None):

        saved_selection = cmds.ls(sl=True)

        #ctrls.load_all('C:\\Users\\PC\\Desktop\\ctrls.json')
        if path is None:
            path = mh.import_window(extension = ".json")
            path = path[0]
        if not path:
            return False

        vis_data = self.save_all_vis_connections()

        all_data = self.loadData(path)
        color_info_presence = False

        #Check if the json file has color info or if it is the old version. 
        try:
            data = all_data["ctrl_shape_data"]
            color_info_presence = True
        
        except:
            data = all_data

        for ctrl in saved_selection:
            try:
                shape_data = data[ctrl]
                self.setShape(ctrl, shape_data)
                self.reparent_locators(ctrl)
            except Exception as e:
                print ('Error with load_selected: {}'.format(ctrl), e)

        self.load_all_vis_connections(vis_data)

        #Setting Colors from json info.
        if color_info_presence:
            color_data = all_data["ctrl_color_data"]    
            self.apply_ctrls_color_data(colors_data=color_data, selection=saved_selection)


    #---------------------------------------------------------------------------
    @undo
    def mirror_all(self):

        vis_data = self.save_all_vis_connections()
        colors_data = self.get_ctrl_colors(True)

        cmds.select('*{}'.format(nc['ctrl']))
        for ctrl in cmds.ls(sl=True):
            cmds.select(ctrl)
            self.mirrorCtlShapes()

        cmds.select(cl=True)

        self.load_all_vis_connections(vis_data)
        self.apply_ctrls_color_data(colors_data=colors_data)

    @undo
    def mirror_all_ctrl_shapes(self, ctrls ='All'):
        # Get ctrls
        if ctrls == 'All':
            ctrls = cmds.ls('*{}'.format(nc['ctrl']))
        else:
            ctrls = cmds.ls(sl=True)
        print(ctrls)

        # Loop ctrls
        for ctrl in ctrls:
            if ctrl.startswith(nc['right']):
                continue
            # Get shape data
            shapes = cmds.listRelatives(ctrl, s=True, type="nurbsCurve")
            if not shapes:
                continue
            for shape in shapes:
                # Calculate mirror shape
                current_side = shape[0]
                mirror_side = {"L": "R", "R": "L"}.get(current_side)
                if not mirror_side:
                    continue
                mirror_shape = shape.replace(current_side, mirror_side, 1)
                # Calculate mirror points
                mirror_points = {}
                points = cmds.ls("{}.cv[*]".format(shape), fl=True)  # crv.points doesn't get what we need
                for pt in points:
                    cv = pt.split(".")[1]
                    pos = cmds.xform(pt, q=True, ws=True, t=True)
                    mirror_pos = list(pos)
                    mirror_pos[0] *= -1
                    mirror_points["{}.{}".format(mirror_shape, cv)] = mirror_pos
                # Mirror the cvs
                for cv, pos in mirror_points.items():
                    cmds.xform(cv, t=pos, ws=True)

    #---------------------------------------------------------------------------

    def reparent_locators(self, ctrl=None):
        if ctrl ==None:
            ctrl = cmds.ls(sl=True)[0]

        shapes = cmds.listRelatives(ctrl, s=1)

        for shape in shapes:
            if cmds.nodeType(shape) != 'locator':
                cmds.reorder(shape, f=True)
            if cmds.nodeType(shape) == 'locator':
                cmds.reorder(shape, b=True)

    #---------------------------------------------------------------------------

    def smart_assign_colors(self):
        ''

    #---------------------------------------------------------------------------
    def save_all_vis_connections(self, ctrls=''):
        if not ctrls:
            cmds.select('*{}'.format(nc['ctrl']))
            ctrls = cmds.ls(sl=True)

        connections = {}
        to_delete =[]
        no_shapes_ctrl = []
        for ctrl in ctrls:
            if not ctrl.endswith(nc['ctrl']):
                continue
            shapes = cmds.listRelatives(ctrl, s=True)
            if not shapes:
                no_shapes_ctrl.append(ctrl)
                continue
            for shape in shapes:
                if cmds.nodeType(shape) == 'nurbsCurve':
                    break
            vis_connection = cmds.listConnections(shape + '.v', p=True)
            if not vis_connection:
                continue
            if vis_connection:
                vis_connection = vis_connection[0]
            connections[ctrl] = vis_connection

            #connect a dummy node so it remains in scene after load
            try:
                dummy_node = cmds.spaceLocator()[0]
                to_delete.append(dummy_node)
                cmds.connectAttr(vis_connection, dummy_node+'.v')
            except Exception as e:
                print('Error with save_all_vis_connections: ', ctrl, e)

        self.to_delete = to_delete
        if no_shapes_ctrl:
            cmds.warning('Please check: {}'.format(no_shapes_ctrl))
        return connections

    def load_all_vis_connections(self, ctrls_data):
        for ctrl in ctrls_data:
            shape = cmds.listRelatives(ctrl, s=True)
            if shape:
                shape = shape[0]
            else:
                continue
            connection = ctrls_data[ctrl]
            if connection:
                try:
                    cmds.connectAttr(connection, shape + '.v', f=True)
                except Exception as e:
                    print('Error with load_all_vis_connections: ', shape+'.v', connection, e)

        if self.to_delete:
            for node in self.to_delete:
                cmds.delete(node)

    #---------------------------------------------------------------------------

    def get_ctrl_colors(self, selection=[], long_name=True):

        ctrs_enciclopedia = {}

        if selection and long_name:
            selection = cmds.ls(selection, long=True)

        if not selection:
            if long_name:
                selection = cmds.ls(sl=True, long=True)
            else:
                selection = cmds.ls(sl=True)

        if not selection:
            # Getting all transforms in scene with the *trl termination.
            if long_name:
                selection = cmds.ls("*_*trl", type="transform", l=True)
            else:
                selection = cmds.ls("*_*trl", type="transform")

        all_ctrls = selection

        for ctrl in all_ctrls:
            # Getting ctrl attributes info.
            ctrl_info_dict = {}

            # 1) Get if the object has override on it's transform node. If it doesn't record it on the dictionary as false and move to the next part.
            if cmds.getAttr("{}.overrideEnabled".format(ctrl)) == 0:
                ctrl_info_dict["overrideEnabled"] = False

            # 2) If the object has override get the type of color.
            else:
                color_type = cmds.getAttr("{}.drawOverride.overrideRGBColors".format(ctrl))

                # 3) Acording to the type of color record RGB.
                if color_type:
                    transform_color = cmds.getAttr("{}.drawOverride.overrideColorRGB".format(ctrl))[0]

                else:
                    transform_color = cmds.getAttr("{}.drawOverride.overrideColor".format(ctrl))

                # Add result as info for the key 'overrideEnabled'.
                ctrl_info_dict["overrideEnabled"] = [color_type, transform_color]

            # 4) Get all curve shapes from the object.
            if long_name:
                ctrl_shapes = cmds.ls(cmds.listRelatives(ctrl, shapes=True, f=True), type="nurbsCurve", l=True)
            else:
                ctrl_shapes = cmds.ls(cmds.listRelatives(ctrl, shapes=True, f=True), type="nurbsCurve")

            if not ctrl_shapes:
                print("Control: '{}' has no shapes.".format(ctrl))
                continue

            # Created empty list to group dictionaries.
            shape_dictionaries = []

            for shape in ctrl_shapes:
                shape_info_dict = {}

                #Add alwaysDrawOnTop
                shape_info_dict["alwaysDrawOnTop"] = cmds.getAttr("{}.alwaysDrawOnTop".format(shape))

                # 5) For each shape get if they have color override and if they do record which color it is.
                if cmds.getAttr("{}.overrideEnabled".format(shape)) == 0:
                    shape_info_dict["shapeOverrideEnabled"] = False

                else:
                    shape_color_type = cmds.getAttr("{}.drawOverride.overrideRGBColors".format(shape))

                    # 6) Acording to the type of color record RGB for shape.
                    if shape_color_type:
                        shape_color = cmds.getAttr("{}.drawOverride.overrideColorRGB".format(shape))[0]

                    else:
                        shape_color = cmds.getAttr("{}.drawOverride.overrideColor".format(shape))

                    # Add result as info for the key 'overrideEnabled'.
                    shape_info_dict["shapeOverrideEnabled"] = [shape_color_type, shape_color]

                # 6) Add the shape dictionary to the main dictionary above.
                shape_dict = {shape: shape_info_dict}

                # 7) Appending shape disctionary to the group shape dictionary.
                shape_dictionaries.append(shape_dict)

            # 8) Apending finalized group shape dictionary to the ctrl info dictionary.
            ctrl_info_dict["shapes"] = shape_dictionaries

            # Grouping all attributes of the ctrl unders a single dictionary with it's name.
            ctrl_dict = {ctrl: ctrl_info_dict}

            ctrs_enciclopedia[ctrl] = ctrl_info_dict

        return ctrs_enciclopedia

    #---------------------------------------------------------------------------

    def apply_ctrls_color_data(self, colors_data={}, selection=[]):
        if not selection:
            selection = cmds.ls(sl=True, long=True)

        if not selection:
            selection = []
            for i in colors_data.keys():
                selection.append(i)
        
        color_problematic_ctrls = []

        for ctrl in colors_data:
                if ctrl in selection:
                    # Getting the info from the control's dictionary.
                    ctrl_info = colors_data[ctrl]
                    try:
                        # Checking if the transform's drawing override is on.
                        if ctrl_info["overrideEnabled"]:
                            # If Yes then turn it on.
                            cmds.setAttr("{}.overrideEnabled".format(ctrl), True)

                            # Extract which type of color it is. False = Index, True = Color.
                            if ctrl_info["overrideEnabled"][0]:
                                # If the type is RGB set it to True.
                                cmds.setAttr("{}.drawOverride.overrideRGBColors".format(ctrl), True)

                                # Set the 3 rgb colors.
                                r, g, b = ctrl_info["overrideEnabled"][1]
                                cmds.setAttr("{}.drawOverride.overrideColorRGB.overrideColorR".format(ctrl), r)
                                cmds.setAttr("{}.drawOverride.overrideColorRGB.overrideColorG".format(ctrl), g)
                                cmds.setAttr("{}.drawOverride.overrideColorRGB.overrideColorB".format(ctrl), b)

                            else:
                                # If the type is index set it to false.
                                cmds.setAttr("{}.drawOverride.overrideRGBColors".format(ctrl), False)
                                cmds.setAttr("{}.drawOverride.overrideColor".format(ctrl), ctrl_info["overrideEnabled"][1])

                        else:
                            cmds.setAttr("{}.overrideEnabled".format(ctrl), False)

                        # Getting shape dictionary lists.
                        shape_dictionaries = ctrl_info["shapes"]

                        #Getting current ctrl shapes. 
                        current_ctrl_shapes = cmds.ls(cmds.listRelatives(ctrl, shapes=True, f=True), type="nurbsCurve")
                        
                        #Setting a count for connecting current ctrl shapes. 
                        current_shape_number = 0

                        # Guesting each shape and dictionary.
                        for shape_dict in shape_dictionaries:
                            for shape in shape_dict:
                                shape_info = shape_dict[shape]

                                # Checking if the transform's drawing override is on.
                                try:
                                    if shape_info["alwaysDrawOnTop"]:
                                        cmds.setAttr(
                                            "{}.alwaysDrawOnTop".format(current_ctrl_shapes[current_shape_number]),
                                            True)
                                except Exception as e:
                                    cmds.warning(e)

                                if shape_info["shapeOverrideEnabled"]:
                                    # If Yes then turn it on.
                                    cmds.setAttr("{}.overrideEnabled".format(current_ctrl_shapes[current_shape_number]), True)

                                    # Extract which type of color it is. False = Index, True = Color.
                                    if shape_info["shapeOverrideEnabled"][0]:
                                        # If the type is RGB set it to True.
                                        cmds.setAttr("{}.drawOverride.overrideRGBColors".format(current_ctrl_shapes[current_shape_number]), True)

                                        # Set the 3 rgb colors.
                                        r, g, b = shape_info["shapeOverrideEnabled"][1]
                                        cmds.setAttr("{}.drawOverride.overrideColorRGB.overrideColorR".format(current_ctrl_shapes[current_shape_number]), r)
                                        cmds.setAttr("{}.drawOverride.overrideColorRGB.overrideColorG".format(current_ctrl_shapes[current_shape_number]), g)
                                        cmds.setAttr("{}.drawOverride.overrideColorRGB.overrideColorB".format(current_ctrl_shapes[current_shape_number]), b)

                                    else:
                                        # If the type is index set it to false.
                                        cmds.setAttr("{}.drawOverride.overrideRGBColors".format(current_ctrl_shapes[current_shape_number]), False)
                                        cmds.setAttr("{}.drawOverride.overrideColor".format(current_ctrl_shapes[current_shape_number]),
                                                    shape_info["shapeOverrideEnabled"][1])
                                else:
                                    cmds.setAttr("{}.overrideEnabled".format(current_ctrl_shapes[current_shape_number]), False)

                            #Adding value to the counter to move on to next shape.
                            current_shape_number = current_shape_number + 1
                    except:
                        color_problematic_ctrls.append(ctrl)
        if color_problematic_ctrls: print(color_problematic_ctrls)

    #---------------------------------------------------------------------------

    def store_ctrl_cvs_world(self, ctrls='All'):
        data = {}

        if ctrls == 'All':
            all_ctrls = cmds.ls('*{}'.format(nc['ctrl']), type='transform')
        elif ctrls == 'Selected':
            all_ctrls = cmds.ls(sl=True, type='transform')
        else:
            all_ctrls = cmds.ls(ctrls, type='transform')

        for ctrl in all_ctrls or []:
            shapes = cmds.listRelatives(ctrl, shapes=True, type='nurbsCurve') or []
            if not shapes:
                continue

            data[ctrl] = {}

            for shape in shapes:
                cvs = cmds.ls('{}.cv[*]'.format(shape), fl=True) or []
                positions = []

                for cv in cvs:
                    pos = cmds.xform(cv, q=True, ws=True, t=True)
                    positions.append(pos)

                data[ctrl][shape] = positions

        return data

    #---------------------------------------------------------------------------

    def restore_ctrl_cvs_world(self, data):
        if not data:
            return

        if om2 is None:
            cmds.warning('maya.api.OpenMaya not available. Cannot load world ctrl CVs.')
            return

        for ctrl, shapes in data.items():
            if not cmds.objExists(ctrl):
                continue

            try:
                selection_list = om2.MSelectionList()
                selection_list.add(ctrl)
                dag = selection_list.getDagPath(0)
                world_matrix = dag.inclusiveMatrix()
                inv_world_matrix = world_matrix.inverse()
            except Exception as e:
                print('Error getting world matrix for {}: {}'.format(ctrl, e))
                continue

            for shape, positions in shapes.items():
                if not cmds.objExists(shape):
                    continue

                cvs = cmds.ls('{}.cv[*]'.format(shape), fl=True) or []

                for index, pos in enumerate(positions):
                    if index >= len(cvs):
                        continue
                    try:
                        world_point = om2.MPoint(pos)
                        object_point = world_point * inv_world_matrix
                        cmds.xform(cvs[index], os=True, t=[object_point.x, object_point.y, object_point.z])
                    except Exception as e:
                        print('Error restoring {} {}: {}'.format(shape, index, e))

    #---------------------------------------------------------------------------

    def save_world_ctrls(self, ctrls='All', path=None, force_validate=False):
        if not path:
            path = mh.export_window(extension='.json')
            if path:
                path = path[0]

        if not path:
            return False

        data = self.store_ctrl_cvs_world(ctrls=ctrls)
        if not data:
            cmds.warning('No controller curves found to save world positions.')
            return False

        self.saveData(path=path, data=data, force_validate=force_validate)
        return True

    #---------------------------------------------------------------------------

    @undo
    def load_world_ctrls(self, path=None):
        if path is None:
            path = mh.import_window(extension='.json')
            if path:
                path = path[0]

        if not path:
            return False

        if not os.path.isfile(path):
            cmds.warning('Path doesnt exists', path)
            return False

        data = self.loadData(path)
        self.restore_ctrl_cvs_world(data)
        return True

