from __future__ import absolute_import
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
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import EasySkin
reload(Mutant_Tools.Utils.IO.EasySkin)

EasySkin.save_all_skins_to()
EasySkin.load_all_skins_from()

EasySkin.save_selected_geos()
EasySkin.load_selected_geos()

#----------------
dependencies:

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

from maya import cmds
import os
import glob
from pathlib import Path
from os import listdir
from os.path import isfile, join
import pprint

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import SkinUtils
reload(Mutant_Tools.Utils.IO.SkinUtils)
cSkin = SkinUtils.Skinning()

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

import Mutant_Tools


def save_all_skins_to(folder_path=''):

    if not folder_path:
        folder_path = mh.folder_window()
        print(folder_path)

    skins = cmds.ls(type='skinCluster')
    if not skins:
        cmds.warning('No Skins on the scene')
        return

    geos = []
    from Mutant_Tools.UI.ProgressBar import load_progress_bar
    reload(load_progress_bar)
    cProgressBarUI = load_progress_bar.ProgressBarUI(items=skins, title='Saving Skins')
    cProgressBarUI.show()
    for num, skin in enumerate(skins):
        geo = cSkin.get_geo_from_skin(skin=skin)[0]
        #geo = cmds.listRelatives(shape, p=True)[0]
        geos.append(geo)
        print(skin, geo)

        # save
        cProgressBarUI.set_percent(num)

        data = cSkin.get_weights(geo)
        cSkin.save(data=data, path=os.path.join(folder_path, geo+'.json'))
    cProgressBarUI.close()

def load_all_skins_from(folder_path='', accept_errors=True, namespace=False, avoid_rename=[]):

    if not folder_path:
        folder_path = mh.folder_window()

    skin_files = glob.glob(os.path.join(folder_path, '*'))
    if not skin_files:
        cmds.warning('No Skin Files on Selected Folder')
    from Mutant_Tools.UI.ProgressBar import load_progress_bar
    reload(load_progress_bar)
    cProgressBarUI = load_progress_bar.ProgressBarUI(items=skin_files, title='Loading Skins')
    cProgressBarUI.show()

    errors = []
    for num, file in enumerate(skin_files):
        cProgressBarUI.set_percent(num)
        geo = os.path.basename(file).replace('.json', '')
        print(file, geo)
        if not cmds.objExists(geo):
            continue
        print(cmds.nodeType(geo))
        if cmds.nodeType(geo) != 'mesh':
            continue
        skin_data = cSkin.load_data(path=file)
        if namespace and avoid_rename:
            skin_data = add_namespace_to_json(file, namespace, avoid_rename)
            #pprint.pprint(skin_data)
        #try:
        cSkin.set_weights(all_data=skin_data, geometry=geo, remove_unused=True, namespace=namespace, crowd_joints=avoid_rename)
        '''
        except Exception as e:
            if not accept_errors:
                print(file)
                cmds.error(e)
            print(e)
            errors.append(e)
        '''
        

    if errors:
        for e in errors:
            print('?' * 50)
            print('?' * 50)
            print('?' * 50)
            print(e)
            print('?' * 50)
            print('?' * 50)
            print('?' * 50)

    print('Import Complete')
    cProgressBarUI.close()
def save_selected_geos(folder_path=''):

    if not folder_path:
        folder_path = mh.folder_window()
        print(folder_path)

    geos = cmds.ls(sl=True)
    from Mutant_Tools.UI.ProgressBar import load_progress_bar
    reload(load_progress_bar)
    cProgressBarUI = load_progress_bar.ProgressBarUI(items=geos, title='Saving Skins')
    cProgressBarUI.show()

    for num, geo in enumerate(geos):
        # save
        cProgressBarUI.set_percent(num)
        shape=cmds.listRelatives(geo, s=True)[0]
        data = cSkin.get_weights(shape)
        cSkin.save(data=data, path=os.path.join(folder_path, shape+'.json'))
    cProgressBarUI.close()
def load_selected_geos(folder_path=''):

    if not folder_path:
        folder_path = mh.folder_window()

    skin_files = glob.glob(os.path.join(folder_path, '*'))
    geos = cmds.ls(sl=True)
    if not skin_files:
        cmds.warning('No Skin Files on Selected Folder')
    from Mutant_Tools.UI.ProgressBar import load_progress_bar
    reload(load_progress_bar)
    cProgressBarUI = load_progress_bar.ProgressBarUI(items=skin_files, title='Loading Skins')
    cProgressBarUI.show()
    for file in skin_files:
        for desire_geo in geos:
            geo = os.path.basename(file).replace('.json', '')
            if not desire_geo in geo:
                continue
            print("Importing:", desire_geo)
            print(file, geo)
            if not cmds.objExists(geo):
                continue
            print(cmds.nodeType(geo))
            if cmds.nodeType(geo) != 'mesh':
                continue
            skin_data = cSkin.load_data(path=file)
            cSkin.set_weights(all_data=skin_data, geometry=geo, remove_unused=True)

        #print('Skinning Import Complete on:', geo)

    #Force Test
    # print(os.path.join(folder_path, 'SUITFBXASC046001Shape.json'))
    # skin_data = cSkin.load_data(path=os.path.join(folder_path, 'SUITFBXASC046001Shape.json'))
    # cSkin.set_weights(all_data=skin_data, geometry='SUITFBXASC046001Shape', remove_unused=True)
    cProgressBarUI.close()
    print('Import Complete')

def add_namespace_to_json(file, namespace, avoid_this=[]):

    skin_data = cSkin.load_data(path=file)
    new_data = {}
    for geo in skin_data:
        new_data[geo] = {}
        new_data[geo]['count'] = skin_data[geo]['count']
        new_data[geo]['geo'] = skin_data[geo]['geo']
        influences = []
        for inf in skin_data[geo]['influences']:
            influences.append('{}:{}'.format(namespace, inf))
        new_data[geo]['influences'] = influences
        weights = {}
        new_data[geo]['weights'] = weights  # Assign the 'weights' dictionary to the 'new_data' dictionary
        for w in skin_data[geo]['weights']:
            new_data[geo]['weights'][w] = {}  # Initialize a new dictionary for 'w'
            for jnt in skin_data[geo]['weights'][w]:
                if jnt in avoid_this:
                    new_data[geo]['weights'][w]['{}'.format(jnt)] = skin_data[geo]['weights'][w][jnt]
                else:
                    new_data[geo]['weights'][w]['{}:{}'.format(namespace, jnt)] = skin_data[geo]['weights'][w][jnt]

        #import pprint
        #pprint.pprint(new_data)

    return new_data