from __future__ import absolute_import

# Start Mutant Tools
try:
    from maya import cmds
    import sys
    import os
    from maya import cmds

    try:
        import importlib;
        from importlib import reload
    except:
        import imp;
        from imp import reload

    mutant_path = 'C://Users//Esteban//Documents//maya//2022//scripts//rigging'
    if mutant_path not in sys.path:
        sys.path.append(mutant_path)

    import Mutant_Tools
    import Mutant_Tools.Utils
    from Mutant_Tools.Utils import mt_menu

    reload(Mutant_Tools.Utils.mt_menu)


    def load_mutant_menu():
        try:
            import importlib;
            from importlib import reload
        except:
            import imp;
            from imp import reload

        import Mutant_Tools
        import Mutant_Tools.Utils
        from Mutant_Tools.Utils import mt_menu
        reload(Mutant_Tools.Utils.mt_menu)
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