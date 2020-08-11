import json
import sys

#constant
DIRECT = "./helpers/data/timesheets/"
SHEET = "timesheet.json"

def load_sheet(week):
	try:
		with open(DIRECT + week + SHEET, "r") as file:
			data = json.load(file)

			file.close()

			return data
	except Exception: 
		#if the file doesnt exist, return an empty dict
		return {}

def set_sheet(timesheet, week):
	try:
		with open(DIRECT + week + SHEET, "w") as file:
			json.dump(timesheet, file)

			file.close()

	except Exception as e:
		print(e)
		troubleshoot = "Error: timesheet file writing."
		print(troubleshoot)
		sys.exit()