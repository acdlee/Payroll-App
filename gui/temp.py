"""Timesheet window GUI"""

#misc  imports
import sys
from numpy import arange
from functools import partial

#pyqt imports
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QMainWindow, QStatusBar, QGridLayout, QLineEdit,
						QLabel, QVBoxLayout, QWidget, QFrame, QComboBox,
						QHBoxLayout, QPushButton, QCompleter)
from  PyQt5.QtCore import QStringListModel


#helper functions
sys.path.append("./helpers/")
from load_favorites import generate_favorites
from generator import generate_list
from generate_sheet import load_sheet, set_sheet

#GLOBAL CONSTANTS FOR IMPORTS
PROJECTS = 'projects.txt'
PAY =  "payitem.txt"
WBS = "wbs.txt"

#GLOBAL CONSTANTS FOR GEOMETRIC PROPERTIES
NOTES_SIZE = 200
PAYITEM_SIZE = 210
WBS_SIZE = 68
PROJECT_NAME_SIZE = 250
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
#MISC GLOBALS
ROWS = 15


class Timesheet(QMainWindow):
	"""Timesheet Window GUI"""

	#window switching signal
	switch_toHome = QtCore.pyqtSignal()

	def __init__(self, currDate,  currWeek, employee_name, user_filter):
		"""Define an instance of the Login GUI"""
		super().__init__()

		#instance variables
		self._date = currDate
		self._currWeek =  currWeek
		self._favs = generate_favorites(employee_name)
		self._sheet = load_sheet(currWeek)
		self._filter = user_filter

		#set the geometry of the welcome window
		self.setWindowTitle('Timesheet')
		self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

		#create an instance of QVBox for the generalLayout
		#and create/set the central widget
		self.generalLayout = QVBoxLayout()
		self._centralWidget = QWidget(self)
		self.setCentralWidget(self._centralWidget)
		self._centralWidget.setLayout(self.generalLayout)

		#create a status bar to communicate app status
		self._createStatusBar()

		#let's create our timesheet layout
		self._addCurrentDate()
		self._createCompleters()
		self._timesheetLayout()
		self._createBtns()

	def _timesheetLayout(self):
		"""Create the timesheet layout and its widgets"""
		#create the timesheet layout
		self._timesheetGrid = QGridLayout()

		#let's create and add widgets to the timesheet layout
		self._createHeaders()
		self._addRows()

		#add the bordered timesheet layout to the generalLayout
		self.generalLayout.addLayout(self._timesheetGrid)

	def _addRows(self, num_rows=ROWS):
		"""Create the rows where the user will insert projects"""
		if not self._sheet:
			#if the sheet is empty
			for row in range(1, num_rows):
				self._addRow(row_num=row)
		else:
			#load the previous sheet
			self._loadSheet()

	def _scrapeSheet(self):
		""""""
		self._sheet = {}	#reset sheet
		for row in range(1, ROWS):
			curr_p = ((self._timesheetGrid.itemAtPosition(row, 1)).widget()).text()
			tmp = []
			for col in range(2, 10):
				entry = ((self._timesheetGrid.itemAtPosition(row, col)).widget()).text()

				if col > 4 and entry != "":
					#flip the ints to strings for Hours columns
					entry = int(entry)

				if curr_p == "":	#if there's no project, assume no info
					col = 9

				tmp.append(entry)

			#check to make sure hours are filled
			if any(isinstance(item, int) for item in tmp[3:]):
				self._sheet[curr_p] = tmp


		if self._sheet != {}:
			set_sheet(self._sheet, self._currWeek)

		#adjust the statusBar
		self.statusBar.clearMessage()
		self.statusBar.repaint()
		self.statusBar.showMessage("Successfully Saved.")

	def _addRow(self, row_num):
		col = -1
		while col < 9:
			col += 1
			if col == 0:
				#clear btn
				widget = QPushButton(str(row_num))
				self._timesheetGrid.addWidget(widget, row_num, col)

			elif col < 4:
				#could be projname, wbs, payitem
				if self._favs != {}:
					#load the favorites project name
					p_name = list(self._favs.keys())[0]
					#grab its items, if they exist
					items = self._favs[p_name]

					#delete the favorite entry
					del self._favs[p_name]

					for i in range(1, 4):
						widget = QLineEdit()
						if i == 1:
							widget.setText(p_name)
							widget.setFixedWidth(PROJECT_NAME_SIZE)
							widget.setDisabled(True)
							self._timesheetGrid.addWidget(widget, row_num, i)
						elif i == 2:
							widget.setText(items[0])
							completer = self._grabCompleter(i)
							widget.setFixedWidth(WBS_SIZE)
							widget.setCompleter(completer)
							self._timesheetGrid.addWidget(widget, row_num, i)
						else:
							widget.setText(items[1])
							widget.setFixedWidth(PAYITEM_SIZE)
							completer = self._grabCompleter(i)
							widget.setCompleter(completer)
							self._timesheetGrid.addWidget(widget, row_num, i)	

					col = 3
					#add the project name, wbs, and pay item to the grid

				else:
					# print("In self favs else for: (" + str(row_num) + ", " + str(col) + ")")
					completer = self._grabCompleter(col)
					widget = QLineEdit()
					widget.setCompleter(completer)
					self._timesheetGrid.addWidget(widget, row_num, col)

			else:
				widget = QLineEdit()
				if col == 4:
					#notes col
					widget.setPlaceholderText("Notes")
					widget.setFixedWidth(NOTES_SIZE)
				else:
					#hours col
					widget.setPlaceholderText("Hour(s)")
					widget.setValidator(QtGui.QIntValidator())
				
				self._timesheetGrid.addWidget(widget, row_num, col)

	def _loadSheet(self):
		'''A user is revisiting a saved sheet;
		load the shet for use.'''
		for row_num in range(1, ROWS):
			if self._sheet != {}:
				self._addSheet(row_num)
			else:
				self._addRow(row_num)

	def _addSheet(self, row_num):
		'''load the saved timesheet onto the current timehseet.
		Note: we add one row at a time'''
		if self._sheet != {}:	#empty sheet check

			#example entry in the _sheet dictionary:
			#"VIS:18_021 Ft Sam B2264": ["03.01.610", "OH Labor-Employees", 3, "", 2, 2, 3]

			#let's grab the project name and its items, then delete the entry
			p_name = list(self._sheet.keys())[0]
			items = self._sheet[p_name]
			del self._sheet[p_name]

			#check if the project we're about to add is in favorites.
			#if it is, delete the favorite entry
			if p_name in self._favs:
				del self._favs[p_name]

			#add the row number button
			row_btn = QPushButton(str(row_num))
			self._timesheetGrid.addWidget(row_btn, row_num, 0)

			#add the project name to the current timesheet; set column properties
			p_nameWidget = QLineEdit()
			p_nameWidget.setText(p_name)
			p_nameWidget.setFixedWidth(PROJECT_NAME_SIZE)
			p_nameWidget.setDisabled(True)
			self._timesheetGrid.addWidget(p_nameWidget, row_num, 1)

			col = 2

			#now let's add items
			for item in items:
				widget = QLineEdit()
				if col == 2:
					#WBS col
					widget.setText(item)
					completer = self._grabCompleter(col)
					widget.setFixedWidth(WBS_SIZE)
					widget.setCompleter(completer)
					self._timesheetGrid.addWidget(widget, row_num, col)
				elif col == 3:
					#pay item col
					widget.setText(item)
					completer = self._grabCompleter(col)
					widget.setFixedWidth(PAYITEM_SIZE)
					widget.setCompleter(completer)
					self._timesheetGrid.addWidget(widget, row_num, col)
				elif col == 4:
					if item != '':
						widget.setText(item)
					else:
						widget.setPlaceholderText("Notes")
					widget.setFixedWidth(NOTES_SIZE)
					self._timesheetGrid.addWidget(widget, row_num, col)
				else:
					#hours col
					if item == '':
						widget.setPlaceholderText("Hour(s)")
					else:
						widget.setText(str(item))
					widget.setValidator(QtGui.QIntValidator())
					self._timesheetGrid.addWidget(widget, row_num, col)

				#increment the col number
				col += 1
























	##########################
	"""Mutators & Accessors"""
	##########################


	####################
	"""Widget Methods"""
	####################

	def _createHeaders(self):
		"""Add the headers to the timesheet grid layout"""
		#create a dictionary with label: position
		labels = {
			"Row": (0, 0),
			"Projects": (0, 1),
			"WBS": (0, 2),
			"Pay Item": (0, 3),
			"Notes": (0, 4),
			"Mon": (0, 5),
			"Tues": (0, 6),
			"Wed": (0, 7),
			"Thur": (0, 8),
			"Fri": (0, 9)
		}

		#style options
		style = "background-color: rgb(230, 249, 255);"
		style += "border-style: solid;"
		style += "font: bold;"
		style += "border-color: rgb(179, 209, 255);"
		style += "border-width: 1px;" 

		#add each <labelTxt: pos> with style <style> as
		#a widget to the _timesheetGrid. 
		for labelTxt, pos in labels.items():
			tmp_label = QLabel(labelTxt)
			tmp_label.setFixedHeight(20)	#limit the height of each label
			tmp_label.setStyleSheet(style)
			self._timesheetGrid.addWidget(tmp_label, pos[0], pos[1])


	def _createStatusBar(self):
		"""Create a status bar for user communication"""
		#create an instance of QStatusBar
		self.statusBar = QStatusBar()
		#set the text for the statusBar
		msg = "Fill Out Your Timesheet For: "
		msg += self._currWeek
		self.statusBar.showMessage(msg)
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

	def _createCompleters(self):
		"""Create the auto-complete functionality for 
		the Add QLineEdit box"""

		#load in the lists
		project_lst = generate_list(PROJECTS)
		pay_lst  = generate_list(PAY)
		wbs_lst = generate_list(WBS)

		#adjust pay_lst based on user's filter
		pay_lst = [item for item in pay_lst 
					if (item.lower().find(self._filter) == -1)]

		#create the dictionaries
		modelA = QStringListModel()
		modelA.setStringList(project_lst)

		modelB = QStringListModel()
		modelB.setStringList(pay_lst)

		modelC = QStringListModel()
		modelC.setStringList(wbs_lst)


		#create the auto-completer widget & set its dictionary
		self.completerProj = QCompleter()
		self.completerProj.setModel(modelA)

		self.completerPay = QCompleter()
		self.completerPay.setModel(modelB)

		self.completerWBS = QCompleter()
		self.completerWBS.setModel(modelC)

	def _createBtns(self):
		""""""
		#create a layout for the buttons
		layout = QHBoxLayout()

		#create an instance for the back button
		self.backBtn =  QPushButton()
		#add the backbtns text
		self.backBtn.setText('Back')
		#set the signal
		self.backBtn.clicked.connect(self._toHome)
		#set the width of the button
		self.backBtn.setFixedWidth(150)
		#add the button the the  layout
		layout.addWidget(self.backBtn)

		#create an instance of QPushButton
		self.saveBtn = QPushButton()
		#set some text for the saveBtn
		self.saveBtn.setText('Save')
		#est the width for the saveBtn
		self.saveBtn.setFixedWidth(150)
		#sset the sitgnal for the  button
		self.saveBtn.clicked.connect(self._scrapeSheet)
		#add the widget
		layout.addWidget(self.saveBtn)

		#nest  the layout
		self.generalLayout.addLayout(layout)


	##################
	"""Slot Methods"""
	##################

	def _toHome(self):
		"""Switch back to the home screen window GUI"""
		self.switch_toHome.emit()



	#######################
	"""Utility functions"""
	#######################

	def _grabCompleter(self, col):
		if col == 1:
			return self.completerProj
		elif col == 2:
			return self.completerWBS
		else:
			return self.completerPay
