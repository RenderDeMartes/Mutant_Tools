'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

import imp
import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import CtrlUtils
imp.reload(Mutant_Tools.Utils.IO.CtrlUtils)

ctrls = CtrlUtils.Ctrls()
ctrls.FUNC_NAME(argument = '')

#----------------
dependencies:

NG

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

import os
import imp
import json
from maya import cmds as cmds
from maya import OpenMaya as om

import Mutant_Tools
from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

# ---------------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\Utils\\IO', '//Config')

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
SETUP_FILE = (PATH +'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

# ---------------------------------------------------------------------------

class Ctrls(object):

    #Thanks to: https://github.com/vshotarov/controlShapeManager/blob/master/utils.py
    #Thanks To: https://bindpose.com/creating-maya-control-shape-manager/

    #---------------------------------------------------------------------------

    def validateCurve(self, crv=None):
        if cmds.nodeType(crv) == "transform" or cmds.nodeType(cmds.listRelatives(crv, c=1, s=1)[0]) == "nurbsCurve":
            crvShapes = cmds.listRelatives(crv, c=1, s=1)

        elif cmds.nodeType(crv) == "nurbsCurve":
            crvShapes = cmds.listRelatives(cmds.listRelatives(crv, p=1)[0], c=1, s=1)

        return_list = []
        for node in crvShapes:
            if cmds.nodeType(node) == 'locator':
                continue
            else:
                return_list.append(node)

        return return_list

    #---------------------------------------------------------------------------

    def getShape(self, crv=None):
        crvShapes = self.validateCurve(crv)

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
        mObj = om.MObject()
        sel = om.MSelectionList()
        sel.add(crvShape)
        sel.getDependNode(0, mObj)

        fnCurve = om.MFnNurbsCurve(mObj)
        tmpKnots = om.MDoubleArray()
        fnCurve.getKnots(tmpKnots)

        return [tmpKnots[i] for i in range(tmpKnots.length())]

    #---------------------------------------------------------------------------

    def setShape(self, crv, crvShapeList):
        crvShapes = self.validateCurve(crv)

        oldColour = cmds.getAttr(crvShapes[0] + ".overrideColor")
        cmds.delete(crvShapes)

        for i, crvShapeDict in enumerate(crvShapeList):
            tmpCrv = cmds.curve(p=crvShapeDict["points"], k=crvShapeDict["knots"], d=crvShapeDict["degree"], per=bool(crvShapeDict["form"]))
            newShape = cmds.listRelatives(tmpCrv, s=1)[0]
            cmds.parent(newShape, crv, r=1, s=1)

        cmds.delete(tmpCrv)
        newShape = cmds.rename(newShape, crv + "Shape" + str(i + 1).zfill(2))

        #cmds.setAttr(newShape + ".overrideEnabled", 1)
        cmds.setAttr(newShape + ".lineWidth", int(setup['line_width']))

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

    def saveData(self, path=None,data=None):

        if self.validatePath(path):
            f = open(path, "w")
            f.write(json.dumps(data, sort_keys=1, indent=4, separators=(",", ":")))
            f.close()
            return 1
        return 0

    #---------------------------------------------------------------------------

    def validatePath(self, path=None):
        '''Checks if the file already exists and provides a dialog to overwrite or not'''
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
    def save_all(self):
        #ctrls.save_all('C:\\Users\\PC\\Desktop\\ctrls.json')
        path = mh.export_window(extension = ".json")
        if not path:
            return
        path = path[0]
        all_ctrls = {}
        cmds.select('*{}'.format(nc['ctrl']))
        for ctrl in cmds.ls(sl=True):
            data = self.getShape(ctrl)
            all_ctrls[ctrl] = data

        self.saveData(path=path, data=all_ctrls)

    #---------------------------------------------------------------------------
    def load_all(self, path=None):
        #ctrls.load_all('C:\\Users\\PC\\Desktop\\ctrls.json')
        if path is None:
            path = mh.import_window(extension = ".json")
            path = path[0]
        if not path:
            return False

        data = self.loadData(path)
        cmds.select('*{}'.format(nc['ctrl']))
        for ctrl in cmds.ls(sl=True):
            try:
                shape_data = data[ctrl]
                self.setShape(ctrl, shape_data)
                self.reparent_locators(ctrl)
            except:
                print ('Error with: {}'.format(ctrl))

    #---------------------------------------------------------------------------
    def mirror_all(self):

        cmds.select('*{}'.format(nc['ctrl']))
        for ctrl in cmds.ls(sl=True):
            cmds.select(ctrl)
            self.mirrorCtlShapes()

        cmds.select(cl=True)

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