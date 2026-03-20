from __future__ import absolute_import
from maya import cmds
import json
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

# ---------------------------------------------

TAB_FOLDER = '010_Other'
PYBLOCK_NAME = 'exec_label_joints'

# ---------------------------------------------

LEFT_TOKENS = {'L', 'LF', 'LB', 'LC', 'LEFT'}
RIGHT_TOKENS = {'R', 'RF', 'RB', 'RC', 'RIGHT'}

COSTUME_PREFIXES = {'SKIRT', 'COAT', 'CAPE', 'DRESS', 'JACKET', 'FLAPS', 'SWEATER'}

JOINT_END_TOKENS = {
    'BND', 'BIND', 'SKIN', 'SKN', 'JNT', 'JOINT', 'SKL',
    'GUIDE', 'JNTCTRL', 'CTRL', 'DRIVER', 'DRV'
}


def create_label_joints_block(name='LabelJoints'):
    # Read name conventions as nc[''] and setup as setup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '012_Label_Joints.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    # Name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(
        name=name,
        icon='Label',
        attrs=module['attrs'],
        build_command=module['build_command'],
        import_command=module['import']
    )
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))


# create_label_joints_block()


def _clean_name(node_name):
    short_name = node_name.split('|')[-1]
    short_name = short_name.split(':')[-1]
    return short_name


def _split_tokens(short_name):
    return [token for token in short_name.split('_') if token]


def _token_is_left(token):
    token_up = token.upper()
    return token_up in LEFT_TOKENS or token_up.startswith('LEFT')


def _token_is_right(token):
    token_up = token.upper()
    return token_up in RIGHT_TOKENS or token_up.startswith('RIGHT')


def _name_is_left(short_name):
    short_lower = short_name.lower()
    return (
        short_lower.startswith('left')
        or short_lower.endswith('_l')
        or short_lower.endswith('.l')
        or short_lower.endswith('-l')
    )


def _name_is_right(short_name):
    short_lower = short_name.lower()
    return (
        short_lower.startswith('right')
        or short_lower.endswith('_r')
        or short_lower.endswith('.r')
        or short_lower.endswith('-r')
    )


def _detect_side(tokens, short_name):
    if tokens:
        first_token = tokens[0]
        if _token_is_left(first_token):
            return 1
        if _token_is_right(first_token):
            return 2

        # Handle names like Skirt_L_A_Bnd where side can be the second token.
        if first_token.upper() in COSTUME_PREFIXES and len(tokens) > 1:
            second_token = tokens[1]
            if _token_is_left(second_token):
                return 1
            if _token_is_right(second_token):
                return 2

        last_token = tokens[-1]
        if _token_is_left(last_token):
            return 1
        if _token_is_right(last_token):
            return 2

    if _name_is_left(short_name):
        return 1
    if _name_is_right(short_name):
        return 2

    for token in tokens:
        if _token_is_left(token):
            return 1
        if _token_is_right(token):
            return 2

    return 0


def _remove_side_tokens(tokens, side):
    clean_tokens = list(tokens)

    if side == 1:
        while clean_tokens and _token_is_left(clean_tokens[0]):
            clean_tokens.pop(0)
        while clean_tokens and _token_is_left(clean_tokens[-1]):
            clean_tokens.pop()
    elif side == 2:
        while clean_tokens and _token_is_right(clean_tokens[0]):
            clean_tokens.pop(0)
        while clean_tokens and _token_is_right(clean_tokens[-1]):
            clean_tokens.pop()

    if len(clean_tokens) > 1 and clean_tokens[0].upper() in COSTUME_PREFIXES:
        if side == 1 and _token_is_left(clean_tokens[1]):
            clean_tokens.pop(1)
        elif side == 2 and _token_is_right(clean_tokens[1]):
            clean_tokens.pop(1)

    return clean_tokens


def _remove_joint_tail_tokens(tokens):
    clean_tokens = list(tokens)
    while clean_tokens and clean_tokens[-1].upper() in JOINT_END_TOKENS:
        clean_tokens.pop()
    return clean_tokens


def _strip_text_side_prefixes(label_name):
    # Supports compact names like LeftEye / RightEye where underscore splitting is not present.
    if label_name.lower().startswith('left'):
        return label_name[4:]
    if label_name.lower().startswith('right'):
        return label_name[5:]
    return label_name


def _build_label_name(short_name, side):
    tokens = _split_tokens(short_name)
    if not tokens:
        return short_name

    tokens = _remove_side_tokens(tokens, side)
    tokens = _remove_joint_tail_tokens(tokens)

    if tokens:
        return '_'.join(tokens)

    fallback = _strip_text_side_prefixes(short_name)
    if side == 1 and fallback.lower().endswith('_l'):
        fallback = fallback[:-2]
    elif side == 2 and fallback.lower().endswith('_r'):
        fallback = fallback[:-2]

    fallback = fallback.strip('_')
    return fallback if fallback else short_name


def _set_joint_label(joint_name, side, label_name):
    if cmds.attributeQuery('side', node=joint_name, exists=True):
        cmds.setAttr('{}.side'.format(joint_name), side)

    if cmds.attributeQuery('type', node=joint_name, exists=True):
        cmds.setAttr('{}.type'.format(joint_name), 18)

    if cmds.attributeQuery('otherType', node=joint_name, exists=True):
        cmds.setAttr('{}.otherType'.format(joint_name), label_name, type='string')


def label_all_scene_joints():
    all_joints = cmds.ls(type='joint', long=True) or []

    if not all_joints:
        cmds.warning('No joints found in scene.')
        return 0, 0

    labeled_count = 0
    skipped_count = 0

    for joint_name in all_joints:
        short_name = _clean_name(joint_name)
        tokens = _split_tokens(short_name)
        side = _detect_side(tokens, short_name)
        label_name = _build_label_name(short_name, side)

        try:
            _set_joint_label(joint_name, side, label_name)
            labeled_count += 1
        except Exception as error:
            skipped_count += 1
            print('Could not label {}: {}'.format(joint_name, error))

    return labeled_count, skipped_count


def build_label_joints_block():
    nc, curve_data, setup = mt.import_configs()
    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    if block:
        block = block[0]
    else:
        block = 'LabelJoints'

    labeled_count, skipped_count = label_all_scene_joints()

    if labeled_count:
        cmds.warning('Labeled {} joints. Skipped {} joints.'.format(labeled_count, skipped_count))

    print('Build {} Success'.format(block))


# build_label_joints_block()