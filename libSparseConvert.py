# permits IO and conversion on various sparse matrix formats.
import libhsm 
import clogs
import scipy
import numpy
import scipy.io
from numpy.lib.recfunctions import append_fields
import traceback
import pprint 

class HercmioValidationError(Exception):
	pass

class hercmio:
	# permits IO on HeRCM files 
	def __init__(this, logger=None):
		# logger may optionally by an existing instance of clogs.clogs 
		if logger == None:
			this.logger = clogs.clogs() 
		else:
			this.logger = logger

		this.logger.log('new hercmio instance instantiated')

	def read(this, filename):
		# reads in the HeRCM file specified by filename 
		# returns it as an instance of libhsm.hsm

		HSM = libhsm.hsm()
		contents = {}

		this.logger.log("Reading HeRCM file {0}".format(filename))

		try:
			fileObject = open(filename, 'r')
		except FileNotFoundError: 
			this.logger.log("could not open file: file not found (31)", "error")
			raise FileNotFoundError("could not open file: {0} no such file"
									.format(filename))
		except PermissionError: 
			this.logger.log("could not open file: permissions error (34)", 
							"error")
			raise PermissionError("could not open file: {0}, permission denied"
								  .format(filename))

		lines = fileObject.readlines() 
		fileObject.close() 

		# read in the header
		header = lines[0]
		lines.pop(0)
		splitHeader = header.split() 

		if len(splitHeader) != 6:
			this.logger.log("invalid header: too few fields (46)","error")
			raise HercmioValidationError("header contains too few fields")

		if splitHeader[0] != 'HERCM':
			this.logger.log("could not read file, not a HeRCM file (50)", 
						    "error")
			raise HercmioValidationError("header does not contain HeRCM") 
		try:
			width = int(splitHeader[1])
			height = int(splitHeader[2])
			nzentries = int(splitHeader[3])
			verification = float(splitHeader[5])
		except ValueError:
			this.logger.log("could not read file, mangled header (57)", "error")
			raise HercmioValidationError("Could not extract values from header")

		symmetry = splitHeader[4]
		if symmetry not in ['SYM','ASYM']:
			raise HercmioValidationError("header contains invalid symmetry")
		

		HSM.width 		= width
		HSM.height 		= height
		HSM.nzentries	= nzentries 
		HSM.symmetry	= symmetry
		HSM.verification = verification
		

		contents['width'] = width
		contents['height'] = height
		contents['nzentries'] = nzentries 
		contents['symmetry'] = symmetry
		contents['verification'] = verification
		contents['val'] = []
		contents['col'] = []
		contents['row'] = []

		inField 	    = False
		currentHeader   = ''
		fieldname	    = ''
		ctype		    = ''
		vtype 		    = ''
		currentContents = []
		for line in lines:
			if not inField:
				currentHeader = line.rstrip() 
				splitHeader   = currentHeader.split()
				fieldname 	  = splitHeader[0]
				ctype 		  = splitHeader[1]
				vtype 		  = splitHeader[2]
				inField = True
			elif 'ENDFIELD' in line:
				inField = False 
				contents[fieldname.lower()] = currentContents 
				currentContents = []
				inField = False 
			else:
				if ctype == 'SINGLE':
					if vtype == 'INT':
						try:
							currentContents = int(line)
						except ValueError:
							this.logger.log("could not read file: bad vtype " +
											"99", "error")
							return None 
					elif vtype == 'FLOAT':
						try:
							currentContents = float(line)
						except ValueError:
							this.logger.log("could not read file: bad vtype " + 
											"(104)", "error")
							return None 
					else: 
						currentContents = line.rstrip() 
				elif ctype == 'LIST':
					for value in line.split():
						
						if vtype == 'INT':
							try:
								currentContents.append(int(value))
							except ValueError:
								this.logger.log("could not read file: bad vtype " +
												"(115)", "error")
								return None 
						elif vtype == 'FLOAT':
							try:
								currentContents.append(float(value))
							except ValueError:
								this.logger.log("could not read file: bad vtype " + 
												"(115)", "error")
								return None
						else: 
							currentContents.append(value)
				else:
					this.logger.log("could not read file: bad cytpe (125)",
									"error")
					return None 

		for field in ['val','col','row','nzentries','width','height','symmetry',
					  'verification']:
			if field not in contents:
				this.logger.log("read file, but needed field {0} missing (136)"
								.format(field), 'error')
				raise HercmioValidationError("field {0} is missing from file"
											 .format(field)) 

		for field in ['row','val','col']:
			if len(contents[field]) != HSM.nzentries:
				this.logger.log("length of {0} {1} does not match nzentries {2}"
					.format(field, 
						len(contents[field]), 
						HSM.nzentries), 
					'warning')

		for i in range(0,HSM.nzentries):
			try:
				HSM.addElement([contents['row'][i],
								contents['col'][i],
								contents['val'][i]])
			except IndexError:
				this.logger.log("""could not add index {0} of contents to HSM 
 instance. Nzentries is {1} and len val is {2}""".format(i, HSM.nzentries, 
								len(contents['val'])),'warning')
				raise IndexError("Unable to add index {0} to HSM".format(i))
		
		if this.verify(contents): 
			return HSM
		else: 
			this.logger.log("verification failed (155)", "error")
			return None 

	def generateVerificationSum(this,hercm):
		# returns the verification sum of hercm
		# hercm should be in the format: 

		# {'col': [4, 4, 3, 2, 1, 4, 2, 1],
	    # 'height': 5,
	    # 'nzentries': 8,
	    # 'remarks': [],
	    # 'row': [4, 3, 3, 4, 1, 1, 2, 4],
	    # 'symmetry': 'ASYM',
	    # 'val': [8.0, 7.0, 5.0, 3.0, 4.0, 2.0, 1.0, 6.0],
	    # 'verification': 7.0,
	    # 'width': 5}

	    # hercm may also be an instance of libhsm.hsm 

		if type(hercm) == dict:
			fields = ['val','col','row']
			sum = 0
			for field in fields:
				try:
					for value in hercm[field]:
						sum += value 
				except KeyError as e:
					this.logger.log("could not verify, missing field (157)",
						"error")
					raise KeyError("missing field... ",str(e))
				except TypeError as e:
					this.logger.log("could not verify, mangled field (159)",
									"error")
					raise TypeError("one or more fields is of invalid type",
									str(e))
	
			return sum % float(len(hercm['val']))
		else:
			val = hercm.elements['val']
			row = hercm.elements['row']
			col = hercm.elements['col'] 

			return this.generateVerificationSum({'val':val, 'row':row,'col':col})
		
		

	def verify(this, hercm):
		# verifies the hercm provided 
		# hercm should be the same dict format as generateVerificationSum()
		# hercm may also be an instance of libhsm.hsm

		# returns True of the hercm is valid
		# returns False if it is not 
		# returns None if an error is encountered 

		this.logger.log("verifying HeRCM...")

		if type(hercm) == dict:
			try:
				verification = this.generateVerificationSum(hercm)
			except KeyError as e:
				raise KeyError("failed to generate verification sum... ",str(e))
				return None 
			except TypeError as e:
				raise TypeError("failed to generate verification sum... ",str(e))
				return None
	
			try: 
				if verification == hercm['verification']:
					this.logger.log("verification passed")
					return True
				else:
					this.logger.log("verification failed, expected {0}, got {1}"
									.format(hercm['verification'], verification))
					return False 
			except ValueError as e:
				this.logger.log("could not verify, mangled field (165)", "error")
				raise ValueError("Could not verify, mangled field...",str(e))
				return None 
			except KeyError:
				this.logger.log("could not verify, missing field (168)", "error")
				raise KeyError("could not verify, missing field...",str(e))
				return None 
		else:
			try:
				verification = this.generateVerificationSum(hercm)
			except KeyError as e:
				raise KeyError("failed to generate verification sum... ",str(e))
				return None 
			except TypeError as e:
				raise TypeError("failed to generate verification sum... ",str(e))
				return None

			return hercm.verification == verification

	def write(this, HSM, filename):
		# HSM should be an instance of libhsm.hsm 
		# fileame is the string path to the file to write
		# writes a hercm file with contents matching hercm to filename 


		this.logger.log("writing file {0}".format(filename))

		try:
			fileObject = open(filename, 'w')
		except FileNotFoundError as e: 
			this.logger.log("could not open file: file not found (207)","error")
			raise FileNotFoundError("could not open file {0}... "
									.format(filename), str(e))
		except PermissionError as e: 
			this.logger.log("could not open file: permissions error (210)", 
							"error")
			raise PermissionError("Could not open file {0}..."
								  .format(filename), str(e)) 

		if not this.verify(HSM): 
			this.logger.log("verification failed (217)", "warning")
			raise HercmioValidationError("matrix did not pass validation")
			

		header = 'HERCM '
		header = header + str(HSM.width) + ' '
		header = header + str(HSM.height) + ' '
		header = header + str(HSM.nzentries) + ' '
		header = header + str(HSM.symmetry) + ' '
		header = header + str(HSM.verification) + '\n'

		this.logger.log("generated header: {0}".format(header))

		fileObject.write(header)

		fileObject.write('REMARKS LIST STRING\n')
		itemcounter = 0
		line = ''
		for item in HSM.remarks:
			line = line + item + ' '
			itemcounter += 1
			if itemcounter == 9:
				fileObject.write(line+'\n')
				line = '' 
				itemcounter = 0
		if itemcounter > 0:
			fileObject.write(line+'\n')
		fileObject.write('ENDFIELD\n')

		fileObject.write('VAL LIST FLOAT\n')
		itemcounter = 0
		line = ''
		for item in HSM.elements['val']:
			line = line + str(item) + ' '
			itemcounter += 1
			if itemcounter == 9:
				fileObject.write(line+'\n')
				line = '' 
				itemcounter = 0
		if itemcounter > 0:
			fileObject.write(line+'\n')
		fileObject.write('ENDFIELD\n')

		fileObject.write('ROW LIST INT\n')
		itemcounter = 0
		line = ''
		for item in HSM.elements['row']:
			line = line + str(item) + ' '
			itemcounter += 1
			if itemcounter == 9:
				fileObject.write(line+'\n')
				line = '' 
				itemcounter = 0
		if itemcounter > 0:
			fileObject.write(line+'\n')
		fileObject.write('ENDFIELD\n')

		fileObject.write('COL LIST INT\n')
		itemcounter = 0
		line = ''
		for item in HSM.elements['col']:
			line = line + str(item) + ' '
			itemcounter += 1
			if itemcounter == 9:
				fileObject.write(line+'\n')
				line = '' 
				itemcounter = 0
		if itemcounter > 0:
			fileObject.write(line+'\n')
		fileObject.write('ENDFIELD\n')

		fileObject.close() 

class SparseConvertFormatError:
	pass

class sparseConvert:
	def __init__(this, logger=None):
		# if a clogs.clogs instance is given as logger, it will be used for 
		# logging. Otherwise, a new clogs.clogs instance will be created 

		this.HSM = libhsm.hsm() 
		
		if logger == None:
			this.logger = clogs.clogs() 
		else:
			this.logger = logger 

		this.HERCMIO = hercmio(this.logger)


	def readMatrix(this, filename, form):
		# filename is the string path to the matrix file to open
		# format is the string 'hercm' or 'mtx' specifying matrix format 

		# reads the matrix into this.HSM for later processing 
		# converts non-hercm matrices to hercm internally 

		# verbose will cause the progress of reading the matrix to be printed 
 

		this.logger.log("reading matrix {0} which is format {1}"
					 	.format(filename, form))

		if form == 'hercm':
			matrix = None 
			try:
				matrix = this.HERCMIO.read(filename)
			except Exception as e:
				print("ERROR: could not read matrix")
				print("stack trace...")
				print(traceback.format_exc())
				print("log...")
				pp = pprint.PrettyPrinter()
				pp.pprint(this.logger.contents)

			this.HSM = matrix
			this.HSM.nzentries = len(this.HSM.elements['val'])

		elif form == 'mtx':
			from scipy import io
			from scipy.sparse import csr_matrix 
			from numpy import array
	
			# reads in an MTX file and converts it to hercm 
	
			try:

				
				rawMatrix = scipy.sparse.coo_matrix(scipy.io.mmread(filename)) 
	
				if 'symmetric' in io.mminfo(filename):
					this.HSM.symmetry = "SYM"
				else:
					this.HSM.symmetry = "ASYM"

				hercm = {} # needed to generate verification 
	
				hercm['val'] 			= rawMatrix.data
				hercm['col'] 			= rawMatrix.col.tolist()
				hercm['row'] 			= rawMatrix.row.tolist()
				(matrixWidth, matrixHeight) = rawMatrix.shape
				this.HSM.height			= int(matrixHeight)
				this.HSM.width 			= int(matrixWidth)
				vs = this.HERCMIO.generateVerificationSum(hercm)
				this.HSM.verification   = vs 
				this.HSM.remarks		= []


				# I'm not sure why this has to be hard...
				# http://stackoverflow.com/questions/26018781/numpy-is-it-possible-to-preserve-the-dtype-of-columns-when-using-column-stack

				val = numpy.asarray(hercm['val'], dtype='float64')
				col = numpy.asarray(hercm['col'], dtype='int32')
				row = numpy.asarray(hercm['row'], dtype='int32')

				val = numpy.rec.array(val, dtype=[(('val'), numpy.float64)])
				col = numpy.rec.array(col, dtype=[(('col'), numpy.int32)])
				row = numpy.rec.array(row, dtype=[(('row'), numpy.int32)])

				this.HSM.elements = append_fields(row, 'col', col, usemask = False, dtypes=[numpy.int32])
				this.HSM.elements = append_fields(this.HSM.elements, 'val', val, usemask = False, dtypes=[numpy.float64])

				
				this.HSM.nzentries = len(this.HSM.elements['val'])
				
					
			except IOError as e: # make sure the file exists and is readable
				this.logger.log("could not open matrix file (375)", "error")
				raise IOError("could not open matrix file for writing...",
							  str(e))
			

		else:
			this.logger.log("format must be hercm or mtx, cannot use format {0}"
							.format(form), "error")
			raise SparseConvertFormatError("{0} is not a valid format"
											.format(form))
		this.logger.log("converting matrix to row major format...")
		this.HSM.makeRowMajor()

		if this.HSM.symmetry == 'SYM':
			this.HSM.makeSymmetrical('truncate') 


	def writeMatrix(this, filename, form):
		# writes this.HSM to the file 
		# filename is a string indicating path of file
		# format is a string indicating file format (mtx or hercm)
		# returns True on success, None on failure

		if this.HSM.symmetry == 'SYM':
			this.HSM.makeSymmetrical('truncate')
		
		this.logger.log("writing matrix to file {0} in format {1}"
						.format(filename, format))

		this.logger.log("converting matrix to row majro format...")
		this.HSM.makeRowMajor()

		if form == 'hercm':
			try:
				this.HERCMIO.write(this.HSM, filename)
			except HercmioValidationError:
				print("ERROR: matrix did not pass validation!")
				print("Matrix will not be written to file")
			

		elif form == 'mtx':
			print("WARNING: scipy.io.mmwrite does not support writing mtx ")
			print("matrices in symmetric mode! Matrix will be converted to ")
			print("Asymmetric! ")
	
			try:
				scipy.io.mmwrite(filename, this.HSM.getInFormat('coo'))
			except ValueError as e: 
				this.logger.log("""encountered ValueError exception while
 writing file. Exception: {0}. You probably have out of bounds indices in row or
 col""".format(e), 'error')
			except Exception as e:
				this.logger.log("encountered exception while writing" +
								" matrix: {0} (412)".format(str(e)),'error')
				raise IOError("encountered exception while writing matrix")
	
		else:
			this.logger.log("format must be hercm or mtx, cannot use format {0}"
							.format(form), 'error')
			raise SparseConvertFormatError("{0} is not a valid format"
											.format(form))


