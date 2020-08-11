"""Submit Window GUI"""


#misc imports
import sys


#PyQt imports
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
						QPushButton, QFormLayout, QLabel, QRadioButton,
						QStatusBar, QCheckBox)


#helper functs import
sys.path.append('./helpers')
from generate_errors import check_sheet
sys.path.append("./submitting")
from submit_sheets import save_sheets

class Submit(QMainWindow):
	"""Submit Window GUI"""

	#window switching signal
	switch_toHome = QtCore.pyqtSignal()

	def __init__(self, currWeek, prevWeek, employee_name):
		"""Define an instance of the Submit GUI"""
		super().__init__()

		#set the geometry of the welcome window
		self.setWindowTitle('Timesheet - Submit Window')
		self.setFixedSize(600, 600)

		#instance vars
		self._submitable = [False, False, False]
		self.currWeek = currWeek
		self.prevWeek = prevWeek
		self.employee_name = employee_name

		#create an instance of QVBox for the generalLayout
		#and create/set the central widget
		self.generalLayout = QVBoxLayout()
		self.generalLayout.setAlignment(QtCore.Qt.AlignCenter)	#widgets centered 
		self._centralWidget = QWidget(self)
		self.setCentralWidget(self._centralWidget)
		self._centralWidget.setLayout(self.generalLayout)

		#let's generate the error listings
		self.errs_lst = check_sheet(self.currWeek, self.prevWeek)

		#create a status bar to communicate app status
		self._createStatusBar()

		#let's create some widgets
		self._checkHours()
		self._displayText()
		self._createBtns()





	##########################
	"""Mutators & Accessors"""
	##########################


	####################
	"""Widget Methods"""
	####################

	def _checkHours(self):
		self._hrsBtn = QCheckBox()
		txt = "Confirm You Worked " + str(self.errs_lst[2])
		txt += " Hours."
		self._hrsBtn.setText(txt)
		self._hrsBtn.setStyleSheet("font: 20px;")
		

		#set signal
		self._hrsBtn.toggled.connect(self._checkHrsBtn)

		self.generalLayout.addWidget(self._hrsBtn)

	def _createStatusBar(self):
		"""Create a status bar for user communication"""
		#create an instance of QStatusBar
		self.statusBar = QStatusBar()
		#set the text for the statusBar
		self.statusBar.showMessage("Verifying Timesheets...")
		#set the  statusBar
		self.setStatusBar(self.statusBar)

	def _displayText(self):
		self._weekError('Current', self.errs_lst[0], 0)
		self._weekError('Previous', self.errs_lst[1], 1)


	def _createBtns(self):
		"""creates the button to return to the home window"""
		layout = QHBoxLayout()
		#create an instance of QPushButton
		self._backBtn = QPushButton()
		#set some physical properties
		self._backBtn.setFixedWidth(150)
		#set the text of the button
		self._backBtn.setText("Back")
		#set the signal
		self._backBtn.clicked.connect(self.switch_home)

		#create an instance of QPushButton
		self._subBtn = QPushButton()
		#set some physical properties
		self._subBtn.setFixedWidth(150)
		#set the text of the button
		self._subBtn.setText('Submit')
		#set the signal
		self._subBtn.clicked.connect(self.submit_timesheets)

		#add widgets to layout
		layout.addWidget(self._backBtn)
		layout.addWidget(self._subBtn)

		if self._submitable[0] and self._submitable[1]:
			self.statusBar.repaint()
			self.statusBar.showMessage('Ready to submit.')

		#add the layout to generalLayout
		self.generalLayout.addLayout(layout)


	##################
	"""Slot Methods"""
	##################

	def _checkHrsBtn(self):
		if self._hrsBtn.isChecked():
			self._submitable[2] = True
		else:
			self._submitable[2] = False

	def switch_home(self):
		"""switch  back to the home window  gui"""
		self.switch_toHome.emit()

	def submit_timesheets(self):
		if self._submitable == [True, True, True]:
			#let's call a helper function to format and 
			#save the raw data (the timesheets)
			save_sheets(self.currWeek, self.prevWeek, self.employee_name)

			self.statusBar.repaint()
			self.statusBar.showMessage('Submitted Timesheets.')


	#######################
	"""Utility functions"""
	#######################

	def _weekError(self, week, errs_lst, i):
		layout = QVBoxLayout()

		#check if there's no errors
		if not errs_lst:
			label = QLabel(week + ' is ready to submit.')
			layout.addWidget(label)
			self._submitable[i] = True
		else:
			label = QLabel("<h1>" + week + " Week:" + "</h1>")
			layout.addWidget(label)
			for error in errs_lst:
				tmp = error.split('$')
				txt = ''
				for i in range(len(tmp)):
					if i == 0:
						#proj name
						txt += "<h3>" + tmp[i] + "</h3>"
					else:
						txt += "<h6>" + tmp[i] + "</h6>"
				label = QLabel(txt)
				layout.addWidget(label)

				#adjust status bar
				self.statusBar.repaint()
				self.statusBar.showMessage('Please complete your timesheet.')


		#add layout
		self.generalLayout.addLayout(layout)




