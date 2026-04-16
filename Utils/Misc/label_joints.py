from __future__ import absolute_import
from maya import cmds

"""   
-------------------------- LABEL JOINTS---------------------------
"""

def split_label_joints():
    """
    #Description :
        Label joints based on selection. 

    #Instructions:
        Select either the specific joints you wish to label or the group they are under and run script. If nothing is selected
        it will look for the "root" joint and label every joint in there; if the joint doesn't exist then it will error. 

    # Return: None
    """


    #Defining possible sufixes.
    joint_naming_ends = ["BND", "SKIN", "SKN", "JNT"]

    #Defining possible prefixes.
    L_joint_letter = ["L", "LF", "LB", "LC", "LEFT"]
    R_joint_letter = ["R", "RF", "RB", "RC", "RIGHT"]
    skirt_prefixes = ["SKIRT", "COAT", "CAPE", "DRESS", "JACKET", "FLAPS", "SWEATER"]


    ###DEFINING LIST SCENARIOS BASED ON SELECTION###
    bind_joint_sel = cmds.ls(sl=True)

    #Check if selection has only one element.
    if len(bind_joint_sel) == 1:
        
        ##If element is joint run as normal.
        if cmds.objectType(bind_joint_sel[0]) == "joint":
            bind_joint_sel = cmds.ls(sl=True, type="joint")
            print("List contains one joint.")

        #If element is transform take all children joints.
        elif cmds.objectType(bind_joint_sel[0]) == "transform":
            bind_joint_sel = cmds.listRelatives(bind_joint_sel[0], allDescendents=True, type="joint")
            print("List contains one transform node. Taking all children joints.")

    #Check if selection has more than one element. If yes, take only the joints.
    elif len(bind_joint_sel) > 1:
        bind_joint_sel = cmds.ls(sl=True, type="joint")

    #When nothing is selected look for the mutant "Bind_Joints_Grp" and apply it to all it's children.          
    else:
        bind_joint_sel = cmds.listRelatives("root", allDescendents=True, type="joint")

    #If the joint "root" does not exist then ask for a selection. 
    if not bind_joint_sel:
        cmds.error("No Mutant Bind_Joints_Grp found. Please select the joints you wish to add labels to.")


    #Setting the naming on the joints.
    for bind_joint in bind_joint_sel:
        
        #Dividing name in parts to analize it.
        bind_joint_names = bind_joint.split("_")
        
        #If name has multiple parts check for a side and remove it from the name. 
        if len(bind_joint_names)>1:
            part_index = 0 
            #Check each part of the name against the list of possible side codes. 
            for name_part in bind_joint_names:
                #If there is a match set the side attribute that side and remove the part from the name. 
                if name_part.upper() in L_joint_letter:
                    cmds.setAttr("{}.side".format(bind_joint), 1)
                    del bind_joint_names[part_index]
                elif name_part.upper() in R_joint_letter:
                    cmds.setAttr("{}.side".format(bind_joint), 2)
                    del bind_joint_names[part_index]
                else:
                    #If nothing matches add one to the count and continue to the next part of the name. 
                    part_index = part_index + 1
            
        #Otherwise assume it's a center joint. 
        else:
            cmds.setAttr("{}.side".format(bind_joint), 0)
        
        #Setting type to "Other" for costume name.
        cmds.setAttr("{}.type".format(bind_joint), 18)
        
        label_name = "_".join(bind_joint_names)
        
        #Setting the label name on the joint
        cmds.setAttr("{}.otherType".format(bind_joint), label_name, type="string")  

        
    cmds.warning("Joints have been labeled without error. Thank you.")


LEFT_TOKENS = {'L', 'LF', 'LB', 'LC', 'LEFT'}
RIGHT_TOKENS = {'R', 'RF', 'RB', 'RC', 'RIGHT'}

COSTUME_PREFIXES = {'SKIRT', 'COAT', 'CAPE', 'DRESS', 'JACKET', 'FLAPS', 'SWEATER'}

JOINT_END_TOKENS = {
    'BND', 'BIND', 'SKIN', 'SKN', 'JNT', 'JOINT', 'SKL',
    'GUIDE', 'JNTCTRL', 'CTRL', 'DRIVER', 'DRV'
}


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
    """
    Label every joint in scene using side/name smart parsing.

    Returns:
        tuple: (labeled_count, skipped_count)
    """

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

