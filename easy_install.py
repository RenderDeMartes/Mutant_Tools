import os
import maya.cmds as cmds

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
    
    