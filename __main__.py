"""Payroll App designed to modernize the payroll process
using Python and PyQt5"""

#Author & version number
__author__ = 'Christopher Lee'
__version__ = '0.2'



#foundation imports
import sys
from PyQt5.QtWidgets import QApplication

#import the controller
from controller import Controller

#Client Code

def main():
	"""Main function"""
	#Create an instance of QApplication; no cmd line args => [] param
	payroll = QApplication([])

	#create an instance of Control & show the app's login GUI
	cntrl = Controller()
	cntrl.show_login()

	#Main loop for the app
	sys.exit(payroll.exec())

#Pythonic formalities
if __name__ == '__main__':
	main()
