from __future__ import absolute_import
from maya import cmds

"""   
---------------Create skinned rigmesh for skirt for paintinng and copying weights-----------------
"""

# Run to create FK and IK vis toggles for a skirt setup. 
# Arguments:
    #prefix: (string) Prefix name given to create the skirt block. 
    #dup_levels: (integer) Number of times the rigmesh will get duplicated and subdivided.
    #skirt_bind_geos: (list) List of objects you want to add joint influences to. Default is selection based. 
    #open: (Boole) If true it deletes the front faces of the cylinder to create an open jacket.

# Return: (List) Created rigmeshes.



def create_skirt_rigmeshes(prefix="Skirt", dup_levels=2, skirt_bind_geos=[], open=False):
    from maya import cmds

    #Defining Important lists
    cylinder_vertices = [".vtx[13]", ".vtx[14]", ".vtx[15]", ".vtx[8]", ".vtx[9]", ".vtx[10]",
                        ".vtx[11]", ".vtx[12]", ".vtx[5]", ".vtx[6]", ".vtx[7]", ".vtx[0]",
                        ".vtx[1]", ".vtx[2]", ".vtx[3]", ".vtx[4]"]

    skirt_pos_ref_jnts = ["_Fr_Bind_01_Bnd", "_L_Fr_Bind_01_Bnd", "_L_Bind_01_Bnd", "_L_Bk_Bind_01_Bnd", "_Bk_Bind_01_Bnd", "_R_Bk_Bind_01_Bnd",
                         "_R_Bind_01_Bnd", "_R_Fr_Bind_01_Bnd", "_Fr_Bind_10_Bnd", "_L_Fr_Bind_10_Bnd", "_L_Bind_10_Bnd", "_L_Bk_Bind_10_Bnd", "_Bk_Bind_10_Bnd", 
                         "_R_Bk_Bind_10_Bnd", "_R_Bind_10_Bnd", "_R_Fr_Bind_10_Bnd"]

    skirt_bind_jnts = cmds.ls("{}_*_Bnd".format(prefix))

    newest_skinCluster = ""

    created_rigmeshes = []
    
    geo_skinCluster = ""

    if not skirt_bind_geos:
        skirt_bind_geos=cmds.ls(sl=True, type="transform")


    #Determining if prefix is correct. 
    if not cmds.objExists("{}{}".format(prefix, skirt_pos_ref_jnts[0])):
        cmds.error("Specified prefix does not match an existing skirt setup in scene.")


    #Creating Cylinder Rigmesh
    skirt_low_rigmesh = cmds.polyCylinder(name="{}_Low_Rigmesh".format(prefix), subdivisionsAxis=8)[0]
    created_rigmeshes.append(skirt_low_rigmesh)
    cmds.setAttr("{}.translateY".format(skirt_low_rigmesh), cmds.getAttr("{}_Fr_Ctrl_Main_Offset_Grp.translateY".format(prefix)))


    cmds.delete("{}.f[9]".format(skirt_low_rigmesh))
    cmds.delete("{}.f[8]".format(skirt_low_rigmesh))

    cmds.delete(skirt_low_rigmesh, constructionHistory = True)



    #Setting Vertex positions
    for vertex, ref_jnt in zip(cylinder_vertices, skirt_pos_ref_jnts):
        new_cluster = cmds.cluster("{}{}".format(skirt_low_rigmesh, vertex))[1]
        cmds.matchTransform(new_cluster, "{}{}".format(prefix, ref_jnt))
        
        
    cmds.delete(skirt_low_rigmesh, constructionHistory = True)
    
    #Making front open if specified
    if open:
        cmds.delete(["{}.f[5]".format(skirt_low_rigmesh), "{}.f[4]".format(skirt_low_rigmesh)])


    #Adding Loops
    if not open:
        cmds.select("{}.e[16:23]".format(skirt_low_rigmesh))
    if open:
        cmds.select("{}.e[12:18]".format(skirt_low_rigmesh))
        
    cmds.polySplitRing(ch=True, splitType=2, divisions=17, useEqualMultiplier=1, smoothingAngle=30, fixQuads=1)

    cmds.delete(skirt_low_rigmesh, constructionHistory = True)


    #Binding low poly geo
    low_poly_skinCluster = cmds.skinCluster(skirt_bind_jnts, skirt_low_rigmesh, toSelectedBones=True, dropoffRate=10,
    removeUnusedInfluence=False, bindMethod=0, ignoreHierarchy=True, maximumInfluences=2, obeyMaxInfluences=True)


    #Creating Higher Polycount geos.
    for number in range(1, dup_levels):
        subDiv_rigmesh = cmds.duplicate(skirt_low_rigmesh, name="{}_Level_{}_Rigmesh".format(prefix,number))
        created_rigmeshes.append(subDiv_rigmesh[0])
        
        cmds.polySmooth(subDiv_rigmesh, mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=number, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0,
        sl=1, dpe=1, ps=0.1, ro=1, ch=1)
        
        cmds.delete(subDiv_rigmesh, constructionHistory = True)
        
        subDiv_skinCluster = cmds.skinCluster(skirt_bind_jnts, subDiv_rigmesh, toSelectedBones=True, dropoffRate=10,
                             removeUnusedInfluence=False, bindMethod=0, ignoreHierarchy=True, maximumInfluences=12, obeyMaxInfluences=True)
                             
        if not newest_skinCluster:
            newest_skinCluster = low_poly_skinCluster
                             

        #Copy skin weights from last created rigmsesh to higher level rig mesh.    
        cmds.copySkinWeights(sourceSkin=newest_skinCluster[0],  destinationSkin=subDiv_skinCluster[0], influenceAssociation="closestJoint", surfaceAssociation="closestPoint", noMirror=True)
        print("Copied weight from {} to {}".format(newest_skinCluster, subDiv_skinCluster))
        
        newest_skinCluster = subDiv_skinCluster
        

    #Adding influence to selected geo's existing skinclusters.
        if skirt_bind_geos:
            for geo in skirt_bind_geos:
                try: 
                    geo_skinCluster = cmds.ls(cmds.listHistory(geo), type="skinCluster")[0]

                except:
                    print("No geos selected to add joint influences to.")
                
                if geo_skinCluster:
                    for jnt in skirt_bind_jnts:
                        cmds.skinCluster(geo_skinCluster, e=True, dr=10, lw=True, wt=0, ai=jnt)
                

    #Grouping_RigMeshes
    cmds.group(created_rigmeshes, name="{}_RigMeshes_grp".format(prefix))

    return created_rigmeshes


#create_skirt_rigmeshes(prefix="Jacket", open=True)





"""   
---------------Create visibility toggles for the Fk and IKs in a skirt block in a specified ctrl. -----------------
"""

# Run to create FK and IK vis toggles for a skirt setup. 
# Arguments:
    #block_prefix: (string) Prefix name given to create the block. 
    #attribute_location: (string) name of controller to have the visibility attributes. 
# Return: None


def add_skirt_vis_toggle(block_prefix='', attribute_location=''):

    #Definint block prefix. 
    if not block_prefix:
        block_prefix = "Skirt"

    #Defining Attribute location 
    if not attribute_location:
        attribute_location = "Global_Ctrl"

    if cmds.objExists(attribute_location):
        for ending in ["Grp", "grp"]:
            if cmds.objExists("{}_Ctrl_{}".format(block_prefix, ending)):
                if cmds.attributeQuery("{}_Ctrl_Vis".format(block_prefix), node=attribute_location, exists=True):
                    print("Main Ctrl Attribute already exists")
                    cmds.deleteAttr("{}.{}_Ctrl_Vis".format(attribute_location,block_prefix))
                    print("Main Ctrl Attribute deleted")

                if cmds.attributeQuery("{}_IK_Ctrl_Vis".format(block_prefix), node=attribute_location, exists=True):
                    print("Sub IK Ctrl Attribute already exists")
                    cmds.deleteAttr("{}.{}_IK_Ctrl_Vis".format(attribute_location,block_prefix))
                    print("Sub IK Ctrl Attribute deleted")

                cmds.addAttr(attribute_location, ln="{}_Ctrl_Vis".format(block_prefix), at="bool", keyable=True)
                cmds.addAttr(attribute_location, ln="{}_IK_Ctrl_Vis".format(block_prefix), at="bool", keyable=True)

                cmds.connectAttr("{}.{}_Ctrl_Vis".format(attribute_location, block_prefix), "{}_Ctrl_{}.visibility".format(block_prefix, ending))
                print("Successfully created main ctrl vis toggle.")

                skirt_ik_offset_groups = [u'_R_Fr_04_Ctrl_constr_',
                 u'_R_04_Ctrl_constr_',
                 u'_Fr_04_Ctrl_constr_',
                 u'_L_Fr_04_Ctrl_constr_',
                 u'_L_04_Ctrl_constr_',
                 u'_Fr_03_Ctrl_constr_',
                 u'_R_Fr_03_Ctrl_constr_',
                 u'_R_03_Ctrl_constr_',
                 u'_L_Fr_03_Ctrl_constr_',
                 u'_L_03_Ctrl_constr_',
                 u'_L_Bk_04_Ctrl_constr_',
                 u'_Bk_04_Ctrl_constr_',
                 u'_L_Fr_02_Ctrl_constr_',
                 u'_Fr_02_Ctrl_constr_',
                 u'_L_Bk_03_Ctrl_constr_',
                 u'_L_02_Ctrl_constr_',
                 u'_R_Bk_04_Ctrl_constr_',
                 u'_R_Fr_02_Ctrl_constr_',
                 u'_Bk_03_Ctrl_constr_',
                 u'_L_Bk_02_Ctrl_constr_',
                 u'_L_Fr_01_Ctrl_constr_',
                 u'_Fr_01_Ctrl_constr_',
                 u'_R_Bk_03_Ctrl_constr_',
                 u'_L_01_Ctrl_constr_',
                 u'_Bk_02_Ctrl_constr_',
                 u'_L_Bk_01_Ctrl_constr_',
                 u'_R_Bk_02_Ctrl_constr_',
                 u'_R_02_Ctrl_constr_',
                 u'_R_Fr_01_Ctrl_constr_',
                 u'_L_Fr_00_Ctrl_constr_',
                 u'_Bk_01_Ctrl_constr_',
                 u'_L_00_Ctrl_constr_',
                 u'_Fr_00_Ctrl_constr_',
                 u'_R_Fr_00_Ctrl_constr_',
                 u'_R_00_Ctrl_constr_',
                 u'_R_Bk_00_Ctrl_constr_',
                 u'_Bk_00_Ctrl_constr_',
                 u'_L_Bk_00_Ctrl_constr_',
                 u'_R_Bk_01_Ctrl_constr_',
                 u'_R_01_Ctrl_constr_']
                 
                for offset_group in skirt_ik_offset_groups:
                    for suffix in ["Grp","grp"]:
                        if cmds.objExists("{}{}{}".format(block_prefix, offset_group, suffix)):
                            cmds.connectAttr("{}.{}_IK_Ctrl_Vis".format(attribute_location, block_prefix), "{}{}{}.visibility".format(block_prefix,offset_group, suffix))
            else:
                print("Block prefix: '{}' doesn't exist with suffix '{}'".format(block_prefix, ending))
    else:
        cmds.error("Specified attribute location controller doesn't exist.")

#add_skirt_vis_toggle(block_prefix='Jacket')




"""   
---------------Create groups to move the skirt surfaces in mirror mode-----------------
"""
# First script creates mirrored offset groups on the the skirt guides in order to move them symmetrically. 
# Second script deleted them and places them in the block in the right order.
# Write the block's prefix as a string in arguments and run to create groups or delete them when you're done.   
# Return: None


def create_mirror_skirt_groups(block_prefix=""):
    if not block_prefix:
        block_prefix = "Skirt"
    if cmds.objExists("{}_Block".format(block_prefix)):

        for side_prefix in ["", "_Fr", "_Bk"]:
            L_Fr_group = cmds.createNode("transform", name="{}_L{}_group".format(block_prefix,side_prefix))
            piv = cmds.matchTransform(L_Fr_group, "{}_L{}_Guide".format(block_prefix, side_prefix))
        
            R_Fr_group = cmds.duplicate(L_Fr_group, name="{}_R{}_group".format(block_prefix, side_prefix))
            R_Fr_mirror_group = cmds.createNode("transform", name="{}_R{}_group_mirror".format(block_prefix, side_prefix))
            cmds.parent(R_Fr_group, R_Fr_mirror_group)
            cmds.setAttr("{}.scaleX".format(R_Fr_mirror_group), -1)
        
        
            cmds.parent(L_Fr_group, "{}_Block".format(block_prefix))
            cmds.parent("{}_L{}_Guide".format(block_prefix, side_prefix), L_Fr_group)
        
        
            cmds.parent(R_Fr_mirror_group, "{}_Block".format(block_prefix))
            cmds.parent("{}_R{}_Guide".format(block_prefix, side_prefix), R_Fr_group)
    else:
        cmds.error("specified prefix does not correspond to an existing skirt block")

def delete_mirror_skirt_groups(block_prefix=""):

    if not block_prefix:
        block_prefix = "Skirt"

    guide_surfaces = ["_Fr_Guide", "_L_Fr_Guide", "_L_Guide", "_L_Bk_Guide","_Bk_Guide", "_R_Bk_Guide", "_R_Guide", "_R_Fr_Guide"]
    
    if cmds.objExists("{}_R_Fr_group_mirror".format(block_prefix)):
        for guide in guide_surfaces:
            cmds.parent("{}{}".format(block_prefix, guide), world=True)
            
        block_children = cmds.listRelatives("{}_Block".format(block_prefix), children=True)
        cmds.delete(block_children)
        
        for guide in guide_surfaces:
            cmds.parent("{}{}".format(block_prefix, guide), "{}_Block".format(block_prefix))

    else:
        cmds.error("There are no mirror offset groups to delete.")



#create_mirror_skirt_groups()       
#delete_mirror_skirt_groups()      
