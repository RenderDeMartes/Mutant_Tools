from __future__ import absolute_import
import os
import shutil
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload


import maya.cmds as cmds

#---------------------------------------------------------------------


def onMayaDroppedPythonFile(obj):

    try:
        print('Installing Mutant Tools...')

        current_folder = os.path.dirname(__file__)
        scripts_folder = os.path.join(cmds.internalVar(usd=True), 'Mutant_Tools')

        #Drag and drop can happen from any folder name (eg a github zip unpacks as 'Mutant_Tools-main'),
        #so we always copy the contents into the proper 'Mutant_Tools' folder under the Maya scripts dir.
        if os.path.normcase(os.path.normpath(current_folder)) != os.path.normcase(os.path.normpath(scripts_folder)):
            print('Copying from {} to {}'.format(current_folder, scripts_folder))
            from distutils.dir_util import copy_tree
            copy_tree(current_folder, scripts_folder)
            print('Copy done.')

            try:
                shutil.rmtree(current_folder)
                print('Removed source folder: {}'.format(current_folder))
            except Exception:
                print('Could not remove source folder, you can delete it manually: {}'.format(current_folder))

        #---------------------------------------------------------------------
        #Install the Bluetape Rigging shelf so the user doesn't have to do it by hand

        shelf_name = 'shelf_Bluetape_Rigging.mel'
        shelf_source = os.path.join(scripts_folder, shelf_name)
        shelf_target_folder = cmds.internalVar(ush=True)

        if os.path.isfile(shelf_source) and os.path.isdir(shelf_target_folder):
            try:
                shutil.copy(shelf_source, os.path.join(shelf_target_folder, shelf_name))
                print('Shelf installed: {}'.format(shelf_name))
            except Exception:
                print('Could not install the shelf automatically, copy it manually from {}'.format(shelf_source))

        #---------------------------------------------------------------------

        import Mutant_Tools
        import Mutant_Tools.Utils
        from Mutant_Tools.Utils import mt_menu
        reload(Mutant_Tools.Utils.mt_menu)

        mt_menu.create_mutant_menu()
        mt_menu.put_in_userSetup()
        mt_menu.create_mutant_menu()

        cmds.confirmDialog(
            title='Mutant Tools',
            message='Mutant Tools installed successfully!\n\n'
                    'Look for the "Mutant-Tools" menu in Maya\'s top menu bar.\n'
                    'It will load automatically every time you open Maya, and will '
                    'let you know when a new version is available.',
            button=['Awesome!'])

        print('Mutant Tools installed.')

    except Exception as e:
        print('Mutant Tools install failed: {}'.format(e))
        cmds.confirmDialog(
            title='Mutant Tools - Install Failed',
            message='Something went wrong during the install:\n\n{}\n\n'
                    'Please follow the manual steps in INSTALLATION_GUIDE.txt instead, '
                    'or reach out on Discord for help.'.format(e),
            button=['OK'],
            icon='critical')
