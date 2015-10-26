
#!/usr/bin/python3
# utility for exploring and editing the contents of hercm matrix files 

import readline
import libHercMatrix
import libHercmIO
import matplotlib
import matplotlib.pyplot
import logging
import os
import BXFUtils


def main(override = None):
	# override will be parsted instead of the user's input, if specified

	import pprint
	pp = pprint.PrettyPrinter()

	if override == None:
		usrIn = input("> ")
	else:
		usrIn = override 

	usrIn = usrIn.rstrip()
	splitInput = usrIn.split()
	try: 
		command = splitInput[0] 
		arguments = splitInput[1:]
	except IndexError:
		return
	
	commandInfo = {} 
	commandInfo['help'] = {'requiredArguments':None,
		'optionalArguments':[[0, str, 'command']],
		'argumentInfo':['specific command to retrieve help for'],
		'help':'Prints help for all commands, or prints the help for the ' + 
		'command specified in the first argument'}
	commandInfo['exit'] = {'requiredArguments':None, 
		'optionalArguments':None, 
		'argumentInfo':None,
		'help':'exits the program'}
	commandInfo['load'] = {'requiredArguments':[[0, str, 'path'],
			[1,str,'format']],
		'optionalArguments':None,
		'argumentInfo':['The file to load', 'The format of said file'],
		'help':'Reads in the file for viewing and manipulation'}
	commandInfo['write'] = {'requiredArguments':[[0, str, 'path'], 
			[1, str, 'format']], 
		'optionalArguments':None,
		'argumentInfo':['The file to write to', 'The format of said file'],
		'help':'Writes current matrix to specified file, in specified format' +
		' note that the given path should include the desired file extension'}
	commandInfo['info'] = {'requiredArguments':None,
		'optionalArguments':None,
		'argumentInfo':None,
		'help':'Prints information about the loaded matrix'}
	commandInfo['display'] = {'requiredArguments':None, 
		'optionalArguments':[[0, int, 'height'],[1, int, 'width']],
		'argumentInfo':['maximum number of elemets to display vertically',
			'maximum number of elements to display horizontally'],
		'help':'Displays a visualization of the matrix. If the matrix is ' + 
			'very large, only the corners will be displayed'}
	commandInfo['csrdisplay'] = {'requiredArguments':None, 
	'optionalArguments':[[0, int, 'rowStart'],[1,int,'rowEnd']],
	'argumentInfo':['first row to display', 'last row to display'],
	'help':'Displays the matrix as raw CSR data, prompts if nzentries > 25.' +
	' if provided, will only display the CSR values between a particular' +
	' range of rows in the matrix'}
	

	if command not in commandInfo:
		print("WARNING: command is not in commandInfo, cannot check required " +
			"arguments!")
	else:
		if commandInfo[command]['requiredArguments'] != None:
			if len(arguments) < len(commandInfo[command]['requiredArguments']):
				print("ERROR, incorrect number of arguments for {0}"
					.format(command))
				firstMisingArgument = len(arguments)
				for i in range(firstMisingArgument, 
					len(commandInfo[command]['requiredArguments'])):
					print("Missing argument '{1}' at position {0}".format(i,
						commandInfo[command]['requiredArguments'][i][2]))
				return
			
			for arg in commandInfo[command]['requiredArguments']:
				try:
					arg[1](arguments[arg[0]])
				except Exception:
					print("ERROR: argument {0} was present, but is not of " +
						" required type {1}".format(arg[0], str(arg[1])))
					return

		if commandInfo[command]['optionalArguments'] != None:
			for arg in commandInfo[command]['optionalArguments']:
				argOffset = 0
				if commandInfo[command]['requiredArguments'] != None:
					argOffset = len(commandInfo[command]['requiredArguments'])
				if argOffset + arg[0] > len(arguments): # this optional arg was
				# not given
					break

				try:
					arguments[arg[0] + argOffset] = \
						arg[1](arguments[arg[0] + argOffset])

				except IndexError:
					print("ERROR: index error while accessing index {0} of {1}"
						.format(arg[0] + argOffset, arguments))
				except Exception:
					print("ERROR: argument {0} was present, but of type {1} " +
						" not required type {2}".format(arg[0] + argOffset,
						 	type(arguments[arg[0]+argOffset]),
						 	str(arg[1])))
					return

	if command == 'help':
		if len(arguments) > 0:
			BXFUtils.printHelp(commandInfo, arguments[0])
		else:
			BXFUtils.printHelp(commandInfo)

	elif command == 'exit':
		exit() 

	elif command == 'load':
		try:
			BXFUtils.load(arguments[0], arguments[1], SC)
		except AttributeError:
			print("ERROR: file does not exist")
			return
		except OSError:
			print("ERROR: file does not exist")
		except KeyError:
			print("ERROR: requested format is not supported")

		print("done reading matrix")
		if SC.HSM.symmetry == 'SYM':
			print("INFO: matrix is symmetric, bottom triangle should be only " 
				  +"zeros")

	elif command == 'write':
		fileName = arguments[0]
		fileFormat = arguments[1]
		try:
			BXFUtils.write(fileName, fileFormat, SC)
		except FileExistsError:
			print("ERROR: file already exists!")
			return 


	elif command == 'info':
		BXFUtils.printInfo(SC.HSM)

	elif command == 'display':
		if len(arguments) == 2:
			height = arguments[0]
			width = arguments[1]
			try:
				BXFUtils.displayMatrix(SC.HSM, height, width)
			except ValueError:
				print("ERROR: display dimensions must be even numbers!")
		else:
			BXFUtils.displayMatrix(SC.HSM)


	elif command == 'csrdisplay':
		if len(arguments) == 2:
			BXFUtils.printCSR(SC.HSM, arguments[0], arguments[1])
		else:
			BXFUtils.printCSR(SC.HSM)

	elif command == 'raw':
		BXFUtils.printRaw(SC.HSM)

	elif command == 'value':
		if len(arguments) != 2:
			print("ERROR: incorrect number of arguments")
			return

		row = int(arguments[0])
		col = int(arguments[1])
		print("value of {0},{1}:".format(row, col), 
			  SC.HSM.getValue(row, col))

	elif command == 'row':
		if len(arguments) != 1:
			print("ERROR: incorrect number of arguments") 
			return 
		rowNumber = 0
		try: 
			rowNumber = int(arguments[0])
		except ValueError:
			print("ERROR: {0} is not a valid row number".format(arguments[0]))
			return

		matrix = SC.HSM.getInFormat('coo')
		print("row {0} contents: \n{1}"
			  .format(rowNumber, matrix.getrow(rowNumber)))

	elif command == 'col':
		if len(arguments) != 1:
			print("ERROR: incorrect number of arguments") 
			return 
		colNumber = 0
		try: 
			colNumber = int(arguments[0])
		except ValueError:
			print("ERROR: {0} is not a valid column number".format(arguments[0]))
			return

		matrix = SC.HSM.getInFormat('coo')
		print("column {0} contents: \n{1}"
			  .format(colNumber, matrix.getcol(colNumber)))

	elif command == 'range':
		if len(arguments) != 4:
			print("ERROR: incorrect number of arguments")
			return 
		r1 = 0
		r2 = 0
		c1 = 0
		c2 = 0 

		try:
			r1 = int(arguments[0])
			c1 = int(arguments[1])
			r2 = int(arguments[2])
			c2 = int(arguments[3])
		except ValueError:
			print("ERROR: one or more arguments are not valid integers")
			return 

		width = SC.HSM.width
		height = SC.HSM.height

		for row in range(0,height):
			for col in range (0,width):
				if col >= c1 and col <= c2:
					if row >= r1 and row <= r2:
						print("{0},{1} = {2}".format(row, col, 
													 SC.HSM.getValue(row, col)))

	elif command == 'touch':
		if len(arguments) != 3:
			print("ERROR: incorrect number of arguments")
			return 
		row = 0
		col = 0
		val = 0

		try:
			row = int(arguments[0])
			col = int(arguments[1])
			val = float(arguments[2])
		except ValueError:
			print("ERROR: one or more arguments are not valid numbers")
			return 

		oldValue = SC.HSM.getValue(row, col)

		SC.HSM.setValue(row, col, val)
		print("updated value of {0},{1}: {2}"
			  .format(row, col, SC.HSM.getValue(row, col)))
		
		if oldValue == 0 and val != 0: 
			print("WARNING: you have added a new non zero entry, COO vectors")
			print("may not be in row-major form!")

	elif command == 'paint':
		if len(arguments) != 5:
			print("ERROR: incorrect number of arguments")
			return 
		r1 = 0
		r2 = 0
		c1 = 0
		c2 = 0 
		val = 0

		try:
			r1 = int(arguments[0])
			c1 = int(arguments[1])
			r2 = int(arguments[2])
			c2 = int(arguments[3])
			val = float(arguments[4])
		except ValueError:
			print("ERROR: one or more arguments are not valid numbers")
			return 

		print("painting values... (this may take several minutes)")

		width = SC.HSM.width
		height = SC.HSM.height

		for row in range(0,height):
			for col in range (0,width):
				if col >= c1 and col <= c2:
					if row >= r1 and row <= r2:
						SC.HSM.setValue(row, col,val)

	elif command == 'paint-diag': 
		if len(arguments) < 4: 
			print("ERROR: incorrect number of arguments")
		begin = 0
		end = 0 
		spread = 0
		val = 0
		offset = 0

		try:
			begin  = int(arguments[0])
			end    = int(arguments[1])
			spread = int(arguments[2])
			val    = float(arguments[3])
			if len(arguments) == 5:
				offset = int(arguments[4])
		except ValueError:
			print("ERROR: one or more arguments are not valid numbers")
			return 

		for i in range(begin, end):
			for j in range(0, spread):
				try:
					col = offset + i + j # right side
					SC.HSM.setValue(i, col, val)
					col = offset + i - j # left side
					SC.HSM.setValue(i, col, val)
				except IndexError:
					pass # out of bounds 
						


	elif command == 'row-major':
		print("making matrix row major, standby...")
		SC.HSM.makeRowMajor() 
		print("done")

	elif command == 'rmzeros':
		print("removing zeros, standby...")
		SC.HSM.removeZeros()
		print("done")

	elif command == 'setdims':
		if len(arguments) != 2:
			print("ERROR: incorrect number of arguments") 
			return
		width = 0
		height = 0

		try:
			height = int(arguments[0])
			width = int(arguments[1])
		except ValueError:
			print("ERROR: one or more arguments are not valid integers")
			return 

		# remove out of bounds entries 
		for i in reversed(range(0, SC.HSM.nzentries)):
			if SC.HSM.elements['row'][i] >= height:
				SC.HSM.setValue(SC.HSM.elements['row'][i], 
								SC.HSM.elements['col'][i], 0)
			elif SC.HSM.elements['col'][i] >= width:
				SC.HSM.setValue(SC.HSM.elements['row'][i], 
								SC.HSM.elements['col'][i], 0)

		SC.HSM.height = height
		SC.HSM.width = width 

		SC.HSM.removeZeros()

		print("Updated matrix dimensions. New values:")
		main("info")


	elif command == 'setsym':
		if len(arguments) < 1:
			print("ERROR: incorrect number of arguments")
			return 

		method = 'truncate'

		if len(arguments) == 2:
			method = arguments[1]
			if method not in ['truncate', 'add', 'smart']:
				print("method {0} is not valid, defaulting to truncate")
				
		validOptions = ['sym','asym','asymmetric','symmetric',
		'symmetrical','asymmetrical'] 

		arguments[0] = arguments[0].lower()

		if arguments[0] not in validOptions:
			print("ERROR: argument {0} is not a valid symmetry option, Valid ")
			print("options are: ")
			pp.pprint(validOptions)
			return 

		if arguments[0] in ['sym','symmetric','symmetrical']:
			symmetry = 'SYM'
		else:
			symmetry = 'ASYM'



		if symmetry != SC.HSM.symmetry:
			if symmetry == 'SYM':
				SC.HSM.makeSymmetrical(method)
			elif symmetry == 'ASYM':
				SC.HSM.makeAsymmetrical(method)


		SC.HSM.symmetry = symmetry

	elif command == 'init': 
		height = 5
		width = 5
		val = 0
		if len(arguments) >= 2:
			try:
				height = int(arguments[0]) 
				width  = int(arguments[1])
			except ValueError:
				print("ERROR: cannot convert one or more arguments to integer")
				return
		if len(arguments) >= 3:
			try:
				val = float(arguments[2])
			except ValueError:
				print("ERROR: cannot convert {0} to float".format(arguments[2]))
				return 

		main("setdims 0 0")
		main("setdims {0} {1}".format(height, width))
		for i in range(0, height): # this is faster than using paint
			for j in range(0,width): 
				SC.HSM.setValue(i, j, val)
		if SC.HSM.elements == None:
			SC.HSM.nzentries = 0
		else:
			SC.HSM.nzentries = len(SC.HSM.elements['val'])
		SC.HSM.symmetry = 'ASYM' 
		SC.HSM.remarks = []

		print("finished initializing matrix, new matrix info:")
		main("info")



	elif command == 'shell':
		print("Entering python interactive debug shell...")
		print("Enter \"runMain()\" to return to normal execution")
		import pdb
		pdb.set_trace()

	elif command == 'check-symmetry':
		if SC.HSM.symmetry != 'SYM':
			print("symmetry attribute is not SYM")

		foundElements = 0
		for i in range(0, SC.HSM.nzentries): 
			element = SC.HSM.getElement(i)
			row = element[0]
			col = element[1]
			val = element[2] 
			if row > col:
				if val != 0:
					if foundElements < 5:
						print("non zero element at {0},{1}:{2}"
							  .format(row, col, val))
					if foundElements == 5:
						print("""Found more than five elements in bottom 
triangle, further messages will be squelched""")
					foundElements = foundElements + 1
		print("If no previous messages were displayed, the matrix is symmetric")



	elif command == 'gen-verification':
		newSum = SC.HERCMIO.generateVerificationSum(SC.HSM)
		SC.HSM.verification = newSum 
		print("updated verification sum to: {0}".format(newSum))

	elif command == 'plot':
		matrix = SC.HSM.getInFormat('coo')
		
		matplotlib.pyplot.spy(matrix)
		matplotlib.pyplot.show()

	elif command == 'log-info':
		print("setting loglevel to info")
		logging.basicConfig(level=logging.INFO)
	elif command == 'log-debug':
		print("setting loglevel to debug")
		logging.basicConfig(level=logging.DEBUG)

	elif command == "transpose":
		# reflects the matrix around the diagonal
		print("performing matrix transpose, please wait...")
		SC.HSM.transpose()
		print("matrix transpose complete")

	elif command == "ls":
		directory = ''
		if len(arguments) > 0:
			if os.path.exists(arguments[0]):
				directory = arguments[0] 
			elif os.path.exists(os.path.join(os.getcwd(), arguments[0])):
				directory = os.path.join(os.getcwd(), arguments[0])
			else:
				print("ERROR: could not get directory listing")
				print(arguments[0], " is not a valid path")
				print(os.path.join(os.getcwd(), arguments[0]), 
					" is not a valid path")
				directory = os.getcwd()
		else:
			directory = os.getcwd()

		print("Directory listing for: ", directory)
		for item in os.listdir(directory):
			print(item)

	elif command == "pwd":
		print(os.getcwd())

	elif command == "head":
		if len(arguments) != 1:
			print("ERROR: incorrect number of arguments")
			return 
		f = open(arguments[0])
		for line in f.readlines()[0:10]:
			print(line, end='')

	elif command == "cat":
		if len(arguments) != 1:
			print("ERROR: incorrect number of arguments")
			return 
		f = open(arguments[0])
		for line in f.readlines():
			print(line, end='')

	elif command == "cd":
		if len(arguments) != 1:
			print("ERROR: incorrect number of arguments")
			return 
		if not os.path.exists(arguments[0]):
			print("ERROR: cannot cd to nonexistent path")
			return 
		if os.path.isfile(arguments[0]):
			print("ERROR: {0} is not a directory".format(arguments[0]))
			return
		os.chdir(arguments[0])

	elif command == "convert":
		if len(arguments) != 4:
			print("ERROR: incorrect number of arguments")
			return 
		source = arguments[0] 
		destination = arguments[2]
		sourceFormat = arguments[1]
		destinationFormat = arguments[3]

		if not os.path.exists(source):
			print("ERROR: load from nonexistent path")
			return 
		if not os.path.isfile(source ):
			print("ERROR: {0} is not a file".format(source))
			return


		main("load " + source)
		main("gen-verification")
		main("write " + destination + " " + destinationFormat)


	else:
		print("ERROR: Command not recognized") 
	


def runMain():
	while True:
		main()

print("welcome to BXFExplorer. Enter \"help\" for help")
SC = libHercmIO.hercmIO()
runMain()