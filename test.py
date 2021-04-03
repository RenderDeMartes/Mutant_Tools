import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
reload(Mosaic_Tools.Utils.main_mosaic)

#mosaic = main_mosaic.Mosaic()
#rdm.rig_base_module()
#rdm.bounding_cube(axis = 'Z')
#help(rdm)
#from see import see
#see(rdm) 
#rdm.joints_middle()
#rdm.streatchy_ik(ik_ctrl = 'joint3_Ik_Ctrl',top_ctrl = 'joint1_Ik_Ctrl', attrs_location= 'joint3_Fk_Ctrl|joint1_Jnt_Switch_Loc')
#rdm.connect_md_node(in_x1='joint1_Jnt.translateX',in_x2=5,out_x = 'joint2_Jnt.visibility', mode = 'divide')

#ikfk = rdm.twist_fk_ik(start = '', mid = '', end = '', size = 3, color = 'red')
#rdm.twist_rotate_info()
#rdm.advance_twist(mode = 'down')
#rdm.joints_middle_no_chain()
#rdm.invert_fk_chain()
#rdm.connect_with_line()
#rdm.create_joint_guide()
#rdm.build_base(size = 3, name = 'lol')
#rdm.curve(type = 'root')

import Mosaic_Tools
from Mosaic_Tools.UI import load_autoRigger
reload(load_autoRigger)

try:AutoRigger.close()
except:pass
AutoRigger = load_autoRigger.AutoRigger()
AutoRigger.show()