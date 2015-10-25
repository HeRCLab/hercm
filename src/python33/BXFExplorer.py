
#!/usr/bin/python3
# utility for exploring and editing the contents of hercm matrix files 

import readline
import libHercMatrix
import libHercmIO
import matplotlib
import matplotlib.pyplot
import logging
import os






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
	

	if command == 'help':
		print(helpString)
	elif command == 'exit':
		exit() 

	elif command == 'log':
		if len(arguments) == 0:
			pp.pprint(SC.logger.contents)
		elif len(arguments) == 1: 
			numberOfLines = 0
			try: 
				numberOfLines = int(arguments[0])
			except ValueError:
				print("ERROR: {0} is not a valid number of lines"
					  .format(arguments[0]))
				return 
			pp.pprint(SC.logger.contents[- numberOfLines:])

	elif command == 'load':
		if len(arguments) == 1:
			if 'hercm' in arguments[0]:
				print("""WARNING: matrix format not specified, assuming hercm 
from filename""")
				arguments.append('hercm')
			elif 'mtx' in arguments[0]:
				print("""WARNING: matrix format not specified, assuming mtx 
from filename""")
				arguments.append('mtx')
			elif 'mat' in arguments[0]:
				print("""WARNING: matrix format not specified, assuming mtx 
from filename""")
				arguments.append('mat')
			elif 'bxf' in arguments[0]:
				print("""WARNING: matrix format not specified, assuming mtx 
from filename""")
				arguments.append('bxf')

		if len(arguments) != 2:
			print("ERROR: incorrect number of arguments")
			return
		fileName = arguments[0]
		fileFormat = arguments[1] 

		try:
			SC.readMatrix(fileName, fileFormat)
		except AttributeError:
			print("ERROR: file does not exist")
			return
		except OSError:
			print("ERROR: file does not exist")

		print("done reading matrix")
		if SC.HSM.symmetry == 'SYM':
			print("INFO: matrix is symmetric, bottom triangle should be only " 
				  +"zeros")

	elif command == 'write':
		if len(arguments) != 2:
			print("ERROR: incorrect number of arguments")
			return
		fileName = arguments[0]
		fileFormat = arguments[1]
		print("Writing {0} in format {1}".format(fileName, fileFormat))

		try:
			SC.writeMatrix(fileName, fileFormat)
		except FileExistsError:
			print("ERROR: file already exists!")
			return 

		

	elif command == 'info':
		height    = SC.HSM.height
		width     = SC.HSM.width
		nzentries = SC.HSM.nzentries
		symmetry  = SC.HSM.symmetry
		verification = SC.HSM.verification

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

	elif command == 'display':
		if SC.HSM.symmetry == 'SYM':
			print("INFO: matrix is symmetric, bottom triangle should be only "+
				  "zeros")
		matrix = None
		try:
			matrix = SC.HSM.getInFormat('coo')
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


	elif command == 'csrdisplay':
		if SC.HSM.nzentries > 25:
			print("WARNING: matrix contains more than 25 entries, ")
			print("are you sure you wish to proceed?")
			if input('(yes/no)> ').upper() != "YES":
				return

		matrix = SC.HSM.getInFormat('csr')
		print("val:"      ,matrix.data)
		print("row_ptr:"  ,matrix.indices)
		print("colind:"   ,matrix.indptr)
		print("nzentries:",SC.HSM.nzentries)

	elif command == 'raw':
		main("info")
		print("- raw matrix contents -")
		print("{0:6} {1:6} {2:6}".format("row","col","val"))
		for i in range (0,SC.HSM.nzentries):
			element = SC.HSM.getElement(i)
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