import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart\

#GLOBAL CONSTANTS
DATA_PATH = './helpers/data/'
USER_FILE = 'user_info.txt'

def email_supervisor(curr_txt, prev_txt):
	employee_name, sender_email, password = loadInfo()

	port = 465 # for ssl
	smtp_server = "smtp.gmail.com"
	receiver_email = "clsnowboy@gmail.com"	#supervisor email

	#html and plain text formats alternatives
	message = MIMEMultipart()

	#message formalities
	message["Subject"] = "Timesheet Submission - " + employee_name
	message["From"] = sender_email
	message["To"] = receiver_email

	text = curr_txt

	#Turn these into plain/html MIMEText objects
	part1 = MIMEText(text, "plain")

	#add the parts to the message
	#email client tries to render the last part first
	message.attach(part1)

	try:
		#attempt to send the email
		context = ssl.create_default_context()	#safety measures
		with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
			#access the server, login, and send the email
			server.login(sender_email, password)
			server.sendmail(
					sender_email, receiver_email, message.as_string()
				)
	except Exception as e:
		#catch errors & troubleshoot
		msg = "Error: unable to email timesheet.\n"
		msg += "If you've changed your email/password, update\n"
		msg += "<user_info.txt> in the data folder."
		print(msg)

		sys.exit()






def loadInfo():
	"""Load in the login information"""
	#let's grab the user's info
	try:
		with open(DATA_PATH + USER_FILE, 'r') as user_info:
			login_data = user_info.readlines()
	except Exception:
		#troubleshoot if you cant open the file
		print("Could not find file: <user_info.txt>")
		sys.exit()

	#do some cleaning on login_data; return email, password
	employee_name = login_data[0].replace('\n', '')
	employee_email = login_data[2].replace('\n', '')
	email_pass =  login_data[3].replace('\n', '')

	return employee_name, employee_email, email_pass