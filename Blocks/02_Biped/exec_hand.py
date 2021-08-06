from maya import cmds
import json
import imp
import os

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import main_mutant
imp.reload(Mutant_Tools.Utils.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '02_Biped'
PYBLOCK_NAME = 'exec_hand'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\Blocks//{}'.format(TAB_FOLDER), '//Config') #change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = (PATH+'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)	

MODULE_FILE = (os.path.dirname(__file__) +'/06_Hand.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_hand_block(name = 'Hand'):


    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''
    fingers = mt.ask_name(text = 'Thumb_Index_Middle_Ring_Pinky', ask_for = 'Comfirm fingers (Delete if not needed)')

    block = mt.create_block(name = name, icon = 'Hand',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    
        
    cmds.select (cl = True)
    palm = mt.create_joint_guide(name = name + '_Palm')

    def genericFinger (finger, phalanges,x,y,z,mult):
        cmds.select (palm)
        guides = []
        for f in range(phalanges):
            try:old_guide = guide
            except:pass
            guide = mt.create_joint_guide(name = (name + '_' + finger + '_0' + str (f)))
            cmds.move(f*mult,0,0)
            cmds.move (x,y,z, r = True)    
            try: cmds.parent(guide, old_guide)
            except:pass
            guides.append(guide)
        return guides

        cmds.select (cl = True)
                  
    if 'Index' in fingers: 
        indexs = genericFinger ('Index', 5,4,0,3,3)
        cmds.parent(indexs[0], palm)

    if 'Middle' in fingers: 
        middles = genericFinger ('Middle', 5,4,0,0,4.5)
        cmds.parent(middles[0], palm)
           
    if 'Ring' in fingers: 
        rings = genericFinger ('Ring', 5,4,0,-3,4)
        cmds.parent(rings[0], palm)
    
    if 'Pinky' in fingers: 
        pinkys = genericFinger ('Pinky', 5,4,0,-6,3)
        cmds.parent(pinkys[0], palm)
          
    if 'Thumb' in fingers: 
        thumbs = genericFinger ('Thumb', 4,3,0,7,3)
        cmds.setAttr ('{}.rotateY'.format(thumbs[0]), -50)
        
        inner_cup = mt.create_joint_guide(name = (name + '_' + 'InnerCup' ))
        cmds.delete(cmds.parentConstraint(palm, thumbs[0],inner_cup, mo=False))
        
        cmds.parent(thumbs[0], inner_cup)
        cmds.parent(inner_cup, palm)

    #create Outter Cup joints
    if 'Pinky' or 'Ring' in fingers:
        outter_cup = mt.create_joint_guide(name = (name + '_' + 'OutterCup' ))
        try:cmds.delete(cmds.parentConstraint(palm, pinkys[0],outter_cup ,mo=False))
        except:cmds.delete(cmds.parentConstraint(palm, rings[0],outter_cup ,mo=False))

        if cmds.objExists(pinkys[0]):
            cmds.parent(pinkys[0], outter_cup)

        if cmds.objExists(rings[0]):
            cmds.parent(rings[0], outter_cup)

        cmds.parent(outter_cup, palm)
    
    cmds.parent(palm, block)

    cmds.select(block)
    print('{} Created Successfully'.format(name))

#create_hand_block()

#-------------------------

def build_hand_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = str(block).replace(nc['module'], '')
    print (name)

    #orient the joints
    #mt.orient_joint(input = guide)
    new_guide = mt.duplicate_and_remove_guides(guide)
    print (new_guide)
    to_build = [new_guide]

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_type = cmds.getAttr('{}.CtrlType'.format(config), asString = True)
    attrs_ctrl = cmds.getAttr('{}.SetAttrsCtrl'.format(config), asString = True)
    attrs_parent = cmds.getAttr('{}.SetCtrlAttrsParent'.format(config), asString = True)
    curls_axis = 'Z'

    #use this group for later cleaning, just assign them when you create the top on hierarchy
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    #prep work for right side ------------------------------------------------------

    #if mirror is set only to right we need to build on left for mirror behavior then putt it back to righ side
    if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
        miror_grp = mt.mirror_group(new_guide, world = True)
        cmds.makeIdentity(miror_grp, a=True, t=True, r=True, s=True)
        cmds.parent(new_guide, w = True)
        cmds.delete(miror_grp)
        #mt.orient_joint(input = new_guide)

    elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
        right_guide = mt.duplicate_change_names(input = new_guide, hi = True, search=nc['left'], replace =nc['right'])[0]
        to_build.append(right_guide)
        print (to_build)

    #build ------------------------------------------------------

    for side_guide in to_build:
        cmds.select(side_guide)

        #orient Joints becouse the thumbs sucks
        #hardcoded becouse fuck it
        cmds.select('*Thumb_01*')
        cmds.hide(guide)
        #cmds.joint(e=True, oj='yxz', ch=True, secondaryAxisOrient='{}'.format(setup['secondaryAxisOrient']))

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']       
        else:
            color = setup['main_color']

        #ctrl list for the clean up
        main_ctrl_grps = []

        #create hand Ctrl if there is no ctrl for the Attrs
        if attrs_ctrl == 'new_ctrl':
            ctrl_with_attrs = mt.curve(input = side_guide, type = 'hand', 
                                            rename = False, 
                                            custom_name = True, 
                                            name = side_guide.replace(nc['joint'],nc['ctrl']), 
                                            size = ctrl_size)

            mt.assign_color(ctrl_with_attrs, color)
            cmds.move(0,0,0)
            cmds.rotate(0,0,0)
            mt.match(ctrl_with_attrs, side_guide, t=True, r=False)
            hand_grp = mt.root_grp()
            #cmds.move(0,2 * ctrl_size,0, ctrl_with_attrs, r=True)
            mt.hide_attr(input = ctrl_with_attrs, t=True, r=True, s=True, rotate_order=True)
            cmds.parentConstraint(side_guide, hand_grp, mo=True)

        else:
            ctrl_with_attrs = attrs_ctrl

        #create ctrl attrs
        mt.line_attr(input = ctrl_with_attrs, name = 'Fingers', lines = 10)

        #--------------------------------

        #use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator( n = '{}'.format(str(side_guide).replace(nc['joint'],'_Parent' + nc['locator'])))
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if side_guide.startswith(nc['right']):
                block_parent = block_parent.replace(nc['left'],nc['right'])

        #main funcion -------------------------------------------
        cmds.select(side_guide)

        #get phalange 0 for the main FK chain
        fingers_zero = []

        for finger in reversed(['Pinky_00','Ring_00','Middle_00','Index_00','Thumb_00']):
            if cmds.objExists(side_guide.replace('Palm',finger)):
                fingers_zero.append(side_guide.replace('Palm',finger))
                #mt.orient_joint(input=fingers_zero)
                #create curl attrs
                mt.new_attr(input= ctrl_with_attrs, 
                            name = finger.replace('_00','') + 'Curl', 
                            min = -100 , 
                            max = 100, 
                            default = 0)
                
                #add the 1 back to the hand: it losses it becouse the duplicate guide removes the 1 at the end fo duplicates
                finger_one = cmds.listRelatives(side_guide.replace('Palm',finger), c=True)[0]
                cmds.rename(finger_one, finger_one.replace('_0_','_01_'))  
        
        print (fingers_zero)

        #create bind joints for later
        bind_joints = mt.duplicate_change_names(input = side_guide, hi = True, search=nc['joint'], replace =nc['joint_bind'])

        #create main fk chains
        for finger in fingers_zero:
            cmds.select(finger)
            range = [0,1,2]
            if 'Thumb' in str(finger): # do less if is the thumb
                range = [0,1]

            #add to select for the fk chain in order
            for i in range:
                cmds.select(cmds.listRelatives(cmds.ls(sl=True)[-1], c=True), add=True)
            sel = cmds.ls(sl=True)
            #create fk chain
            fk_ctrls = mt.fk_chain(input = '', size = ctrl_size, color = color, curve_type = ctrl_type, scale = True, twist_axis = setup['twist_axis'])
            print(fk_ctrls)
            main_ctrl_grps.append(cmds.listRelatives(fk_ctrls[0], p=True)[0])
            for ctrl in fk_ctrls[1:]:
                #add auto curl
                curl_grp = mt.root_grp(input = ctrl, custom = True, custom_name = '_Curl', autoRoot = False, replace_nc = True)[0]
                #connect to attr
                finger_name = finger.split('_')[2] 
                cmds.connectAttr('{}.{}Curl'.format(ctrl_with_attrs, finger_name),'{}.rotate{}'.format(curl_grp,curls_axis), f=True)

            #parent to end joint
            cmds.parentConstraint(fk_ctrls[-1], cmds.listRelatives(sel[-1], c=True)[0], mo=True)

        #main ctrl grp
        ctrls_grp = cmds.group(main_ctrl_grps, n = '{}{}'.format(side_guide.replace(nc['joint'],nc['ctrl']), nc['group']))
        pivot = cmds.xform(side_guide ,rp =True, q=True, ws=True)
        print(pivot)
        cmds.move(pivot[0],pivot[1],pivot[2], "{}.scalePivot".format(ctrls_grp),"{}.rotatePivot".format(ctrls_grp), absolute=True)

        try:cmds.parent(hand_grp, ctrls_grp)
        except:pass
        cmds.parentConstraint(ctrls_grp,side_guide, mo=True)


        #create cup inner and outter stuff
        mt.line_attr(input = ctrl_with_attrs, name = 'Hand', lines = 10)

        try:
            inner_cup = side_guide.replace('Palm','InnerCup')
            if cmds.objExists(inner_cup):
                print (side_guide + ':INNER CUP')
                inner_cup_attr = mt.new_attr(input= ctrl_with_attrs, 
                                            name = 'Inner_Cup', 
                                            min = -100 , 
                                            max = 100, 
                                            default = 0)
                
                inner_cup_group = mt.root_grp(input = fingers_zero[0].replace(nc['joint'], nc['ctrl']), custom=True,custom_name='_Inner_Cup{}'.format(nc['group']) ,replace_nc=True)[0]
                inner_cup_group = cmds.rename(inner_cup_group, inner_cup_group.replace('_Thumb_00_Ctrl',''))
                pivot = cmds.xform(inner_cup ,rp =True, q=True, ws=True)
                print(pivot)
                cmds.move(pivot[0],pivot[1],pivot[2], "{}.scalePivot".format(inner_cup_group),"{}.rotatePivot".format(inner_cup_group), absolute=True)

                cmds.connectAttr(inner_cup_attr , '{}.rotateY'.format(inner_cup_group))
                cmds.connectAttr(inner_cup_attr , '{}.rotateY'.format(inner_cup))
                cmds.parentConstraint(ctrls_grp,inner_cup, mo=True)


        except:
            pass
        
        outter_cup = side_guide.replace('Palm','OutterCup')
        if cmds.objExists(outter_cup):
            print (side_guide + ': OUTTER CUP')
            outter_cup_attr = mt.new_attr(input= ctrl_with_attrs, 
                                        name = 'OutterCup', 
                                        min = -100 , 
                                        max = 100, 
                                        default = 0)

            outter_cup_group = cmds.group(n = '{}Outter{}'.format(side_guide.replace('Palm'+nc['joint'], ''),nc['group']), em=True)
            outter_offset = mt.root_grp(replace_nc=True)[0]
            cmds.delete(cmds.parentConstraint(outter_cup,outter_offset, mo=False))
            cmds.connectAttr(outter_cup_attr , '{}.rotateX'.format(outter_cup_group))
            cmds.connectAttr(outter_cup_attr , '{}.rotateX'.format(outter_cup))
            #cmds.parentConstraint(ctrls_grp,outter_cup, mo=True)

            pinky = side_guide.replace('Palm'+nc['joint'],'Pinky_00'+nc['ctrl'])
            print (pinky)
            if cmds.objExists(pinky):
                cmds.parent(cmds.listRelatives(pinky, p=True), outter_cup_group)

            ring = side_guide.replace('Palm'+nc['joint'],'Ring_00'+nc['ctrl'])
            if cmds.objExists(ring):
                cmds.parent(cmds.listRelatives(ring, p=True), outter_cup_group)

            cmds.parent(outter_offset, ctrls_grp)

        #spread stuff
        spread_attr = mt.new_attr(input= ctrl_with_attrs, 
                            name = 'Spread', 
                            min = -100 , 
                            max = 100, 
                            default = 0)
        for finger in ['Pinky_01','Ring_01','Middle_01','Index_01']:
            finger_ctrl = side_guide.replace('Palm'+nc['joint'],finger + nc['ctrl'])
            print(finger)
            if cmds.objExists(finger_ctrl):
                spread_grp = mt.root_grp(input = finger_ctrl, custom = True, custom_name = '_Spread', autoRoot = False, replace_nc = True)[0]
                #cmds.connectAttr(spread_cup_attr,'{}.rotateZ'.format(spread_grp), f=True)
                if finger == 'Pinky_01':
                    mult = 2
                elif finger == 'Ring_01':
                    mult = 1
                elif finger == 'Middle_01':
                    mult = 0.5
                elif finger == 'Index_01':
                    mult = -0.5

                mt.connect_md_node(in_x1 = spread_attr, in_x2 = mult, out_x = '{}.rotateY'.format(spread_grp), mode = 'mult', name = 'Spread', force = False)

        #relax stuff
        relax_attr = mt.new_attr(input= ctrl_with_attrs, 
                            name = 'Relax', 
                            min = -100 , 
                            max = 100, 
                            default = 0)
        for finger in ['Pinky_01','Ring_01','Middle_01','Index_01']:
            finger_ctrl = side_guide.replace('Palm'+nc['joint'],finger + nc['ctrl'])
            print(finger)
            if cmds.objExists(finger_ctrl):
                relax_grp = mt.root_grp(input = finger_ctrl, custom = True, custom_name = '_Relax', autoRoot = False, replace_nc = True)[0]
                #cmds.connectAttr(spread_cup_attr,'{}.rotateZ'.format(spread_grp), f=True)
                if finger == 'Pinky_01':
                    mult = 3.5
                elif finger == 'Ring_01':
                    mult = 2.5
                elif finger == 'Middle_01':
                    mult = 1.5
                elif finger == 'Index_01':
                    mult = 1

                mt.connect_md_node(in_x1 = relax_attr, in_x2 = mult, out_x = '{}.rotate{}'.format(relax_grp, curls_axis), mode = 'mult', name = 'Relax', force = False)

        #thumb relax
        thumb_ctrl = side_guide.replace('Palm'+nc['joint'],'Thumb_00' + nc['ctrl'])
        if cmds.objExists(thumb_ctrl):
            thumb_relax_atrr = mt.new_attr(input= ctrl_with_attrs, 
                                name = 'Thumb_Relax', 
                                min = -100 , 
                                max = 100, 
                                default = 0)
            thumb_relax_grp = mt.root_grp(input = thumb_ctrl, custom = True, custom_name = '_Relax', autoRoot = False, replace_nc = True)[0]
            thumb_mult = 1
            mt.connect_md_node(in_x1 = thumb_relax_atrr, in_x2 = thumb_mult, out_x = '{}.rotateZ'.format(thumb_relax_grp), mode = 'mult', name = 'Relax', force = False)
        

        #create bind Joints for the skin ------------------------- 
        print(bind_joints) #created on top
  

        for jnt in cmds.listRelatives(bind_joints[0], ad=True):
            cmds.parentConstraint(jnt.replace(nc['joint_bind'],nc['joint']),jnt)
            cmds.scaleConstraint(jnt.replace(nc['joint_bind'],nc['joint']),jnt)
    
        cmds.parentConstraint(side_guide,bind_joints[0])
        cmds.scaleConstraint(side_guide,bind_joints[0])  

        #flip right rig  to right side ------------------------- 
        
        #check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
            miror_ctrl_grp = mt.mirror_group(ctrls_grp, world = True)
            miror_jnt_grp = mt.mirror_group(side_guide, world = True)
            cmds.parentConstraint(block_parent, miror_ctrl_grp , mo = True)     
            clean_rig_grp = miror_jnt_grp
            clean_ctrl_grp = miror_ctrl_grp

        elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
            if str(side_guide).startswith(nc['right']) :

                miror_ctrl_grp = mt.mirror_group(ctrls_grp, world = True)
                miror_jnt_grp = mt.mirror_group(side_guide, world = True)
                cmds.parentConstraint(block_parent, miror_ctrl_grp , mo = True)     
                clean_rig_grp = miror_jnt_grp
                clean_ctrl_grp = miror_ctrl_grp
            else:
                cmds.parentConstraint(block_parent, ctrls_grp , mo = True) 
                clean_rig_grp = side_guide
                clean_ctrl_grp = ctrls_grp        
        
        else: #only left side
            cmds.parentConstraint(block_parent, ctrls_grp , mo = True) 
        

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
        
        #game parents for bind joints
        game_parent = cmds.getAttr('{}.SetGameParent'.format(config))
        if side_guide.startswith(nc['right']):
            game_parent = game_parent.replace(nc['left'],nc['right'])

        if cmds.objExists(game_parent):
            cmds.parent(bind_joints[0], game_parent) 
        else: 
            bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
            if cmds.objExists(bind_jnt_grp):
                cmds.parent(bind_joints[0], bind_jnt_grp) 
           
        #clean ctrls
        cmds.parent(clean_ctrl_grp, 'Rig_Ctrl_Grp')

        #parent rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

          

    #clean a bit
    #clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))

    

    # build complete ----------------------------------------------------    
    print ('Build {} Success'.format(block))


#build_hand_block()
