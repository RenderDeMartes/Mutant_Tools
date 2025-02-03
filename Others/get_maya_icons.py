from __future__ import absolute_import
import maya.cmds as cmds
for item in cmds.resourceManager(nf='*png'):
    cmds.resourceManager(s=(item, "C:\\Users\\rodri\\OneDrive\\Documents\\maya\\2022\\scripts\\MayaIcons\\{}".format(item)))
