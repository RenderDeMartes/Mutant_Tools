import maya.mel as mel
mel.eval('file -f -options "v=0;"  -ignoreVersion  -typ "mayaBinary" -o "/Users/estebanrdgz/Desktop/eyeDev.mb";addRecentFile("/Users/estebanrdgz/Desktop/eyeDev.mb", "mayaBinary");')
import imp
import Mutant_Tools
from Mutant_Tools.UI.AutoRigger import load_autoRigger
imp.reload(load_autoRigger)

try:AutoRigger.close()
except:pass
AutoRigger = load_autoRigger.AutoRigger()
AutoRigger.build_autorigger()




