# Charles's Logging System 
# Used for keeping logs of things 

import time
import datetime

class clogs:
	def __init__(this):
		this.contents = [] 
	def log(this, message, level='info'):
		# logs the string message to this.log in the format 'timestamp|level|message'

		message = level.upper() + '|' + message

		timeStamp = time.time()
		timeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
		message = timeStamp + '|' + message

		this.contents.append(message) 

