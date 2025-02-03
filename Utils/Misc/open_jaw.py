from __future__ import absolute_import
from maya import cmds, mel
import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()
nc, curve_data, setup = mt.import_configs()

from rigSystem.utils.io.core import IO
from rigSystem.utils.io import skin

from pathlib import Path
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:]
FOLDER = ''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)

def open_jaw_rig():
    """
    how to run the script
    import Mutant_Tools
    from Mutant_Tools.Utils.Misc import open_jaw
    reload(open_jaw)

    open_jaw.open_jaw_rig()


    how to save the skin:
    from rigSystem.utils.io.core import IO
    from rigSystem.utils.io import skin

    data = skin.save()
    path = '/net/pipeline/git/esteban.rodriguez/rigging/Mutant_Tools/Utils/Misc/jaw_skin_KidDodgeball3.json'
    IO.write_json(path, data)

    """
    head = 'C_Head_hi'
    jaw_vtx = ['C_Head_hi.vtx[3772]', 'C_Head_hi.vtx[644]'] #Ant Man: jaw_vtx = ['C_Head_hi.vtx[4566]', 'C_Head_hi.vtx[940]']
    chin_vtx = 'C_Head_hi.vtx[2944]' #AntMan: chin_vtx = 'C_Head_hi.vtx[3320]'

    cmds.select(jaw_vtx)
    jaw_cls = cmds.cluster()
    cmds.select(chin_vtx)
    chin_cls = cmds.cluster()

    cmds.select(cl=True)
    jaw_jnt = cmds.joint(n = 'Jaw_Jnt')
    cmds.select(cl=True)
    end_jnt = cmds.joint(n = 'Jaw_jntend')
    cmds.select(cl=True)
    null_jnt = cmds.joint(n = 'Null')

    pc1=cmds.parentConstraint(jaw_cls, jaw_jnt)
    pc2=cmds.parentConstraint(chin_cls, end_jnt)

    cmds.delete(pc1, pc2)
    cmds.delete(jaw_cls, chin_cls)

    cmds.parent(end_jnt, jaw_jnt)
    cmds.select(jaw_jnt)
    mel.eval('joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;')

    cmds.select(jaw_jnt, null_jnt, head)
    skin_cluster = cmds.skinCluster(tsb=True)

    #load skin:
    skin_data_antMan = IO.read_json(os.path.join(FOLDER, 'jaw_skin.json'))
    skin_data_KidDodgeball3 = IO.read_json(os.path.join(FOLDER, 'jaw_skin_KidDodgeball3.json'))

    skins = [skin_data_antMan]

    skin.load(skin_data_KidDodgeball3, head+'Shape')


    #Ctrl to move itq
    ctrl = mt.curve(input=jaw_jnt,
                    type='cube',
                    rename=True,
                    custom_name=True,
                    name=jaw_jnt.replace(nc['joint'], nc['ctrl']),
                    size=20)

    mt.assign_color(color='lightBlue')
    root_grp = mt.root_grp()[0]
    cmds.parentConstraint(ctrl, jaw_jnt)

    put_inside_container = [jaw_jnt, end_jnt, null_jnt, skin_cluster, root_grp]

    jaw_container = cmds.container(name='Jaw_Rig', type='dagContainer')
    for node in put_inside_container:
        cmds.container('Jaw_Rig', e=True, addNode=node)
    cmds.setAttr('Jaw_Rig.blackBox', 1)

def delete_jaw_rig():
    cmds.delete('Jaw_Rig')
