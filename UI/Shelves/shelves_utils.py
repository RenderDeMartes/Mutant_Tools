from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.Shelves import shelves_utils
reload(shelves_utils)

cShelves = shelves_utils.Shelves()

#----------------
dependencies:

Main Mutant

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
# ---------------------------------------------------------------------------------------------
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload


from maya import cmds
import os

import Mutant_Tools
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()


# ---------------------------------------------------------------------------------------------

class Shelves(object):

    def __init__(self, folder=None, name=None, file_path=None):

        self.folder = folder or self.get_shelves_path()
        self.name = name
        self.file_path = file_path

        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)

    #---------------------------------------------------------------------------------------------

    def open_file(self, file_path=None):

        if not file_path:
            file_path = self.file_path
        print(file_path)

        cmds.file(file_path, o=True, force=True)

        return True

    #---------------------------------------------------------------------------------------------

    def import_file(self, file_path=None):
        if not file_path:
            file_path = self.file_path
        print(file_path)

        cmds.file(file_path, i=True, type="mayaAscii")

        return True
    #---------------------------------------------------------------------------------------------

    def reference_file(self, file_path=None):
        if not file_path:
            file_path = self.file_path
        print(file_path)

        cmds.file(file_path, reference=True)

        return True
    #---------------------------------------------------------------------------------------------

    def save_file(self, path=None, name=None):

        self.name = name

        if not path and not name:
            path = self.get_file_path(name=None)

        if not path:
            path = os.path.join(self.folder, name)

        print(path)
        cmds.file(rename=path)
        cmds.file(s=True, f=True, typ='mayaAscii')

        return path

    #---------------------------------------------------------------------------------------------

    def create_image(self):
        image_name = self.name
        print(self.folder, image_name)
        image_file = os.path.join(self.folder, image_name)
        width = 1000
        height = 1000
        exported_image = cmds.playblast(orn=True, c='jpg', st=cmds.currentTime(query=True),
                                        et=cmds.currentTime(query=True), w=width, h=height, p=100, v=False, fo=True,
                                        fmt='image', f=image_file, cc=True, os=True, fp=1)
        return exported_image

    #---------------------------------------------------------------------------------------------

    def export_sel(self, path=None, name=None):

        self.name = name

        if not path:
            path = os.path.join(self.folder, name)

        if not path and not name:
            path = self.get_file_path(name=name)


        print(path)
        cmds.file(rename=path)
        cmds.file(type="mayaAscii", exportSelected=True,
                  preserveReferences=True, shader=True, expressions=False,
                  constructionHistory=True)

        return path

    #---------------------------------------------------------------------------------------------

    def get_shelves_path(self):
        shelves_path = os.path.join(cmds.internalVar(usd=True), 'Mutant_Shelves')
        return shelves_path

    #---------------------------------------------------------------------------------------------

    def get_file_path(self, folder=None, name=None):

        if not folder:
            folder = self.folder
        else:
            self.folder = folder

        if not name:
            name = self.name
        else:
            self.name = name

        if not folder:
            cmds.error('File Path != working, we need a path for this to work...')

        if not name:
            name = self.create_new_name()

        self.file_path = os.path.join(folder, name)

        return self.file_path

    #---------------------------------------------------------------------------------------------

    def create_new_name(self):
        import uuid
        return str(uuid.uuid4().hex+'.ma')

    #---------------------------------------------------------------------------------------------

    def open_shelves_in_explorer(self):
        try:
            import subprocess
            subprocess.Popen('explorer "{}"'.format(self.folder))
        except:
            os.system('xdg-open "{}"'.format(self.folder))

        return True

    #---------------------------------------------------------------------------------------------

    def list_shelved_files(self):
        import glob
        files = glob.glob(os.path.join(self.folder, '*.ma'))
        return files

    #---------------------------------------------------------------------------------------------

