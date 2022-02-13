'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

import imp
import Mutant_Tools
import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import Guides
imp.reload(Mutant_Tools.Utils.IO.Guides)

guides = Guides.Guides()
guides.FUNC_NAME(argument = '')

#----------------
dependencies:

NG

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

import os
import json
import imp
from pathlib import Path

from maya import cmds as cmds
from maya import OpenMaya as om

import Mutant_Tools
from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()


# ---------------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

# ---------------------------------------------------------------------------


class Guides(object):

    def __init__(self):
        self.guide = 'Mutant_Build'

    # ----------------------------------------------------------------------------------------------------------------

    def export_ma_guide(self):
        guide = self.guide
        path = mh.export_window(extension = ".ma")
        if path:
            filepath = path[0]
            cmds.select(guide)
            cmds.file(filepath, force = True, options = "v = 0", type = "mayaAscii", exportSelected = True)
            print(filepath)

    # ----------------------------------------------------------------------------------------------------------------

    def import_ma_guide(self):
        guide = self.guide

        if cmds.objExists(guide):
            cmds.confirmDialog(title='Ups, Sorry!',
                               message='We already have a  build group in the scene ---{}--, please rename it and reparent it later.'.format(guide),
                               button=['Ok'],
                               defaultButton='Ok',
                               cancelButton='Ok',
                               dismissString='Ok')
            return

        path = mh.import_window(extension = ".ma")
        if path:
            filepath = path[0]
            cmds.file(filepath, i=True, type = "mayaAscii")
            print(filepath)

    # ----------------------------------------------------------------------------------------------------------------

    def save_preset(self, path=None, name='Mutant_Preset.json'):

        build_bloc = 'Mutant_Build'
        if not cmds.objExists(build_bloc):
            return

        if name.endswith('.json') == False:
            name = name + '.json'

        if path == None:
            cmds.error('We need a path to save')

        block_preset = OrderedDict()

        # Attrs
        blocks = cmds.listRelatives(build_bloc, c=True)
        for block in blocks:
            config = cmds.listConnections(block)[1]
            print(block, config)
            block_info = {}
            attrs_data = OrderedDict()

            attrs = cmds.listAttr(config, ud=True)
            attrs_data['config'] = config
            for attr in attrs:
                # individual per atrr
                attr_data = {}
                attr_data['name'] = attr
                attr_data['value'] = cmds.getAttr(config + '.' + attr)
                attr_data['type'] = cmds.getAttr(config + '.' + attr, type=True)
                # add to attrs dic
                attrs_data[attr] = attr_data

            # ------------------------------------------------------------
            # Guide
            guides_data = OrderedDict()
            guides = cmds.listRelatives(block, ad=True)
            if guides:  # if not guides send null
                for guide in guides:
                    # avoid shapes in guides
                    if 'Shape' in guide:
                        continue
                    guide_data = {}
                    guide_data['name'] = guide
                    guide_data['matrix'] = cmds.xform(guide, q=True, m=True)
                    guide_data['parent'] = cmds.listRelatives(guide, p=True)[0]
                    guides_data[guide] = guide_data
            else:
                guides_data = {}
            # ------------------------------------------------------------

            # complete dictionary
            block_info['attrs'] = attrs_data
            block_info['guide'] = guides_data
            block_preset[block] = block_info

            import pprint
            pprint.pprint(block_preset)

            # publish
            self.write_json(path=path,
                            json_file=name,
                            data=block_preset)

    # ----------------------------------------------------------------------------------------------------------------

    def load_preset(self, path=None, name='Mutant_Preset.json'):

        build_bloc = 'Mutant_Build'
        if not cmds.objExists(build_bloc):
            cmds.group(em=True, n=build_bloc)

        if name.endswith('.json') == False:
            name = name + '.json'

        if path == None:
            cmds.error('We need a path to Load')

        data = self.read_json(path=path,
                              json_file=name)

        import pprint
        pprint.pprint(data)

    # ----------------------------------------------------------------------------------------------------------------

