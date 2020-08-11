"""This file orchestrates the control flow of
the app through different PyQt windows"""

#sys import
import sys

#GUI file imports
sys.path.append('./gui/')
from login_gui import Login
from home_gui import Home
from favs_edit import EditFavorites
from temp import Timesheet
from submit_gui import  Submit

class Controller():

	"""Control Flow of Payroll App"""
	def __init__(self):
		#instance variables for window switching
		self.employee_name = ''
		self.prev_window = ''
		self.currWeek = ''
		self.prevWeek = ''
		self.filter = ''

	def show_login(self):
		"""Create and show the Login GUI"""
		#create an instance of the Login GUI
		self.login = Login()
		#set the signal for switching the the Favorites Selection GUI window
		self.login.switch_window.connect(self.show_home)
		#set the previous window
		self.prev_window = 'login'

		#show the Login GUI
		self.login.show()

	def show_home(self):
		"""Show the home screen for the application"""
		#grab the employee name
		self.employee_name = self.login._getName()
		self.filter = self.login._getFilter()

		#create an instance of the home screen
		self.home = Home()
		#set signals for switching screens
		self.home.switch_toEditFavs.connect(self.show_edit_favs)
		self.home.switch_toSheets.connect(self.show_timesheets)
		self.home.switch_toSubSheets.connect(self.show_submit)

		#close the previous window
		self.close_previous()
		#set the previous window
		self.prev_window = 'home'

		#save some instance variables
		self.currWeek = self.home._getCurrWeek()
		self.prevWeek = self.home._getPrevWeek()

		#show the Home GUI
		self.home.show()

	def show_edit_favs(self):
		"""Show the Edit Favorites screen for the application"""
		#create an instance of the EditFavorites Gui
		self.edit_favs = EditFavorites(self.filter)
		#set the signal to switch to the Home GUI
		self.edit_favs.switch_window.connect(self.show_home)
		#close the previous window
		self.close_previous()
		#set the previous window
		self.prev_window = 'edit favs'

		#show the EditFavorites GUI
		self.edit_favs.show()

	def show_timesheets(self):
		"""Show the Timesheeets screen for the application"""
		#create an instance of Timesheet GUI
		self.currWeek = self.home._getCurrWeek()
		self.timesheet = Timesheet(self.home._getDay(), self.currWeek,
									self.employee_name, self.filter)
		#set the signal to switch to Home GUI
		self.timesheet.switch_toHome.connect(self.show_home)
		#close the previous window
		self.close_previous()
		#set the previous window
		self.prev_window = 'timesheet'

		#show the timesheet gui
		self.timesheet.show()


	def show_submit(self):
		"""Show the Submit Timesheets screen for the application"""
		#create an instance of the submit gui
		self.submit = Submit(self.currWeek, self.prevWeek, self.employee_name)
		#set the signal to switch back to the home gui
		self.submit.switch_toHome.connect(self.show_home)
		#close  the  previous window
		self.close_previous()
		#set  the  previous window
		self.prev_window = 'sub'

		#show the submit  gui
		self.submit.show()


	def close_previous(self):
		"""Helper function to close  the  previous GUI window"""
		if self.prev_window == 'login':
			self.login.close()
		elif self.prev_window ==  'edit favs': 
			self.edit_favs.close()
		elif self.prev_window == 'home':
			self.home.close()
		elif self.prev_window == 'timesheet':
			self.timesheet.close()
		elif self.prev_window == 'sub':
			self.submit.close()





