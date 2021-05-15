import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
import imp
imp.reload(Mosaic_Tools.Utils.main_mosaic)
mt = main_mosaic.Mosaic()

#mt.create_block()
#cmds.reorder( 'Mosaic_Block6', r=-1 )
#mt.move_outliner(input = 'Mosaic_Block3', up =True)
#mt.bounding_cube(axis = 'Z')
#help(rdm)
#from see import see
#see(rdm) 
#mt.joints_middle()
#mt.streatchy_ik(ik_ctrl = 'joint3_Ik_Ctrl',top_ctrl = 'joint1_Ik_Ctrl', attrs_location= 'joint3_Fk_Ctrl|joint1_Jnt_Switch_Loc')
#mt.connect_md_node(in_x1='joint1_Jnt.translateX',in_x2=5,out_x = 'joint2_Jnt.visibility', mode = 'divide')
#miror_grp = mt.mirror_group('Clavicle_Ctrl_Offset_Grp', world = True)
#ikfk = mt.twist_fk_ik(start = '', mid = '', end = '', size = 3, color = 'red')
#mt.twist_rotate_info()
#mt.advance_twist(mode = 'down')
#mt.joints_middle_no_chain()
#mt.invert_fk_chain()
#mt.connect_with_line()
#mt.create_joint_guide()
#mt.build_base(size = 3, name = 'lol')
#mt.curve(type = 'root')
#mt.ribbon_between('joint1', 'joint2', 4 , 'hola')
#mt.check_is_there_is_base()

'''
import Mosaic_Tools
from Mosaic_Tools.UI import load_autoRigger
import imp
imp.reload(load_autoRigger)

try:AutoRigger.close()
except:pass
AutoRigger = load_autoRigger.AutoRigger()
AutoRigger.show()

import Mosaic_Tools
from Mosaic_Tools.UI import load_blockBuilder
import imp
imp.reload(load_blockBuilder)

try:BlockBuilder.close()
except:pass
BlockBuilder = load_blockBuilder.BlockBuilder()
BlockBuilder.show()

'''
