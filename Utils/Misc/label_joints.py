from __future__ import absolute_import
from maya import cmds

"""   
--------------------------LABEL JOINTS---------------------------
"""

def mass_label_joints():
    """
    #Description :
        Label joints based on selection. 

    #Instructions:
        Select either the specific joints you wish to label, the group they are under and run script. If nothing is selected
        it will look for Mutant's "Bind_Joints_Grp" and label every joint in there; if the group doesn't exist then it will error. 

    # Return: None
    """


    #Defining possible sufixes.
    joint_naming_ends = ["BND", "SKIN", "SKN", "JNT"]

    #Defining possible prefixes.
    L_joint_prefixes = ["L", "LF", "LB", "LC"]
    R_joint_prefixes = ["R", "RF", "RB", "RC"]
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
        bind_joint_sel = cmds.listRelatives("Bind_Joints_Grp", allDescendents=True, type="joint")

    #If the mutant "Bind_Joints_Grp" does not exist then ask for a selection. 
    if not bind_joint_sel:
        cmds.error("No Mutant Bind_Joints_Grp found. Please select the joints you wish to add labels to.")


    #Setting the naming on the joints.
    for bind_joint in bind_joint_sel:
        
        #Dividing name in parts to analize it.
        bind_joint_names = bind_joint.split("_")
        
        #Determining Label side based on initial letter.
        if bind_joint_names[0].upper() in L_joint_prefixes or bind_joint_names[0].upper().startswith("LEFT"):
            cmds.setAttr("{}.side".format(bind_joint), 1)   
        elif bind_joint_names[0].upper() in R_joint_prefixes or bind_joint_names[0].upper().startswith("RIGHT"):
            cmds.setAttr("{}.side".format(bind_joint), 2)
        
        #Creating scenario for skirt setup variants.
        elif bind_joint_names[0].upper() in skirt_prefixes:
            
            #Setting label side based on second split instead of first one. 
            if bind_joint_names[1].upper() in L_joint_prefixes:
                cmds.setAttr("{}.side".format(bind_joint), 1)
            elif bind_joint_names[1].upper() in R_joint_prefixes:
                cmds.setAttr("{}.side".format(bind_joint), 2)
            else:
                cmds.setAttr("{}.side".format(bind_joint), 0)
        
        #If no letter and no exception as first split, set as center.             
        else:
            cmds.setAttr("{}.side".format(bind_joint), 0)
            
        #Setting type to "Other" for costume name.
        cmds.setAttr("{}.type".format(bind_joint), 18)
        
        
        """
        #Idea to remove joint suffix. Not needed but will keep just in case.
        #Determining what name to write in label box.
        if bind_joint_names[-1].upper() in joint_naming_ends:
            print("JOINT HAS SUFFIX")
            
            if bind_joint_names[0].upper() in L_joint_prefixes or bind_joint_names[0] in R_joint_prefixes:
                label_name = "_".join(bind_joint_names[1:-1])
                print("JOINT HAS PREFIX")
            else:
                label_name = "_".join(bind_joint_names[0:-1])
                print("JOINT HAS NO PREFIX")
        else:
            print("JOINT HAS NO SUFFIX")
            if bind_joint_names[0].upper() in L_joint_prefixes or bind_joint_names[0] in R_joint_prefixes:
                label_name = "_".join(bind_joint_names[1:])
                print("JOINT HAS PREFIX")
                
            
            else:
                label_name = "_".join(bind_joint_names)
                print("JOINT HAS NO PREFIX")
        """
        
        #Determining what name to write in label box.
        if bind_joint_names[0].upper() in L_joint_prefixes or bind_joint_names[0].upper() in R_joint_prefixes:
            label_name = "_".join(bind_joint_names[1:])
            
        elif bind_joint.upper().startswith("LEFT"):
            label_name = bind_joint.replace("Left", "")
            
        elif bind_joint.upper().startswith("RIGHT"):
            label_name = bind_joint.replace("Right", "")

        else:
            label_name = "_".join(bind_joint_names[0:])        
        

        #Setting the label name on the joint
        cmds.setAttr("{}.otherType".format(bind_joint), label_name, type="string")  
        
    cmds.warning("Joints have been labeled without error. Thank you.")

