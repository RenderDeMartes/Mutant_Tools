'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:
import imp
import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import SkinUtils
imp.reload(Mutant_Tools.Utils.IO.SkinUtils)

skin = SkinUtils.Skinning()
skin.FUNC_NAME(argument = '')

#----------------
dependencies:

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

import os
import json
import imp
from maya import cmds
import Mutant_Tools
import maya.mel as mel
from pathlib import Path

from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH = os.path.join(*PATH.parts[:-2], 'Config')

JSON_FILE = (os.path.join(PATH, "name_conventions.json"))
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)

#----------------------------------------------------------

class Skinning(object):

    def __init__(self):

        self.bind_joints = cmds.ls('*{}'.format(nc['joint_bind']))
        self.skin_nodes = cmds.ls('*{}'.format(nc['skin_cluster']))

    # ----------------------------------------------------------
    def update_properties(self):
        self.bind_joints = cmds.ls('*{}'.format(nc['joint_bind']))
        self.skin_nodes = cmds.ls('*{}'.format(nc['skin_cluster']))

    # ----------------------------------------------------------

    def bind_to_bnd(self, geo=None):

        if geo is None:
            geo = cmds.ls(sl=True)

        self.update_properties()
        try: mel.eval('doDetachSkin "2" { "1","1" };')
        except: pass
        skin = self.bind_skin(joints=self.bind_joints, geo=geo)
        return skin

    # ----------------------------------------------------------

    def deformable_dual_quaternion(self, skin = None):
        if skin == None:
            skin = cmds.ls(sl=True)

        try:
            cmds.setAttr('{}.skinningMethod'.format(skin), 1)
            cmds.setAttr('{}.dqsSupportNonRigid'.format(skin), 1)
        except:
            cmds.warning('No skin selected.')

    # ----------------------------------------------------------

    def get_skins(self):
        return cmds.ls(typ='skinCluster')

    # ----------------------------------------------------------
    def get_all_geo_with_skin(self):

        skinned_geos = []
        skins = self.get_skins()
        shapes = set(sum([cmds.skinCluster(c, q=1, g=1) for c in skins], []))
        for s in shapes:
            if cmds.nodeType(s) == 'mesh':
                transform_node = cmds.listRelatives(s, p=True)
                if transform_node:
                    skinned_geos.append(transform_node[0])

        return skinned_geos

    # ----------------------------------------------------------

    def rename_skin_clusters(self, input):
        return cmds.rename(input, input + nc['skin_cluster'])

    #----------------------------------------------------------

    def bind_skin(self, joints=None, geo=None):

        if joints == None:
            joints = self.bind_joints
        if geo == None:
            geo = cmds.ls(sl=True)

        if  not type(geo) == 'list':
            geo = [geo]

        for transform in geo:
            if cmds.nodeType(transform) == 'transform':
                cmds.select(joints,transform)
                skin = cmds.skinCluster(toSelectedBones=True)[0]
                skin=cmds.rename(skin, '{}{}'.format(transform, nc['skin_cluster']))
                self.deformable_dual_quaternion(skin=skin)

        return skin

    #----------------------------------------------------------


