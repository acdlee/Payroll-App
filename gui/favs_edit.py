"""Edit Favorites GUI"""

# misc imports
import sys
import copy
import json

#PyQt imports
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QComboBox,
					QPushButton, QLineEdit, QStatusBar, QCompleter, QHBoxLayout)
from  PyQt5.QtCore import QStringListModel

#helper function import
sys.path.append('./helpers/')
from generator import generate_list

# GLOBAL CONSTANTS
DIRECT_PATH = './example_tdrive/payroll_data/'
PROJECTS = 'projects.txt'
FAVS = 'favorites.json'
PAY =  "payitem.txt"
WBS = "wbs.txt"
LIMIT_FAVS = 10	#a user can have a maximum of 10 favorites


class EditFavorites(QMainWindow):
	#signal for switching screens
	switch_window = QtCore.pyqtSignal()

	"""Favorites Menu Screen (GUI)"""
	def __init__(self, empl_filter):
		"""View initializer"""
		super().__init__()

		#set some window properties
		self.setWindowTitle('Timesheet - Favorites Menu')
		self.setFixedSize(800, 600)

		#set an instance variable for a dict of favorites,
		#Pay Item filter, and projects_lst
		self.favorite_projects = {}
		self.project_lst = []
		self._filter = empl_filter

		#set the central widget and the general layout
		self.generalLayout = QVBoxLayout()
		self._centralWidget = QWidget(self)
		self.setCentralWidget(self._centralWidget)
		self._centralWidget.setLayout(self.generalLayout)

		#create a status bar to communicate app status
		self._createStatusBar()

		#load in the favorites
		self._loadFavorites()

		#let's add some widgets
		self._displayFavorites()
		self._createFunctionality()
		self._createBtns()

		#let's create signals for our widgets
		self._createSlots()

		self.statusBar.showMessage("Add, Remove, or Clear Projects From Favorites.")


	##########################
	"""Mutators & Accessors"""
	##########################

	def _getFavs(self):
		"""getter (accessor) method for favorite_projects dict"""
		return self.favorite_projects

	def _setFavs(self, favs_dict):
		"""setter (mutator) for  favorite_projects dict"""
		#check for an empty dict before setting
		if not self.favorite_projects:
			self.favorite_projects = favs_dict
		else:
			#if there are already items in the dict, just add to the dict
			for project, items in favs_dict.items():
				#check if the proj name is in the key list of favorite_projects
				if project not in self.favorite_projects.keys():
					self.favorite_projects[project] = items


	#################################
	"""Class Methods (for widgets)"""
	#################################	
	
	def _createStatusBar(self):
		"""Create a status bar for user communication"""
		#create an instance of QStatusBar
		self.statusBar = QStatusBar()
		#set the text for the statusBar
		self.statusBar.showMessage("Click a Button")
		#set the  statusBar
		self.setStatusBar(self.statusBar)

	def _createBtns(self):
		"""Creates the back button for page navigation"""
		#create a nested layout for alignment
		layout = QHBoxLayout()
		#create an instance for the back btn
		self.backBtn =  QPushButton()
		#set the text, width, and slot
		self.backBtn.setText('Back')
		self.backBtn.setFixedWidth(200)
		self.backBtn.clicked.connect(self.switch)

		#add the widget to the nested layout
		layout.addWidget(self.backBtn)
		#nest the layout
		self.generalLayout.addLayout(layout)

	def _createFunctionality(self):
		"""Create the buttons and text boxes for window functionality"""
		#create an instance of QVBoxLayout for our widgets
		layout = QVBoxLayout()
		#create two instances for hboxlayout
		h_layout1 = QHBoxLayout()
		h_layout2 = QHBoxLayout()

		#create instances of QLineEdit
		self.addProjectBox = QLineEdit()
		self.wbsBox = QLineEdit()
		self.payBox = QLineEdit()
		self.removeProjectBox = QLineEdit()

		#let's add some default text to the text boxes
		self.addProjectBox.setPlaceholderText('Input Project Name (Required) (Case Sensitive)')
		self.wbsBox.setPlaceholderText('Input WBS (Optional)')
		self.payBox.setPlaceholderText('Input Pay Item (Optional)')
		self.removeProjectBox.setPlaceholderText('Input Project Name (Case Sensitive)')

		#set the size of the addProjectBox and payBox
		self.addProjectBox.setFixedWidth(300)
		self.payBox.setFixedWidth(200)

		#let's create the auto-complete functionality for the text boxes
		self._completeAdd()
		self._completeRemove()
		self._createCompleters()

		#create instances of QPushButton
		self.clearFavsBtn = QPushButton()
		self.addBtn = QPushButton()
		self.removeBtn = QPushButton()

		#let's add some text to the button
		self.clearFavsBtn.setText('Clear Favorites')
		self.addBtn.setText('Add Favorite')
		self.removeBtn.setText('Remove Favorite')

		#let's add our widgets to our layouts
		h_layout1.addWidget(self.addProjectBox)
		h_layout1.addWidget(self.wbsBox)
		h_layout1.addWidget(self.payBox)
		h_layout1.addWidget(self.addBtn)

		h_layout2.addWidget(self.removeProjectBox)
		h_layout2.addWidget(self.removeBtn)

		#nest layouts
		layout.addLayout(h_layout1)
		layout.addLayout(h_layout2)

		#let's add layout to our generalLayout
		self.generalLayout.addLayout(layout)

	def _completeAdd(self):
		"""Create the auto-complete functionality for 
		the Add QLineEdit box"""

		#load in the list of projects
		self.project_lst = generate_list(PROJECTS)

		#create the dictionary
		model = QStringListModel()
		model.setStringList(self.project_lst)

		#create the auto-completer widget & set its dictionary
		completer = QCompleter()
		completer.setModel(model)

		#add the auto-completer functionality to our addProjectBox
		self.addProjectBox.setCompleter(completer)

	def _completeRemove(self):
		"""Create the auto-complete functionality for
		the Remove QLineEdit box"""

		#create the dictionary
		model = QStringListModel()
		model.setStringList(self.favorite_projects.keys())

		#create the auto-completer widget & set its dictionary
		completer = QCompleter()
		completer.setModel(model)

		#add the auto-completer functionality to our addProjectBox
		self.removeProjectBox.setCompleter(completer)

	def _createCompleters(self):
		"""Create the auto-complete functionality for 
		the Add QLineEdit box"""

		#load in the lists
		pay_lst  = generate_list(PAY)
		wbs_lst = generate_list(WBS)

		#adjust pay_lst based on user's filter
		pay_lst = [item for item in pay_lst 
					if (item.lower().find(self._filter) == -1)]

		#create the dictionaries
		modelB = QStringListModel()
		modelB.setStringList(pay_lst)

		modelC = QStringListModel()
		modelC.setStringList(wbs_lst)

		#create the auto-completer widget & set its dictionary
		self.completerPay = QCompleter()
		self.completerPay.setModel(modelB)

		self.completerWBS = QCompleter()
		self.completerWBS.setModel(modelC)

		#add the completers to the QLineEdits
		self.payBox.setCompleter(self.completerPay)
		self.wbsBox.setCompleter(self.completerWBS)


	####################
	"""Slot Functions"""
	####################

	def switch(self):
		"""Slot function for switching windows"""
		self.switch_window.emit()

	def _createSlots(self):
		"""Create the signals for the widgets"""
		#create signals for the add and remove buttons
		self.addBtn.clicked.connect(self._addBtnSlot)
		self.removeBtn.clicked.connect(self._removeBtnSlot)

		#create a singal for the clearFavsBtn
		self.clearFavsBtn.clicked.connect(self._clearFavsSlot)

	def _clearFavsSlot(self):
		"""Clear all projects from the favorite_projects"""
		#make a deep copy of the favorite projects (for the error case)
		tmp = copy.deepcopy(self.favorite_projects)
		self.favorite_projects = {}
		val = self._updateFavs()	#update display & system file of favorites

		#if the file didn't open, don't change the statusBar text
		if val:	#val is 1 for success; 0 for failure
			self._updateBar("Favorite Projects List Successfully Cleared.")
		else:
			#undo changes to favorite_projects & troubleshoot
			self._updateBar("Error Clearing Favorites")
			self.favorite_projects = tmp

	def _addBtnSlot(self):
		"""Slot for adding a project to favorites"""
		#grab the current text in the addProjectBox
		txt = self.addProjectBox.text()
		#checks: there's text in the box; the text is a valid project
		if txt != '' and txt in self.project_lst:
			#grab wbs and pay item text
			wbs_txt = self.wbsBox.text()
			pay_txt = self.payBox.text()

			#add the valid project to our favorites & reset text boxes
			self.addProjectBox.clear()
			self.wbsBox.clear()
			self.payBox.clear()
			self._addFav(project=txt, items=[wbs_txt, pay_txt])
		else:
			#troubleshoot
			self._updateBar("Please Select a Valid Project Name and Click <Add Favorite>.")

	def _removeBtnSlot(self):
		"""Slot function for removing a project from favorites"""
		#grab the current text in the removeProjectBox
		txt = self.removeProjectBox.text()
		#checks: there's text in the box; the text is in favorite projects
		if txt != '' and txt in self.favorite_projects.keys():
			#add the valid project to our favorites & reset text box
			self.removeProjectBox.clear()
			self._removeFav(project=txt)
		else:
			#troubleshoot
			msg = "Please Select a Valid Project Name and Click <Remove Favorite>."
			self._updateBar(msg)


	#######################
	"""Utility functions"""
	#######################

	def _updateBar(self, msg):
		""""""
		self.statusBar.clearMessage()
		self.statusBar.showMessage(msg)
		self.statusBar.repaint()

	def _addFav(self, project, items):
		"""Utility function for adding projects to favorites"""
		#check for duplicate projects and max number (10) of user favorites
		if project in self.favorite_projects.keys(): 
			msg = "Error: Project <" + project + "> already in Favorites."
			self._updateBar(msg)
		elif not len(self.favorite_projects) < LIMIT_FAVS:
			msg = "Error: Trying to Exceed 10 Favorite Projects Limit."
			msg += " Remove a Favorite Before Adding Another."
			self._updateBar(msg)
		else:
			#add the project to our instance dict and update the project on file
			self.favorite_projects[project] = items
			val = self._updateFavs()
			#if the file didn't open, don't change the statusBar text
			if val:	#val is 1 for success; 0 for failure
				msg = "Successfully added <" + project + "> to Favorites."
				self._updateBar(msg)
			else:
				#undo the failed add
				msg = "Error: Failed to add project: <" + project + "> to Favorites."
				self._updateBar(msg)
				del self.favorite_projects[project]

	def _removeFav(self, project):
		"""Utility function for removing projects from favorites"""
		#remove only if the project is in favorite_projects
		if project in self.favorite_projects.keys():
			#save incase of error
			tmp_lst = copy.deepcopy(self.favorite_projects[project])
			#delete the project and its items
			del self.favorite_projects[project]

			val = self._updateFavs()
			#if the file didn't open, don't change the statusBar text
			if val:	#val is 1 for success; 0 for failure
				msg = "Successfully removed <" + project + "> from Favorites."
				self._updateBar(msg)
			else:
				#undo the failed remove
				msg = "Error Removing Project: <" + project + ">."
				self._updateBar(msg)
				self.favorite_projects[project] = tmp_lst

	def _loadFavorites(self):
		"""read a file and load recorded favorites"""
		#open  the favorites  file
		try:
			with open(DIRECT_PATH + FAVS, 'r') as file_favs:
				favsDict = json.load(file_favs)

		except Exception as e:
			#report if we cant find the file & exit the program
			print("Error: couldn't find file:  <favorites.json>")
			sys.exit()

		#prep the status bar message
		msg = 'Favorites Updating...'

		#check that the dict isn't empty
		if not favsDict:
			#troubleshoot message for empty favorites file
			msg = "No favorites currently recorded."
			msg += " Please clickt the <Add Favorites> button."

		#show the appropraite message on the status bar
		self._updateBar(msg)

		#close the file
		file_favs.close()

		#if names  match and favorites file is not empty, load the favs
		if msg == 'Favorites Updating...':
			self._setFavs(favsDict)	#call the mutator for the favorite dict
			self._updateBar(msg)
			msg = "Favorites Successfully Loaded."

	def _updateFavs(self):
		"""Write the newly added project to our favorites text file"""
		#open the file
		try:
			with open(DIRECT_PATH + FAVS, 'w') as favs_file:
				#update the projects
				json.dump(self.favorite_projects, favs_file)

				#update the display for auto-complete remove and 
				#for the QCbox that lists favorites
				self._updateDisplay()
				self._completeRemove()

				#close the file
				favs_file.close()

		except Exception:
			#troubleshoot if we couldn't open the file
			msg = "Error: Could not locate file: <" + FAVS + ">"
			self._updateBar(msg)

			#since the file wasn't found, return failure (0)
			return 0
		
		#return success
		return 1

	def _displayFavorites(self):
		"""Create a display for the currently listed favorites"""
		#create a nested layout for centering
		layout = QHBoxLayout()
		#create an instance of QComboBox that displays the favorited project names
		self.fav_box = QComboBox()
		self.fav_box.setMaxVisibleItems(5)
		self.fav_box.setPlaceholderText('Scroll to  view favorites.')
		self.fav_box.setFixedWidth(400)

		#call _updateDisplay() to add the contents of 
		#the favorites dict to the display
		self._updateDisplay(init=True)

		#add the widget to the generalLayout & nest the layout
		layout.addWidget(self.fav_box)
		self.generalLayout.addLayout(layout)


	def _updateDisplay(self, init=False):
		"""Update the text of the Favorites QComboBox"""
		#check if we're initializing
		if init:
			#if we're initializing, nothing to remove
			self.fav_box.addItems(self.favorite_projects.keys())
		else:
			#else, reset the favs list completely
			while self.fav_box.count(): #count returns 0 when QCbox is empty
				#remove all the items in the list
				self.fav_box.removeItem(0)

			#set the new list of project names
			self.fav_box.addItems(self.favorite_projects.keys())

