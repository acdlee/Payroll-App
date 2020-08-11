import sys
import json

sys.path.append('./helpers')
from generate_errors import check_sheet

from PyQt5.QtCore import QDate, Qt

#tdrive path
TRDRIVE_PATH = './example_tdrive/timesheets/'


def save_sheets(currWeek, prevWeek, employee_name):
	sheetCurr, sheetPrev = check_sheet(currWeek, prevWeek, returnSheet=True)

	#filname will be date-formated; previous week filename
	monday = prevWeek.split('-')[0]
	prev_date = QDate.fromString(monday).toString('MM/dd/yyyy')
	prev_date = prev_date.replace('/', '') + '.json'

	#filname will be date-formated; current week filename
	monday = currWeek.split('-')[0]
	curr_date = QDate.fromString(monday).toString('MM/dd/yyyy')
	curr_date = curr_date.replace('/', '') + '.json'

	try:
		#format the employee name to get the directory 
		#for their timesheets on the tdrive
		name_path = employee_name.replace(" ", "_")
		name_path += '/'

		#try to write the timesheets to the tdrive
		with open(TRDRIVE_PATH + name_path + prev_date, 'w') as outfile:
			json.dump(sheetPrev, outfile)
			outfile.close()
		with open(TRDRIVE_PATH + name_path + curr_date, 'w') as outfile:
			json.dump(sheetCurr, outfile)
			outfile.close()
	except Exception as e:
		#catch exception
		print(e)
		print("Unable to locate to timesheet file from submit_sheets")
		sys.exit()






















