import os
import imp

import maya.cmds as cmds

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import mt_menu
imp.reload(Mutant_Tools.Utils.mt_menu)

#---------------------------------------------------------------------

def onMayaDroppedPythonFile(obj):

    print('Installing Mutant Tools')

    current_folder = os.path.dirname(__file__)
    scripts_folder = cmds.internalVar(usd=True) + '//Mutant_Tools'

    if current_folder is not scripts_folder:
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

    mt_menu.put_in_userSetup()
    mt_menu.create_mutant_menu()

    #---------------------------------------------------------------------

    