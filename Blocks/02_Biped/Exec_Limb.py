from maya import cmds

import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
reload(Mosaic_Tools.Utils.main_mosaic)

mosaic = main_mosaic.Mosaic()

def create_limb_base():

    cmds.select(cl=True)
    cmds.joint(p = (0,0,0))
    cmds.joint(p = (0,10,0))
    cmds.joint(p = (0,20,0))
    
    print('Limb Base Created Successfully'),

#create_limb_base()

#-------------------------

def build_limb_block():
    ''