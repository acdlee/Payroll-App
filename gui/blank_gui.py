"""Home Window GUI"""


#misc imports
import sys


#PyQt imports
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit

class Home(QMainWindow):
	"""Home Window GUI"""

	#window switching signal
	switch_toEditFavs = QtCore.pyqtSignal()
	switch_toSubSheets = QtCore.pyqtSignal()

	def __init__(self):
		"""Define an instance of the Login GUI"""
		super().__init__()

		#set the geometry of the welcome window
		self.setWindowTitle('Timesheet - Home Window')
		self.setFixedSize(600, 600)

		#create an instance of QVBox for the generalLayout
		#and create/set the central widget
		self.generalLayout = QVBoxLayout()
		self._centralWidget = QWidget(self)
		self.setCentralWidget(self._centralWidget)
		self._centralWidget.setLayout(self.generalLayout)

		#let's create some widgets and nested layout
		self._fillTop()
		self.fillBot()




	##########################
	"""Mutators & Accessors"""
	##########################


	####################
	"""Widget Methods"""
	####################


	##################
	"""Slot Methods"""
	##################

        #######################
	"""Utility functions"""
	#######################
