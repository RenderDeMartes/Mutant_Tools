from __future__ import absolute_import
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2 import QtGui,QtCore
from shiboken2 import wrapInstance

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.OpenMayaUI as omui
from maya import OpenMaya
import maya.mel as mel
from maya import cmds

#QT WIndow!

TITLE = 'TITLE'
FOLDER = 'FOLDER'
UI_FILE = 'QT_FILE.ui'
ICONS_PATH =  FOLDER + '/Resources/'

def maya_main_window():
	
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class UI_CLASS(MayaQWidgetDockableMixin , QtWidgets.QMainWindow):
	
	def __init__(self, parent=maya_main_window()):
		super(UI_CLASS, self).__init__(parent)

		self.setWindowTitle(TITLE)
		self.setGeometry(280,270,0,0)
		
		self.init_ui()
		self.create_layout()
		self.create_connections()
		self.create_menus()

		OpenMaya.MGlobal.displayInfo('www.renderdemartes.com')

	def init_ui(self):
		
		UIPath  = cmds.internalVar(usd = True) + FOLDER + '/'
		f = QtCore.QFile(UIPath + UI_FILE)
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.ui = loader.load(f, parentWidget=self)

		f.close()
	
	def create_menus(self):

		#create menu bar
		self.menuBar = QtWidgets.QMenuBar()  # requires parent

		#File Menu
		self.optionsMenu = QtWidgets.QMenu(self)
		self.optionsMenu.setTitle("File")
		self.optionsMenu.addAction("www.renderdemartes.com")

		self.menuBar.addMenu(self.optionsMenu)


		#add menu bar to layout
		#self.ui.menuLayout.addWidget(self.menuBar)

	def create_layout(self):
				
		imagePath  = cmds.internalVar(usd = True) + ICONS_PATH
		#self.ui.ButtonName.setIcon(QtGui.QIcon(imagePath+'Locator.png'))

	def create_connections(self):

		def Demo(self):
			print('This is a DemoFunc')
		
		#self.ui.ButtonName.clicked.connect(self.Demo)
		#self.ui.ButtonName.clicked.connect(lambda: print 'this is lambda')
		
				
if __name__ == "__main__":

	try:
		Name_UI.close() # pylint: disable=E0601
		Name_UI.deleteLater()
	except:
		pass
		
	Name_UI = UI_CLASS()
	Name_UI.show(dockable=True)


