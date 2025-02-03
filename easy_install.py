from __future__ import absolute_import
import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload


import maya.cmds as cmds

#---------------------------------------------------------------------


def onMayaDroppedPythonFile(obj):

    print('Installing Mutant Tools')

    current_folder = os.path.dirname(__file__)
    scripts_folder = os.path.join(cmds.internalVar(usd=True), 'Mutant_Tools')

    if current_folder != scripts_folder:
        print ('from {} : to {}.'.format(current_folder, scripts_folder))
        from distutils.dir_util import copy_tree
        copy_tree(current_folder, scripts_folder)
        print ('Copy done.')
        try:
            os.rmdir(current_folder)
            print('Duplicate removed.')
        except:
            print('Duplicate not removed.')

    #---------------------------------------------------------------------

    import Mutant_Tools
    import Mutant_Tools.Utils
    from Mutant_Tools.Utils import mt_menu
    reload(Mutant_Tools.Utils.mt_menu)
    mt_menu.create_mutant_menu()

    mt_menu.put_in_userSetup()
    mt_menu.create_mutant_menu()

    #---------------------------------------------------------------------

    