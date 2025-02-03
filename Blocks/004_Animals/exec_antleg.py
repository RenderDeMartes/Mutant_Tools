from __future__ import absolute_import,division
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
TAB_FOLDER = '004_Animals'
PYBLOCK_NAME = 'exec_antleg'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'02_AntLeg.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_antleg_block(name = 'AntLeg'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'AntLeg',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums

    joint_one = mt.create_joint_guide(name = name + '_1') #guide base with shapes
    joint_two = mt.create_joint_guide(name = name +'_2') #guide base with shapes
    joint_three = mt.create_joint_guide(name = name +'_3') #guide base with shapes
    joint_four = mt.create_joint_guide(name = name +'_4') #guide base with shapes
    joint_five = mt.create_joint_guide(name = name +'_5') #guide base with shapes

    cmds.parent(joint_five,joint_four)
    cmds.parent(joint_four,joint_three)
    cmds.parent(joint_three,joint_two)
    cmds.parent(joint_two,joint_one)
    cmds.parent(joint_one,block)

    cmds.setAttr('{}.ty'.format(joint_one),16)
    cmds.setAttr('{}.rz'.format(joint_one),-20)

    cmds.setAttr('{}.tx'.format(joint_two),8)
    cmds.setAttr('{}.rz'.format(joint_two),-8)

    cmds.setAttr('{}.tx'.format(joint_three),4)
    cmds.setAttr('{}.rz'.format(joint_three),-12)

    cmds.setAttr('{}.tx'.format(joint_four),3.876)
    cmds.setAttr('{}.rz'.format(joint_four),-50)

    cmds.setAttr('{}.tx'.format(joint_five),8.1)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_antleg_block()

#-------------------------

def build_antleg_block():

    mt.check_is_there_is_base()


    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    #orient the joints
    #mt.orient_joint(input = guide)
    new_guide = mt.duplicate_and_remove_guides(guide)
    cmds.makeIdentity(new_guide,a=True,t=True,r=True,s=True,n=False,pn=True)
    print (new_guide)
    to_build = [new_guide]

    #prep work for right side ------------------------------------------------------

    #if mirror is set only to right we need to build on left for mirror behavior then putt it back to righ side
    if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
        miror_grp = mt.mirror_group(new_guide, world = True)
        cmds.makeIdentity(miror_grp, a=True, t=True, r=True, s=True)
        cmds.parent(new_guide, w = True)
        cmds.delete(miror_grp)
        mt.orient_joint(input = new_guide)

    elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
        right_guide = mt.duplicate_change_names(input = new_guide, hi = True, search=nc['left'], replace =nc['right'])[0]
        to_build.append(right_guide)
        print (to_build)


    #build ------------------------------------------------------
    for side_guide in to_build:

        #use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator( n = '{}'.format(str(side_guide).replace(nc['joint'],'_Parent' + nc['locator'])))
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if side_guide.startswith(nc['right']):
                block_parent = block_parent.replace(nc['left'],nc['right'])

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']       
        else:
            color = setup['main_color']       


        #main funcion -------------------------------------------
        cmds.select(side_guide)

        #create limb setup
        main_joints = []
        main_joints.append(side_guide)
        for jnt in cmds.listRelatives(side_guide,ad=True):
            main_joints.append(jnt)
        main_joints.sort()
        size=3
        start_jnt = cmds.ls(sl=True)[0]
        ik_curve = setup['ik_ctrl']

        #duplicate chains to have the 3 of them
        cmds.select(start_jnt)
        ik_joints = mt.duplicate_change_names( input = '', hi = True, search=nc['joint'], replace =nc['ik'])
        cmds.select(start_jnt)
        fk_joints = mt.duplicate_change_names( input = '', hi = True, search=nc['joint'], replace =nc['fk'])

        #create FK System
        cmds.select(cl =True)
        
        for jnt in range(0,len(fk_joints)-1):
            cmds.select(fk_joints[jnt], add = True)
        
        if side_guide.startswith(nc['left']):
                fk_system = mt.fk_chain(size = size, color = 'blue', curve_type = 'circleX', scale = False)
        else:
            fk_system = mt.fk_chain(size = size, color = 'red', curve_type = 'circleX', scale = False)
    
        cmds.select(cl=True)

        end_jnt = ik_joints[-2]
        ik_handle = cmds.ikHandle (n = '{}{}'.format(end_jnt.replace(nc['joint'], ''), nc['ik_rp']), sj=ik_joints[0], ee=end_jnt, sol = 'ikRPsolver')
        cmds.rename(ik_handle[1],'{}{}'.format(end_jnt, nc['effector']))
        ik_handle = ik_handle[0]
        ik_handle_grp = mt.root_grp()

        cmds.select(cl=True)
        #Create IK System in proxy skeleton
        list_proxy_ik = []
        
        for jnt in ik_joints:
            if jnt == ik_joints[2] or jnt == ik_joints[4]:
                pass
            else:
                position = cmds.xform(jnt,ws=True,q=True,t=True)
                jnt_proxy_ik = cmds.joint(n='{}_Proxy'.format(jnt))
                cmds.xform(jnt_proxy_ik,ws=True,t=position)    
                list_proxy_ik.append(jnt_proxy_ik)

        ik_system = []
        ik_handle_proxy = cmds.ikHandle (n = '{}{}'.format(list_proxy_ik[-1].replace(nc['joint'], ''), nc['ik_rp']), sj=list_proxy_ik[0], ee=list_proxy_ik[-1], sol = 'ikRPsolver')
        cmds.rename(ik_handle_proxy[1],'{}{}'.format(list_proxy_ik[-1], nc['effector']))
        ik_handle_proxy = ik_handle_proxy[0]
        ik_handle_proxy_grp = mt.root_grp()

        #create ik Controller with offset grp and clean attr
        ctrl = mt.curve(type = ik_curve , rename = False, custom_name = True, name = '{}{}'.format(list_proxy_ik[-1], nc ['ctrl']), size = size)
        ctrl = cmds.rename(ctrl, ctrl.replace(nc['joint'],''))

        ik_system.append(ctrl)
        mt.match(ctrl, end_jnt)
        cmds.rotate(0,0,0, a=True)

        IK_grp = mt.root_grp()
        mt.hide_attr(ctrl, s = True, v = True)
        ik_handle_ankle = cmds.ikHandle (n = '{}{}'.format(ik_joints[-1].replace(nc['joint'], ''), nc['ik_rp']), sj=ik_joints[3], ee=ik_joints[4], sol = 'ikSCsolver')
        cmds.rename(ik_handle_ankle[1],'{}{}'.format(ik_joints[-1], nc['effector']))
        ik_handle_ankle = ik_handle_ankle[0]
        ik_handle_ankle_grp = mt.root_grp()

        cmds.parentConstraint(ctrl, ik_handle_ankle, mo =True)

        cmds.select(cl=True)
        #parent ik to controller
        cmds.parentConstraint(ctrl, ik_handle_proxy, mo =True)
        
        #parent ik_handle_grp to second ik joint proxy
        
        cmds.parent(ik_handle_grp,list_proxy_ik[1])

        #create pole vector
        pv_loc = mt.pole_vector_placement(bone_one = list_proxy_ik[0], bone_two = list_proxy_ik[1], bone_three = list_proxy_ik[2])
        cmds.move(8,0,0,pv_loc,r=True,os=True,wd=True)
        #create controller in position with offset grp
        pv_ctrl = mt.curve(type = setup['pv_ctrl'], rename = False, custom_name = True, name = '{}{}{}'.format(end_jnt,nc ['pole_vector'], nc ['ctrl']), size = size/2)
        pv_ctrl = cmds.rename(pv_ctrl, pv_ctrl.replace(nc['joint'],''))
        ik_system.append(pv_ctrl)
        cmds.pointConstraint(pv_loc, pv_ctrl, mo=False)
        cmds.delete(pv_loc)
        pv_grp = mt.root_grp()
        
        cmds.poleVectorConstraint(pv_ctrl, ik_handle_proxy)
        
        #clean controller
        mt.hide_attr(pv_ctrl, r = True,  s = True, v = True)

        #connect with line
        line = mt.connect_with_line(pv_ctrl, list_proxy_ik[1])
        
        #create top controler
        cmds.select(cl=True)
        top_ctrl = mt.curve(type = setup['top_ik_ctrl'], rename = False, custom_name = True, name = '{}{}'.format(list_proxy_ik[0].replace(nc['joint'], ''), nc ['ctrl']), size = size*0.5)
        mt.match(top_ctrl, list_proxy_ik[0], r=False)
        top_grp = mt.root_grp()
        
        mt.hide_attr(top_ctrl,r = True,  s = True, v = True)
        ik_system.append(top_ctrl)
        
        cmds.parentConstraint(top_ctrl, list_proxy_ik[0])
        cmds.parentConstraint(top_ctrl, ik_joints[0])

        #organize and add color

        #create IK Grp
        cmds.select(cl=True)
        ik_main_grp = cmds.group(n = ik_joints[0] + nc['ctrl'] + nc ['group'], em =True)
        
        cmds.parent(pv_grp[0], ik_main_grp)
        cmds.parent(IK_grp[0], ik_main_grp)
        cmds.parent(top_grp[0], ik_main_grp)
        
        #add color
        for c in ik_system:
            cmds.select(c)
            if side_guide.startswith(nc['left']):
                mt.assign_color(color = 'blue')
            else:
                mt.assign_color(color = 'red')
            
        #put the ik in the return list
        ik_system.append(ik_handle)		
        #add the line at the end
        ik_system.append(line[0])	
        
        #add swtich attr in all controllers
        ik_fk_controllers = fk_system + ik_system
        for ctrl in ik_fk_controllers :
            cmds.select(ctrl)
            if cmds.objectType(ctrl) ==  'transform':
                switch_attr = mt.shape_with_attr(input = '', obj_name = '{}_Switch'.format(start_jnt), attr_name = 'Switch_IK_FK')

        
        #create switch ik fk
        for num, jnt in enumerate(main_joints):
            mt.switch_blend_colors(this = fk_joints[num], that = ik_joints[num], main = jnt, attr = switch_attr)
        
        #switch visibility ctrls
        reverse_node = cmds.createNode('reverse',n='{}_r_vis_fkik'.format(module['Name']))
        cmds.connectAttr(switch_attr,'.inputX'.format(reverse_node),f=True)
        for ctrl_fk in fk_system:
            cmds.connectAttr(switch_attr,'{}Shape.visibility'.format(ctrl_fk),f=True)
        cmds.connectAttr('{}.outputX'.format(reverse_node),'{}.visibility'.format(ik_main_grp),f=True)
        cmds.connectAttr('{}.outputX'.format(reverse_node),'{}.visibility'.format(line[0]),f=True)

        #clean scene
        
        rig_main_grp = cmds.group(n = '{}_Rig_Grp'.format(start_jnt), em =True)
        jnt_main_grp = cmds.group(n = '{}_Jnt_Main_Grp'.format(start_jnt), em =True)
        cmds.parent(jnt_main_grp,rig_main_grp)
        cmds.parent(main_joints[0],jnt_main_grp)
        cmds.parent(fk_joints[0],jnt_main_grp)
        cmds.parent(ik_joints[0],jnt_main_grp)
        cmds.parent(list_proxy_ik[0],jnt_main_grp)
        cmds.parent(ik_handle_proxy_grp,rig_main_grp)
        cmds.parent(ik_handle_ankle_grp,rig_main_grp)

        ctrl_main_grp = cmds.group(n = '{}_Ctrl_Grp'.format(start_jnt),em=True)
        
        cmds.parent(ik_main_grp,ctrl_main_grp)
        cmds.parent(line[0],ctrl_main_grp)
        cmds.parent((cmds.listRelatives(fk_system[0],p=True)),ctrl_main_grp)
        
        cmds.select(cl=True)

     
        #create bind Joints for the skin ------------------------- 
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        for jnt in main_joints:
            cmds.select(cl=True)
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, bind_jnt_grp) 



        #flip right rig  to right side ------------------------- 
        
        #check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
            miror_ctrl_grp = mt.mirror_group(ctrl_main_grp)
            miror_jnt_grp = mt.mirror_group(rig_main_grp, world = True)
            cmds.parentConstraint(block_parent, top_grp , mo = True)
            cmds.parentConstraint(block_parent,(cmds.listRelatives(fk_system[0],p=True)),mo=True)
            clean_rig_grp = miror_jnt_grp
            clean_ctrl_grp = miror_ctrl_grp

        elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
            if str(side_guide).startswith(nc['right']) :
                miror_ctrl_grp = mt.mirror_group(ctrl_main_grp)
                miror_jnt_grp = mt.mirror_group(rig_main_grp, world = True)
                cmds.parentConstraint(block_parent, top_grp , mo = True)
                cmds.parentConstraint(block_parent,(cmds.listRelatives(fk_system[0],p=True)),mo=True)
                clean_rig_grp = miror_jnt_grp
                clean_ctrl_grp = miror_ctrl_grp
            else:
                cmds.parentConstraint(block_parent, top_grp , mo = True)
                cmds.parentConstraint(block_parent,(cmds.listRelatives(fk_system[0],p=True)),mo=True)
                clean_rig_grp = rig_main_grp
                clean_ctrl_grp = ctrl_main_grp        
        
        else: #only left side
            cmds.parentConstraint(block_parent, top_grp , mo = True)
            cmds.parentConstraint(block_parent,(cmds.listRelatives(fk_system[0],p=True)),mo=True)
            clean_rig_grp = rig_main_grp
            clean_ctrl_grp = ctrl_main_grp  

        #blends
        '''
        blends_grp = mt.root_grp(input = '', custom = True, custom_name = 'Blends', autoRoot = False, replace_nc = False)[0]
        blends_grp = blends_grp.replace('_AutoFK','')
        bends = cmds.getAttr('{}.Blends'.format(config).split(':'))
        for blend in bends:
            ''
            #cmds.orientConstraint()
        '''

        #Finish -------------------------------------------
        
        #clean ctrls
        cmds.parent(clean_ctrl_grp, 'Rig_Ctrl_Grp')

        #parent rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        

    #clean a bit
    '''clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])'''
    

    # build complete ----------------------------------------------------    
    print ('Build {} Success'.format(block))


#build_antleg_block()
