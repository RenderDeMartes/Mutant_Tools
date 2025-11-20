from maya import cmds, mel
cmds.file(new=True, f=True)

#Change to open your template scene
mel.eval('file -f -options "v=0;p=17"  -ignoreVersion  -typ "mayaAscii" -o "E:/BlueTape/b0001_Templates/b0002_NewMouth/Rig/WIP/NewMouth_Rig_0001_MouthTemplate.ma";{addRecentFile("E:/BlueTape/b0001_Templates/b0002_NewMouth/Rig/WIP/NewMouth_Rig_0001_MouthTemplate.ma", "mayaAscii");};')

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.AutoRigger import load_autoRigger
reload(load_autoRigger)

try:AutoRigger.close()
except:pass
AutoRigger = load_autoRigger.AutoRigger()
AutoRigger.build_autorigger()