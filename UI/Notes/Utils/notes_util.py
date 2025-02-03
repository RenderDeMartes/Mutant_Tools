from __future__ import absolute_import
from maya import cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

import os
import glob
import time
import base64
import getpass

import tempfile
temp_folder = os.path.join(tempfile.gettempdir(), 'Notes')

PATH = os.path.dirname(__file__)
Folder = os.path.join(PATH).replace('Utils', '')

#----------------------------------------------------------------------------------------

def encode_image(image = os.path.join(temp_folder, 'temp.jpg')):

    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

#----------------------------------------------------------------------------------------

def decode_image(encoded_image='',
                image_path=temp_folder,
                image_name='temp.jpg',
                force_fix=True):

    if force_fix:
        encoded_image = str(encoded_image).replace("b'", '')[:-1].encode('ascii')

    new_image = os.path.join(image_path, image_name)
    bytes_image = encoded_image + b"========"
    with open(new_image, "wb") as fh:
        fh.write(base64.b64decode(bytes_image))
    return new_image

#----------------------------------------------------------------------------------------

def clear_temp_folder(path = temp_folder):
    try:
        files = glob.glob(path + '*')
        for f in files:
            os.remove(f)
    except:
        pass

#----------------------------------------------------------------------------------------

def capture_viewport(image_name = 'temp.jpg',
                     location = temp_folder,
                     width= 600, 
                     height = 400,
                     ornaments = False):

    #playblast -orn 1 -c "jpg" -st 0 -et 0 -w 480 -h 480 -p 65 -v off -fo -fmt image -f "C:/Users/rodri/OneDrive/Documents/maya/projects/default/images/test.jpg"
    image_file = os.path.join(location, image_name)
    exported_image = cmds.playblast(orn=ornaments, c='jpg', st=cmds.currentTime( query=True ), et=cmds.currentTime( query=True ), w=width, h =height, p = 75, v=False, fo=True, fmt = 'image', f = image_file, cc=True, os=True, fp=1)
    time_slider = int(cmds.currentTime( query=True ))
    exported_image = exported_image.replace('.####', '.{}'.format(time_slider))

    print (exported_image)
    return exported_image

#----------------------------------------------------------------------------------------

def show_image(image = os.path.join(temp_folder, 'temp.jpg')):

    window = cmds.window(t = 'Preview image')
    cmds.paneLayout()
    cmds.image( image= image)
    cmds.showWindow( window )
    print (image),

#----------------------------------------------------------------------------------------

def create_container():

    cmds.select(cl=True)
    container_node = cmds.container(name="RdM_Notes")
    cmds.setAttr('{}.blackBox'.format(container_node), 1)
    cmds.setAttr('{}.iconName'.format(container_node), os.path.join(Folder, 'Resources' ,'notes_icon.png'), type ="string")

    return container_node

#----------------------------------------------------------------------------------------

def get_current_camara():

    view = OpenMayaUI.M3dView.active3dView()
    cam = OpenMaya.MDagPath()
    view.getCamera(cam)
    camPath = cam.fullPathName()
    camara = camPath.split('|')[1] 
    return camara

#----------------------------------------------------------------------------------------

def create_note_node(name = 'RdM_Note', 
                     note = 'Note Details Here',
                     encoded_image = os.path.join(temp_folder, 'temp.jpg'),
                     current_mode=0):

    user = getpass.getuser()
    date = time.ctime()
    creation_time = time.time()

    modes = "to_do:done:urgent"

    name = name
    note = note
    encoded_image = encoded_image

    time_slider = cmds.currentTime( query=True )
    current_camara= get_current_camara()
    camara_xform = cmds.xform(current_camara, q=True, m=True)

    #craete note transform
    node = cmds.createNode('transform', name = name)
    #search for the container
    if cmds.objExists("RdM_Notes") == False:
        create_container()
    cmds.container('RdM_Notes', edit=1, includeTransform=1, force=1, addNode=node, includeShapes=1)

    #crate custom attrs with correct inputs

    attrs = {'node': node,
            'user':user,
            'date':date,
            'creation_time':creation_time,
            'name':name,
            'notes':note,
            'image':encoded_image,
            'time_slider':time_slider,
            'current_camara':current_camara,
            'camara_xform':camara_xform}
    
    for attr in attrs:
        print (str(attr) + ':' + str(attrs[attr]))
        cmds.addAttr(node, ln=attr, dt="string", w=True)
        cmds.setAttr('{}.{}'.format(node,attr), str(attrs[attr]), type="string")
    for attr in attrs:
        if attr != 'notes':
            cmds.setAttr('{}.{}'.format(node,attr), l=True)

    #add notes modes
    cmds.addAttr(node, ln="mode", en=modes, at="enum")
    cmds.setAttr(node+'.mode', current_mode)

    return node

#----------------------------------------------------------------------------------------

def go_to_camera(node):

    camera = cmds.getAttr('{}.current_camara'.format(node))
    camera_matrix = cmds.getAttr('{}.camara_xform'.format(node))

    camera_matrix = str(camera_matrix).split(',')
    #camera_matrix = camera_matrix[1,-2]
    camera_matrix = str(camera_matrix).replace("'", "")
    camera_matrix = str(camera_matrix).replace("[", "")
    camera_matrix = str(camera_matrix).replace("]", "")
    camera_matrix = str(camera_matrix).replace(" ", "")

    camera_matrix = camera_matrix.split(',')

    matrix = []
    for i in camera_matrix:
        i = float(i)
        matrix.append(i)

    cmds.xform(camera, m = matrix)
    cmds.lookThru(camera)

    #also go to the frame
    note_time = cmds.getAttr('{}.time_slider'.format(node))
    print (note_time)
    cmds.currentTime(note_time)

    print (camera_matrix),
    print (camera),


