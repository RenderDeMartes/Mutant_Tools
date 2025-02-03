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
PYBLOCK_NAME = 'exec_wings'

#---------------------------------------------

def create_wings_block(name = 'Wings'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    import Mutant_Tools
    from Mutant_Tools.Utils.External.RdMWings import autoWings, wingModule, BindFeathers, autoFold
    reload(autoWings)
    reload(wingModule)
    reload(BindFeathers)
    reload(autoFold)

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '01_Wings.json')
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

    if cmds.objExists('L_Clav_Guide'):
        cmds.warning('Only one wings sysmtem can be build per Scene sorry.')
        return ''

    if cmds.objExists('L_Clav_Jnt'):
        cmds.warning('Only one wings sysmtem can be build per Scene sorry.')
        return ''

    scap_amount= int(mt.ask_name(ask_for='Scapular Amount', text = 5))
    sec_amount= int(mt.ask_name(ask_for='Secundary Amount', text = 8))
    prim_amount= int(mt.ask_name(ask_for='Primary Amount', text = 10))


    block = mt.create_block(name = name, icon = 'Wing',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    mt.new_attr(input=config, name='Scapular', min=0, max=100000, default=scap_amount)
    mt.new_attr(input=config, name='Secundary', min=0, max=100000, default=sec_amount)
    mt.new_attr(input=config, name='Primary', min=0, max=100000, default=prim_amount)

    autoWings.CreateJoints()
    autoWings.buildWingsRef(
        ScapAmount=scap_amount,
        ScaptBack=5,
        SecAmount=sec_amount,
        SecBack=5,
        PrimAmount=prim_amount,
        PrimBack=5)

    spec_root = mt.root_grp(input='L_Scapulars_Guide_Wing_000')
    sec_root = mt.root_grp(input='L_Secondaries_Guide_Wing_000')
    prim_root = mt.root_grp(input='L_Primaries_Guide_Wing_000')

    cmds.parentConstraint('L_Scapulars_Guide', spec_root, mo =True)
    cmds.parentConstraint('L_Secondaries_Guide', sec_root, mo=True)
    cmds.parentConstraint('L_Primaries_Guide', prim_root, mo=True)

    cmds.parent('L_Clav_Guide',spec_root, sec_root, prim_root, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_wings_block()

#-------------------------

def build_wings_block():

    import Mutant_Tools
    from Mutant_Tools.Utils.External.RdMWings import autoWings, wingModule, BindFeathers, autoFold
    reload(autoWings)
    reload(wingModule)
    reload(BindFeathers)
    reload(autoFold)

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'],'')


    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    #create correct guide
    guide_roots = ['L_Clav_Guide', 'L_Primaries_Guide_Wing_000', 'L_Secondaries_Guide_Wing_000',
                   'L_Scapulars_Guide_Wing_000']
    for guide in guide_roots:
        new_guide = cmds.duplicate(guide, n=guide.replace('Guide', 'JR'), rr=True)[0]
        cmds.parent(new_guide, w=True)
        for jnt in cmds.listRelatives(new_guide, ad=True, f=True):
            if 'Guide' in jnt:
                cmds.select(jnt)
                mel.eval('searchReplaceNames {} {} "selected"'.format('Guide', 'JR'))

    autoWings.buildWingsSystem(
        ScapAmount=int(cmds.getAttr('{}.Scapular'.format(config))),
        ScaptBack=1,
        SecAmount=int(cmds.getAttr('{}.Secundary'.format(config))),
        SecBack=1,
        PrimAmount=int(cmds.getAttr('{}.Primary'.format(config))),
        PrimBack=1,
        sizeUI=1)

    cmds.rename('GlobalLoc', 'L_GlobalLoc')

    autoWings.getPivot(side='L', part='Primaries')
    autoWings.getPivot(side='L', part='Secondaries')
    autoWings.getPivot(side='L', part='Scapulars')

    cmds.rename('WingRef_Loc', 'L_WingRef_Loc')

    autoWings.mirrorWing()

    cmds.parent('L_Wing_AutoRig','Ctrl_Grp')
    cmds.parent('R_Wing_AutoRig_Mirror_GRP','Ctrl_Grp')

    #Quick fixes to make it cleaner for anim
    cmds.rename('L_Wing_CC', 'L_Wing_Ctrl')
    cmds.rename('R_Wing_CC', 'R_Wing_Ctrl')

    #clean the outliner
    cmds.parent('L_GlobalLoc', 'L_GlobalLoc','L_WingRef_Loc', 'R_WingRef_Loc','L_Wing_Nurbs_GRP', 'R_Wing_Nurbs_GRP', clean_rig_grp)
    for c in cmds.listRelatives('L_Wing_AutoRig', type='joint', ad=True):
        cmds.setAttr('{}.drawStyle'.format(c), 2)
    for c in cmds.listRelatives('R_Wing_AutoRig_Mirror_GRP', type='joint', ad=True):
        cmds.setAttr('{}.drawStyle'.format(c), 2)

    #Block aprent connections
    cmds.parentConstraint(block_parent, 'L_Clavicle_JC_Root', mo=True)
    cmds.parentConstraint(block_parent, 'R_Clavicle_JC_Root', mo=True)
    cmds.scaleConstraint(block_parent, 'L_Clavicle_JC_Root', mo=True)
    cmds.scaleConstraint(block_parent, 'R_Clavicle_JC_Root', mo=True)

    #Update curves to be 2 line
    curves = cmds.ls('*_Ctrl')
    for c in curves:
        cmds.setAttr(c+'.lineWidth', 2)

    #Create bind joints

    feathers = {

    'Clavicles' : ['L_Clav_JR','R_Clav_JR'],

    'Scapulars' : ['*_Scapulars_JR', '*_Scapulars_JR_Wing_*'],
    'Secundaries' : ['*_Secondaries_JR', '*_Secondaries_JR_Wing_*'],
    'Primaries' : ['*_Primaries_JR', '*_Primaries_JR_Wing_*'],

    'Scauplars_feathers' : ['*_Scapulars_JR_Fthr_*', '*_Scapulars_JR_Fthr_*Bend*'],
    'Secondaries_feathers' : ['*_Secondaries_JR_Fthr_*', '*_Secondaries_JR_Fthr_*Bend*'],
    'Primaries_feathers' : ['*_Primaries_JR_Fthr_*', '*_Primaries_JR_Fthr_*Bend*']
                }
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    for f in feathers:
        grp = cmds.group(em=True, n=f+'_Bnd'+'_Grp')
        cmds.parent(grp, bind_jnt_grp)
        joints = cmds.ls(feathers[f], type='joint')
        for jnt in joints:
            cmds.select(cl=True)
            if cmds.objExists(jnt + nc['joint_bind']):
                continue
            bind_joint = cmds.joint(n=jnt + nc['joint_bind'])
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, grp)

        # Fix R Swing Wings
        primaries_grp = cmds.ls('R_Primaries_JR_Fthr_0*_Ctrl_Auto_Grp')
        secundaries_grp = cmds.ls('R_Secondaries_JR_Fthr_0*_Ctrl_Auto_Grp')
        scauplars_grp = cmds.ls('R_Scapulars_JR_Fthr_00*_Ctrl_Auto_Grp')

        for grp in primaries_grp:
            cmds.connectAttr('R_Wing_Ctrl.PrimariesSwing', grp + '.rotateZ', f=True)
        for grp in secundaries_grp:
            cmds.connectAttr('R_Wing_Ctrl.SecondariesSwing', grp + '.rotateZ', f=True)
        for grp in scauplars_grp:
            cmds.connectAttr('R_Wing_Ctrl.ScapularsSwing', grp + '.rotateZ', f=True)

    print ('Build {} Success'.format(block))



#build_wings_block()
