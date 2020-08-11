#import for timesheets
import sys
import json

sys.path.append('./helpers/data/timesheets')

#constant
DIRECT = "./helpers/data/timesheets/"
SHEET = "timesheet.json"

#constants for errors
WBS = "Missing WBS"
PAY = "Missing Pay Item"

def check_sheet(currWeek, prevWeek, returnSheet=False, checker=False):
	#first we load in the timesheet for the current
	#week and the previous week 

	errs_lst_curr = {}	#list of errors to report back
	errs_lst_prev = {}
	try:
		with open(DIRECT + currWeek + SHEET, "r") as file:
			curr_data = json.load(file)

			file.close()

	except Exception as e:
		#if checker is true, we're just checking for the
		#existence of the files; no error msg needed
		if checker:
			return False

		print(str(e))
		#if the file doesnt exist, return an empty dict
		print("No File For Week: " + str(currWeek))
		sys.exit()


	try:
		with open(DIRECT + prevWeek + SHEET, "r") as file:
			prev_data = json.load(file)

			file.close()

	except Exception:
		#if checker is true, we're just checking for the
		#existence of the files; no error msg needed
		if checker:
			return False
		#if the file doesnt exist, return an empty dict
		print("No File For Week: " + str(prevWeek))
		sys.exit()

	if checker:
		return True

	#now that we have both timesheets as dictionaries, let's do
	#some checking

	#layout: 
	#{project: [WBS, PayItem, Mon, Tues, Weds, Thurs, Fri]}

	ret_lst_curr = []
	ret_lst_prev = []
	total_hours = 0
	#checks: every entry should have a WBS & PayItem
	for proj, proj_details in curr_data.items():
		s = proj

		if proj_details[0] == "":
			#add no WBS error
			s += "$" + WBS

		if proj_details[1] == "":
			#add no PayItem error
			s += "$" + PAY

		#sum hours
		for hrs in proj_details[3:]:
			if type(hrs) != type("Easter Egg"):
				total_hours += hrs

		if s != (proj) :
			ret_lst_curr.append(s)

	for proj, proj_details in prev_data.items():
		s = proj

		if proj_details[0] == "":
			#add no WBS error
			s += "$" + WBS

		if proj_details[1] == "":
			#add no PayItem error
			s += "$" + PAY

		#sum hours
		for hrs in proj_details[3:]:
			if type(hrs) != type("Easter Egg"):
				total_hours += hrs

		if s != (proj) :
			ret_lst_prev.append(s)

	if returnSheet:
		#return sheets
		return curr_data, prev_data
	else:
		return ret_lst_curr, ret_lst_prev, total_hours













