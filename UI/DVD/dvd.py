from __future__ import absolute_import, division
from PySide2 import QtWidgets, QtGui, QtCore

import os
from pathlib import Path

# QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

IconsPath = os.path.join(FOLDER, 'Icons')

class SquareMoveApp(QtWidgets.QWidget):
	def __init__(self):
		super(SquareMoveApp, self).__init__()

		# Set the window flags
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

		# Set the window to full screen
		screen = QtWidgets.QDesktopWidget().screenGeometry()
		self.setGeometry(screen)

		# Create a QGraphicsScene
		self.scene = QtWidgets.QGraphicsScene(self)
		self.scene.setSceneRect(0, 0, screen.width(), screen.height())

		# Load and create a QPixmap from the image file
		image_path = os.path.join(IconsPath, 'LogoWhite03.png')  # Replace with your image path
		original_pixmap = QtGui.QPixmap(image_path)

		# Set the fixed scale factor for the logo
		scale_factor = 0.5  # Replace with your desired scale factor

		# Scale the original pixmap to the desired size
		scaled_pixmap = original_pixmap.scaledToWidth(original_pixmap.width() * scale_factor)

		# Create a QGraphicsPixmapItem representing the square with the image
		self.square = QtWidgets.QGraphicsPixmapItem(scaled_pixmap)
		self.square.setPos(0, 0)  # Set initial position

		# Add the square to the scene
		self.scene.addItem(self.square)

		# Create a QGraphicsView to display the scene
		self.view = QtWidgets.QGraphicsView(self.scene, self)
		self.view.setGeometry(0, 0, screen.width(), screen.height())
		self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		# Set up initial direction
		self.direction = QtCore.QPointF(2, 2)

		# Set up a timer to move the square
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.moveSquare)
		self.timer.start(16)  # Update every 16 milliseconds (about 60 frames per second)

	def moveSquare(self):
		# Move the square with the current direction
		current_pos = self.square.pos()
		new_pos = current_pos + self.direction
		self.square.setPos(new_pos)

		# Check if the square hits the edges of the screen
		if new_pos.x() < 0 or new_pos.x() + self.square.pixmap().width() > self.view.width():
			self.direction.setX(-self.direction.x())  # Reverse the x-direction

		if new_pos.y() < 0 or new_pos.y() + self.square.pixmap().height() > self.view.height():
			self.direction.setY(-self.direction.y())  # Reverse the y-direction

if __name__ == "__main__":
	# Check if the window already exists and close it
	try:
		square_app.close()
	except NameError:
		pass

	print('DVD')

	# Create and show the SquareMoveApp window
	square_app = SquareMoveApp()
	square_app.showFullScreen()  # Show the window in full screen

	# Execute the application
	QtWidgets.QApplication.instance().exec_()