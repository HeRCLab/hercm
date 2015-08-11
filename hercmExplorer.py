#!/usr/bin/python3
# utility for exploring and editing the contents of hercm matrix files 

import libSparseConvert
import readline
import libhsm


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

		SC.readMatrix(fileName, fileFormat)
		print("done reading matrix")

	elif command == 'write':
		if len(arguments) != 2:
			print("ERROR: incorrect number of arguments")
			return
		fileName = arguments[0]
		fileFormat = arguments[1]
		print("Writing {0} in format {1}".format(fileName, fileFormat))

		SC.writeMatrix(fileName, fileFormat)
		

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
		matrix = None
		try:
			matrix = SC.HSM.getInFormat('csr')
		except TypeError:
			print("ERROR: could not get matrix in CSR format")
		try:
			import numpy
			numpy.set_printoptions(precision=5, suppress=True)
			print(matrix.todense())
		except MemoryError:
			print("ERROR: out of memory error, array to large to display")
		except AttributeError:
			print("ERROR: no matrix loaded")


	elif command == 'csrdisplay':
		if SC.HSM.contents['nzentries'] > 25:
			print("WARNING: matrix contains more than 25 entries, ")
			print("are you sure you wish to proceed?")
			if input('(yes/no)> ').upper() != "YES":
				return

		matrix = SC.HSM.getInFormat('csr')
		print("val:"      ,matrix.data)
		print("row_ptr:"  ,matrix.indices)
		print("colind:"   ,matrix.indptr)
		print("nzentries:",SC.HSM.contents['nzentries'])

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

		if SC.HSM.setValue(row, col, val):
			print("updated value of {0},{1}: {2}"
				  .format(row, col, SC.HSM.getValue(row, col)))
		else:
			print("ERROR: could not set value (row, col probably out of bounds")

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

		width = SC.HSM.contents['width']
		height = SC.HSM.contents['height']

		for row in range(0,height):
			print("painting in row {0} of {1}...".format(row, height))
			for col in range (0,width):
				if col >= c1 and col <= c2:
					if row >= r1 and row <= r2:
						if not SC.HSM.setValue(row, col,val, True):
							print("""WARNING: failed to paint value at {0},{1} 
								  to {2}""".format(row, col, val))


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
		for i in reversed(range(0, SC.HSM.contents['nzentries'])):
			if SC.HSM.contents['row'][i] >= height:
				SC.HSM.setValue(SC.HSM.contents['row'][i], 
								SC.HSM.contents['col'][i], 0)
			elif SC.HSM.contents['col'][i] >= width:
				SC.HSM.setValue(SC.HSM.contents['row'][i], 
								SC.HSM.contents['col'][i], 0)

		SC.HSM.contents['height'] = height
		SC.HSM.contents['width'] = width 

		print("Updated matrix dimensions. New values:")
		main("info")


	elif command == 'setsym':
		if len(arguments) != 1:
			print("ERROR: incorrect number of arguments")
			return 

		validOptions = ['SYM','ASYM','asymmetric','symmetric',
		'symmetrical','asymmetrical'] 

		if arguments[0] not in validOptions:
			print("ERROR: argument {0} is not a valid symmetry option, Valid ")
			print("options are: ")
			pp.pprint(validOptions)
			return 

		if arguments[0] in ['SYM','symmetric','symmetrical']:
			symmetry = 'SYM'
		else:
			symmetry = 'ASYM'

		SC.HSM.contents['symmetry'] = symmetry

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

		SC.HSM.contents['nzentries'] = 0
		SC.HSM.contents['row'] = []
		SC.HSM.contents['col'] = []
		SC.HSM.contents['val'] = []
		main("setdims {0} {1}".format(height, width))
		for i in range(0, height): # this is faster than using paint
			for j in range(0,width): 
				SC.HSM.contents['val'].append(val)
				SC.HSM.contents['col'].append(j)
				SC.HSM.contents['row'].append(i) 
		SC.HSM.contents['nzentries'] = len(SC.HSM.contents['val'])
		SC.HSM.contents['symmetry'] = 'ASYM' 
		SC.HSM.contents['remarks'] = []

		print("finished initializing matrix, new matrix info:")
		main("info")



	elif command == 'shell':
		print("Entering python interactive debug shell...")
		print("Enter \"runMain()\" to return to normal execution")
		import pdb
		pdb.set_trace()


	elif command == 'gen-verification':
		newSum = SC.HERCMIO.generateVerificationSum(SC.HSM.contents)
		SC.HSM.contents['verification'] = newSum 
		print("updated verification sum to: {0}".format(newSum))

	else:
		print("ERROR: Command not recognized") 
	


def runMain():
	while True:
		main()

print("welcome to HeRCM Explorer. Enter \"help\" for help")
SC = libSparseConvert.sparseConvert()
runMain()