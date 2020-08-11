"""Home Window GUI"""


#misc imports
import sys


#PyQt imports
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QComboBox,
 				QLabel, QStatusBar, QVBoxLayout, QHBoxLayout, QWidget)


#import helper function for dates
sys.path.append('./helpers')
from generate_errors import check_sheet
from handle_dates import initDate, setWeek


class Home(QMainWindow):
	"""Home Window GUI"""

	#window switching signal
	switch_toEditFavs = QtCore.pyqtSignal()
	switch_toSubSheets = QtCore.pyqtSignal()
	switch_toSheets = QtCore.pyqtSignal()

	def __init__(self):
		"""Define an instance of the Login GUI"""
		super().__init__()

		#instance variable for date & weeks
		self._selectedWeek = ""		#selected week
		self._prevWeek = ""			#holds the previous week
		self._date = initDate()		#holds the current date
		self._weeks = setWeek()		#holds [prev week, curr week, next week] dates

		#set the geometry of the welcome window
		self.setWindowTitle('Timesheet - Home Window')
		self.setFixedSize(600, 600)

		#create an instance of QVBox for the generalLayout
		#and create/set the central widget
		self.generalLayout = QVBoxLayout()
		self._centralWidget = QWidget(self)
		self.setCentralWidget(self._centralWidget)
		self._centralWidget.setLayout(self.generalLayout)

		#create a bar to communicate app status
		self._createStatusBar()

		#let's create some widgets and nested layout
		self._addCurrentDate()
		self._fillTop()
		self._fillBot()

	##########################
	"""Mutators & Accessors"""
	##########################

	def _getDay(self):
		return self._date

	def _setSelectedWeek(self, week):
		self._selectedWeek =  week

	def _getCurrWeek(self):
		return self._selectedWeek

	def _getPrevWeek(self):
		return self._prevWeek

	def _setPrevWeek(self, week):
		self._prevWeek = week

	####################
	"""Widget Methods"""
	####################

	def _createStatusBar(self):
		"""Create a status bar for user communication"""
		#create an instance of QStatusBar
		self.statusBar = QStatusBar()
		#set the text for the statusBar
		self.statusBar.showMessage("Click a Button or Change  the Date")
		#set the  statusBar
		self.setStatusBar(self.statusBar)

	def _addCurrentDate(self):
		"""Set a widget to display the current date"""
		#create an instance of QLabel
		self._dateLabel = QLabel()
		#set the max size of the label
		self._dateLabel.setFixedSize(400, 20)
		#set the text of the label to the date
		self._dateLabel.setText('Current Date: ' + self._date)
		#adjust the font of the text
		self._dateLabel.setStyleSheet("font-size:18px")
		#add the widget to the generalLayout
		self.generalLayout.addWidget(self._dateLabel)

	def _fillTop(self):
		"""Create the widgets and nested layout for the top
		region of generalLayout"""
		#create our two layouts
		outer_layout = QHBoxLayout()
		inner_layout = QVBoxLayout()

		#create the widgets through helper functions
		self._createCurrWeekBtn()
		self._createTimesheetBtn()
		self._createChangeWeekBox()

		#add widgets to desired layouts
		inner_layout.addWidget(self._currWeekBtn)
		inner_layout.addWidget(self._changeWeekBox)
		outer_layout.addWidget(self._timesheetBtn)

		#nest layouts
		outer_layout.addLayout(inner_layout)
		self.generalLayout.addLayout(outer_layout)

	def _createTimesheetBtn(self):
		"""Creates the widget for editing a timesheet for
		a particular week"""
		#create an instance of QPushButton
		self._timesheetBtn = QPushButton()
		#set the size of the _timesheetBtn widget
		self._timesheetBtn.setFixedSize(150, 150)
		#set the text of the _timesheetBtn widget
		self._timesheetBtn.setText('Edit Timesheet')
		#set the signal  to switch to the Timesheet GUI
		self._timesheetBtn.clicked.connect(self.switch_toSheets)

	def _createCurrWeekBtn(self):
		"""Creates the widget for displaying the current week
		of the timesheet"""
		#createe an instance of QPushButton
		self._currWeekBtn = QPushButton()
		#set the text of the button
		txt = 'Current Week: ' + list(self._weeks.keys())[2]
		txt += ' - ' +  list(self._weeks.values())[2]
		self._currWeekBtn.setText(txt)
		#set the style of the button
		self._currWeekBtn.setStyleSheet("text-align:left")

	def _createChangeWeekBox(self):
		"""Creates the widget for changing the current
		week of the timesheet"""
		#create an instance of QComboBox
		self._changeWeekBox = QComboBox()
		#set the default text of the QComboBox
		self._changeWeekBox.setPlaceholderText('Change Week')

		#generate the box text
		self._createItems()
		#let's add some items to the box
		self._changeWeekBox.addItems(self._formatted_lst)

		#create the signal for the box
		self._changeWeekBox.currentTextChanged.connect(self._changeWeekSlot)


	def _fillBot(self):
		"""Create the widgets and nested layout
		for the bottom region of generalLayout"""
		#create an instance of QHBoxLayout
		nested_layout = QHBoxLayout()

		#create the widgets through helper functions
		self._createEditFavsBtn()
		self._createSubmitBtn()

		#add the widgets to the nested layout
		nested_layout.addWidget(self._editFavsBtn)
		nested_layout.addWidget(self._submitBtn)

		#add the nested layout the the generalLayout
		self.generalLayout.addLayout(nested_layout)

	def _createEditFavsBtn(self):
		"""Creates the widget for switching to the 
		EditFavorites GUI"""
		#create an instance of QPushButton
		self._editFavsBtn =  QPushButton()
		#set the text of the button
		self._editFavsBtn.setText('Edit Favorites')
		#set the size of the button
		self._editFavsBtn.setFixedSize(280, 150)
		#create the signal for the button
		self._editFavsBtn.clicked.connect(self._editFavsSlot)

	def _createSubmitBtn(self):
		"""Creates the widget for switching to the 
		SubmitTimesheets GUI"""
		#create an instance of QPushButton
		self._submitBtn =  QPushButton()
		#set the text of the button
		txt = 'Submit Timesheets For:\n'
		txt += self._formatted_lst[1] + ' AND \n' + self._formatted_lst[2]
		self._submitBtn.setText(txt)
		#set the size of the button
		self._submitBtn.setFixedSize(280, 150)
		#create the signal for the button
		self._submitBtn.clicked.connect(self._submitSlot)

	##################
	"""Slot Methods"""
	##################

	def _changeWeekSlot(self):
		"""Changes the current week to the selected week"""
		#change the current week text if valid input
		if self._changeWeekBox.currentText() != 'Change Week':
			#update text
			txt =  'Selected Week: ' + self._changeWeekBox.currentText()
			self._currWeekBtn.setText(txt)

			#set the selected week
			self._setSelectedWeek(self._changeWeekBox.currentText())

			#update the current week button
			self._currWeekBtn.update()
			#reset the default text on the combo box & update the box
			self._changeWeekBox.clear()
			self._changeWeekBox.addItems(self._formatted_lst)



	def _editFavsSlot(self):
		"""Switches the window to the EditFavorites GUI"""
		self.switch_toEditFavs.emit()

	def _submitSlot(self):
		"""Switches the window to the Submit GUI"""

		#let's check for the existence of the two time sheets before
		#we allow them to switch screens. 
		#check for sheets returns true if the user has filled out sheets
		#for the two submital weeks
		if self._checkForSheets():
			self.switch_toSubSheets.emit()
		else:
			#msg to status bar
			msg = "Fill out your sheets for BOTH weeks."
			self.statusBar.showMessage(msg)

	def _timesheetSlot(self):
		"""Switches the window to the Timesheet GUI"""
		self.switch_toSheets.emit()

	#######################
	"""Utility functions"""
	#######################

	def _checkForSheets(self):
		#return false if the user hasnt filled out their timesheets
		#for the submital weeks
		return check_sheet(self._selectedWeek, self._prevWeek, checker=True)

	def _createItems(self):
		"""Create the contents of the QComboBox _changeWeekBox"""
		#create a list of formatted strings from our _weeks dict
		formatted_lst = []
		for start_date, end_date in self._weeks.items():
			txt = start_date + " - " + end_date	#format the dates
			formatted_lst.append(txt)			#add the formatted dates

		self._formatted_lst = formatted_lst

		#also set the _selectedWeek to curr week & previous week
		self._setSelectedWeek(formatted_lst[2])
		self._setPrevWeek(formatted_lst[1])

















