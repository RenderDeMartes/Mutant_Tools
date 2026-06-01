from __future__ import absolute_import
# coding: utf-8
'''
MutantKanban - Scene Utilities
Handles all Maya scene data storage and retrieval for the Kanban board.

Data hierarchy in Maya:
  MutantKanban (transform group)
    MK_Backlog  (transform group)
      MK_Note1  (transform node with card attrs)
    MK_Todo
      ...
    MK_InProgress
    MK_ForReview
    MK_Done

www.mutanttools.com
author: Esteban Rodriguez <info@renderdemartes.com>
'''

from maya import cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

import os
import glob
import time
import base64
import getpass
import json
import tempfile

# -------------------------------------------------------
# Temp folder for decoded images

temp_folder = os.path.join(tempfile.gettempdir(), 'MutantKanban')
if not os.path.exists(temp_folder):
    try:
        os.makedirs(temp_folder)
    except Exception:
        pass

# -------------------------------------------------------
# Constants

KANBAN_ROOT = 'MutantKanban'

DEFAULT_COLUMNS = ['To Do', 'Done', 'Nice to Have']

DEFAULT_COLUMN_PRESETS = {
    'Default': ['Backlog', 'To Do', 'In Progress', 'For Review', 'Done'],
    'Simple': ['To Do', 'In Progress', 'Done'],
    'Dev': ['Backlog', 'Todo', 'InProgress', 'Review', 'Testing', 'Done'],
    'Art': ['Concept', 'InProgress', 'Feedback', 'Approved', 'Done'],
    'Pipeline': ['Brief', 'Todo', 'InProgress', 'QA', 'Delivered'],
}

PRIORITY_COLORS = {
    0: '#6c757d',   # Low    - grey
    1: '#4a90e2',   # Medium - blue
    2: '#f0a500',   # High   - orange
    3: '#e74c3c',   # Urgent - red
}

PRIORITY_LABELS = ['Low', 'Medium', 'High', 'Urgent']


# -------------------------------------------------------
# Helpers

def node_name_for_column(column_name):
    """Return the Maya group node name for a given column label."""
    clean = column_name.replace(' ', '_').replace('-', '_')
    return 'MK_{}'.format(clean)


# -------------------------------------------------------
# Root / Column group management

def get_or_create_kanban_root():
    """Get or create the root MutantKanban transform group."""
    if not cmds.objExists(KANBAN_ROOT):
        cmds.select(cl=True)
        root = cmds.group(empty=True, name=KANBAN_ROOT)
        cmds.addAttr(root, ln='columns', dt='string', w=True)
        cmds.setAttr('{}.columns'.format(root),
                     json.dumps(DEFAULT_COLUMNS), type='string')
        cmds.addAttr(root, ln='kanban_version', dt='string', w=True)
        cmds.setAttr('{}.kanban_version'.format(root), '1.0', type='string')
        print('MutantKanban: Created root node.')
    return KANBAN_ROOT


def get_columns():
    """Return ordered list of column names from the scene."""
    root = get_or_create_kanban_root()
    if not cmds.attributeQuery('columns', node=root, exists=True):
        return DEFAULT_COLUMNS[:]
    try:
        raw = cmds.getAttr('{}.columns'.format(root))
        return json.loads(raw)
    except Exception:
        return DEFAULT_COLUMNS[:]


def set_columns(column_names):
    """Persist the column order/list to the scene."""
    root = get_or_create_kanban_root()
    if not cmds.attributeQuery('columns', node=root, exists=True):
        cmds.addAttr(root, ln='columns', dt='string', w=True)
    try:
        cmds.setAttr('{}.columns'.format(root),
                     json.dumps(column_names), type='string')
    except Exception as e:
        cmds.warning('MutantKanban: Could not save columns: {}'.format(e))


def get_or_create_column_group(column_name):
    """Return (creating if necessary) the Maya group for a column."""
    root = get_or_create_kanban_root()
    node = node_name_for_column(column_name)
    if not cmds.objExists(node):
        cmds.select(cl=True)
        grp = cmds.group(empty=True, name=node)
        if cmds.objExists(root):
            cmds.parent(grp, root)
        cmds.addAttr(grp, ln='column_label', dt='string', w=True)
        cmds.setAttr('{}.column_label'.format(grp), column_name, type='string')
        print('MutantKanban: Created column group {}.'.format(node))
    return node


def get_notes_in_column(column_name):
    """Return note node names inside a column group, sorted by card_order."""
    col_node = node_name_for_column(column_name)
    if not cmds.objExists(col_node):
        return []
    children = cmds.listRelatives(col_node, children=True, type='transform') or []

    def _order(n):
        if cmds.attributeQuery('card_order', node=n, exists=True):
            try:
                return cmds.getAttr('{}.card_order'.format(n))
            except Exception:
                return 0
        return 0

    children.sort(key=_order)
    return children


# -------------------------------------------------------
# Image utilities

def encode_image(image_path):
    """Read a file and return its base64-encoded ASCII string."""
    with open(image_path, 'rb') as fh:
        return base64.b64encode(fh.read()).decode('ascii')


def decode_image(encoded_image, image_name='temp.jpg'):
    """
    Write a base64-encoded image to the temp folder and return the path.
    Returns None on failure.
    """
    if not encoded_image:
        return None
    try:
        new_image = os.path.join(temp_folder, image_name)
        # Normalise: strip b'...' wrapper that older Python repr may add
        clean = str(encoded_image)
        if clean.startswith("b'") and clean.endswith("'"):
            clean = clean[2:-1]
        # Pad to multiple of 4 so b64decode doesn't complain
        pad = len(clean) % 4
        if pad:
            clean += '=' * (4 - pad)
        data = base64.b64decode(clean)
        with open(new_image, 'wb') as fh:
            fh.write(data)
        return new_image
    except Exception as e:
        cmds.warning('MutantKanban: Could not decode image: {}'.format(e))
        return None


def clear_temp_folder():
    """Remove all files from the temp image folder."""
    try:
        for f in glob.glob(os.path.join(temp_folder, '*')):
            os.remove(f)
    except Exception:
        pass


# -------------------------------------------------------
# Viewport capture

def capture_viewport(image_name='kanban_snap', width=640, height=400,
                     ornaments=False):
    """
    Capture the current viewport via playblast and return the file path.
    Maya appends its own frame number + extension, so never pass an
    extension in image_name.
    """
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    # Strip any extension the caller may have supplied
    base_name = os.path.splitext(image_name)[0]
    image_file = os.path.join(temp_folder, base_name)
    frame = int(cmds.currentTime(query=True))
    exported = cmds.playblast(
        orn=ornaments, c='jpg',
        st=cmds.currentTime(query=True),
        et=cmds.currentTime(query=True),
        w=width, h=height, p=75,
        v=False, fo=True, fmt='image',
        f=image_file, cc=True, os=True, fp=4
    )
    # playblast returns path with .#### padding placeholder — replace it
    exported = exported.replace('.####', '.{:04d}'.format(frame))
    return exported


# -------------------------------------------------------
# Camera helpers

def get_current_camera():
    """Return the name of the currently active viewport camera."""
    try:
        view = OpenMayaUI.M3dView.active3dView()
        cam = OpenMaya.MDagPath()
        view.getCamera(cam)
        return cam.fullPathName().split('|')[1]
    except Exception:
        return 'persp'


def go_to_camera(node):
    """Restore the camera position that was saved on a note node."""
    data = get_note_data(node)
    camera = data.get('camera', 'persp')
    camera_xform_raw = data.get('camera_xform', '')
    if camera_xform_raw and cmds.objExists(camera):
        try:
            raw = str(camera_xform_raw).strip().strip('[]')
            matrix = [float(x.strip()) for x in raw.split(',')]
            cmds.xform(camera, m=matrix)
            cmds.lookThru(camera)
        except Exception as e:
            cmds.warning('MutantKanban: Could not restore camera: {}'.format(e))
    time_slider_raw = data.get('time_slider', '')
    if time_slider_raw:
        try:
            cmds.currentTime(float(time_slider_raw))
        except Exception:
            pass


# -------------------------------------------------------
# Note node CRUD

def create_note_node(title='New Task', notes='', encoded_image='',
                     column_name='Backlog', priority=1, tags=''):
    """
    Create a card transform node inside the given column group.
    Returns the node name.
    """
    user = getpass.getuser()
    date = time.ctime()
    creation_time = str(time.time())
    time_slider = cmds.currentTime(query=True)
    current_camera = get_current_camera()
    try:
        camera_xform = str(cmds.xform(current_camera, q=True, m=True))
    except Exception:
        camera_xform = ''

    get_or_create_kanban_root()
    col_grp = get_or_create_column_group(column_name)
    existing = get_notes_in_column(column_name)
    order = len(existing)

    # Build a Maya-safe node name from the title so the outliner is readable
    import re as _re
    safe_title = _re.sub(r'[^A-Za-z0-9_]', '_', title.strip()) or 'Note'
    if not safe_title[0].isalpha() and safe_title[0] != '_':
        safe_title = '_' + safe_title
    base_name = 'MK_{}'.format(safe_title)

    # Find a unique node name — never let Maya auto-number silently,
    # as that causes "more than one object matches name" errors later.
    desired_name = base_name
    counter = 1
    while cmds.objExists(desired_name):
        desired_name = '{}{}'.format(base_name, counter)
        counter += 1

    node = cmds.createNode('transform', name=desired_name)

    str_attrs = {
        'card_title': title,
        'card_notes': notes,
        'card_image': encoded_image,
        'card_user': user,
        'card_date': date,
        'card_creation_time': creation_time,
        'card_time_slider': str(time_slider),
        'card_camera': current_camera,
        'card_camera_xform': camera_xform,
        'card_tags': tags,
    }

    for attr, val in str_attrs.items():
        cmds.addAttr(node, ln=attr, dt='string', w=True)
        cmds.setAttr('{}.{}'.format(node, attr), str(val), type='string')

    # Lock metadata-only attrs
    for attr in ('card_user', 'card_date', 'card_creation_time',
                 'card_camera', 'card_camera_xform'):
        try:
            cmds.setAttr('{}.{}'.format(node, attr), l=True)
        except Exception:
            pass

    # Priority enum
    cmds.addAttr(node, ln='card_priority', en='Low:Medium:High:Urgent',
                 at='enum', w=True)
    cmds.setAttr('{}.card_priority'.format(node), int(priority))

    # Display order
    cmds.addAttr(node, ln='card_order', at='long', w=True)
    cmds.setAttr('{}.card_order'.format(node), order)

    cmds.parent(node, col_grp)
    print('MutantKanban: Created card {}.'.format(node))
    return node


def move_note_to_column(node, target_column, target_order=None):
    """Re-parent a note node to a different column group."""
    if not cmds.objExists(node):
        cmds.warning('MutantKanban: Node {} does not exist.'.format(node))
        return
    target_grp = get_or_create_column_group(target_column)
    cmds.parent(node, target_grp)
    if target_order is not None:
        if cmds.attributeQuery('card_order', node=node, exists=True):
            try:
                cmds.setAttr('{}.card_order'.format(node), int(target_order))
            except Exception:
                pass
    print('MutantKanban: Moved {} to {}.'.format(node, target_column))


def reorder_note(node, new_order):
    """Update the card_order attribute on a note node."""
    if not cmds.objExists(node):
        return
    if cmds.attributeQuery('card_order', node=node, exists=True):
        try:
            cmds.setAttr('{}.card_order'.format(node), int(new_order))
        except Exception:
            pass


def delete_note(node):
    """Delete a note node from the scene."""
    if cmds.objExists(node):
        cmds.delete(node)
        print('MutantKanban: Deleted {}.'.format(node))


def get_note_data(node):
    """Return a dict of all card attributes for a node."""
    def _get(attr):
        if cmds.objExists(node) and cmds.attributeQuery(attr, node=node, exists=True):
            try:
                return cmds.getAttr('{}.{}'.format(node, attr))
            except Exception:
                return ''
        return ''

    priority_raw = _get('card_priority')
    try:
        priority_val = int(priority_raw)
    except (TypeError, ValueError):
        priority_val = 1

    order_raw = _get('card_order')
    try:
        order_val = int(order_raw)
    except (TypeError, ValueError):
        order_val = 0

    return {
        'node': node,
        'title': _get('card_title') or 'Untitled',
        'notes': _get('card_notes'),
        'image': _get('card_image'),
        'user': _get('card_user'),
        'date': _get('card_date'),
        'creation_time': _get('card_creation_time'),
        'time_slider': _get('card_time_slider'),
        'camera': _get('card_camera'),
        'camera_xform': _get('card_camera_xform'),
        'tags': _get('card_tags'),
        'priority': priority_val,
        'order': order_val,
    }


def update_note_data(node, title=None, notes=None, priority=None, tags=None,
                     encoded_image=None):
    """Update editable fields on a note node."""
    if not cmds.objExists(node):
        cmds.warning('MutantKanban: Node {} does not exist.'.format(node))
        return

    def _safe_set_str(attr, val):
        full = '{}.{}'.format(node, attr)
        if not cmds.attributeQuery(attr, node=node, exists=True):
            return
        try:
            if not cmds.getAttr(full, lock=True):
                cmds.setAttr(full, str(val), type='string')
        except Exception as e:
            cmds.warning('MutantKanban: Could not set {}: {}'.format(full, e))

    if title is not None:
        _safe_set_str('card_title', title)
    if notes is not None:
        _safe_set_str('card_notes', notes)
    if tags is not None:
        _safe_set_str('card_tags', tags)
    if encoded_image is not None:
        _safe_set_str('card_image', encoded_image)
    if priority is not None:
        try:
            cmds.setAttr('{}.card_priority'.format(node), int(priority))
        except Exception as e:
            cmds.warning('MutantKanban: Could not set priority: {}'.format(e))
