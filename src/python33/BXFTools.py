# tools used by BXF explorer 

class command:
	# an interactive command 
	def __init__(this, name, func, argSpec, helpMesage):
		# name is the command the user types to run the command

		# func should be the actual function executed when this command is run

		

		# helpMessage is the help message for this command 

		this.func = func 
		this.argSpec = args 
		this.helpMessage = helpMessage
		this.name = name

	def run(this, arguments):
		# arguments should be a list of strings, which is already split on ' '
		# including the command 

		if arguments[0] != this.name: # this should never happen
			raise ValueError("cannot run command " + this.name + 
				" with command " + arguments[0])
		for i in range(1,len(arguments)):
			currentSpec = None
			for spec in this.argSpec: 
				if spec[1] == i:
					currentSpec = spec 
			if currentSpec == None:
				raise IndexError("ERROR: no argument spec for argument " + i)



class uiTools:
	def __init__(this):
		this.argSpecs = {}
		# argSpec should be dict of  argument specifiers which look like this: 
		# [type, pos] - keys are command names
		# type is the type (eg. int) WITHOUT quotes (not a string), pos is the
		# int indicating the argument's position within split user input. eg.
		# the argument specifier for "somecommand 5 8", for the first argument 
		# (the 5) might be [int, 1] 

		this.helpMessages = {} 
		# help messages, with commands as keys 

		this.argSpecs["help"] = [] 
		this.argSpecs["viewLogs"] = []
		


class manipulation: 
	# matrix manipulation utils used by BXFExplorer

	def __init__(this, HERCMIO):
		this.HERCMIO = HERCMIO # HERCMIO instance used internally

	def help(this):
		print(this.helpString)

	def viewLogs(this, numberOfLines=0):
		# this is supposed to print current logs, but it probably does not work 
		# anymore

		if numberOfLines == 0:
			pp.pprint(this.HERCMIO.logger.contents)
		else:
			pp.pprint(this.HERCMIO.logger.contents[- numberOfLines:])

	def load(this, path, form):
		# loads the file at path, which is format form (bxf, hercmio, mat, or
		# mtx)
		
		try:
			this.HERCMIO.readMatrix(path, form)
		except AttributeError:
			raise FileNotFoundError("file " + path + " does not exist!")
		except OSError:
			raise FileNotFoundError("file " + path + " does not exist!")


	def write(this, path, form):
		# writes out the contents of this instance's HERCMIO instance to path
		# in format form 

		try:
			this.HERCMIO.writeMatrix(fileName, fileFormat)
		except FileExistsError:
			raise FileExistsError("file " + path + " already exists")

		

	def printInfo(this):
		# pirint info about matrix 
		height    = this.HERCMIO.HSM.height
		width     = this.HERCMIO.HSM.width
		nzentries = this.HERCMIO.HSM.nzentries
		symmetry  = this.HERCMIO.HSM.symmetry
		verification = this.HERCMIO.verification

		print("""- matrix properties -
height (number of rows) - {0}
width (number of cols)  - {1}
non zero elements - - - - {2} 
symmetry  - - - - - - - - {3}
verification  - - - - - - {4} 
- end matrix properties -""".format(height, 
									width, 
									nzentries, 
									symmetry, 
									verification)) 

	def displayMatrix(this):
		# displays the matrix densely 
		if this.HERCMIO.HSM.symmetry == 'SYM':
			print("INFO: matrix is symmetric, bottom triangle should be only "+
				  "zeros")
		matrix = None
		try:
			matrix = this.HERCMIO.HSM.getInFormat('coo')
		except TypeError:
			print("ERROR: could not get matrix in COO format")
		try:
			import numpy
			numpy.set_printoptions(precision=5, suppress=True)
			print(matrix.todense())
		except MemoryError:
			print("ERROR: out of memory error, array to large to display")
		except AttributeError:
			print("ERROR: no matrix loaded")
		except ValuerError:
			print("ERROR: matrix is too large")


	def CSRDisplay(this):
		# print out the contents of the matrix in CSR format

		if this.HERCMIO.HSM.nzentries > 25:
			print("WARNING: matrix contains more than 25 entries, ")
			print("are you sure you wish to proceed?")
			if input('(yes/no)> ').upper() != "YES":
				return

		matrix = this.HERCMIO.HSM.getInFormat('csr')
		print("val:"      ,matrix.data)
		print("row_ptr:"  ,matrix.indices)
		print("colind:"   ,matrix.indptr)
		print("nzentries:",this.HERCMIO.nzentries)

	def rawDisplay(this):
		# pint out the contents of the matrix in COO format 

		print("- raw matrix contents -")
		print("{0:6} {1:6} {2:6}".format("row","col","val"))
		for i in range (0,this.HERCMIO.HSM.nzentries):
			element = this.HERCMIO.getElement(i)
			row = element[0]
			col = element[1]
			val = element[2]
			print("{0:6} {1:6} {2:6}".format(row, col, val))

	elif command == 'value':
		if len(arguments) != 2:
			print("ERROR: incorrect number of arguments")
			return

		row = int(arguments[0])
		col = int(arguments[1])
		print("value of {0},{1}:".format(row, col), 
			  this.HERCMIO.getValue(row, col))

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

		matrix = this.HERCMIO.getInFormat('coo')
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

		matrix = this.HERCMIO.getInFormat('coo')
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

		width = this.HERCMIO.width
		height = this.HERCMIO.height

		for row in range(0,height):
			for col in range (0,width):
				if col >= c1 and col <= c2:
					if row >= r1 and row <= r2:
						print("{0},{1} = {2}".format(row, col, 
													 this.HERCMIO.getValue(row, col)))

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

		oldValue = this.HERCMIO.getValue(row, col)

		this.HERCMIO.setValue(row, col, val)
		print("updated value of {0},{1}: {2}"
			  .format(row, col, this.HERCMIO.getValue(row, col)))
		
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

		width = this.HERCMIO.width
		height = this.HERCMIO.height

		for row in range(0,height):
			for col in range (0,width):
				if col >= c1 and col <= c2:
					if row >= r1 and row <= r2:
						this.HERCMIO.setValue(row, col,val)

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
					this.HERCMIO.setValue(i, col, val)
					col = offset + i - j # left side
					this.HERCMIO.setValue(i, col, val)
				except IndexError:
					pass # out of bounds 
						


	elif command == 'row-major':
		print("making matrix row major, standby...")
		this.HERCMIO.makeRowMajor() 
		print("done")

	elif command == 'rmzeros':
		print("removing zeros, standby...")
		this.HERCMIO.removeZeros()
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
		for i in reversed(range(0, this.HERCMIO.nzentries)):
			if this.HERCMIO.elements['row'][i] >= height:
				this.HERCMIO.setValue(this.HERCMIO.elements['row'][i], 
								this.HERCMIO.elements['col'][i], 0)
			elif this.HERCMIO.elements['col'][i] >= width:
				this.HERCMIO.setValue(this.HERCMIO.elements['row'][i], 
								this.HERCMIO.elements['col'][i], 0)

		this.HERCMIO.height = height
		this.HERCMIO.width = width 

		this.HERCMIO.removeZeros()

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



		if symmetry != this.HERCMIO.symmetry:
			if symmetry == 'SYM':
				this.HERCMIO.makeSymmetrical(method)
			elif symmetry == 'ASYM':
				this.HERCMIO.makeAsymmetrical(method)


		this.HERCMIO.symmetry = symmetry

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
				this.HERCMIO.setValue(i, j, val)
		if this.HERCMIO.elements == None:
			this.HERCMIO.nzentries = 0
		else:
			this.HERCMIO.nzentries = len(this.HERCMIO.elements['val'])
		this.HERCMIO.symmetry = 'ASYM' 
		this.HERCMIO.remarks = []

		print("finished initializing matrix, new matrix info:")
		main("info")



	elif command == 'shell':
		print("Entering python interactive debug shell...")
		print("Enter \"runMain()\" to return to normal execution")
		import pdb
		pdb.set_trace()

	elif command == 'check-symmetry':
		if this.HERCMIO.symmetry != 'SYM':
			print("symmetry attribute is not SYM")

		foundElements = 0
		for i in range(0, this.HERCMIO.nzentries): 
			element = this.HERCMIO.getElement(i)
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
		newSum = SC.HERCMIO.generateVerificationSum(this.HERCMIO)
		this.HERCMIO.verification = newSum 
		print("updated verification sum to: {0}".format(newSum))

	elif command == 'plot':
		matrix = this.HERCMIO.getInFormat('coo')
		
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
		print("performing matrix tranpose, please wait...")
		matrix = this.HERCMIO.getInFormat('coo')
		matrix = matrix.transpose()
		this.HERCMIO.replaceContents(matrix)
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
	