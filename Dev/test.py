import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
import imp
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

mt.put_inside_rig_container(['network1'])

cmds.container('Mutant_Rig', e=True, addNode='network1')

#mt.load_preset(name = 'Biped_180')
#mt.create_block()
#cmds.reorder( 'Mutant_Block6', r=-1 )
#mt.move_outliner(input = 'Mutant_Block3', up =True)
#mt.bounding_cube(axis = 'Z')
#help(rdm)
#from see import see
#see(rdm) 
#mt.joints_middle()
#mt.streatchy_ik(ik_ctrl = 'joint3_Ik_Ctrl',top_ctrl = 'joint1_Ik_Ctrl', attrs_location= 'joint3_Fk_Ctrl|joint1_Jnt_Switch_Loc')
#mt.connect_md_node(in_x1='joint1_Jnt.translateX',in_x2=5,out_x = 'joint2_Jnt.visibility', mode = 'divide')
#miror_grp = mt.mirror_group('Clavicle_Ctrl_Offset_Grp', world = True)
#ff#mt.twist_rotate_info()
#mt.advance_twist(mode = 'down')
#mt.joints_middle_no_chain()
#mt.invert_fk_chain()
#mt.connect_with_line()
#mt.create_joint_guide()
#mt.build_base(size = 3, name = 'lol')
#mt.curve(type = 'pin_cube')
#mt.ribbon_between('joint1', 'joint2', 4 , 'hola')
#mt.check_is_there_is_base()
#mt.connect_with_line('R_Knee_Ik_Jnt','R_Wrist_Ik_PoleVector_Ctrl')
'''
mt.Mutant_logger(mode = 'create')
mt.Mutant_logger(mode = 'stop')
mt.Mutant_logger(mode = 'clear')
'''

#mt.replace_connection_with_doublelinear('Spine_Belly_Jnt','scaleX')

'''
import Mutant_Tools
from Mutant_Tools.UI import load_autoRigger
import imp
imp.reload(load_autoRigger)

try:AutoRigger.close()
except:pass
AutoRigger = load_autoRigger.AutoRigger()
AutoRigger.show()

import Mutant_Tools
from Mutant_Tools.UI import load_blockBuilder
import imp
imp.reload(load_blockBuilder)

try:BlockBuilder.close()
except:pass
BlockBuilder = load_blockBuilder.BlockBuilder()
BlockBuilder.show()

'''
