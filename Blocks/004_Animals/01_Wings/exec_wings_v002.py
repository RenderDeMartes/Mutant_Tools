from __future__ import absolute_import
from maya import cmds, mel
import maya.api.OpenMaya as om
import json
import math
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '004_Animals'
PYBLOCK_NAME = 'exec_wings'

# config attr -> (wing part, next part guide). Guides are L_<Part>_Guide_Wing_00<i> with the
# feather L_<Part>_Guide_Fthr_00<i>_posStart > (posBend01 > posBend02 > ...) > posEnd under each one
PARTS = [('Scapular', 'Scapulars', 'Secondaries'),
         ('Secundary', 'Secondaries', 'Primaries'),
         ('Primary', 'Primaries', 'End')]
# per part, next to its amount: <Amount>FeatherJoints = joints in every feather FK chain (Fthr + Bend01...),
# <Amount>Preview = feather FK guides (posStart, one posBendNN per joint in between, posEnd)
FEATHER_JOINTS_SUFFIX = 'FeatherJoints'
PREVIEW_SUFFIX = 'Preview'
DEFAULT_FEATHER_JOINTS = 4
# shown in the builder Dynamic section, editing them runs on_attr_changed on the guides
DYNAMIC_ATTRS = [attr for p in PARTS for attr in (p[0], p[0] + FEATHER_JOINTS_SUFFIX, p[0] + PREVIEW_SUFFIX)]
STORED_BENDS_ATTR = 'StoredFeatherBends'

#---------------------------------------------

def create_wings_block(name = 'Wings'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    import Mutant_Tools
    from Mutant_Tools.Utils.External.RdMWings import autoWings, wingModule, BindFeathers, autoFold
    reload(autoWings)
    reload(wingModule)
    reload(BindFeathers)
    reload(autoFold)

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-3]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '01_Wings_v002.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    if cmds.objExists('L_Clav_Guide'):
        cmds.warning('Only one wings sysmtem can be build per Scene sorry.')
        return ''

    if cmds.objExists('L_Clav_Jnt'):
        cmds.warning('Only one wings sysmtem can be build per Scene sorry.')
        return ''

    scap_amount= int(mt.ask_name(ask_for='Scapular Amount', text = 5))
    sec_amount= int(mt.ask_name(ask_for='Secundary Amount', text = 8))
    prim_amount= int(mt.ask_name(ask_for='Primary Amount', text = 10))


    block = mt.create_block(name = name, icon = 'Wing',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    # the json makes the amount attrs (1-20), raise the max for bigger amounts
    for attr, amount in (('Scapular', scap_amount), ('Secundary', sec_amount), ('Primary', prim_amount)):
        amount = max(1, amount)
        if amount > cmds.attributeQuery(attr, n=config, maximum=True)[0]:
            cmds.addAttr('{}.{}'.format(config, attr), e=True, max=max(100, amount))
        cmds.setAttr('{}.{}'.format(config, attr), amount)

    autoWings.CreateJoints()
    autoWings.buildWingsRef(
        ScapAmount=scap_amount,
        ScaptBack=5,
        SecAmount=sec_amount,
        SecBack=5,
        PrimAmount=prim_amount,
        PrimBack=5)

    spec_root = mt.root_grp(input='L_Scapulars_Guide_Wing_000')
    sec_root = mt.root_grp(input='L_Secondaries_Guide_Wing_000')
    prim_root = mt.root_grp(input='L_Primaries_Guide_Wing_000')

    cmds.parentConstraint('L_Scapulars_Guide', spec_root, mo =True)
    cmds.parentConstraint('L_Secondaries_Guide', sec_root, mo=True)
    cmds.parentConstraint('L_Primaries_Guide', prim_root, mo=True)

    cmds.parent('L_Clav_Guide',spec_root, sec_root, prim_root, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_wings_block()

#-------------------------

def build_wings_block():

    import Mutant_Tools
    from Mutant_Tools.Utils.External.RdMWings import autoWings, wingModule, BindFeathers, autoFold
    reload(autoWings)
    reload(wingModule)
    reload(BindFeathers)
    reload(autoFold)

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    # the config network (the connection order changes, a hyperLayout can come first)
    config = [node for node in cmds.listConnections(block) if cmds.nodeType(node) == 'network'][0]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'],'')


    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    #create correct guide
    guide_roots = ['L_Clav_Guide', 'L_Primaries_Guide_Wing_000', 'L_Secondaries_Guide_Wing_000',
                   'L_Scapulars_Guide_Wing_000']
    for guide in guide_roots:
        new_guide = cmds.duplicate(guide, n=guide.replace('Guide', 'JR'), rr=True)[0]
        cmds.parent(new_guide, w=True)
        for jnt in cmds.listRelatives(new_guide, ad=True, f=True):
            if 'Guide' in jnt:
                cmds.select(jnt)
                mel.eval('searchReplaceNames {} {} "selected"'.format('Guide', 'JR'))

    # <Part>Preview guides: keep where the feather FK joints go, then back to a straight
    # posStart > posEnd feather so autoWings builds as always
    feather_curves = take_feather_curves()

    autoWings.buildWingsSystem(
        ScapAmount=int(cmds.getAttr('{}.Scapular'.format(config))),
        ScaptBack=1,
        SecAmount=int(cmds.getAttr('{}.Secundary'.format(config))),
        SecBack=1,
        PrimAmount=int(cmds.getAttr('{}.Primary'.format(config))),
        PrimBack=1,
        sizeUI=1)

    # before the mirror, the R wing copies them: joints per feather, then the curved feathers
    feather_joints = dict((part, _feather_joints(config, part)) for count_attr, part, next_part in PARTS)
    set_built_feather_joints(feather_joints)
    apply_feather_curves(feather_curves, feather_joints)
    # one ctrl at the elbow and one at the wrist drive both spread ctrls there and keep the parts together
    create_junction_spread_ctrls()
    lock_spread_ctrls()
    # SpreadMode Roll: spread ctrls tilt the feathers, they roll with the feather next to them so the overlap
    # does not clip. Classic: as before (blocks made before SpreadMode get Roll)
    spread_mode = 'Roll'
    if cmds.attributeQuery('SpreadMode', n=config, exists=True):
        spread_mode = cmds.getAttr('{}.SpreadMode'.format(config), asString=True)
    if spread_mode == 'Roll':
        create_spread_roll(feather_joints)

    cmds.rename('GlobalLoc', 'L_GlobalLoc')

    autoWings.getPivot(side='L', part='Primaries')
    autoWings.getPivot(side='L', part='Secondaries')
    autoWings.getPivot(side='L', part='Scapulars')

    cmds.rename('WingRef_Loc', 'L_WingRef_Loc')

    autoWings.mirrorWing()

    cmds.parent('L_Wing_AutoRig','Ctrl_Grp')
    cmds.parent('R_Wing_AutoRig_Mirror_GRP','Ctrl_Grp')

    #Quick fixes to make it cleaner for anim
    cmds.rename('L_Wing_CC', 'L_Wing_Ctrl')
    cmds.rename('R_Wing_CC', 'R_Wing_Ctrl')

    #clean the outliner
    cmds.parent('L_GlobalLoc', 'L_GlobalLoc','L_WingRef_Loc', 'R_WingRef_Loc','L_Wing_Nurbs_GRP', 'R_Wing_Nurbs_GRP', clean_rig_grp)
    for c in cmds.listRelatives('L_Wing_AutoRig', type='joint', ad=True):
        cmds.setAttr('{}.drawStyle'.format(c), 2)
    for c in cmds.listRelatives('R_Wing_AutoRig_Mirror_GRP', type='joint', ad=True):
        cmds.setAttr('{}.drawStyle'.format(c), 2)

    #Update curves to be 2 line
    curves = cmds.ls('*_Ctrl')
    for c in curves:
        cmds.setAttr(c+'.lineWidth', 2)

    #Create bind joints

    feathers = {

    'Clavicles' : ['L_Clav_JR','R_Clav_JR'],

    'Scapulars' : ['*_Scapulars_JR', '*_Scapulars_JR_Wing_*'],
    'Secundaries' : ['*_Secondaries_JR', '*_Secondaries_JR_Wing_*'],
    'Primaries' : ['*_Primaries_JR', '*_Primaries_JR_Wing_*'],

    'Scauplars_feathers' : ['*_Scapulars_JR_Fthr_*', '*_Scapulars_JR_Fthr_*Bend*'],
    'Secondaries_feathers' : ['*_Secondaries_JR_Fthr_*', '*_Secondaries_JR_Fthr_*Bend*'],
    'Primaries_feathers' : ['*_Primaries_JR_Fthr_*', '*_Primaries_JR_Fthr_*Bend*']
                }
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    #Remove the flip
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.rotateX', 0)
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.scaleX', 1)
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.scaleY', 1)
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.scaleZ', 1)

    for f in feathers:
        grp = cmds.group(em=True, n=f + '_Bnd' + '_Grp')
        cmds.parent(grp, bind_jnt_grp)
        joints = cmds.ls(feathers[f], type='joint')
        for jnt in joints:
            cmds.select(cl=True)
            if cmds.objExists(jnt + nc['joint_bind']):
                continue
            bind_joint = cmds.joint(n=jnt + nc['joint_bind'])
            mt.match(bind_joint, jnt, s=False)
            if 'Fthr' in jnt:
                ctrl = mt.curve(input=jnt,
                                type='pin_cube',
                                rename=True,
                                custom_name=True,
                                name=jnt + '_Indiv' + nc['ctrl'],
                                size=0.5)

                root_grp = mt.root_grp()[0]
                mt.match(root_grp, jnt, r=True, t=True)

                child = cmds.listRelatives(jnt, c=True)
                if child:
                    cmds.parent(child, ctrl)
                cmds.parent(root_grp, jnt)

                cmds.parentConstraint(ctrl, bind_joint, mo=True)
                #cmds.scaleConstraint(ctrl, bind_joint, mo=True)
            else:
                cmds.parentConstraint(jnt, bind_joint, mo=True)
                #cmds.scaleConstraint(jnt, bind_joint, mo=True)
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, grp)

        # Fix R Swing Wings
        primaries_grp = cmds.ls('R_Primaries_JR_Fthr_0*_Ctrl_Auto_Grp')
        secundaries_grp = cmds.ls('R_Secondaries_JR_Fthr_0*_Ctrl_Auto_Grp')
        scauplars_grp = cmds.ls('R_Scapulars_JR_Fthr_00*_Ctrl_Auto_Grp')

        for grp in primaries_grp:
            cmds.connectAttr('R_Wing_Ctrl.PrimariesSwing', grp + '.rotateZ', f=True)
        for grp in secundaries_grp:
            cmds.connectAttr('R_Wing_Ctrl.SecondariesSwing', grp + '.rotateZ', f=True)
        for grp in scauplars_grp:
            cmds.connectAttr('R_Wing_Ctrl.ScapularsSwing', grp + '.rotateZ', f=True)

        parent_feather_bends_chained()

    #Redo the flip
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.rotateX', 180)
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.scaleX', -1)
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.scaleY', -1)
    cmds.setAttr('R_Wing_AutoRig_Mirror_GRP.scaleZ', -1)

    # Block parent connections
    cmds.parentConstraint(block_parent, 'L_Clavicle_JC_Root', mo=True)
    cmds.parentConstraint(block_parent, 'R_Clavicle_JC_Root', mo=True)
    cmds.scaleConstraint(block_parent, 'L_Clavicle_JC_Root', mo=True)
    cmds.scaleConstraint(block_parent, 'R_Clavicle_JC_Root', mo=True)

    cmds.scaleConstraint(block_parent, bind_jnt_grp, mo=True)
    cmds.scaleConstraint(block_parent, 'L_Wing_CC_Auto', mo=True)
    cmds.scaleConstraint(block_parent, 'R_Wing_CC_Auto', mo=True)

    clean_cc_names()
    # Pivots on the first ctrl of every feather move its pivot and the automation groups above it
    create_feather_pivots()
    # the spread ctrls reach the far feather too (SpreadMin on the part Wing_000 ctrl)
    create_spread_min()

    print ('Build {} Success'.format(block))



#build_wings_block()


def parent_feather_bends_chained(
    sides=("L_", "R_"),
    parts=("Secondaries", "Scapulars", "Primaries"),
    max_feathers=50 #Sorry just been safe
):
    """
    Creates a chained hierarchy:
    Base
      > Bend01
          > Bend02
              > Bend03 (and on, FeatherJoints)
    """

    for side in sides:
        for part in parts:

            for num in range(max_feathers):
                # Matches: 000, 001, ... 009, 0010, 0011
                num_str = f"{num:03d}" if num < 10 else f"00{num}"

                base_joint = f"{side}{part}_JR_Fthr_{num_str}_Bnd"
                if not cmds.objExists(base_joint):
                    continue

                previous_parent = base_joint
                bend_index = 1

                while True:
                    bend_num = str(bend_index).zfill(2)
                    bend_joint = f"{side}{part}_JR_Fthr_{num_str}Bend{bend_num}_Bnd"

                    if not cmds.objExists(bend_joint):
                        break

                    current_parent = cmds.listRelatives(bend_joint, parent=True) or []
                    if current_parent != [previous_parent]:
                        cmds.parent(bend_joint, previous_parent)

                    previous_parent = bend_joint
                    bend_index += 1

    print("Feather bend chained parenting completed.")



def clean_cc_names():
    cc_names = cmds.ls('*_CC', type='transform', long=True)

    for cc in cc_names:
        new_name = cc.split('|')[-1].replace('_CC', '_Ctrl')
        cmds.rename(cc, new_name)


#-------------------------
# Builder hook (Utils/Rigging/block_hooks.py), per part (Scapular / Secundary / Primary): the amount
# adds or removes feather guides, <Part>Preview adds or removes the feather FK guides (posBendNN),
# <Part>FeatherJoints sets how many.

def on_attr_changed(config, attr, value):
    for count_attr, part, next_part in PARTS:
        if attr == count_attr:
            set_feather_count(config, part, next_part, int(round(value)))
        elif attr == count_attr + PREVIEW_SUFFIX:
            set_feather_preview(config, parts=[part])
        elif attr == count_attr + FEATHER_JOINTS_SUFFIX and _preview_on(config, part):
            # the bend guides follow the new amount, spread along the feather as it is now
            set_feather_preview(config, parts=[part])


def _num(index):
    # same names as wingModule: 000 ... 009, 0010, 0011
    return '00' + str(index)


def _wing_guide(part, index):
    return 'L_{}_Guide_Wing_{}'.format(part, _num(index))


def _feather_guide(part, index, end):
    return 'L_{}_Guide_Fthr_{}_{}'.format(part, _num(index), end)


def _bend_end(number):
    return 'posBend{:02d}'.format(number)


def _feather_count(part):
    count = 0
    while cmds.objExists(_wing_guide(part, count)):
        count += 1
    return count


def _part_attr(part, suffix):
    return [count_attr for count_attr, name, next_part in PARTS if name == part][0] + suffix


def _preview_on(config, part):
    attr = _part_attr(part, PREVIEW_SUFFIX)
    return cmds.attributeQuery(attr, n=config, exists=True) and bool(cmds.getAttr('{}.{}'.format(config, attr)))


def _feather_joints(config, part):
    attr = _part_attr(part, FEATHER_JOINTS_SUFFIX)
    if not cmds.attributeQuery(attr, n=config, exists=True):
        return DEFAULT_FEATHER_JOINTS
    return max(2, int(cmds.getAttr('{}.{}'.format(config, attr))))


def _wings_block(config):
    for node in cmds.listConnections(config, s=True, d=True) or []:
        if cmds.nodeType(node) == 'dagContainer':
            return node
    return None


CHANNELS = ('translate', 'rotate', 'jointOrient')


def _channels(node):
    return [value for channel in CHANNELS for value in cmds.getAttr('{}.{}'.format(node, channel))[0]]


def _set_channels(node, values):
    # local channels with setAttr (an xform -ws does not redo right)
    for num, channel in enumerate(CHANNELS):
        cmds.setAttr('{}.{}'.format(node, channel), *values[num * 3:num * 3 + 3])


def _world_position(node):
    return om.MVector(om.MTransformationMatrix(om.MMatrix(cmds.getAttr(node + '.worldMatrix[0]'))).translation(om.MSpace.kWorld))


def _resample(rows, count):
    """count rows spread over rows, first and last kept, the ones in between interpolated."""
    if not rows:
        return [[0.0] * 9 for _ in range(count)]
    if len(rows) == 1 or count == 1:
        return [list(rows[0]) for _ in range(count)]
    resampled = []
    for num in range(count):
        u = num * (len(rows) - 1) / float(count - 1)
        low = int(math.floor(u))
        high = min(low + 1, len(rows) - 1)
        blend = u - low
        resampled.append([a + (b - a) * blend for a, b in zip(rows[low], rows[high])])
    return resampled


def _resample_polyline(points, count):
    """count points evenly spread (by length) along the polyline, first and last kept."""
    points = [om.MVector(*p) for p in points]
    if count < 2 or len(points) < 2:
        return points[:count]
    lengths = [0.0]
    for low, high in zip(points[:-1], points[1:]):
        lengths.append(lengths[-1] + (high - low).length())
    total = lengths[-1]
    resampled = []
    segment = 0
    for num in range(count):
        target = total * num / float(count - 1)
        while segment < len(points) - 2 and lengths[segment + 1] < target:
            segment += 1
        span = lengths[segment + 1] - lengths[segment]
        blend = (target - lengths[segment]) / span if span > 1e-9 else 0.0
        resampled.append(points[segment] + (points[segment + 1] - points[segment]) * blend)
    return resampled


def _new_joint(name, parent, radius=None):
    joint = cmds.createNode('joint', n=name, p=parent, ss=True)
    if joint != name:
        cmds.warning('{} already exists, the new guide is {}'.format(name, joint))
    if radius:
        cmds.setAttr(joint + '.radius', radius)
    return joint


def _bend_chain(start, end):
    """Joints between start and end (posBendNN guides or JR copies), in order."""
    chain = []
    node = start
    while True:
        children = cmds.listRelatives(node, c=True, type='joint') or []
        if not children or end in children:
            return chain
        node = children[0]
        chain.append(node)


def _set_local_from_world(node, world, parent):
    local = om.MTransformationMatrix(world * om.MMatrix(cmds.getAttr(parent + '.worldInverseMatrix[0]')))
    cmds.setAttr(node + '.translate', *local.translation(om.MSpace.kTransform))
    cmds.setAttr(node + '.rotate', *[math.degrees(value) for value in local.rotation()])
    cmds.setAttr(node + '.jointOrient', 0, 0, 0)


def _set_bend_guides(part, num, points):
    """posBendNN guides of one feather on points (world), posEnd stays where it is. No points: posEnd
    goes back under posStart (straight feather)."""
    start = _feather_guide(part, num, 'posStart')
    end = _feather_guide(part, num, 'posEnd')
    end_world = om.MMatrix(cmds.getAttr(end + '.worldMatrix[0]'))
    old = _bend_chain(start, end)
    if old:
        cmds.parent(end, start, r=True)
        cmds.delete(old[0])
    parent = start
    for number, point in enumerate(points, 1):
        joint = _new_joint(_feather_guide(part, num, _bend_end(number)), parent, radius=0.5)
        local = om.MPoint(point) * om.MMatrix(cmds.getAttr(parent + '.worldInverseMatrix[0]'))
        cmds.setAttr(joint + '.translate', local.x, local.y, local.z)
        parent = joint
    if parent != start:
        cmds.parent(end, parent, r=True)
    _set_local_from_world(end, end_world, parent)


def set_feather_count(config, part, next_part, count):
    """Feather guides of one part (Scapulars, Secondaries, Primaries) to count. The first and last wing
    joints stay, the joints in between are spread again and the feathers (posStart, posEnd and the bends)
    are interpolated from the old ones, so the fan keeps its shape."""
    count = max(1, count)
    old_count = _feather_count(part)
    if not old_count:
        cmds.warning('No {} feather guides found ({})'.format(part, _wing_guide(part, 0)))
        return
    if count == old_count:
        return

    # every feather like the part toggle says, so all of them have the same guides
    set_feather_preview(config, parts=[part])
    bends = _feather_joints(config, part) - 2 if _preview_on(config, part) else 0
    ends = ['posStart'] + [_bend_end(number) for number in range(1, bends + 1)] + ['posEnd']

    feathers = [[_channels(_feather_guide(part, num, end)) for end in ends] for num in range(old_count)]
    wings = [_channels(_wing_guide(part, num)) for num in range(1, old_count)]
    if wings:
        step = sum(wing[0] for wing in wings) / float(count - 1) if count > 1 else 0
    else:
        step = cmds.getAttr('L_{}_Guide.translateX'.format(next_part)) / float(count)

    first = _wing_guide(part, 0)
    cmds.delete(cmds.listRelatives(first, c=True, type='joint', f=True) or [])

    new_wings = _resample(wings, count - 1)
    new_feathers = [_resample([feather[num] for feather in feathers], count) for num in range(len(ends))]
    wing = first
    for num in range(count):
        if num:
            wing = _new_joint(_wing_guide(part, num), wing)
            values = list(new_wings[num - 1])
            values[0] = step
            _set_channels(wing, values)
        parent = wing
        for end_num, end in enumerate(ends):
            parent = _new_joint(_feather_guide(part, num, end), parent, radius=0.5 if end.startswith('posBend') else None)
            _set_channels(parent, new_feathers[end_num][num])
    print('Wings: {} feathers {} -> {}'.format(part, old_count, count))


def _read_stored_bends(block):
    if not block or not cmds.attributeQuery(STORED_BENDS_ATTR, n=block, exists=True):
        return {}
    try:
        return json.loads(cmds.getAttr('{}.{}'.format(block, STORED_BENDS_ATTR)) or '{}')
    except (ValueError, TypeError):
        return {}


def _write_stored_bends(block, stored):
    if not block:
        return
    if not cmds.attributeQuery(STORED_BENDS_ATTR, n=block, exists=True):
        cmds.addAttr(block, ln=STORED_BENDS_ATTR, dt='string')
    cmds.setAttr('{}.{}'.format(block, STORED_BENDS_ATTR), json.dumps(stored), type='string')


def set_feather_preview(config, parts=None):
    """Feather guides of each part like its Preview / FeatherJoints attrs say. Preview on: FeatherJoints - 2
    posBendNN guides between posStart and posEnd of every feather, spread along it (or where they were
    when it was turned off). A feather with another amount of bends gets them spread again along its
    current curve. Preview off: posEnd back under posStart where it is."""
    block = _wings_block(config)
    stored = _read_stored_bends(block)
    store_changed = False
    for count_attr, part, next_part in PARTS:
        if parts and part not in parts:
            continue
        on = _preview_on(config, part)
        bends = _feather_joints(config, part) - 2
        for num in range(_feather_count(part)):
            start = _feather_guide(part, num, 'posStart')
            end = _feather_guide(part, num, 'posEnd')
            if not cmds.objExists(start) or not cmds.objExists(end):
                continue
            chain = _bend_chain(start, end)

            if on:
                if len(chain) == bends:
                    continue
                if chain:
                    # keep the curve: new bends on the current one
                    curve = [_world_position(node) for node in [start] + chain + [end]]
                    _set_bend_guides(part, num, _resample_polyline(curve, bends + 2)[1:-1])
                    continue
                entry = stored.get(end)
                _set_bend_guides(part, num, _resample_polyline([_world_position(start), _world_position(end)], bends + 2)[1:-1])
                if entry and len(entry['chain']) == bends + 1 and \
                        all(abs(a - b) < 1e-3 for a, b in zip(entry['end'], _channels_at_start(end, start))):
                    names = [_feather_guide(part, num, _bend_end(number)) for number in range(1, bends + 1)] + [end]
                    for node, values in zip(names, entry['chain']):
                        _set_channels(node, values)

            elif chain:
                names = chain + [end]
                saved = [_channels(node) for node in names]
                _set_bend_guides(part, num, [])
                stored[end] = {'end': _channels(end), 'chain': saved}
                store_changed = True
    if store_changed:
        _write_stored_bends(block, stored)


def _channels_at_start(end, start):
    """posEnd channels as if it was right under posStart (jointOrient 0), to compare with the stored ones."""
    local = om.MTransformationMatrix(om.MMatrix(cmds.getAttr(end + '.worldMatrix[0]')) * om.MMatrix(cmds.getAttr(start + '.worldInverseMatrix[0]')))
    return list(local.translation(om.MSpace.kTransform)) + [math.degrees(v) for v in local.rotation()] + [0.0, 0.0, 0.0]


#-------------------------
# Build: joints per feather and curved feathers from the <Part>Preview guides

def take_feather_curves():
    """World positions of posStart, the posBendNN and posEnd of every L feather with bends (JR copies of
    the guides). The bends are deleted after, the feather is posStart > posEnd again for autoWings."""
    curves = {}
    for count_attr, part, next_part in PARTS:
        num = 0
        while cmds.objExists('L_{}_JR_Wing_{}'.format(part, _num(num))):
            start = 'L_{}_JR_Fthr_{}_posStart'.format(part, _num(num))
            end = 'L_{}_JR_Fthr_{}_posEnd'.format(part, _num(num))
            chain = _bend_chain(start, end) if cmds.objExists(start) and cmds.objExists(end) else []
            if chain:
                curves[(part, num)] = [cmds.xform(node, q=True, ws=True, t=True) for node in [start] + chain + [end]]
                cmds.parent(end, start)
                cmds.delete(chain[0])
            num += 1
    return curves


def _built_feathers():
    """(part, number, prefix) of every L feather autoWings built."""
    feathers = []
    for count_attr, part, next_part in PARTS:
        num = 0
        while cmds.objExists('L_{}_JR_Fthr_{}'.format(part, _num(num))):
            feathers.append((part, num, 'L_{}_JR_Fthr_{}'.format(part, _num(num))))
            num += 1
    return feathers


def _feather_fk(prefix, joints):
    return ([prefix] + ['{}Bend{:02d}'.format(prefix, num) for num in range(1, joints)],
            [None] + ['{}_BendJnt{}'.format(prefix, num) for num in range(1, joints)])


def set_built_feather_joints(joints_by_part):
    """autoWings makes 4 joints per feather (Fthr, Bend01-03), this adds or removes bends to get the
    joints of each part (joints_by_part), spread evenly on the same length. New bends get the same drivers as Bend03 (bend ctrl on the
    BendJnt group rotate, feather ctrl BendX/Y/Z on the joint rotate)."""
    built = 3
    for part, num, prefix in _built_feathers():
        joints = joints_by_part.get(part, DEFAULT_FEATHER_JOINTS)
        bends = joints - 1
        if bends == built:
            continue
        old_joints, old_groups = _feather_fk(prefix, built + 1)
        if not all(cmds.objExists(node) for node in old_joints + old_groups[1:]):
            cmds.warning('{} feather joints not found, it keeps {} joints'.format(prefix, built + 1))
            continue
        offsets = [om.MVector(*cmds.getAttr(group + '.translate')[0]) for group in old_groups[1:]]
        length = sum(offset.length() for offset in offsets)
        direction = offsets[0].normal() if offsets[0].length() > 1e-9 else om.MVector(0, 0, -1)

        if bends < built:
            cmds.delete(old_groups[bends + 1])
        else:
            for bend in range(built + 1, bends + 1):
                group = cmds.createNode('transform', n='{}_BendJnt{}'.format(prefix, bend), p='{}Bend{:02d}'.format(prefix, bend - 1), ss=True)
                joint = cmds.createNode('joint', n='{}Bend{:02d}'.format(prefix, bend), p=group, ss=True)
                cmds.setAttr(joint + '.radius', 0.5)
                for source, target in ((old_groups[-1], group), (old_joints[-1], joint)):
                    for channel in ('rx', 'ry', 'rz'):
                        driver = cmds.listConnections('{}.{}'.format(source, channel), s=True, d=False, p=True) or []
                        if driver:
                            cmds.connectAttr(driver[0], '{}.{}'.format(target, channel), f=True)
        new_joints, new_groups = _feather_fk(prefix, joints)
        for group in new_groups[1:]:
            cmds.setAttr(group + '.translate', *(direction * (length / bends)))


def _aim_down_z(joint, target):
    """jointOrient so the joint -Z (the way the feather goes) points to target. rotate stays 0, it is
    driven by the feather ctrl bends."""
    world = om.MMatrix(cmds.getAttr(joint + '.worldMatrix[0]'))
    transform = om.MTransformationMatrix(world)
    want = om.MVector(*target) - om.MVector(transform.translation(om.MSpace.kWorld))
    current = -om.MVector(world[8], world[9], world[10])
    if want.length() < 1e-6 or current.length() < 1e-6:
        return
    rotation = transform.rotation(asQuaternion=True) * om.MQuaternion(current.normal(), want.normal())
    parent = om.MMatrix(cmds.getAttr(joint + '.parentMatrix[0]'))
    local = om.MTransformationMatrix(rotation.asMatrix() * parent.inverse()).rotation()
    cmds.setAttr(joint + '.jointOrient', math.degrees(local.x), math.degrees(local.y), math.degrees(local.z))


def apply_feather_curves(curves, joints_by_part):
    """Feather FK joints (Fthr, BendNN in their BendJnt groups) on the <Part>Preview guides, each
    joint aimed to the next one. Guides with another amount of bends are spread along their curve."""
    for (part, num), points in curves.items():
        prefix = 'L_{}_JR_Fthr_{}'.format(part, _num(num))
        joints = joints_by_part.get(part, DEFAULT_FEATHER_JOINTS)
        fk_joints, groups = _feather_fk(prefix, joints)
        if not all(cmds.objExists(node) for node in fk_joints + groups[1:]):
            cmds.warning('{} feather joints not found, it stays straight'.format(prefix))
            continue
        if len(points) != joints:
            points = _resample_polyline(points, joints)
        points = [om.MVector(*p) for p in points]
        for index in range(joints - 1):
            _aim_down_z(fk_joints[index], points[index + 1])
            # BendJnt rotations are driven, the translate places the next joint
            local = om.MPoint(points[index + 1]) * om.MMatrix(cmds.getAttr(groups[index + 1] + '.parentInverseMatrix[0]'))
            cmds.setAttr(groups[index + 1] + '.translate', local.x, local.y, local.z)


#-------------------------
# Build: elbow / wrist spread ctrls. Where two parts meet, the Spread_Out ctrl of one and the Spread_In ctrl
# of the next sit together. A new ctrl drives both (through their Auto groups, the old ctrls keep their names
# and anim and become sub ctrls), and AutoClose turns the edge feathers half the elbow / wrist bend each so
# the two parts do not open a gap.

# (ctrl name, part before, part after)
JUNCTIONS = [('L_Elbow_Spread', 'Scapulars', 'Secondaries'),
             ('L_Wrist_Spread', 'Secondaries', 'Primaries')]


def _last_built_wing(part):
    num = 0
    while cmds.objExists('L_{}_JR_Wing_{}'.format(part, _num(num + 1))):
        num += 1
    return 'L_{}_JR_Wing_{}'.format(part, _num(num))


def create_junction_spread_ctrls():
    nc = mt.import_configs()[0]
    for name, before, after in JUNCTIONS:
        out_ctrl = 'L_{}_JR_Spread_Out{}'.format(before, nc['ctrl'])
        in_ctrl = 'L_{}_JR_Spread_In{}'.format(after, nc['ctrl'])
        out_auto = 'L_{}_JR_Spread_Out_Auto{}'.format(before, nc['group'])
        in_auto = 'L_{}_JR_Spread_In_Auto{}'.format(after, nc['group'])
        before_wing = _last_built_wing(before)
        after_wing = 'L_{}_JR_Wing_{}'.format(after, _num(0))
        after_cube = after_wing + nc['ctrl']
        if not all(cmds.objExists(node) for node in (out_ctrl, in_ctrl, out_auto, in_auto, before_wing, after_wing, after_cube)):
            cmds.warning('{}: spread ctrls not found, skipped'.format(name))
            continue

        # bend between the parts: an after-part locator seen from a before-part one, both start with the
        # orientation of the after-part cube ctrl (Y is the wing up), so the rest is 0
        locators = []
        for side_name, parent in (('Before', before_wing), ('After', after_wing)):
            loc = cmds.spaceLocator(n='{}_{}_Loc'.format(name, side_name))[0]
            cmds.delete(cmds.parentConstraint(after_cube, loc, mo=False))
            cmds.parent(loc, parent)
            cmds.setAttr(loc + '.visibility', 0)
            locators.append(loc)
        relative = cmds.createNode('multMatrix', n=name + '_Bend_MM')
        cmds.connectAttr(locators[1] + '.worldMatrix[0]', relative + '.matrixIn[0]')
        cmds.connectAttr(locators[0] + '.worldInverseMatrix[0]', relative + '.matrixIn[1]')
        bend = cmds.createNode('decomposeMatrix', n=name + '_Bend_DM')
        # yzx: Y is not the middle axis, so the bend reads past 90 degrees without flipping back
        cmds.setAttr(bend + '.inputRotateOrder', 1)
        cmds.connectAttr(relative + '.matrixSum', bend + '.inputMatrix')

        # the ctrl between both spread ctrls, following both parts half and half
        cmds.select(cl=True)
        ctrl = mt.curve(input='', type='sphere', custom_name=True, name=name + nc['ctrl'], size=1, tag=False, playback=False)
        mt.assign_color(ctrl, 'yellow')
        root = cmds.group(ctrl, n=name + '_Root' + nc['group'])
        cmds.delete(cmds.parentConstraint(out_ctrl, in_ctrl, root, mo=False))
        cmds.delete(cmds.orientConstraint(after_cube, root, mo=False))
        cmds.parent(root, 'L_Wing_AutoRig')
        constraint = cmds.parentConstraint(locators[0], locators[1], root, mo=True)[0]
        cmds.setAttr(constraint + '.interpType', 2)
        for attr in ('tx', 'ty', 'tz', 'rz', 'sx', 'sy', 'sz', 'v'):
            cmds.setAttr('{}.{}'.format(ctrl, attr), lock=True, keyable=False, channelBox=False)

        cmds.addAttr(ctrl, ln='AutoClose', at='double', min=0, max=1, dv=1, k=True)
        cmds.addAttr(ctrl, ln='SubCtrls', at='enum', en='Hide:Show', dv=0, k=True)
        for sub in (out_ctrl, in_ctrl):
            cmds.connectAttr(ctrl + '.SubCtrls', sub.replace(nc['ctrl'], '_Root' + nc['group']) + '.visibility', f=True)

        # half the bend each way, times AutoClose (two nodes, one feeding itself reads as a cycle)
        close = cmds.createNode('multiplyDivide', n=name + '_CloseBend_MD')
        cmds.connectAttr(bend + '.outputRotateY', close + '.input1X')
        cmds.connectAttr(ctrl + '.AutoClose', close + '.input2X')
        # multiplyDivide / plusMinusAverage, not multDoubleLinear / addDoubleLinear: Maya 2026 turns those into multDL / addDL, which Maya 2024 can not open
        half = cmds.createNode('multiplyDivide', n=name + '_HalfBend_MDL')
        cmds.connectAttr(close + '.outputX', half + '.input1X')
        cmds.setAttr(half + '.input2X', 0.5)
        for auto, sign in ((out_auto, 1), (in_auto, -1)):
            sum_node = cmds.createNode('plusMinusAverage', n='{}_{}_PMA'.format(name, 'Out' if sign > 0 else 'In'))
            cmds.setAttr(sum_node + '.operation', 1 if sign > 0 else 2)
            cmds.connectAttr(ctrl + '.ry', sum_node + '.input1D[0]')
            cmds.connectAttr(half + '.outputX', sum_node + '.input1D[1]')
            cmds.connectAttr(sum_node + '.output1D', auto + '.ry', f=True)
            cmds.connectAttr(ctrl + '.rx', auto + '.rx', f=True)


# wingModule hides t / s on the spread Root group (the selection there), not on the ctrl, so the spread
# In / Out ctrls of every part are locked here, rotate only
def lock_spread_ctrls():
    nc = mt.import_configs()[0]
    for count_attr, part, next_part in PARTS:
        for mode in ('In', 'Out'):
            ctrl = 'L_{}_JR_Spread_{}{}'.format(part, mode, nc['ctrl'])
            if not cmds.objExists(ctrl):
                continue
            for attr in ('tx', 'ty', 'tz', 'sx', 'sy', 'sz'):
                cmds.setAttr('{}.{}'.format(ctrl, attr), lock=True, keyable=False, channelBox=False)


#-------------------------
# Build: spread roll. The spread In / Out ctrls tilt every feather a share of their rx, so the feathers step
# down flat next to each other and their overlap cuts through. Every feather gets a SpreadRoll group under its
# RootJnt, aimed at its own tip with X to the tip of the next feather (the last one: away from the one before),
# so it rolls with the feather sheet. All of it in the RootJnt space (aimMatrix), so the mirrored R wing works
# the same. <Part>_JR_Wing_000_Ctrl.SheetFollow blends it (aimMatrix envelope).
# Bend_Ctrl twist turns SpreadCtrlGrp (above the RootJnt), the roll would undo it, so a Twist group under the
# roll turns it back on the feather.

SHEET_FOLLOW_ATTR = 'SheetFollow'


def _rest_matrix(origin, tip, side, flip):
    """origin > tip is Z, X towards side (flip: away from it), as a list for setAttr."""
    z = (tip - origin).normal()
    x = (side - tip) * (-1 if flip else 1)
    y = (z ^ x).normal()
    x = (y ^ z).normal()
    return [x.x, x.y, x.z, 0, y.x, y.y, y.z, 0, z.x, z.y, z.z, 0, origin.x, origin.y, origin.z, 1]


def create_spread_roll(joints_by_part, side='L'):
    nc = mt.import_configs()[0]
    for count_attr, part, next_part in PARTS:
        prefixes = []
        while cmds.objExists('{}_{}_JR_Fthr_{}'.format(side, part, _num(len(prefixes)))):
            prefixes.append('{}_{}_JR_Fthr_{}'.format(side, part, _num(len(prefixes))))
        cube = '{}_{}_JR_Wing_{}{}'.format(side, part, _num(0), nc['ctrl'])
        if len(prefixes) < 2 or not cmds.objExists(cube):
            cmds.warning('{} {}: feathers not found, no spread roll'.format(side, part))
            continue
        joints = joints_by_part.get(part, DEFAULT_FEATHER_JOINTS)
        if not cmds.attributeQuery(SHEET_FOLLOW_ATTR, n=cube, exists=True):
            cmds.addAttr(cube, ln=SHEET_FOLLOW_ATTR, at='double', min=0, max=1, dv=1, k=True)

        # twist back: -Bend_Ctrl.rz times SheetFollow, one for the part
        twist = cmds.listConnections(prefixes[0] + '_SpreadCtrlGrp.rotateZ', s=True, d=False, p=True) or []
        untwist = None
        if twist:
            follow = cmds.createNode('multiplyDivide', n='{}_{}_JR_SpreadRoll_Twist_MDL'.format(side, part))
            cmds.connectAttr(twist[0], follow + '.input1X')
            cmds.connectAttr('{}.{}'.format(cube, SHEET_FOLLOW_ATTR), follow + '.input2X')
            untwist = cmds.createNode('multiplyDivide', n='{}_{}_JR_SpreadRoll_Untwist_MDL'.format(side, part))
            cmds.connectAttr(follow + '.outputX', untwist + '.input1X')
            cmds.setAttr(untwist + '.input2X', -1)

        tips = []
        for prefix in prefixes:
            tip = cmds.createNode('transform', n=prefix + '_SheetTip', p=prefix + '_RootJnt')
            cmds.xform(tip, ws=True, t=cmds.xform(_feather_fk(prefix, joints)[0][-1], q=True, ws=True, t=True))
            tips.append(tip)

        for index, prefix in enumerate(prefixes):
            root = prefix + '_RootJnt'
            last = index == len(prefixes) - 1
            side_tip = tips[index - 1] if last else tips[index + 1]
            children = [c for c in cmds.listRelatives(root, c=True, type='transform') if c != tips[index]]

            # rest frame in the RootJnt space
            root_inverse = om.MMatrix(cmds.getAttr(root + '.worldInverseMatrix[0]'))
            local = lambda node: om.MVector(om.MPoint(cmds.xform(node, q=True, ws=True, t=True)) * root_inverse)
            rest = _rest_matrix(local(prefix), local(tips[index]), local(side_tip), last)

            side_local = cmds.createNode('multMatrix', n=prefix + '_SpreadRoll_MM')
            cmds.connectAttr(side_tip + '.worldMatrix[0]', side_local + '.matrixIn[0]')
            cmds.connectAttr(root + '.worldInverseMatrix[0]', side_local + '.matrixIn[1]')
            aim = cmds.createNode('aimMatrix', n=prefix + '_SpreadRoll_AM')
            cmds.setAttr(aim + '.inputMatrix', rest, type='matrix')
            cmds.setAttr(aim + '.primaryInputAxis', 0, 0, 1)
            cmds.setAttr(aim + '.primaryMode', 1)
            cmds.connectAttr(tips[index] + '.matrix', aim + '.primaryTargetMatrix')
            cmds.setAttr(aim + '.secondaryInputAxis', -1 if last else 1, 0, 0)
            cmds.setAttr(aim + '.secondaryMode', 1)
            cmds.connectAttr(side_local + '.matrixSum', aim + '.secondaryTargetMatrix')
            cmds.connectAttr('{}.{}'.format(cube, SHEET_FOLLOW_ATTR), aim + '.envelope')

            roll = cmds.createNode('transform', n=prefix + '_SpreadRoll_Grp', p=root)
            cmds.connectAttr(aim + '.outputMatrix', roll + '.offsetParentMatrix')
            twist_grp = cmds.createNode('transform', n=prefix + '_SpreadRoll_Twist_Grp', p=roll)
            if untwist:
                cmds.connectAttr(untwist + '.outputX', twist_grp + '.rotateZ')
            if children:
                cmds.parent(children, twist_grp)


#-------------------------
# Build: feather pivots. The first ctrl of every feather (<Side>_<Part>_JR_<i>_Ctrl, parent of the Fthr AutoJnt)
# gets Pivots > PivotX / PivotY / PivotZ, an offset in the ctrl space for the rotate / scale pivot of the ctrl
# and of every group above it (AutoFold, SpreadRoll, RootJnt, SpreadCtrlGrp, SpreadAuto...) up to the
# constrained Wing joint, so the automations turn the feather around it.
# - groups turned from the ctrl (SpreadRoll aim, mirrored R wing) get the offset through a vectorProduct
# - groups rotated at rest (AutoFold under the roll) get rotatePivotTranslate = pivot * (rest rotate - 1),
#   the feather does not pop and they still turn around the pivot
# - SpreadRoll_Grp turns from its offsetParentMatrix (no pivot there): rest * T(-pivot) * rest^-1 * aim * T(pivot)
#   turns the roll around the pivot too

PIVOTS_SEPARATOR = '__________'  # the Bends separator on the same ctrl has 9
PIVOT_ATTRS = ('PivotX', 'PivotY', 'PivotZ')


def _feather_pivot_nodes(ctrl):
    nodes = [ctrl]
    parent = (cmds.listRelatives(ctrl, p=True) or [None])[0]
    while parent and not cmds.listRelatives(parent, type='constraint'):
        nodes.append(parent)
        parent = (cmds.listRelatives(parent, p=True) or [None])[0]
    return nodes


def _linear(matrix):
    """3x3 of a matrix as a list for setAttr, no translate."""
    return list(matrix)[:12] + [0, 0, 0, 1]


def _pivot_vector(ctrl, matrix, name):
    """ctrl PivotX / Y / Z times the 3x3 of matrix, as 3 plugs (the ctrl plugs if it is the identity)."""
    if matrix.isEquivalent(om.MMatrix(), 1e-4):
        return ['{}.{}'.format(ctrl, attr) for attr in PIVOT_ATTRS]
    product = cmds.createNode('vectorProduct', n=name)
    cmds.setAttr(product + '.operation', 3)
    cmds.setAttr(product + '.matrix', _linear(matrix), type='matrix')
    for attr, axis in zip(PIVOT_ATTRS, 'XYZ'):
        cmds.connectAttr('{}.{}'.format(ctrl, attr), '{}.input1{}'.format(product, axis))
    return ['{}.output{}'.format(product, axis) for axis in 'XYZ']


def _pivot_roll(ctrl, ctrl_world, node, aim):
    parent = cmds.listRelatives(node, p=True)[0]
    to_parent = ctrl_world * om.MMatrix(cmds.getAttr(parent + '.worldInverseMatrix[0]'))
    # T(pivot) and T(-pivot), inverseMatrix needs the matrixNodes plugin
    to_pivot = cmds.createNode('composeMatrix', n=node + '_Pivot_CM')
    for plug, axis in zip(_pivot_vector(ctrl, to_parent, node + '_Pivot_Parent_VP'), 'XYZ'):
        cmds.connectAttr(plug, '{}.inputTranslate{}'.format(to_pivot, axis))
    from_pivot = cmds.createNode('composeMatrix', n=node + '_Pivot_Back_CM')
    for plug, axis in zip(_pivot_vector(ctrl, to_parent * -1.0, node + '_Pivot_Back_VP'), 'XYZ'):
        cmds.connectAttr(plug, '{}.inputTranslate{}'.format(from_pivot, axis))

    rest = om.MMatrix(cmds.getAttr(aim + '.outputMatrix'))
    around = cmds.createNode('multMatrix', n=node + '_Pivot_MM')
    cmds.setAttr(around + '.matrixIn[0]', list(rest), type='matrix')
    cmds.connectAttr(from_pivot + '.outputMatrix', around + '.matrixIn[1]')
    cmds.setAttr(around + '.matrixIn[2]', list(rest.inverse()), type='matrix')
    cmds.connectAttr(aim + '.outputMatrix', around + '.matrixIn[3]')
    cmds.connectAttr(to_pivot + '.outputMatrix', around + '.matrixIn[4]')
    cmds.connectAttr(around + '.matrixSum', node + '.offsetParentMatrix', f=True)


def create_feather_pivots():
    for auto in sorted(cmds.ls('L_*_JR_Fthr_*_AutoJnt', 'R_*_JR_Fthr_*_AutoJnt', type='transform')):
        ctrl = cmds.listRelatives(auto, p=True)[0]
        if not cmds.attributeQuery(PIVOTS_SEPARATOR, n=ctrl, exists=True):
            cmds.addAttr(ctrl, ln=PIVOTS_SEPARATOR, nn=PIVOTS_SEPARATOR, at='enum', en='Pivots')
            cmds.setAttr('{}.{}'.format(ctrl, PIVOTS_SEPARATOR), e=True, channelBox=True)
            cmds.setAttr('{}.{}'.format(ctrl, PIVOTS_SEPARATOR), lock=True)
        for attr in PIVOT_ATTRS:
            if not cmds.attributeQuery(attr, n=ctrl, exists=True):
                cmds.addAttr(ctrl, ln=attr, at='double', dv=0, k=True)

        ctrl_world = om.MMatrix(cmds.getAttr(ctrl + '.worldMatrix[0]'))
        for node in _feather_pivot_nodes(ctrl):
            pivot = _pivot_vector(ctrl, ctrl_world * om.MMatrix(cmds.getAttr(node + '.worldInverseMatrix[0]')),
                                  node + '_Pivot_VP')
            for plug, axis in zip(pivot, 'XYZ'):
                cmds.connectAttr(plug, '{}.rotatePivot{}'.format(node, axis), f=True)
                cmds.connectAttr(plug, '{}.scalePivot{}'.format(node, axis), f=True)

            rest_turn = om.MMatrix(_linear(om.MMatrix(cmds.getAttr(node + '.matrix'))))
            if not rest_turn.isEquivalent(om.MMatrix(), 1e-4):
                minus_one = om.MMatrix(_linear(rest_turn))
                for i in range(3):
                    minus_one.setElement(i, i, minus_one.getElement(i, i) - 1)
                compensate = cmds.createNode('vectorProduct', n=node + '_Pivot_Rest_VP')
                cmds.setAttr(compensate + '.operation', 3)
                cmds.setAttr(compensate + '.matrix', _linear(minus_one), type='matrix')
                for plug, axis in zip(pivot, 'XYZ'):
                    cmds.connectAttr(plug, '{}.input1{}'.format(compensate, axis))
                    cmds.connectAttr('{}.output{}'.format(compensate, axis),
                                     '{}.rotatePivotTranslate{}'.format(node, axis), f=True)

            aim = cmds.listConnections(node + '.offsetParentMatrix', s=True, d=False, type='aimMatrix')
            if aim:
                _pivot_roll(ctrl, ctrl_world, node, aim[0])


#-------------------------
# Build: spread min. wingModule spreads every part from 1 on one end to 0 on the other (Spread_In: first
# feather 1, last 0. Spread_Out: first 0, last 1), so the far feather does not move. Every feather share w
# becomes w + SpreadMin * (1 - w), SpreadMin (0-1) on the part Wing_000 ctrl. The R wing has the mirrored
# multiplyDivides (L_..._MD1), so they are found from the feather they drive, not by name.

SPREAD_MIN_ATTR = 'SpreadMin'
SPREAD_MIN_DEFAULT = 0.2


def create_spread_min():
    nc = mt.import_configs()[0]
    shares = {}
    for md in cmds.ls('*_JR_Fthr_*_MD*', type='multiplyDivide'):
        if '_In_' in md or '_InAuto_' in md:
            mode = 'In'
        elif '_Out_' in md or '_OutAuto_' in md:
            mode = 'Out'
        else:
            continue
        if cmds.listConnections(md + '.input2X', s=True, d=False):
            continue
        driven = cmds.listConnections(md + '.outputX', s=False, d=True, skipConversionNodes=True) or []
        # L / R wings only, other blocks (TailWing) have feathers too
        driven = [node for node in driven if '_JR_Fthr_' in node and node[:2] in ('L_', 'R_')]
        if not driven:
            continue
        part, number = driven[0].split('_JR_Fthr_')
        feather = '{}_JR_Fthr_{}'.format(part, number.split('_')[0])
        cube = '{}_JR_Wing_{}{}'.format(part, _num(0), nc['ctrl'])
        if not cmds.objExists(cube):
            continue
        if not cmds.attributeQuery(SPREAD_MIN_ATTR, n=cube, exists=True):
            cmds.addAttr(cube, ln=SPREAD_MIN_ATTR, at='double', min=0, max=1, dv=SPREAD_MIN_DEFAULT, k=True)

        key = (feather, mode)
        if key not in shares:
            weight = cmds.getAttr(md + '.input2X')
            reach = cmds.createNode('multiplyDivide', n='{}_Spread{}Min_MDL'.format(feather, mode))
            cmds.connectAttr('{}.{}'.format(cube, SPREAD_MIN_ATTR), reach + '.input1X')
            cmds.setAttr(reach + '.input2X', 1 - weight)
            share = cmds.createNode('plusMinusAverage', n='{}_Spread{}Min_ADL'.format(feather, mode))
            cmds.connectAttr(reach + '.outputX', share + '.input1D[0]')
            cmds.setAttr(share + '.input1D[1]', weight)
            shares[key] = share + '.output1D'
        cmds.connectAttr(shares[key], md + '.input2X', f=True)
