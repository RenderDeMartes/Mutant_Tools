from maya import cmds, OpenMaya
import json
import imp
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '03_Facial'
PYBLOCK_NAME = 'exec_eyelids'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'04_Eyelids.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)


# ---------------------------------------------

def create_eyelids_block(name='Nose'):
	# name checks and block creation
	name = mt.ask_name(text=module['Name'])
	if cmds.objExists('{}{}'.format(name, nc['module'])):
		cmds.warning('Name already exists.')
		return ''

	block = mt.create_block(name=name, icon='Nose', attrs=module['attrs'], build_command=module['build_command'],
							import_command=module['import'])
	config = block[1]
	block = block[0]

	cmds.select(block)

	print('{} Created Successfully'.format(name))


# create_nose_block()

# -------------------------

def build_eyelids_block():
	mt.check_is_there_is_base()

	block = cmds.ls(sl=True)
	config = cmds.listConnections(block)[1]
	block = block[0]
	guide = cmds.listRelatives(block, c=True)[0]
	name = guide.replace(nc['guide'], '')

	# use this locator in case parent is set to new locator
	if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
		block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))
	else:
		block_parent = cmds.getAttr('{}.SetParent'.format(config))

	ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))


#Video give us this ones

def getUParam(pnt=[], crv=None):
    point = OpenMaya.MPoint(pnt[0], pnt[1], pnt[2])
    curveFn = OpenMaya.MFnNurbsCurve(getDagPath(crv))
    paramUtill = OpenMaya.MScriptUtil()
    paramPtr = paramUtill.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve == True:

        curveFn.getParamAtPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)
    else:
        point = curveFn.closestPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)
        curveFn.getParamAtPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)

    param = paramUtill.getDouble(paramPtr)
    return param


def getDagPath(objectName):
    if isinstance(objectName, list) == True:
        oNodeList = []
        for o in objectName:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(o)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            oNodeList.append(oNode)
        return oNodeList
    else:
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(objectName)
        oNode = OpenMaya.MDagPath()
        selectionList.getDagPath(0, oNode)
        return oNode

#Created during video

'''
#instrucciones
video 1
create locator in center of eye
create up vector for center of eye
crear cadenas de joint por vertices 1 en el centro y otro en el vertice, oritnarlos para que queden viendo bien
create a locator in every eye end jnt
aim constraint del locator nuevo al centro del ojo

video 2

LINEAR!!! crear curva cv per vtx LINEAR!!!!
usar getUParam(pos_locator, curva) para para saber donde poner cada locator en la curva
point on curve info para poner el locator que tiene al aim en el upParam que conseguimos

Crear una curva cubica con 5 puntos, 2 bordes, 1 centro y 2 medios (Creo que duplicar y rebuild es la forma para que haga match)
recordar poner en degree 3 
 
Conectar la curva con 5 puntos a la linear por wire
crear 5 controlles en los 5 puntos de la curva de 5 puntos (las esquinas pueden ser compartidas)
crear 5 joints para binder a la curva de 5 puntos y esos joints son controlados por los 5 controles

los controles de del medio deben moverse con el centro y la esquina50/50

video 3 smart blink



'''


















