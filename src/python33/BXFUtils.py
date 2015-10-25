# this file provides the functions used by BXFExplorer

import readline
import libHercMatrix
import libHercmIO
import matplotlib
import matplotlib.pyplot
import logging
import os
import textwrap

def printHelp(commandInfo, command=None):
	if command == None:
		for c in commandInfo:
			printHelp(commandInfo, c)
	else:
		if command not in commandInfo:
			print("Sorry, no help is available for this command")
			return 

		print("-"*40)
		print(command, end='')

		if commandInfo[command]['requiredArguments'] != None:
			for arg in commandInfo[command]['requiredArguments']:
				print(' ['+arg[2]+'] ', end='')
		if commandInfo[command]['optionalArguments'] != None:
			for arg in commandInfo[command]['optionalArguments']:
				print(' ('+arg[2]+') ', end='')
		print("\n-- arguments --")
		argCounter = 0
		if commandInfo[command]['requiredArguments'] != None:
			for arg in commandInfo[command]['requiredArguments']:
				print('    ['+arg[2]+'] ' + str(arg[1]) + ' - ' + ' ' +
					commandInfo[command]['argumentInfo'][argCounter])
				argCounter += 1
		if commandInfo[command]['optionalArguments'] != None:
			for arg in commandInfo[command]['optionalArguments']:
				print('    ('+arg[2]+') - ' + str(arg[1]) + ' ' +
					commandInfo[command]['argumentInfo'][argCounter])
				argCounter += 1
		print("-- use --")
		for line in textwrap.wrap(commandInfo[command]['help']):
			print('    ' + line)




def load(filename, form, HERCMIO):
	# load filename, which is format format 
	# HERCMIO should be the LibHercmIO.hercmIO instance to load the matrix into

	if form not in ['bxf','hercm','mat','mtx']:
		raise KeyError("format {0} is not supported".format(form))

	print("Loading matrix...")
	HERCMIO.readMatrix(filename, form)
	print("Finished loading matrix.")


def write(filename, form, HERCMIO):
	# write matrix stored in HERCMIO instance to filename in given format

	if form not in ['bxf','hercm','mat','mtx']:
		raise KeyError("format {0} is not supported".format(form))
	print("Writing matrix...")
	HERCMIO.writeMatrix(filename, form)
	print("Finished writing matrix.")
		

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
					

def setDims(height, width, HERCMATRIX):
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



def setSymmetry(newSymmetry, HERCMATRIX, method="truncate"):
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

def initilize(height, width, HERCMATRIX, val = 0):
	# initializes a blank matrix height x width in size in the HERCMATRIX instance
	# optionally sets all elements in the matrix equal to val

	setDims(0,0,HERCMATRIX)
	setDims(height, width, HERCMATRIX)

	for i in range(0, height): # this is faster than using paint
		for j in range(0,width): 
			HERCMATRIX.setValue(i, j, val)
	if HERCMATRIX.elements == None:
		SC.HSM.nzentries = 0
	else:
		SC.HSM.nzentries = len(HERCMATRIX.elements['val'])
	HERCMATRIX.symmetry = 'ASYM' 
	HERCMATRIX.remarks = []

def generateVerification(BXFIO, HERCMATRIX):
	# updates verification sum of matrix 
	newSum = BXFIO.generateVerificationSum(HERCMATRIX)
	HERCMATRIX.verification = newSum 

def plot(HERCMATRIX):
	# plots the matrix with matplotlib
	matrix = HERCMATRIX.getInFormat('coo')
		
	matplotlib.pyplot.spy(matrix)
	matplotlib.pyplot.show()


def printDirectoryListing(directory=None):
	# prints a directory listing of directory, of cwd if directory=None
	if directory != None:
		if os.path.exists(directory):
			pass 
		elif os.path.exists(os.path.join(os.getcwd(), directory)):
			directory = os.path.join(os.getcwd(), directory)
		else:
			print("ERROR: could not get directory listing")
			print(directory, " is not a valid path")
			print(os.path.join(os.getcwd(), directory), 
				" is not a valid path")
			directory = os.getcwd()
	else:
		directory = os.getcwd()

	print("Directory listing for: ", directory)
	for item in os.listdir(directory):
		print(item)

def printWorkingDirectory():
	# prints the CWD
	
	print(os.getcwd())

def head(path, numlines=10):
	# prints the first numlines of file at path
	print("First {0} lines of file {1}".format(numlines, path))
	f = open(path)
	for line in f.readlines()[0:numlines]:
		print(line, end='')

def cat(path):
	# prints all lines in file at path

	print("Contents of file {0}".format(path))
	f = open(path)
	for line in f.readlines():
		print(line, end='')

def changeDirectory(newDir):
	# changes cwd to newDir
	if not os.path.exists(newDir):
		print("ERROR: cannot cd to nonexistent path")
		return 
	if os.path.isfile(newDir):
		print("ERROR: {0} is not a directory".format(arguments[0]))
		return
	os.chdir(newDir)

def convert(source, destination, sourceFormat, destinationFormat):
	# converts the matrix at source in sourceFormat to destinationFormat
	# then writes out at destination

	if not os.path.exists(source):
		print("ERROR: load from nonexistent path")
		return 
	if not os.path.isfile(source ):
		print("ERROR: {0} is not a file".format(source))
		return
	HERCMATRIX = libHercMatrix.hercMatrix()
	BXFIO = libBXF.bxfio()
	HERCMIO = libHercmIO.hercmIO()
	HERCMIO.HSM = HERCMATRIX
	HERCMIO.HERCMIO = BXFIO

	generateVerification(BXFIO, HERCMATRIX)
	write(destination, destinationFormat, HERCMIO)
