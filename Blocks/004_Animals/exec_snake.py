from __future__ import absolute_import
from maya import cmds, mel
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '004_Animals'
PYBLOCK_NAME = 'exec_snake'

#---------------------------------------------

def create_snake_block(name = 'Snake'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------


    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '04_Snake.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    amount = int(mt.ask_name(text=10, ask_for='Joints Amount'))

    block = mt.create_block(name = name, icon = 'Snake',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    curve = mel.eval('curve -d 3 -p 0 0 4 -p 0 0 3.666667 -p 0 0 3 -p 0 0 2 -p 0 0 1 -p 0 0 0 -p 0 0 -1 -p 0 0 -2 -p 0 0 -3 -p 0 0 -4 -p 0 0 -4.666667 -p 0 0 -5 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 9 -k 9 -n {};'.format(name+'_Border'+nc['guide']))
    curve = mel.eval('rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s {} -d 3 -tol 0.0001 "{}";'.format(amount, curve))

    cmds.parent(curve, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_snake_block()

#-------------------------

def build_snake_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'],'')


    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #ctrls_amount = int(cmds.getAttr('{}.CtrlsAmount'.format(config)))

    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    #Build the rig

    #Create a joint pe vtx
    cvs = cmds.getAttr('{}.spans'.format(guide)) + 1
    ik_joints = []
    ctrl_joints = []

    ctrl_joints_group = cmds.group(em=True, n=name+nc['ctrl']+nc['joint']+nc['group'])

    for num in range(cvs+2):
        pos = cmds.xform('{}.cv[{}]'.format(guide, num), ws=True, t=True, q=True)
        print(pos)
        cmds.select(cl=True)
        jnt = cmds.joint(n='{}_{}{}'.format(name, num, nc['joint']))
        ik_joints.append(jnt)
        cmds.xform(jnt, t=pos)
        try:
            cmds.parent(jnt, ik_joints[num-1])
        except:
            pass

        #Create ctrl joints
        cmds.select(cl=True)
        ctrl_jnt = cmds.joint(n='{}_{}{}{}'.format(name, num, nc['ctrl'],  nc['joint']))
        ctrl_joints.append(ctrl_jnt)
        cmds.xform(ctrl_jnt, t=pos)
        cmds.parent(ctrl_jnt, ctrl_joints_group)

    #Duplicate the curve to use on ik spline
    curve = cmds.duplicate(guide, n=name+'_IkCurve')[0]
    cmds.parent(curve, w=True)

    #Create ik spline
    ik_spline = cmds.ikHandle(sj=ik_joints[0],
                                  ee=ik_joints[-1],
                                  sol='ikSplineSolver',
                                  n=name + nc['ik_sc'],
                                  createCurve=False,
                                  parentCurve=False,
                                  c=curve
                                  )
    ik_spline_curve = ik_spline[-1]
    print(ik_spline)

    #Skin the Curve
    cmds.skinCluster(ctrl_joints, curve)

    #Create ctrls per ctrl joint
    ctrl_grp = cmds.group(em=True, n=name+'_Tweeks'+nc['ctrl']+nc['group'])
    ctrls = []
    for jnt in ctrl_joints:
        ctrl = mt.curve(  input=jnt,
                          type='cross',
                          rename=True,
                          custom_name=True,
                          name=jnt.replace(nc['joint'], nc['ctrl']),
                          size=1)

        mt.assign_color(color='purple')
        root_grp = mt.root_grp()[0]
        mt.match(root_grp, jnt, r=True, t=True)
        cmds.parentConstraint(ctrl, jnt)
        ctrls.append(ctrl)
        cmds.parent(root_grp, ctrl_grp)

    # create bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    for jnt in ik_joints:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)

    #Parent the system
    cmds.parentConstraint(block_parent, clean_ctrl_grp)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp)

    cmds.parent(ctrl_grp, clean_ctrl_grp)
    cmds.parent(ik_spline[0], curve, ik_joints[0], ctrl_joints_group, clean_rig_grp)

    print ('Build {} Success'.format(block))



#build_snake_block()
