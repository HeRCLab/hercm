import textwrap
import sys

class argumentSoup:
	def __init__(this, name, headerMessage):
		# name and headerMessage should be strings used for generating
		# the header as described in the argument soup spec

		# neither should contain newlines; these will be added automatically 

		this.options = []
		this.name = name 
		headerMessage = headerMessage.strip()
		headerMessage = ' '.join(headerMessage.split())
		this.headerMessage = headerMessage

	def addOption(this, 
		name, 
		optionType, 
		aliases=[], 
		positionals = [], 
		help = ""):

		# adds a new option to this instance for parsing 

		# name - the name of the option (eg. 'verbose')
		# optionType - the type of option ('flag' or 'argument') 
		# aliases - list of string aliases for the option (eg. ['v'])
		# positionals - list of dicts containing positional argument information
		# example: [{'name':'targetFile', 'requiredType':None},
		#			{'name':'favoriteNumber', 'requiredType':int}]
		# NOTE: positionals is order-sensitive! 
		# NOTE: 'type' should be the actual class type, eg. int, not 'int' 
		# help - help string for this option

		# no return value 

		option = {}
		option['name'] = name
		option['type'] = optionType 
		option['aliases'] = aliases
		option['positionals'] = positionals
		help = help.strip()
		help = ' '.join(help.split())
		option['help'] = help

		if option['type'] == 'flag':
			if positionals:
				raise ValueError("cannot have argument of type flag which" + 
					" takes positional arguments!") 
		this.options.append(option) 


	def resolveAlises(this, toResolve):
		# toResolve should be a string list of the same variety parse() takes
		# returns said list with any aliases resolved to their full names

		resolved = [] 
		for item in toResolve: 
			if item[0] == '-': # make sure this is not a positional
				itemName = None 
				leadingDashes = 0
				if item[1] == '-': # account for number of leading dashes
					itemName = item[2:]
					leadingDashes = 2
				else:
					itemName = item[1:]
					leadingDashes = 1

				for option in this.options: # resolve alias 
					if itemName in option['aliases']:
						resolved.append('-'*leadingDashes + option['name'])
					elif itemName == option['name']:
						resolved.append('-'*leadingDashes + itemName)
			else:
				resolved.append(item) 
		return resolved

	def parse(this, toParse):
		# parses the list toParse, which is an order-sensitive list of arguments 
		# in the same format as sys.argv

		# eg. ['--verbose','-inputfile foobar.txt']

		# returns a dict containing a list of arguments and flags, as specified
		# in the argument soup spec. 

		# eg. {'flags':['verbose'],'arguments':[['inputfile', 'foobar.txt']]}

		# Note how the first element of each argument in 'arguments' is the
		# argument's name, and each index after is a positional for that
		# argument 

		result = {}
		result['flags'] = []
		result['arguments'] = []

		toParse = this.resolveAlises(toParse)

		currentArgument = [] # ['argumentName', 'positional1', 'positional2'...]
		inArgument = False 

		for item in toParse: 
			if item[0] == '-':
				if item[1] != '-':
					if inArgument == False: 
						inArgument = True 
						currentArgument = []
						currentArgument.append(item[1:])
					else: 
						# get everything in the right place now, we will
						# typecast later
						result['arguments'].append(currentArgument)
						currentArgument = [] # we are starting a new argument...
						currentArgument.append(item[1:])
				else:
					result['flags'].append(item[2:])

			else:
				if inArgument:
					currentArgument.append(item)

		# make sure that if the last option is an argument, it is handled 
		if inArgument:
			result['arguments'].append(currentArgument)


		# verify options exist and are of the correct type 
		for item in result['flags']:
			foundItem = False 
			for option in this.options:
				if option['name'] == item: 
					if option['type'] == 'flag':
						foundItem = True
					else: 
						raise TypeError("option {0} found, but is not a flag"
							.format(item))
			if not foundItem:
				raise ValueError("option {0} was not found".format(item)) 

		for item in result['arguments']:
			foundItem = False 
			for option in this.options:
				if option['name'] == item[0]: 
					if option['type'] == 'argument':
						foundItem = True
					else: 
						raise TypeError("option {0} found, but is not a argument"
							.format(item))
			if not foundItem:
				raise ValueError("option {0} was not found".format(item)) 

		newResult = []
		for item in result['arguments']:
			argument = None
			for option in this.options:
				if option['name'] == item[0]:
					argument = option 

			for i in range (1, len(item)):
				if i < len(argument['positionals'])+1:
					# cast the item to the appropriate type
					typeToCast = argument['positionals'][i-1]['requiredType']
					if typeToCast != None:
						item[i] = typeToCast(item[i])

			
			item = item[:len(argument['positionals'])+1] # get rid of unhandled
			# positional options
			newResult.append(item)
			
		result['arguments'] = newResult 
		return result



	def printHelpMessage(this): 
		# generates and prints help message for all options in this instance

		# no return value

		title = textwrap.wrap(this.name, 60) 
		for line in title:
			print(" "*10+line) 

		print(" ")
		print(" ")

		header = textwrap.wrap(this.headerMessage, 80)
		for line in header:
			print(line)

		print(" ")
		print(" ")

		for item in this.options:
			if item['type'] == 'flag':
				sys.stdout.write('--')
			else:
				sys.stdout.write('-')
			sys.stdout.write(item['name'] + ' ')

			for positional in item['positionals']:
				if positional['requiredType'] != None:
					sys.stdout.write(str(positional['requiredType'].__name__)+':')
				sys.stdout.write('['+positional['name']+']')
				sys.stdout.write(' ')

			
			sys.stdout.write('(')
			for alias in item['aliases']:
				sys.stdout.write(alias)
				if alias != item['aliases'][-1]:
					sys.stdout.write(', ')
			sys.stdout.write(')')

			print('')

			for line in textwrap.wrap(item['help'], 76):
				print('    ' + line)
