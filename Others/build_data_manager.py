from __future__ import absolute_import
"""

import Mutant_Tools
from Mutant_Tools.Others import build_data_manager
import imp
imp.reload(build_data_manager)

build_data_manager.save_build_data()

"""


from maya import cmds
import os
import json

def save_build_data():
    path = os.path.join('/home/esteban.rodriguez/maya/2022/scripts', 'build_data.json')
    if os.path.exists(path):
        print(path)
        with open(path) as data_file:
            data = json.load(data_file)
            print(data)

    else:
        return False

    blocks = cmds.ls('*_Block')
    if blocks:
        for block in blocks:
            if block in data:
                block_data = data[block]
            else:
                block_data = {}

            block_childs = cmds.listRelatives(block, c=True, ad=True, type='joint')
            if not block_childs:
                continue

            for child in block_childs:
                matrix = cmds.xform(child, q=True, m=True)
                block_data[child] = matrix

            data[block] = block_data

    with open(path, 'w') as data_file:
        json.dump(data, data_file, indent=4, sort_keys=False)
