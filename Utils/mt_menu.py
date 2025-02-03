from __future__ import absolute_import, division
'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import mt_menu
reload(Mutant_Tools.Utils.mt_menu)
mt_menu.create_mutant_menu()
mt_menu.put_in_userSetup()

#----------------
dependencies:


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''
import re
import os
import sys
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import maya.mel as mel
from pathlib import Path
from functools import partial

from maya import cmds

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()
#try:mt.compare_versions()
#except:pass
# -------------------------------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-1]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)
ICONS_PATH = os.path.join(FOLDER, 'Icons')
# -------------------------------------------------------------------------------------------

def help(*args):
    cmds.launch(web="http://mutanttools.com/")

# -------------------------------------------------------------------------------------------

def open_rig_builder(*args):
    try:
        import importlib;from importlib import reload
    except:
        import imp;from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.AutoRigger import load_autoRigger
    reload(load_autoRigger)
    try:
        AutoRigger.close()
    except:
        pass
    AutoRigger = load_autoRigger.AutoRigger()
    AutoRigger.show()


def load_guide_placement(self):
    from Mutant_Tools.UI.GuidePlacements import load_guide_placements
    reload(load_guide_placements)

    try:
        cGuidePlacements.close()
    except:
        pass
    cGuidePlacements = load_guide_placements.GuidePlacements()
    cGuidePlacements.show()

def open_block_builder(args):
    try:
        import importlib;from importlib import reload
    except:
        import imp;from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.BlockBuilder import load_blockBuilder
    try:
        import importlib;from importlib import reload
    except:
        import imp;from imp import reload

    reload(load_blockBuilder)

    try:
        BlockBuilder.close()
    except:
        pass
    BlockBuilder = load_blockBuilder.BlockBuilder()
    BlockBuilder.show()

def view_log(*args):
    import Mutant_Tools
    from Mutant_Tools.UI.CodeReader import load_codeReader
    try:
        import importlib;from importlib import reload
    except:
        import imp;from imp import reload

    reload(load_codeReader)

    


def open_website(website='http://mutanttools.com/', mode = 'view'):
    from Mutant_Tools.UI.WebsiteViewer import load_website_viewer
    reload(load_website_viewer)
    cWebsiteViewer = load_website_viewer.WebsiteViewerUI(website=website)
    if mode == 'view':
        cWebsiteViewer.show()
    else:
        cWebsiteViewer.open_link(website)


def riggers_help(*args):
    open_website('https://mutanttools.com/riggers/')

def mt_commands(*args):
    open_website('https://mutanttools.com/mt_commands/')

def developers_block_help(*args):
    open_website('https://mutanttools.com/block-creator/')

def install_ng(*args):
    open_website('https://www.ngskintools.com/get/', 'open')

def donate_paypal(*args):
    open_website('https://www.paypal.com/paypalme/renderdemartes', 'open')

def donate_crypto(*args):
    open_website('https://mutanttools.com/donate/')

def join_discord(*args):
    open_website('https://discord.gg/pqGeYhUcAW', 'open')

def report_bug(*args):
    from Mutant_Tools.Utils.Helpers import discord
    reload(discord)
    discord.send_bugs()

def request_feature(*args):
    from Mutant_Tools.Utils.Helpers import discord
    reload(discord)
    discord.send_requests()

def contact(*args):
    open_website('https://mutanttools.com/contact/')

def download_latest(*args):
    open_website('https://mutanttools.com/#download', 'open')

def open_rig_tools(*args):
    try:
        import importlib;from importlib import reload
    except:
        import imp;from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.RigTools import load_RigTools
    reload(load_RigTools)

    try:
        cRigToolsUI.close()
    except:
        pass
    cRigToolsUI = load_RigTools.RigTools_UI()
    cRigToolsUI.show()

def tools_tutorial(*args):
    open_website('https://mutanttools.com/')

def face_install(*args):
    try:
        import importlib;
        from importlib import reload
    except:
        import imp;
        from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.FaceInstall import load_face_install
    reload(load_face_install)

    try:
        cFaceInstallUI.close()
    except:
        pass
    cFaceInstallUI = load_face_install.FaceInstallUI()
    cFaceInstallUI.show()

def zombinator(*args):
    import Mutant_Tools.UI
    try:
        import importlib;
        from importlib import reload
    except:
        import imp;
        from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.Zombinator import load_zombinator
    reload(load_zombinator)

    try:
        cZombinator.close()
    except:
        pass
    cZombinator = load_zombinator.Zombinator()
    cZombinator.show()

def shelves(*args):
    try:
        import importlib;
        from importlib import reload
    except:
        import imp;
        from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.Shelves import load_shelves
    reload(load_shelves)

    try:
        cShelvesUI.close()
    except:
        pass
    cShelvesUI = load_shelves.ShelvesUI()
    cShelvesUI.show()

def ROM(*args):
    try:
        import importlib;
        from importlib import reload
    except:
        import imp;
        from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.AnimLoader import load_anim_loader
    reload(load_anim_loader)

    try:
        cAnimLoaderUI.close()
    except:
        pass
    cAnimLoaderUI = load_anim_loader.AnimLoaderUI()
    cAnimLoaderUI.show()

def crowds(*args):
    try:
        import importlib;
        from importlib import reload
    except:
        import imp;
        from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.GamesCrowds import load_games_crowds
    reload(load_games_crowds)

    try:
        cGamesCrowds.close()
    except:
        pass
    cGamesCrowds = load_games_crowds.GamesCrowds()
    cGamesCrowds.show()

def games(*args):
    try:
        import importlib;
        from importlib import reload
    except:
        import imp;
        from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.GamesCrowds import load_games_crowds
    reload(load_games_crowds)

    try:
        cGamesCrowds.close()
    except:
        pass
    cGamesCrowds = load_games_crowds.GamesCrowds()
    cGamesCrowds.show()
    cGamesCrowds.ui.tabWidget.setCurrentIndex(2)

def helpers(*args):
    import Mutant_Tools.UI

    try:
        import importlib;
        from importlib import reload
    except:
        import imp;
        from imp import reload

    import Mutant_Tools
    from Mutant_Tools.UI.Helpers import load_helpers
    reload(load_helpers)

    try:
        cHelperUI.close()
    except:
        pass
    cHelperUI = load_helpers.HelperUI()
    cHelperUI.show()

def shapes(*args):
    open_website('https://www.braverabbit.com/shapes/', 'open')

def faceform_wrap(*args):
    open_website('https://faceform.com/', 'open')


# -------------------------------------------------------------------------------------------

def create_mutant_menu(*args):
    gMainWindow = mel.eval('$temp1=$gMainWindow')

    if cmds.menu('MutantTools', q=1, exists=1):
        cmds.menu('MutantTools', e=1, dai=1)
        cmds.deleteUI('MutantTools')
        cmds.menu('MutantTools', p='MayaWindow', l="Mutant-Tools", to=True)
    else:
        cmds.menu('MutantTools', p='MayaWindow', l="Mutant-Tools", to=True)

    #-------------------------------------------------------------------------------------------

    menu_organizer = {

            "Mutant Tools": {
                            "Open Website": help,
                            "Download Latest": download_latest,
                            "Line": '',
                            ":)" : make_maya_pretty,
                            ";)": make_outliner_pretty,
                            },


            "Rigging" :{    "Rig Tools": open_rig_tools,
                            "Helpers": helpers,
                            "Line" : '',
                            "Open Autorigger": open_rig_builder,
                            "Face Install" : face_install,
                            "AnotherLine": '',
                            "View Log": view_log,
                            "Help": riggers_help
                             },

            "Games/Crowds" : { "Games" : games,
                               "Crowds": crowds,

                    },

            "Misc" : {"Zombinator" : zombinator,
                      "ROM" : ROM,
                      "Scene Shelves" : shelves,
                    },

            "Developers" :{
                            "Block Builder": open_block_builder,
                            "Line" : '',
                            ".mt commands": mt_commands,
                            "Help": developers_block_help
                            },


            "Dependencies": {
                            "Ng Skin Tools V2": install_ng,
                            "Brave Rabbit Shapes" : shapes,
                            "Faceform Wrap" : faceform_wrap,
                            },

            "Donate": {
                     "Paypal": donate_paypal,
                     "Crypto": donate_crypto
                    },


            "Discord": {
                        "Join Community": join_discord,
                        "Line":'',
                        "Report Bug": report_bug,
                        "Request Feature": request_feature
                        },

            "Help": {
                    "Contact": contact,
                    "Update":download_latest
                    }
            }

    #-------------------------------------------------------------------------------------------

    icon_buttons = {'Mutant Tools': 'LogoBlack03.png',
                    'Open Autorigger':'LogoWhite03.png',

                    'Discord': 'Discord.png',
                    'Join Community':'Discord.png',
                    "Report Bug": "Bot.png",
                    "Request Feature": "HeadNeck.png",

                    }

    #-------------------------------------------------------------------------------------------
    menu_items = {}
    for item in menu_organizer:
        if item in icon_buttons:
            icon = icon_buttons[item]
        else:
            icon = ''
        cmds.setParent('MutantTools', menu=1)
        menu_item = cmds.menuItem(sm=True, to=True, ann='', l=item, i= os.path.join(ICONS_PATH, icon))
        menu_items[item] = menu_item
        submenus = menu_organizer[item]
        for subitem in submenus:
            if subitem in icon_buttons:
                icon = icon_buttons[subitem]
            else:
                icon = ''
            cmds.setParent(menu_item, menu=1)
            if "Line" in subitem:
                cmds.menuItem(divider=True)
            else:
                submenu_item = cmds.menuItem(l=subitem, c=submenus[subitem], i= os.path.join(ICONS_PATH, icon))

    #-------------------------------------------------------------------------------------------

    #Add custom items
    cmds.setParent(menu_items['Mutant Tools'], menu=1)
    dvd_submenu = cmds.menuItem(l='DVD', c=run_screensaver)


def put_in_userSetup():

    # read data
    PATH = os.path.dirname(__file__)
    print(PATH)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)
    user_setup_path = os.path.join(cmds.internalVar(usd=True), 'userSetup.py')

    load = """\n
#Start Mutant Tools
try:
    from maya import cmds
    import sys
    import os
    from maya import cmds
        
    try:
        import importlib;from importlib import reload
    except:
        import imp;from imp import reload
    
    
    import Mutant_Tools
    import Mutant_Tools.Utils
    from Mutant_Tools.Utils import mt_menu
    reload(Mutant_Tools.Utils.mt_menu)
    
    def load_mutant_menu():
            try:
                import importlib;from importlib import reload
            except:
                import imp;from imp import reload
    
            import Mutant_Tools
            import Mutant_Tools.Utils
            from Mutant_Tools.Utils import mt_menu
            reload(Mutant_Tools.Utils.mt_menu)
            mt_menu.create_mutant_menu()
            
    cmds.evalDeferred(load_mutant_menu)
except:
    pass
#--------------------------------
#End Mutant Tools"""

    if os.path.isfile(user_setup_path):
        userSetup = open(user_setup_path, "r")
        print('userSetup Exists')
    else:
        userSetup = Path(user_setup_path)
        userSetup.touch(exist_ok=True)
        userSetup = open(userSetup, "r")
        print('userSetup Created')

    user_data = userSetup.readlines()
    userSetup.close()

    #check if data exists to delete it
    delete_this = False
    clean_data = []
    for line in user_data:
        clean_line = line.strip()
        if clean_line == '#Start Mutant Tools':
            delete_this = True
        if clean_line == '#End Mutant Tools':
            delete_this = False
            continue
        if delete_this:
            continue
        else:
            clean_data.append(line)

    new_userSetup = str()
    for line in clean_data:
        new_userSetup = new_userSetup + line

    new_userSetup = new_userSetup + load

    #add import data
    userSetup = open(user_setup_path, "w")
    userSetup.write(new_userSetup)
    userSetup.close()


def make_maya_pretty(*args):
    code = """
# change colors start
from maya import cmds, mel

def change_colors():
    gMainWindow = mel.eval('$tmpVar=$gMainWindow')
    cmds.window(gMainWindow, e=True, mw=True, bgc=(0.31, 0.3, 0.5))

cmds.evalDeferred(change_colors)
# change colors end
    """
    print(os.path.join(cmds.internalVar(usd=True), 'userSetup.py'))
    print(code)
    exec(code)

def make_outliner_pretty(*args):
    import maya.mel as mel
    sel = cmds.ls(sl=True)
    import random
    from random import randrange
    if not sel:
        reset_colors()

    for i in sel:
        r = randrange(255)
        g = randrange(255)
        b = randrange(255)
        rand_color = [r, g, b]
        cmds.select(i)
        cmds.setAttr ( i + ".useOutlinerColor" , True)
        cmds.setAttr(i + ".outlinerColor", r/255, g/255, b/255)

    cmds.select(sel)
    mel.eval('AEdagNodeCommonRefreshOutliners();')

def reset_colors():
    all = cmds.ls('*')
    print('Reseting')
    for i in all:
        try:
            cmds.setAttr(i + ".useOutlinerColor", False)
        except:
            pass

def run_screensaver(*args):

    code = """
######-----------DVD-----------######
from PySide2 import QtWidgets
import Mutant_Tools
from Mutant_Tools.UI.DVD import dvd

try:
    reload(dvd)

    square_app = dvd.SquareMoveApp()
    square_app.showFullScreen()
    QtWidgets.QApplication.instance().exec_()

except Exception as e:
    print("Error running screensaver: {}".format(e))"""
    exec(code)
    print(code)
