from __future__ import absolute_import, division
from maya import cmds
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

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_lattice'

#---------------------------------------------

def create_lattice_block(name = 'Lattice'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '05_Lattice.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Lattice',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_lattice_block()

#-------------------------

def build_lattice_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    #groups for later cleaning
    clean_rig_grp = ''
    clean_ctrl_grp = ''
    
    size = cmds.getAttr('{}.CtrlSize'.format(config))
    color = cmds.getAttr('{}.CtrlColor'.format(config), asString=True)
    geo = cmds.getAttr('{}.SetGeo'.format(config))
    local_mode =  cmds.getAttr('{}.Local'.format(config))

    if geo == 'new_cube':
        geo = cmds.polyCube(n='geo_'+name, sx=2,sy=2,sz=2)
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)
    if attrs_position == 'new_locator':
        attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
    mt.line_attr(input=attrs_position, name=name)
    vis_attr = mt.new_enum(input=attrs_position, name=name+'Vis', enums='Hide:Show')

    #create lattice
    if ',' in geo:
        geo = geo.split(',')
    cmds.select(geo)
    lattice_deformer = cmds.lattice(divisions=(3, 2, 2), objectCentered=True, ldv=(3, 2, 2), ol=False,
                                    n='{}_Lat_'.format(name), outsideLattice=1)

    cmds.setAttr('{}.outsideLattice'.format(lattice_deformer[0]), 1)

    all_clusters = []
    auto_grps = []
    ctrls =[]
    ctrls_grps = []

    all_cls_group = cmds.group(n=name+'_Clusters'+nc['group'], em=True)
    mt.match(this=all_cls_group, that=lattice_deformer[1], t=True, s=False)
    clean_ctrl_grp = cmds.group(n=name+nc['ctrl']+nc['group'], em=True)
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))

    for loop in range(3):

        #This is a bad code i know pls dont judge me :)
        loop_clusters = []
        loop_ctrls = []

        #cluster with controller per point

        loop_cls_group = cmds.group(n=name + '_{}_LoopCls'.format(loop) + nc['group'], em=True)
        mt.match(this=loop_cls_group, that=lattice_deformer[1], t=True, s=False)
        ctrls_grps.append(loop_cls_group)

        #Overral ctrl
        main_ctrl = mt.curve(
            type='octagon',
            rename=True,
            custom_name=True,
            name=name+'_Main_'+str(loop)+nc['ctrl'],
            size=size)
        main_root = mt.root_grp()
        cmds.parent(main_root, clean_ctrl_grp)
        mt.assign_color(main_ctrl, color)
        mt.match(this=main_ctrl, that=lattice_deformer[1], t=True, s=False)

        #vertex cluster
        cmds.select('{}.pt[{}][0][0]'.format(lattice_deformer[1], loop))
        cls1=cmds.cluster(n='{}_{}00{}'.format(name,loop ,nc['cluster']), rel=False)
        loop_clusters.append(cls1)
        ctrl1 = mt.curve(
                        type='hexagon',
                        rename=True,
                        custom_name=True,
                        name=cls1[1].replace(nc['cluster']+'Handle', nc['ctrl']),
                        size=size/2)
        loop_ctrls.append(ctrl1)
        mt.hide_attr(t=False, r=True, s=True)
        mt.assign_color(color = color)
        cmds.parent(mt.root_grp()[0], main_ctrl)
        cmds.connectAttr('{}.translate'.format(ctrl1), '{}.translate'.format(cls1[1]))
        cmds.connectAttr('{}.rotate'.format(ctrl1), '{}.rotate'.format(cls1[1]))
        cmds.connectAttr('{}.scale'.format(ctrl1), '{}.scale'.format(cls1[1]))

        cmds.select('{}.pt[{}][1][1]'.format(lattice_deformer[1], loop))
        cls2=cmds.cluster(n='{}_{}11{}'.format(name,loop, nc['cluster']), rel=False)
        loop_clusters.append(cls2)
        ctrl2 = mt.curve(
                        type='hexagon',
                        rename=True,
                        custom_name=True,
                        name=cls2[1].replace(nc['cluster']+'Handle', nc['ctrl']),
                        size=size/2)
        loop_ctrls.append(ctrl2)
        mt.hide_attr(t=False, r=True, s=True)
        mt.assign_color(color = color)
        cmds.parent(mt.root_grp()[0], main_ctrl)
        cmds.connectAttr('{}.translate'.format(ctrl2), '{}.translate'.format(cls2[1]))
        cmds.connectAttr('{}.rotate'.format(ctrl2), '{}.rotate'.format(cls2[1]))
        cmds.connectAttr('{}.scale'.format(ctrl2), '{}.scale'.format(cls2[1]))

        cmds.select('{}.pt[{}][0][1]'.format(lattice_deformer[1], loop))
        cls3=cmds.cluster(n='{}_{}01{}'.format(name,loop, nc['cluster']), rel=False)
        loop_clusters.append(cls3)
        ctrl3 = mt.curve(
                        type='hexagon',
                        rename=True,
                        custom_name=True,
                        name=cls3[1].replace(nc['cluster']+'Handle', nc['ctrl']),
                        size=size/2)
        loop_ctrls.append(ctrl3)
        mt.hide_attr(t=False, r=True, s=True)
        mt.assign_color(color = color)
        cmds.parent(mt.root_grp()[0], main_ctrl)
        cmds.connectAttr('{}.translate'.format(ctrl3),'{}.translate'.format(cls3[1]))
        cmds.connectAttr('{}.rotate'.format(ctrl3),'{}.rotate'.format(cls3[1]))
        cmds.connectAttr('{}.scale'.format(ctrl3),'{}.scale'.format(cls3[1]))

        cmds.select('{}.pt[{}][1][0]'.format(lattice_deformer[1], loop))
        cls4=cmds.cluster(n='{}_{}10{}'.format(name,loop, nc['cluster']), rel=False)
        loop_clusters.append(cls4)
        ctrl4 = mt.curve(
                        type='hexagon',
                        rename=True,
                        custom_name=True,
                        name=cls4[1].replace(nc['cluster']+'Handle', nc['ctrl']),
                        size=size/2)
        loop_ctrls.append(ctrl4)
        mt.assign_color(color = color)
        mt.hide_attr(t=False, r=True, s=True)
        cmds.parent(mt.root_grp()[0], main_ctrl)
        cmds.connectAttr('{}.translate'.format(ctrl4),'{}.translate'.format(cls4[1]))
        cmds.connectAttr('{}.rotate'.format(ctrl4),'{}.rotate'.format(cls4[1]))
        cmds.connectAttr('{}.scale'.format(ctrl4),'{}.scale'.format(cls4[1]))

        all_clusters.append(loop_clusters)
        cmds.delete(cmds.parentConstraint(cls1, cls2, cls3, cls4, loop_cls_group))
        cmds.makeIdentity(loop_cls_group, a=True, t=True, r=True, s=True)
        root, auto = mt.root_grp(input=loop_cls_group, autoRoot=True)
        auto_grps.append(auto)
        cmds.parent(root, all_cls_group)

        cmds.parent(cls1, cls2, cls3, cls4, loop_cls_group)
        print(loop_clusters)
        ctrls.append(loop_ctrls)

        #connect main crl to auto grp
        #change pivot to auto
        childs = cmds.listRelatives(main_ctrl, c=True, type='transform')
        print(childs)
        cmds.parent(childs, w=True)
        mt.match(this=main_root, that=auto, t=True)
        cmds.parent(childs, main_ctrl)

        #pivot = cmds.xform(auto ,rp =True, q=True, ws=True)
        #cmds.move(pivot[0],pivot[1],pivot[2], "{}.scalePivot".format(main_ctrl),"{}.rotatePivot".format(main_ctrl), absolute=True)
        cmds.connectAttr('{}.translate'.format(main_ctrl),'{}.translate'.format(auto))
        cmds.connectAttr('{}.rotate'.format(main_ctrl),'{}.rotate'.format(auto))
        cmds.connectAttr('{}.scale'.format(main_ctrl),'{}.scale'.format(auto))

        cmds.connectAttr(vis_attr, cmds.listRelatives(main_ctrl, s=True)[0]+'.v')

        for ctrl in [ctrl1,ctrl2,ctrl3,ctrl4]:
            for s in cmds.listRelatives(ctrl, s=True):
                cmds.connectAttr(vis_attr, s+'.v')

    #Clean a bit
    cmds.parent(lattice_deformer, all_cls_group, clean_rig_grp)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    if not local_mode:
        cmds.parentConstraint(block_parent, '{}_Lat_Base'.format(name), mo=True)
        cmds.parentConstraint(block_parent, all_cls_group, mo=True)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])



    print ('Build {} Success'.format(block))



#build_lattice_block()
