# this file provides the functions used by BXFExplorer

import readline
import libHercMatrix
import libHercmIO
import matplotlib
import matplotlib.pyplot
import logging
import os

helpString = """
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

cd - change current working directory

convert [src] [srcform] [dest] [destform] - converts file [src] in format
[srcform] to [destform] then writes it to [dest]

exit - exits the program
"""

def printHelp(command=None):
	if command == None:
		print(helpString)
	else:
		print("Sorry, per-command help is not implemented yet")


def load(filename, form, HERCMIO):
	# load filename, which is format format 
	# HERCMIO should be the LibHercmIO.hercmIO instance to load the matrix into

	if form not in ['bxf','hercm','mat','mtx']:
		raise KeyError("format {0} is not supported".format(form))

	HERCMIO.readMatrix(fileName, fileFormat)


def write(filename, form, HERMCIO):
	# write matrix stored in HERCMIO instance to filename in given format

	if form not in ['bxf','hercm','mat','mtx']:
		raise KeyError("format {0} is not supported".format(form))
	HERCMIO.writeMatrix(fileName, fileFormat)

		

def printInfo(HERCMATRIX):
	# prints information about HERCMATRIX matrix to console
		height    = HERCMATRIX.height
		width     = HERCMATRIX.width
		nzentries = HERCMATRIX.nzentries
		symmetry  = HERCMATRIX.symmetry
		verification = HERCMATRIX.verification

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

def displayMatrix(HERCMATRIX, maxWidth=20, maxHeight=20): 
	# displays the matrix to the console 
	# elements past 20 wide or 20 high will not be displayed

	if HERCMATRIX.height < maxHeight:
		if HERCMATRIX.width < maxWidth:
			for col in range(0, HERCMATRIX.width):
				for row in range(0,HERCMATRIX.height):
					print(HERCMATRIX.getValue(row, col) + " ")
					return 
				print("")
		else:
			raise NotImplementedError("You are probably trying to preview a " +
				"non-square matrix, which is not yet supported")
	else: 
		for col in range(0, HERCMATRIX.width):
				for row in range(0,HERCMATRIX.height):
					if col == (maxWidth / 2):
						col = HERCMATIX.width - (maxWidth/2)
						print(" ... ", end="")
					if row == (maxWidth / 2):
						row = HERCMATIX.height - (maxHeight/2)
						print(" ... ", end="")
					print(HERCMATRIX.getValue(row, col) + " ", end="")
				print("")
					

def printValue(row, col, HERCMATRIX):
	# prints the value of HERCMATRIX at row, col
	print("value of {0},{1}:".format(row, col), 
		 HERCMATRIX.getValue(row, col))

def printRow(row, HERCMATRIX):
	# prints the rowth row in HERCMATRIX

		matrix = HERCMATRIX.getInFormat('coo')
		print("row {0} contents: \n{1}"
			  .format(rowNumber, matrix.getrow(rowNumber)))

def printCol(col, HERCMATRIX):
	# prints the colth column in HERCMATRIX

	matrix = HERCMATRIX.getInFormat('coo')
	print("column {0} contents: \n{1}"
		 .format(colNumber, matrix.getcol(colNumber)))

def printRange(row1, row2, col1, col2, HERCMATRIX):
	# prints a rectangular range of values in HERCMATRIX, with row1, col1 as
	# the top left corner, and row2, col2 in the bottom right


	width = HERCMATRIX.width
	height = HERCMATRIX.height
	for row in range(0,height):
		for col in range (0,width):
			if col >= col1 and col <= col2:
				if row >= row1 and row <= row2:
					print("{0},{1} = {2}".format(row, col, 
												 SC.HSM.getValue(row, col)))

def touch(row, col, val, HERCMATRIX):
	# sets the value at row, col to val 


	oldValue = HERCMATRIX.getValue(row, col)
	HERCMATRIX.setValue(row, col, val)
	print("updated value of {0},{1} to {2} from {3}"
		  .format(row, col, HERCMATRIX.getValue(row, col), oldValue))
	
	if oldValue == 0 and val != 0: 
		print("WARNING: you have added a new non zero entry, COO vectors")
		print("may not be in row-major form!")

def paint(row1, row2, col1, col2, val, HERCMATRIX):
	# paints a rectangular region of HERCMATRIX with val, with the top left 
	# corner as row1, col1, and the bottom right as row2, col2

	width = HERCMATRIX.width
	height = HERCMATRIX.height
	for row in range(0,height):
		for col in range (0,width):
			if col >= col1 and col <= col2:
				if row >= row1 and row <= row2:
					SC.HSM.setValue(row, col,val)

def paintDiagonal(begin, end, spread, val, HERCMATRIX, offset=0):
	# paints a diagonal, starting at column begin, ending at column end with 
	# the value val, spread indices to either side of the diagonal. 
	# optionally offsets by offset columns to the left or right
	

	for i in range(begin, end):
		for j in range(0, spread):
			try:
				col = offset + i + j # right side
				SC.HSM.setValue(i, col, val)
				col = offset + i - j # left side
				SC.HSM.setValue(i, col, val)
			except IndexError:
				pass # out of bounds 
					

def setDims(width, height, HERCMATRIX):
	# sets the dimensions of HERCMATRIX to width x height 

		# remove out of bounds entries 
		for i in reversed(range(0, HERCMATRIX.nzentries)):
			if HERCMATRIX.elements['row'][i] >= height:
				HERCMATRIX.setValue(SC.HSM.elements['row'][i], 
								SC.HSM.elements['col'][i], 0)
			elif HERCMATRIX.elements['col'][i] >= width:
				HERCMATRIX.setValue(SC.HSM.elements['row'][i], 
								SC.HSM.elements['col'][i], 0)

		HERCMATRIX.height = height
		HERCMATRIX.width = width 
		HERCMATRIX.removeZeros()



def setSymmetry(newSymmetry, HERCMATRIX method="truncate"):
	# wrapper for libHercMatrix.hercMatrix.makeSymmetrical/makeAsymmetrical

		if method not in ['truncate', 'add', 'smart']:
			raise KeyError("method {0} is not valid".format(method))
				
		validOptions = ['sym','asym','asymmetric','symmetric',
		'symmetrical','asymmetrical'] 

		newSymmetry = newSymmetry.lower()

		if newSymmetry not in validOptions:
			raise KeyError("{0} is not a valid symmetry".format(newSymmetry))

		if newSymmetry in ['sym','symmetric','symmetrical']:
			symmetry = 'SYM'
		else:
			symmetry = 'ASYM'



		if symmetry != HERCMATRIX.symmetry:
			if symmetry == 'SYM':
				HERCMATRIX.makeSymmetrical(method)
			elif symmetry == 'ASYM':
				HERCMATRIX.makeAsymmetrical(method)


		HERCMATRIX.symmetry = symmetry

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
