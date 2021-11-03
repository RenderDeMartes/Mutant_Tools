
# Start Mutant Tools
# --------------------------------
from maya import cmds
try:
    def load_mutant_menu():
        import imp
        import Mutant_Tools
        import Mutant_Tools.Utils
        from Mutant_Tools.Utils import mt_menu
        imp.reload(Mutant_Tools.Utils.mt_menu)
        mt_menu.create_mutant_menu()
    cmds.evalDeferred(load_mutant_menu)
except:
    pass
# --------------------------------
# End Mutant Tools

# change colors start
from maya import cmds

def change_colors():
    gMainWindow = maya.mel.eval('$tmpVar=$gMainWindow')
    cmds.window(gMainWindow, e=True, mw=True, bgc=(0.31, 0.3, 0.5))

cmds.evalDeferred(change_colors)
# change colors end

# import comet start
from maya import mel
def import_comet():
    mel.eval('source "cometMenu"')

cmds.evalDeferred(import_comet)
# import comet end