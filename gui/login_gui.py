"""Login GUI"""


#sys import
import sys

#PyQt imports
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget,
							QLineEdit, QStatusBar, QRadioButton,
							QHBoxLayout)

#GLOBAL CONSTANTS
DATA_PATH = './helpers/data/'


class Login(QMainWindow):
	"""Login Window GUI"""

	#window switching signal
	switch_window = QtCore.pyqtSignal()

	def __init__(self):
		"""Define an instance of the Login GUI"""
		super().__init__()

		#set the geometry of the welcome window
		self.setWindowTitle('Timesheet - Login Window')
		self.setFixedSize(300, 300)

		#instance variables for employee info; private scope
		self.__employee_name = ""
		self.__employee_ssn = 0
		self._loadInfo()	#grab the user's info
		self._filter = 'officer'	#default role

		#create an instance of QVBox for the generalLayout
		#and create/set the central widget
		self.generalLayout = QVBoxLayout()
		self._centralWidget = QWidget(self)
		self.setCentralWidget(self._centralWidget)
		self._centralWidget.setLayout(self.generalLayout)

		#create a status bar to communicate app status
		self._createStatusBar()

		#create a boolean for allowing the user to login; make private
		self.__valid_login = False

		#let's add some widgets
		self._addSSNBox()
		self._addFilter()
		self._addLoginBtn()


	##########################
	"""Mutators & Accessors"""
	##########################
	def __setName(self, name):
		"""setter (mutator) for employee name"""
		self.__employee_name =  name
	
	def _getName(self):
		"""getter (accessor) for employee name"""
		return self.__employee_name
	
	def __setSSN(self, ssn):
		"""setterr (mutator) for employee ssn"""
		self.__employee_ssn = ssn

	def _getFilter(self):
		return self._filter.lower()

	def _setFilter(self, new_filter):
		self._filter = new_filter
	


	#################################
	"""Class Methods (for widgets)"""
	#################################

	def _addFilter(self):
		layout = QHBoxLayout()
		self._filterBtn1 = QRadioButton("Employee")
		self._filterBtn1.setChecked(True)
		self._filterBtn2 = QRadioButton("Officer")

		self._filterBtn1.toggled.connect(lambda:self._btnState(self._filterBtn1))
		self._filterBtn2.toggled.connect(lambda:self._btnState(self._filterBtn2))

		layout.addWidget(self._filterBtn1)
		layout.addWidget(self._filterBtn2)

		self.generalLayout.addLayout(layout)

	def _createStatusBar(self):
		"""Create a status bar for user communication"""
		#create an instance of QStatusBar
		self.statusBar = QStatusBar()
		#set the text for the statusBar
		self.statusBar.showMessage("Enter the last 4 of your SSN and hit Enter.")
		#set the  statusBar
		self.setStatusBar(self.statusBar)

	def _addSSNBox(self):
		"""This function creates the SSN LineEdit widget"""
		#create an instance of QLineEdit
		self.ssn_box = QLineEdit()
		#set the max input length
		self.ssn_box.setMaxLength(4)
		#restrict user input
		self.ssn_box.setValidator(QtGui.QIntValidator())
		#create a signal
		self.ssn_box.editingFinished.connect(self._ssnText)
		#set some default text
		self.ssn_box.setPlaceholderText("Enter the last 4 digits of your SSN.")

		#add the widget to the layout
		self.generalLayout.addWidget(self.ssn_box)

	def _addLoginBtn(self):
		"""Adds the login button widget to the layout"""
		#create the widget
		self.button = QtWidgets.QPushButton('Login')
		#create the signal
		self.button.clicked.connect(self._login)
		#add the widget to the layout
		self.generalLayout.addWidget(self.button)


	####################
	"""Slot Functions"""
	####################

	def _btnState(self, button):
		if button.text() == 'Employee':
			self._setFilter('Officer')
		else:
			self._setFilter('Employee')

	def	_ssnText(self):
		"""grab the text in the ssn QLineEdit widget"""
		#grab the current text; cast to an int
		txt = int(self.ssn_box.text())
		self.ssn_box.clear()
		#check the user input against the employee ssn on record
		if txt == self.__employee_ssn:
			self.__valid_login = True	#flip login bool
			#adjust text to communicate instruction to user
			self.ssn_box.setPlaceholderText("SSN Accepted.")
			self.statusBar.showMessage("Click The Login Button.")
		else:
			#if they incorrectly enter their ssn AT ANY POINT
			#invalidate the login attempt
			self.__valid_login = False
			#adjust text to communicate instruction to user
			self.ssn_box.setPlaceholderText("Invalid SSN.")
			msg =  "Incorrect SSN entered. Please try again."
			self.statusBar.showMessage(msg)

	def _login(self):
		"""This function 1)is the  slot for
		the login button signal; 2)switches to another window"""
		if self.__valid_login:
			self.switch_window.emit()


	#######################
	"""Utility functions"""
	#######################

	def _loadInfo(self):
		"""Load in the login information"""
		#let's grab the user's info
		try:
			with open(DATA_PATH + 'user_info.txt', 'r') as user_info:
				login_data = user_info.readlines()
		except Exception:
			#troubleshoot if you cant open the file
			print("Could not find file: <user_info.txt>")
			sys.exit()

		#do some cleaning on login_data; set instance variables
		self.__setName(login_data[0].replace('\n', ''))
		self.__setSSN(int(login_data[1].replace('\n', '')))




