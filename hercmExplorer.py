#!/usr/bin/python3
# utility for exploring and editing the contents of hercm matrix files 

import libhsm
import libmtxio
import readline

MTXIO = None 
helpString = """- HeRCM Explorer Help -
help - display this message

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

range [x1] [y1] [x2] [y2] - prints all elements, zero or nonzero, which lie 
between the upper left bound [x1],[y1], and the lower right bound [x2],[y2]

touch [row] [col] [val] - changes the value at [row] [col] to [val] 

paint [x1] [y1] [x2] [y2] [val] - works the same way as range, but changes
all values encountered to [val]

exit - exits the program
"""

def main():
	usrIn = input("> ")

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

	elif command == 'load':
		if len(arguments) != 2:
			print("ERROR: incorrect number of arguments")
			return
		fileName = arguments[0]
		fileFormat = arguments[1] 
		print("Loading the file {0} which is {1} format".format(fileName, 
																fileFormat)) 
		if fileFormat == 'mtx':
			try:
				status = MTXIO.readMtx(fileName)
				if status != MTXIO.STATUS_SUCCESS:
					print("""WARNING: an error was encountered while loading the 
file""")
			except Exception as e:
				print("""ERROR: could not load file, the exception {0} was 
encountered""".format(str(e)))
		elif fileFormat == 'hercm':
			try:
				status = MTXIO.readHercm(fileName)
				if status != MTXIO.STATUS_SUCCESS:
					print("""WARNING: an error was encountered while loading the 
file""")
			except Exception as e:
				print("""ERROR: could not load file, the exception {0} was 
encountered""".format(str(e)))
		else:
			print("ERROR: file format must be mtx or hercm")

	elif command == 'write':
		if len(arguments) != 2:
			print("ERROR: incorrect number of arguments")
			return
		fileName = arguments[0]
		fileFormat = arguments[1]
		print("Writing {0} in format {1}".format(fileName, fileFormat))

		if fileFormat == 'mtx':
			try: 
				status = MTXIO.writeMtx(fileName)
				if status != MTXIO.STATUS_SUCCESS:
					print("""WARNING: an error was encountered while loading the 
file""")
			except Exception as e:
				print("""ERROR: could not write file, the exception {0} was 
encountered""".format(str(e)))
		elif fileFormat == 'hercm':
			try: 
				status = MTXIO.writeHercm(fileName)
				if status != MTXIO.STATUS_SUCCESS:
					print("""WARNING: an error was encountered while loading the 
file""")
			except Exception as e:
				print("""ERROR: could not write file, the exception {0} was 
encountered""".format(str(e)))
		else:
			print("ERROR: file format must be mtx or hercm")

	elif command == 'info':
		height    = MTXIO.hercm['height']
		width     = MTXIO.hercm['width']
		nzentries = MTXIO.hercm['nzentries']
		symmetry  = MTXIO.hercm['symmetry']

		print("""- matrix properties -
height (number of rows) - {0}
width (number of cols)  - {1}
non zero elements - - - - {2} 
symmetry  - - - - - - - - {3}
- end matrix properties -""".format(height, width, nzentries, symmetry)) 

	elif command == 'display':
		matrix = None
		try:
			matrix = MTXIO.HSM.getScipyCSR()
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
		if MTXIO.hercm['nzentries'] > 25:
			print("WARNING: matrix contains more than 25 entries, ")
			print("are you sure you wish to proceed?")
			if input('(yes/no)> ').upper() != "YES":
				return

		print("val:"      ,MTXIO.hercm['val'])
		print("row_ptr:"  ,MTXIO.hercm['row_ptr'])
		print("colind:"   ,MTXIO.hercm['colind'])
		print("nzentries:",MTXIO.hercm['nzentries'])

	elif command == 'raw':
		import pprint
		pp = pprint.PrettyPrinter()
		pp.pprint(MTXIO.hercm)

	elif command == 'value':
		if len(arguments) != 2:
			print("ERROR: incorrect number of arguments")
			return

		row = int(arguments[0])
		col = int(arguments[1])
		print("value of {0},{1}:".format(row, col), 
			  MTXIO.HSM.getValue(row, col))

	else:
		print("ERROR: Command not recognized") 
	



print("welcome to HeRCM Explorer. Enter \"help\" for help")
MTXIO = libmtxio.mtxio() 
while True:
	main()