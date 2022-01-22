'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

import imp
import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import mt_menu
imp.reload(Mutant_Tools.Utils.mt_menu)
mt_menu.create_mutant_menu()


#----------------
dependencies:


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

import re
import os
import sys
import imp
import maya.mel as mel
from pathlib import Path
from functools import partial

from maya import cmds

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()
try:mt.compare_versions()
except:pass
# -------------------------------------------------------------------------------------------

PATH = os.path.dirname(__file__)
ICONS_PATH = PATH.replace('\\Utils', '//Icons//')

# -------------------------------------------------------------------------------------------

def help(*args):
    cmds.launch(web="http://mutanttools.com/")

# -------------------------------------------------------------------------------------------

def open_rig_builder(*args):
    import imp
    import Mutant_Tools
    from Mutant_Tools.UI.AutoRigger import load_autoRigger
    imp.reload(load_autoRigger)
    try:
        AutoRigger.close()
    except:
        pass
    AutoRigger = load_autoRigger.AutoRigger()
    AutoRigger.show()


def load_guide_placement(self):
    from Mutant_Tools.UI.GuidePlacements import load_guide_placements
    imp.reload(load_guide_placements)

    try:
        cGuidePlacements.close()
    except:
        pass
    cGuidePlacements = load_guide_placements.GuidePlacements()
    cGuidePlacements.show()

def open_block_builder(*args):
    import imp
    import Mutant_Tools
    from Mutant_Tools.UI.BlockBuilder import load_blockBuilder
    import imp
    imp.reload(load_blockBuilder)

    try:
        BlockBuilder.close()
    except:
        pass
    BlockBuilder = load_blockBuilder.BlockBuilder()
    BlockBuilder.show()

def view_log(*args):
    import Mutant_Tools
    from Mutant_Tools.UI.CodeReader import load_codeReader
    import imp
    imp.reload(load_codeReader)

    try:
        codeUI.close()
    except:
        pass

    log_file = mt.Mutant_logger(mode='log')
    with open(log_file) as log_data:
        log = log_data.read()

    codeUI = load_codeReader.Code_Reader(mode='view', code=log, config_attr='')
    codeUI.ui.code_text.verticalScrollBar().setValue(codeUI.ui.code_text.verticalScrollBar().maximum())
    codeUI.set_path_label(code_path=PATH.replace('\\Utils', '/log.txt'))
    codeUI.show()


def open_website(website='http://mutanttools.com/', mode = 'view'):
    from Mutant_Tools.UI.WebsiteViewer import load_website_viewer
    imp.reload(load_website_viewer)
    cWebsiteViewer = load_website_viewer.WebsiteViewerUI(website=website)
    if mode == 'view':
        cWebsiteViewer.show()
    else:
        cWebsiteViewer.open_link(website)


def rigging_tutorial(*args):
    open_website('https://mutanttools.com/riggers/')

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
    imp.reload(discord)
    discord.send_bugs()

def request_feature(*args):
    from Mutant_Tools.Utils.Helpers import discord
    imp.reload(discord)
    discord.send_requests()

def contact(*args):
    open_website('https://mutanttools.com/contact/')

def download_latest(*args):
    open_website('https://mutanttools.com/#download', 'open')

def open_rig_tools(*args):
    import imp
    import Mutant_Tools
    from Mutant_Tools.UI.RigTools import load_RigTools
    imp.reload(load_RigTools)

    try:
        cRigToolsUI.close()
    except:
        pass
    cRigToolsUI = load_RigTools.RigTools_UI()
    cRigToolsUI.show()

def tools_tutorial(*args):
    open_website('https://mutanttools.com/')
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

    menu_organizer = {"Mutant Tools": {
                            "Open Website": help,
                            "Download Latest": download_latest
                            },


            "Auto Rigger" :{
                            "Open Autorigger": open_rig_builder,
                            "Guide Placement" : load_guide_placement,
                            "Tutorial": rigging_tutorial,
                            "View Log": view_log,
                            "Help": riggers_help
                             },
            "Rigging Tools":{
                            "Rig Tools": open_rig_tools,
                            "Tutorial" : tools_tutorial
                            },

            "Developers" :{
                            "Block Builder": open_block_builder,
                            ".mt commands": mt_commands,
                            "Create Blocks Help": developers_block_help
                            },


            "Dependencies": {
                            "Ng Skin Tools V2": install_ng
                            },

            "Donate": {
                     "Paypal": donate_paypal,
                     "Crypto": donate_crypto
                    },


            "Discord": {
                        "Join Community": join_discord,
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

                    'Ng Skin Tools V2':'Ng.png',

                    'Discord': 'Discord.png',
                    'Join Community':'Discord.png',
                    "Report Bug": "Bot.png",
                    "Request Feature": "HeadNeck.png",

                    'Paypal':'Paypal.png',
                    'Crypto':'BTC.png',
                    }

    #-------------------------------------------------------------------------------------------

    for item in menu_organizer:
        if item in icon_buttons:
            icon = icon_buttons[item]
        else:
            icon = ''
        cmds.setParent('MutantTools', menu=1)
        menu_item = cmds.menuItem(sm=True, to=True, ann='', l=item, i= ICONS_PATH + icon)

        submenus = menu_organizer[item]
        for subitem in submenus:
            if subitem in icon_buttons:
                icon = icon_buttons[subitem]
            else:
                icon = ''
            cmds.setParent(menu_item, menu=1)
            submenu_item = cmds.menuItem(l=subitem, c=submenus[subitem], i= ICONS_PATH + icon)

    #-------------------------------------------------------------------------------------------

def put_in_userSetup():
    load = """\n
#Start Mutant Tools
#--------------------------------
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
#--------------------------------
#End Mutant Tools
    
"""

    #read data
    user_setup_path = '{}\\userSetup.py'.format(PATH.replace('\\Mutant_Tools\\Utils', ''))

    if os.path.isfile(user_setup_path):
        userSetup = open(user_setup_path, "r")
        print('userSetup Exists')
    else:
        userSetup = Path('{}\\userSetup.py'.format(PATH.replace('\\Mutant_Tools\\Utils', '')))
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


