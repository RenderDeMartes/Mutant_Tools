from __future__ import absolute_import
def isolate_asset():
    all_sels = []
    for i in range(99):
        current_sel = cmds.ls(sl=True)
        all_sels.append(current_sel[0])
        pw = cmds.pickWalk(d='up')
        if pw == current_sel:
            break

    cmds.select(all_sels[-2])

    currentObj = cmds.ls(selection=True)
    currentPanel = cmds.getPanel(wf=True)
    currentState = cmds.isolateSelect(currentPanel, query=True, state=True)
    if currentState == 0:
        cmds.isolateSelect(currentPanel, state=1)
        cmds.isolateSelect(currentPanel, addSelected=True)
    else:
        cmds.isolateSelect(currentPanel, state=0)
        cmds.isolateSelect(currentPanel, removeSelected=True)


#isolate_asset()