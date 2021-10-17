import maya.cmds as cmds
for item in cmds.resourceManager(nf='*png'):
    cmds.resourceManager(s=(item, "C:\\Users\\PC\\Documents\\maya\\2022\\scripts\\Mutant_Tools\\Icons\\MayaIcons\\{0}".format(item)))
