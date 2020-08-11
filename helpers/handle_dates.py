from PyQt5.QtCore import QDate, Qt

def initDate():
	"""Returns the current date"""
	#use QDate to grab the current date
	curr_date = QDate.currentDate()
	#return the formatted  string date
	return curr_date.toString()


def setWeek():
	"""Returns a list of adjacent weeks (adjacent to the current week, 
	including the current week)"""
	#use QDate to grab the current date
	curr_date = QDate.currentDate()

	#record the closest Monday (start of the current week)
	closest_monday = curr_date.addDays(1-curr_date.dayOfWeek())

	# print(closest_monday.toString())

	#record adjacent mondays
	prev2_monday = closest_monday.addDays(-14)
	prev_monday = closest_monday.addDays(-7)
	next_monday = closest_monday.addDays(7)

	# print(prev_monday.toString())
	# print(next_monday.toString())

	#let's create the WORK week ranges using a dictionary
	weeks = {prev2_monday.toString(): prev2_monday.addDays(4).toString(),
			prev_monday.toString(): prev_monday.addDays(4).toString(), 
			closest_monday.toString(): closest_monday.addDays(4).toString(),
			next_monday.toString(): next_monday.addDays(4).toString()
			}


	# print(mondays_lst)
	#return the list of weeks
	return weeks
