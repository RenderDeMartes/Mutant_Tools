
#change colors start
from maya import cmds
def change_colors(): 
    gMainWindow = maya.mel.eval('$tmpVar=$gMainWindow')
    cmds.window(gMainWindow, e=True, mw=True, bgc=(0.31, 0.3, 0.5))
cmds.evalDeferred(change_colors)
#change colors end
#import comet start
from maya import mel
def import_comet():
    mel.eval('source "cometMenu"')
cmds.evalDeferred(import_comet)
#import comet end

