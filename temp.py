    Normalize0L = cmds.shadingNode('multiplyDivide', asUtility=True, n='L_Arm_normalize_MultDiv')
    cmds.setAttr('L_Arm_normalize_MultDiv.operation', 2)

    cmds.connectAttr(str(Character) + '_MasterControl.scaleX','L_Arm_normalize_MultDiv.input2X')

    cmds.connectAttr('L_Arm_Distance.distance','L_Arm_normalize_MultDiv.input1X', f= True)     
    cmds.connectAttr('L_Arm_normalize_MultDiv.outputX','L_ArmMultDiv.input1X', f= True)     
    cmds.connectAttr('L_Arm_normalize_MultDiv.outputX','L_ArmMultDiv00.input1X', f= True)   