
#!/usr/bin/python3
# utility for exploring and editing the contents of hercm matrix files 

import libSparseConvert
import readline
import libhsm
import matplotlib
import matplotlib.pyplot
import logging
import os


MTXIO = None 
helpString = """- HeRCM Explorer Help -
help - display this message

log / log [N] - prints the libSparseConvert log. If [N] is specified, print only
 the most recent [N] lines. 

load [path] [format] - loads the file at [path] with the format [format]. 
[format] should be mtx or hercm.

write [path] [format] - writes the matrix to the file at [path] using the format
[format], which is mtx or hercm. Will silently overwrite any existing file at
[path]. 

info - prints information on the matrix 

display - prints the entire matrix to the console in dense form

csrdisplay - prints the matrix in csr format to the console 

raw - prints the raw hercm matrix to the console 

value [row] [col] - prints the value at [row],[col]

row [row] - prints all non-zero values in the given row

col [col] - prints all non-zero values in the given col

range [r1] [c1] [r2] [c2] - prints all elements, zero or nonzero, which lie 
between the upper left bound [r1],[c1], and the lower right bound [r2],[c2]

touch [row] [col] [val] - changes the value at [row] [col] to [val] 

paint [x1] [y1] [x2] [y2] [val] - works the same way as range, but changes
all values encountered to [val]

paint-diag [begin] [end] [spread] [value] / 
paint-diag [begin] [end] [spread] [value] [offset] - paints the value [value]
at all indices along the diagonal, from the [begin]th to the [end]th. Paints 
[spread] values to either side of said diagonal. Offsets the diagonal by 
[offset] columns, if [offset] is given. 

row-major - makes the matrix row major 

rmzeros - remove zeros from matrix

setdims [height] [width] - sets the dimensions of the matrix to height by width

setsym [symmetry] - sets symmetry. Will not change array elements, only modifies 
symmetry attribute. 

init / init [height] [width] / init [height] [width] [val] - sets matrix to
a blank 5x5 matrix of zeros. If height and width are supplied, matrix is set to
those dimensions. If val is supplied, initialize matrix elements to val.
Overwrites any already loaded matrix. 

gen-verification - updates verification sum to permit writing out matrix after 
modification. 

check-symmetry - check the symmetry attribute, and searches for any non zero
elements in the bottom triangle, printing the first five if they exist. 

plot - plots the matrix graphically using matplotlib 

head [file path] - prints the first 10 lines of file at [file path]

cat [file path] - prints all lines from [file path] 

ls - get directory listing

pwd - print current working directory 

exit - exits the program
"""


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
			if 'mtx' in arguments[0]:
				print("""WARNING: matrix format not specified, assuming mtx 
from filename""")
				arguments.append('mtx')

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
		print("performing matrix tranpose, please wait...")
		matrix = SC.HSM.getInFormat('coo')
		matrix = matrix.transpose()
		SC.HSM.replaceContents(matrix)
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

	else:
		print("ERROR: Command not recognized") 
	


def runMain():
	while True:
		main()

print("welcome to HeRCM Explorer. Enter \"help\" for help")
SC = libSparseConvert.sparseConvert()
runMain()