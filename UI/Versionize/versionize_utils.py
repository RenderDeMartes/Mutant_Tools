from __future__ import absolute_import
"""
The idea of this is to be able to publish Mutant_Tools to web without the source code

#How to

from Mutant_Tools.UI.Versionize import versionize_utils
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
reload(versionize_utils)

cVersionize = versionize_utils.Versionize()

cVersionize.new_folder
cVersionize.duplicate_mutant_folder()
(delete wiki folder and versionize before continue)
cVersionize.replace_all_strings()
cVersionize.print_new_load_code()

"""
import os
from os import listdir
from os.path import isfile, join
import pprint
import shutil

import sys
import glob
from pathlib import Path
import json
from distutils.dir_util import copy_tree

from maya import cmds

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

import Mutant_Tools
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

VERSION_FILE = os.path.join(FOLDER, 'config', 'version.json')
with open(VERSION_FILE) as version_file:
	version = json.load(version_file)

mutant_version = version['version']
print(mutant_version)

#----------------------------------------------------------------
#----------------------------------------------------------------

replace_this_strings = {

    "'SP'":"'ES'",
    "'sp'": "'es'",
    "'Sp'": "'Es'",
    "'sP'": "'eS'",
    '"SP"': '"ES"',
    '"sp"': '"sp"',
    '"Sp"': '"Es"',
    '"sP"': '"eS"',
    "'AG'": "'TE'",
    "'ag'": "'te'",
    "'Ag'": "'Te'",
    "'aG'": '"tE"',
    '"AG"': '"TE"',
    '"ag"': '"te"',
    '"Ag"': '"Te"',
    '"aG"': '"tE"',
    'MOR': 'BAN',
    'mor': 'ban',
    'Mor': 'Ban',
    'stellar': 'rdm',
    'Stellar': 'RdM',
    'STELLAR': 'RDM',
    'Sandbox' : 'SB',
    'sandbox': 'sb',
    'rstar': 'dogr',
    'mstar': 'dogm',
    'rigSystem': 'bubbles',
    'get_one_sid': 'get_that_node',
    'validate_sid': 'validate_that_node',
    'sid =': 'node =',
    'Project.findby_name': 'P.do_that',
    'AnythingGoes':'WatterBottle',
    'anythinggoes':'watterbottle',
    'Anythinggoes':'Watterbottle',
    'rid =': 'node =',
    'rid.sid.tag_node': 'mpaz',
    'set_tag': 'nachos',
    'assetTemplates': 'sukiTemp',
    'get_hierarchy': 'getFood',
    'get_that_node': 'thatNode',
    'assetChecks': 'cleaner',
    'Shampoo': 'Review',
    'Frank': 'Erick',
    'frank': 'erick',
    'sebastian.cisneros': 'esteban.rodriguez',
    'BasemeshFZombieA': 'base_geoA',
    'BasemeshMZombieA': 'base_geoB',
    'job/': 'disk/',
    'pipeline': 'worlflow',
    'net/': 'red/',
    'KidDodgeball3' : 'guy3',
    "carlos" : "Gabriel",
    "cesar": "Diana",
    "gaston" : "Mike",
    "alejandro" : "Leo",
    "jean" : "Jessy",
    "ricardo" : "Dan",
    "sebastian" : "Jose",
    "alejandra" : "Clara",
    "brisa" : "Pedro",
    "luis" : "Lourdes",
    "Carlos" : "Gabriel",
    "Cesar": "Diana",
    "Gaston" : "Mike",
    "Alejandro" : "Leo",
    "Jean" : "Jessy",
    "Ricardo" : "Dan",
    "Sebastian" : "Jose",
    "Alejandra" : "Clara",
    "Brisa" : "Pedro",
    "Luis" : "Lourdes",
    "Chacon": "Rodriguez",
    "chacon": "rodriguez"
}

#----------------------------------------------------------------
#----------------------------------------------------------------

class Versionize(object):

    def __init__(self):

        self.new_folder = os.path.join(cmds.internalVar(usd=True), 'Mutant_Tools_v{}'.format(mutant_version))
        print(self.new_folder)
        self.omit_list = ['.mb', '.ma', '.psd', '__init__', '.pyc', '.wrap', '.abc', '.png', '.otf', '.jpg', '.git', '.gitignore', 'Qt Designer Setup.exe', 'Qt Designer.dmg', 'DemBones', 'git']
        self.omit_strings = ['setWindowFlags', 'grid =', 'Carlos Chacon L.', 'author = Sebastian Cisneros Sojo', 'By Gaston Aguilar', 'By Ricardo Quiros', 'Franklin Gothic Book']

    # ----------------------------------------------------------------

    def duplicate_mutant_folder(self):
        """

        Returns:

        """

        #print(FOLDER)
        target_folder =  os.path.join(cmds.internalVar(usd=True), 'Mutant_Tools_v{}'.format(mutant_version), 'Mutant_Tools')

        if os.path.exists(target_folder):
            shutil.rmtree(target_folder, ignore_errors=True)

        os.makedirs(target_folder, exist_ok=False)
        #print(target_folder)

        copy_tree(FOLDER, target_folder)

        self.new_folder = target_folder

        self.create_init_file()

        print('remember to delete:', self.new_folder, '/UI/Versionize/versionize_utils')


    def create_init_file(self):

        with open(os.path.join(self.new_folder, '__init__.py'), "w", encoding="utf-8") as f:
            f.write('')

    # ----------------------------------------------------------------

    def get_all_files(self):

        dirName = self.new_folder

        # Get the list of all files in directory tree at given path
        listOfFiles = getListOfFiles(dirName)

        # # Print the files
        # for elem in listOfFiles:
        #     print(elem)
        # print("****************")

        # Get the list of all files in directory tree at given path
        listOfFiles = list()
        for (dirpath, dirnames, filenames) in os.walk(dirName):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]

        # Print the files
        return listOfFiles

    # ----------------------------------------------------------------

    def get_all_py_files(self):
        all_files = self.get_all_files()

        py_files=[]
        for file in all_files:
            if '.py' in file:
                if '.pyc' in file:
                    continue
                else:
                    py_files.append(file)

        return py_files

    def get_all_local_py_files(self):

        dirName = FOLDER

        # Get the list of all files in directory tree at given path
        listOfFiles = getListOfFiles(dirName)

        # # Print the files
        # for elem in listOfFiles:
        #     print(elem)
        # print("****************")

        # Get the list of all files in directory tree at given path
        listOfFiles = list()
        for (dirpath, dirnames, filenames) in os.walk(dirName):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]

        # Print the files
        all_files = listOfFiles

        py_files=[]
        for file in all_files:
            if '.py' in file:
                if '.pyc' in file:
                    continue
                else:
                    py_files.append(file)

        return py_files

    # ----------------------------------------------------------------

    def replace_strings(self, file):

        file_data = {}
        for s in replace_this_strings:
            with open(file, encoding="utf8") as f:
                lines = f.readlines()
                newText = []
                for line in lines:
                    omit_this_line =False
                    for ol in self.omit_strings:
                        if ol in line:
                            omit_this_line=True
                    if omit_this_line:
                        line = line
                    else:
                        if s in line:
                            og_line = line
                            line = line.replace(s, replace_this_strings[s])
                            file_data[s] = og_line
                    newText.append(line)

            with open(file, "w", encoding="utf-8") as f:
                f.writelines(newText)

        return file_data

    # ----------------------------------------------------------------

    def replace_all_strings(self):

        omit_list = self.omit_list
        files_data = {}
        all_files = self.get_all_files()
        for file in all_files:

            #print('Start removing strings on:', file)

            #Amot file types
            omit_this_one = False
            for omit in omit_list:
                if omit in file:
                    omit_this_one = True
                    #print(omit)
            if omit_this_one:
                #print('Omitting File:', file)
                continue

            #Replace studio strings to be safe
            file_data = self.replace_strings(file=file)
            print('Removed strings on:', file)
            if file_data:
                files_data[file] = file_data

        import pprint
        pprint.pprint(files_data)

        mh.write_json(path=cmds.internalVar(usd=True), json_file='mutant_versionize_strings.json', data=files_data)

        print('replace_all_strings', 'Done')
        print('Finished')
        print('#'*50)
        print('#'*50)
        print('#'*50)
        print('remember to delete:', self.new_folder, '/UI/Versionize/versionize_utils', 'Config/Studio.json')

    # ----------------------------------------------------------------

    def remove_all_reloads_in_files(self):

        py_files = self.get_all_py_files()

        for file in py_files:
            #print(file)
            with open(file, encoding="utf8") as f:
                original_text_lines = f.readlines()
                new_lines = []
                for line in original_text_lines:
                    if 'reload(' in line:
                        line=line.replace('imp.reload(', '#imp.reload(').replace('reload(', '#reload(')
                    new_lines.append(line)

            with open(file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)


    # ----------------------------------------------------------------

    def cache_all_files(self):

        omit_files = ['__init__', 'exec_block_sides', 'get_maya_icons', 'user_setup', 'Exec_Block', 'userSetup', 'exec_postbuilds', 'exec_spaceSwitch', 'HIK_BipedDefinition']

        sys.path.insert(0, os.path.join(self.new_folder))
        sys.path.insert(0, os.path.join(self.new_folder, 'Mutant_Tools'))

        py_files = self.get_all_py_files()
        #py_files = self.get_all_local_py_files()


        #Add path to sys
        for file in py_files:
            #Get file and file
            path = Path(file)
            path_parts = path.parts[:-1]
            file = path.parts[-1].replace('.py', '')

            new_path=''
            for f in path_parts:
                new_path = os.path.join(FOLDER, f)
            #print(new_path, file)

            sys.path.insert(0, new_path)


        #Execute impor reloads
        for file in py_files:
            #Get file and file
            path = Path(file)
            path_parts = path.parts[:-1]
            file = path.parts[-1].replace('.py', '')

            #omit certain files that will error the import
            omit_this_one=False
            for omit in omit_files:
                if omit == file:
                    omit_this_one=True
            if omit_this_one:
                continue

            new_path=''
            for f in path_parts:
                new_path = os.path.join(FOLDER, f)
            #print(new_path, file)

            #Impor reload
            #sys.path.insert(0, new_path)

            #("*" * 50)
            try:
                exec('import {}'.format(file))
            except Exception as e:
                ''
                #print('Error Import:', new_path, file)
                #print(e)

            try:
                exec('reload {}'.format(file))
            except Exception as e:
                ''
                #print("*" * 50)
                #print('Error Reload:', new_path, file)
                #print(e)


    def delete_all_non_block_py_files(self):

        py_files = self.get_all_py_files()
        for file in py_files:
            if not 'Blocks' in file:
                ''
                #print(file)
                #Do Delete
            #print(file)

    def hard_code_remove_studio_stuff(self):

        #Remove Studio Blocks
        templates_folder = os.path.join(self.new_folder, 'Mutant_Tools', 'Utils', 'IO', 'Guide_Data')
        #print(templates_folder)
        guides = glob.glob(os.path.join(templates_folder, '*'))
        #print(guides)
        for guide in guides:
            #print(guide)
            if 'AG' in guide:
                shutil.copy(guide, guide.replace('AG', 'AF'))
                os.remove(guide)

            if 'Sausage' in guide:
                shutil.copy(guide, guide.replace('Sausage', 'Toon'))
                os.remove(guide)


    def rename_file(self, file):
        #cVersionize.rename_file(file='C://Users//Esteban//Documents//maya//2022//scripts//Mutant_Tools_v1.03//Mutant_Tools//Blocks//001_Studio//02_Human_Fixes.json')

        #folder = self.new_folder
        for s in replace_this_strings:
            #print(s, file)
            if s in file:
                shutil.copy(file, file.replace(s, replace_this_strings[s]))
                os.remove(file)
                #print("renamed: {}".format(new_name))
                return file.replace(delete_string, add_string)

        return False

    def rename_all_files(self):

        all_files = self.get_all_files()

        # rename_file
        for file in all_files:
            #print(file)
            new_name = self.rename_file(file)

        print('remember to delete:', self.new_folder, '/UI/Versionize/versionize_utils')

    def print_new_load_code(self):
        print("""
import sys
import os
from maya import cmds
mutant_path = '{}'
if mutant_path not in sys.path:
    sys.path.append(mutant_path)
    
import Mutant_Tools

import Mutant_Tools.UI.AutoRigger.load_autoRigger as load_autoRigger
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

reload(load_autoRigger)

try:AutoRigger.close()
except:pass
AutoRigger = load_autoRigger.AutoRigger()
AutoRigger.show()
        
        
        """.format(self.new_folder))

        print('remember to delete:', self.new_folder, '/UI/Versionize/versionize_utils')



#----------------------------------------------------------------
#----------------------------------------------------------------
#----------------------------------------------------------------
#----------------------------------------------------------------

#Utils found online
#https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

