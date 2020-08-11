"""In this file, we'll handle generating the
lists of ComboBox options for the payroll app."""


#import sys for error case exiting
import sys

#directory for the data
TDRIVE_DIRECT = "./example_tdrive/payroll_data/"

def generate_list(filename):
	
	#open the employee names file
	try:
		file  = open(TDRIVE_DIRECT + filename, 'r')
	except Exception:

		#print the error message to the console
		print("Error: couldn't open file <" + filename + ">")
		sys.exit()

	#list of employees
	employee_list = []

	#add each name to thee employee name list; remove '\n'
	for name in file.readlines():
		employee_list.append(name[:-1])

	#close the file
	file.close()

	return employee_list
