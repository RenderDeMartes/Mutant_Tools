from __future__ import absolute_import
from maya import cmds, mel
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import os
from pathlib import Path
from Mutant_Tools.Utils.External import Ribbonizer
reload(Ribbonizer)
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '005_Clothes'
PYBLOCK_NAME = 'exec_cape'

#---------------------------------------------

def create_cape_block(name = 'Cape'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '07_Cape.json')
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

    block = mt.create_block(name = name, icon = 'Cape',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    names = ['L','LC','C','RC','R']
    nurbs_guides = []
    for num, i in enumerate(names):
        guide = mel.eval('nurbsPlane -p 0 -2.5 0 -ax 0 0 1 -w 1 -lr 5 -d 3 -u 1 -v 4 -ch 0 -n {}_{}{};'.format(i, name,  nc['guide']))[0]
        nurbs_guides.append(guide)
        cmds.rotate(0,180,0)
        cmds.move(0,6,0)

    cmds.move(4,6,0, nurbs_guides[0])
    cmds.move(2,6,0, nurbs_guides[1])

    cmds.move(-2,6,0, nurbs_guides[-2])
    cmds.move(-4,6,0, nurbs_guides[-1])


    cmds.parent(nurbs_guides, block)


    cmds.select(block)
    print('{} Created Successfully'.format(name))

#create_cape_block()

#-------------------------

def build_cape_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = block.replace(nc['module'],'')


    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    #Build

    sides = ['L', 'LC', 'C', 'RC', 'R']
    master_ctrls = []
    autos = []

    for num, guide in enumerate(guides):

        new_guide = cmds.duplicate(guide, n=guide.replace(nc['guide'], nc['nurb']))
        cmds.parent(new_guide, w=True)
        ctrl_grp, rig_grp, bnd_grp = Ribbonizer.ribbonize(surf_tr=new_guide,
                                                          equal=True,
                                                          num_of_Ctrls=5,
                                                          num_of_Jnts=10,
                                                          prefix=new_guide[0].replace(nc['nurb'], ''),
                                                          constrain=True,
                                                          add_fk=True,
                                                          wire=False,
                                                          middle_ctrl_pos='Start')

        master_ctrl = new_guide[0].replace(nc['nurb'], '') + '_Main' + nc['ctrl']
        master_ctrls.append(master_ctrl)
        root, auto = mt.root_grp(input = master_ctrl, autoRoot=True)
        autos.append(auto)

        cmds.parent(ctrl_grp, clean_ctrl_grp)
        cmds.parent(rig_grp, clean_rig_grp)
        cmds.parent(bnd_grp, bind_jnt_grp)

    #Create num controllers for overall movement
    old_root = None
    root_grps = []
    main_ctrls = []
    for i in range(4):
        center_fk_controller = 'C_{}_fk_0{}_Ctrl'.format(name, i)
        new_center_ctrl = mt.curve( input=center_fk_controller,
                          type='pringle',
                          rename=True,
                          custom_name=True,
                          name=center_fk_controller.replace(nc['ctrl'], '_Main'+nc['ctrl']),
                          size=5)

        mt.assign_color(color='purple')
        root_grp = mt.root_grp()[0]
        root_grps.append(root_grp)
        mt.match(root_grp, center_fk_controller, r=True, t=True)
        main_ctrls.append(new_center_ctrl)
        # Organize
        if old_root:
            cmds.parent(root_grp, cmds.listRelatives(old_root, c=True))
        old_root = root_grp

        #Fix orientation
        cmds.select(new_center_ctrl+'.cv[0:42]')
        cmds.rotate(0,0,90)

        auto_grps = []
        for side in sides:
            fk_ctrl = '{}_{}_fk_0{}_Ctrl'.format(side, name, i)
            fk_auto = mt.root_grp(input=fk_ctrl)[0]

            #change pivot
            pivot = cmds.xform(new_center_ctrl ,rp =True, q=True, ws=True)
            cmds.move(pivot[0],pivot[1],pivot[2], "{}.scalePivot".format(fk_auto),"{}.rotatePivot".format(fk_auto), absolute=True)

            cmds.connectAttr('{}.translate'.format(new_center_ctrl) , '{}.translate'.format(fk_auto))
            cmds.connectAttr('{}.rotate'.format(new_center_ctrl) , '{}.rotate'.format(fk_auto))
            cmds.connectAttr('{}.scale'.format(new_center_ctrl) , '{}.scale'.format(fk_auto))

    #Organize
    cmds.parent(root_grps[0], clean_ctrl_grp)

    #Create last controller
    center_ik_controller = 'C_{}_04_Ctrl'.format(name)
    last_center_ctrl = mt.curve(input=center_ik_controller,
                               type='pringle',
                               rename=True,
                               custom_name=True,
                               name=center_ik_controller.replace(nc['ctrl'], '_Main' + nc['ctrl']),
                               size=5)

    mt.assign_color(color='orange')
    root_grp = mt.root_grp()[0]
    mt.match(root_grp, center_ik_controller, r=True, t=True)
    # Fix orientation
    cmds.select(last_center_ctrl + '.cv[0:42]')
    cmds.rotate(0, 0, 90)
    cmds.parent(root_grp, cmds.listRelatives(root_grps[-1], c=True))
    root_grps.append(root_grp)
    for side in sides:
        ik_ctrl = '{}_{}_04_Ctrl'.format(side, name, i)
        ik_auto, ik_root = mt.root_grp(input=ik_ctrl, autoRoot=True)

        # change pivot
        pivot = cmds.xform(last_center_ctrl, rp=True, q=True, ws=True)
        cmds.move(pivot[0], pivot[1], pivot[2], "{}.scalePivot".format(ik_auto), "{}.rotatePivot".format(ik_auto),
                  absolute=True)

        cmds.connectAttr('{}.translate'.format(last_center_ctrl), '{}.translate'.format(ik_auto))
        cmds.connectAttr('{}.rotate'.format(last_center_ctrl), '{}.rotate'.format(ik_auto))
        cmds.connectAttr('{}.scale'.format(last_center_ctrl), '{}.scale'.format(ik_auto))
    main_ctrls.append(last_center_ctrl)

    #Add Shared locator
    all_ctrls = cmds.ls('*{}*{}'.format(name, nc['ctrl']))
    for ctrl in all_ctrls:
        cmds.select(ctrl)
        if cmds.objectType(ctrl) == 'transform':
            spine_attrs_loc = mt.shape_with_attr(input='', obj_name='{}_Attrs'.format(name), attr_name='').split('.')[0]

    print(spine_attrs_loc)

    #Vis attrs
    show_main_attr = mt.new_enum(input=spine_attrs_loc, name='Main', enums='Hide:Show')
    show_fk_attr = mt.new_enum(input=spine_attrs_loc, name='FK', enums='Hide:Show')
    show_ik_attr = mt.new_enum(input=spine_attrs_loc, name='IK', enums='Hide:Show')

    for ctrl in all_ctrls:
        cmds.connectAttr(show_ik_attr, cmds.listRelatives(ctrl, s=True)[0]+'.v', f=True)
        if 'fk' in ctrl:
            cmds.connectAttr(show_fk_attr, cmds.listRelatives(ctrl, s=True)[0]+'.v', f=True)
        if 'Main' in ctrl:
            cmds.connectAttr(show_main_attr, cmds.listRelatives(ctrl, s=True)[0] + '.v', f=True)

    cmds.setAttr(show_main_attr, 1)

    #cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)

    #clean a bit
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    print ('Build {} Success'.format(block))



#build_cape_block()
