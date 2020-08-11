import sys
import json

# CONSTANTS
DIRECT_PATH = './example_tdrive/payroll_data/'
FAVS = 'favorites.json'

def generate_favorites(employee_name):
	"""read a file and load recorded favorites"""
	#open  the favorites  file
	try:
		with open(DIRECT_PATH + FAVS, 'r') as file_favs:
			favs_data = json.load(file_favs)
	except Exception:
		#report if we cant find the file & exit the program
		print("Error: couldn't find file:  <favorites.json>")
		sys.exit()

	#prep the status bar message
	msg = 'Favorites Updating...'

	#check that the names are same and file wasn't empty
	if not favs_data:
		#troubleshoot message for empty favorites file
		msg = "No favorites currently recorded."
		msg += " Please clickt the <Add Favorites> button."

	#close the file
	file_favs.close()

	#if names  match and favorites file is not empty, load the favs
	if msg == 'Favorites Updating...':
		#remove newline chars; exclude the first element (employee name)
		return favs_data
	else: 
		#return error case
		return msg

