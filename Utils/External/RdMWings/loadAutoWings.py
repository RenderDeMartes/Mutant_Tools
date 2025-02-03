from __future__ import absolute_import
'''
content: Show UI to create wings
version: 1.0.0

date: 21/04/2020

how to: 
from RdMWings.loadAutoWings import WingsUI
RdMV2_ui = WingsUI()
RdMV2_ui.show()


dependencies:  all RdMWings
            
licence: EULA 
         https://www.eulatemplate.com/live.php?token=uvtn9mOrCrX6m7CkXYA1EPZOFrBTEj67

author:  Esteban Rodriguez <info@renderdemartes.com>

'''

'''

from RdMWings.loadAutoWings import WingsUI
RdMV2_ui = WingsUI()
RdMV2_ui.show()

'''

from PySide2 import QtGui,QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel


try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.Utils.External.RdMWings import autoWings, wingModule, BindFeathers, autoFold
reload(autoWings)
reload(wingModule)
reload(BindFeathers)
reload(autoFold)



#QT WIndow!

Title = 'RdM AutoWings'
Folder = 'RdMWings'
UI_File = 'RdMWingsUI.ui'
ResourcesPath =  Folder + '/Resources/'



def maya_main_window():
    
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)



class WingsUI(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(WingsUI, self).__init__(parent)

        self.setWindowTitle(Title)
        self.setFixedSize(450,409)

        self.init_ui()
        self.create_layout()
        self.create_connections()

    def init_ui(self):
        
        UIPath  = cmds.internalVar(usd = True) + Folder + '/'
        f = QtCore.QFile(UIPath + UI_File)
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self)

        f.close()

    def create_layout(self):
        
        #self.ui.layout().setContentsMargins(3, 3, 3, 3)          
      
        imagePath  = cmds.internalVar(usd = True) + ResourcesPath
        
        #print 'image:' +imagePath+ 'WingBG.png);'
        #self.ui.ButtonName.setIcon(QtGui.QIcon(imagePath+'Locator.png'))
        
        self.ui.BG.setStyleSheet('image : url('+ imagePath +'WingBG.png)')
        self.ui.SystemBtn.setIcon(QtGui.QIcon(imagePath+'Bird.png'))
        self.ui.RefBtn.setIcon(QtGui.QIcon(imagePath+'Ref.png'))
        self.ui.JointsBtn.setIcon(QtGui.QIcon(imagePath+'Joint.png'))

        self.ui.CreateBaseModuleBtn.setIcon(QtGui.QIcon(imagePath+'Base.png'))
        self.ui.CreateWingsModuleBtn.setIcon(QtGui.QIcon(imagePath+'Module.png'))

        self.ui.initialFoldBtn.setIcon(QtGui.QIcon(imagePath+'Fold.png'))
        self.ui.KeysToAutoBtn.setIcon(QtGui.QIcon(imagePath+'SDK.png'))
        self.ui.DeleteBtn.setIcon(QtGui.QIcon(imagePath+'Delete.png'))
        self.ui.BindFeathersBtn.setIcon(QtGui.QIcon(imagePath+'BindSkin.png'))
        self.ui.MirrorBtn.setIcon(QtGui.QIcon(imagePath+'Mirror.png'))
        
        #Realod UI
        if cmds.objExists('WingRef_Loc'):
            try:
                print('loc ref exits')
                self.ui.ScapAmountSlider.setValue(cmds.getAttr('WingRef_Loc.ScapAmount'))
                self.ui.ScapDistanceSlider.setValue(cmds.getAttr('WingRef_Loc.ScapBack'))            
    
                self.ui.SecAmountSlider.setValue(cmds.getAttr('WingRef_Loc.SecAmount'))
                self.ui.SecDistanceSlider.setValue(cmds.getAttr('WingRef_Loc.SecBack'))        
                
                self.ui.PrimAmountSlider.setValue(cmds.getAttr('WingRef_Loc.PrimAmount'))
                self.ui.PrimDistanceSlider.setValue(cmds.getAttr('WingRef_Loc.PrimBack'))        
                print('sucess Evaluating previews versions')

            except:
                print('Cant Evaluate previews versions')
                                  
    def create_connections(self):
       
        '''       
        ScapAmount = self.ui.ScapAmountSlider.value()
        ScaptBack = self.ui.ScapDistanceSlider.value()
        SecAmount = self.ui.SecAmountSlider.value()
        SecBack = self.ui.SecDistanceSlider.value()
        PrimAmount = self.ui.PrimAmountSlider.value()
        PrimBack = self.ui.PrimDistanceSlider.value()
        '''
            
        self.ui.JointsBtn.clicked.connect(lambda: autoWings.CreateJoints())
        self.ui.RefBtn.clicked.connect(self.buildRefUI)
        self.ui.SystemBtn.clicked.connect(self.buildSystemUI)        

        #***************************************************
        self.ui.initialFoldBtn.clicked.connect(lambda: autoFold.setInitialKeys())
        self.ui.KeysToAutoBtn.clicked.connect(lambda: autoFold.keysToSDK2())

        
        self.ui.DeleteBtn.clicked.connect(lambda: autoWings.rebuildLeftWing())

        self.ui.MirrorBtn.clicked.connect(lambda: autoWings.mirrorWing())

        self.ui.BindFeathersBtn.clicked.connect(self.bindFeathersUI)
    

        #***************************************************
        
        self.ui.CreateBaseModuleBtn.clicked.connect(self.wingModuleFuncUI)
        self.ui.CreateWingsModuleBtn.clicked.connect(self.createWingsUI)


    #-----------------------------------------------------------------
    #AutoWings Functions
        
    def buildRefUI(self):
        
        autoWings.buildWingsRef(
            ScapAmount = self.ui.ScapAmountSlider.value(),
            ScaptBack = self.ui.ScapDistanceSlider.value(),
            SecAmount = self.ui.SecAmountSlider.value(),
            SecBack = self.ui.SecDistanceSlider.value(),
            PrimAmount = self.ui.PrimAmountSlider.value(),
            PrimBack = self.ui.PrimDistanceSlider.value()) 
            
    def buildSystemUI(self):
        autoWings.buildWingsSystem(
            ScapAmount = self.ui.ScapAmountSlider.value(),
            ScaptBack = self.ui.ScapDistanceSlider.value(),
            SecAmount = self.ui.SecAmountSlider.value(),
            SecBack = self.ui.SecDistanceSlider.value(),
            PrimAmount = self.ui.PrimAmountSlider.value(),
            PrimBack = self.ui.PrimDistanceSlider.value(),
            sizeUI = 1) 
        

        autoWings.getPivot(side = 'L', part = 'Primaries')
        autoWings.getPivot(side = 'L', part = 'Secondaries')
        autoWings.getPivot(side = 'L', part = 'Scapulars')

	   


    #-----------------------------------------------------------------
    #Fold and Skinning Functions   
    
    def bindFeathersUI(self):
        BindFeathers.bindWings(side = 'L_' if self.ui.leftRadio.isChecked() else 'R_',
        feather = 'Scapulars' if self.ui.scapularsRadio.isChecked() 
        else 'Secondaries' if self.ui.SecundariesRadio.isChecked()
        else 'Primaries',
        bone = True if self.ui.boneBox.isChecked() else False )

    
            
    #-----------------------------------------------------------------
    #WingModule Functions   
    
     
    def wingModuleFuncUI(self):

        wingModule.wingModuleFunc(amount = self.ui.AmounModuleSlider.value() , 
        Axis = 'X' if self.ui.XRB.isChecked() else 'Y' if self.ui.YRB.isChecked() else 'Z',
        distanceBack = self.ui.DistanceBackSliderModule.value())      


    def createWingsUI(self):

        wingModule.createWings(amount = self.ui.AmounModuleSlider.value() , 
        Axis = 'X' if self.ui.XRB.isChecked() else 'Y' if self.ui.YRB.isChecked() else 'Z',
        distanceBack = self.ui.DistanceBackSliderModule.value(),
        size =  1,
        colorCC =  self.ui.ColorModuleSlider.value(),
        name1 = 'Null',
        name2 = 'Null')    
          
        
                
if __name__ == "__main__":

    try:
        WingsUI_ui.close() # pylint: disable=E0601
        WingsUI_ui.deleteLater()
    except:
        pass
    WingsUI_ui = WingsUI()
    WingsUI_ui.show()
