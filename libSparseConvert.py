# permits IO and conversion on various sparse matrix formats.
import libhsm 
import clogs
import scipy
import numpy

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
		# reads the HeRCM file specified by the string filename and stores it as
		# a dict 

		# example: 
		# {'col': [4, 4, 3, 2, 1, 4, 2, 1],
	    # 'height': 5,
	    # 'nzentries': 8,
	    # 'remarks': [],
	    # 'row': [4, 3, 3, 4, 1, 1, 2, 4],
	    # 'symmetry': 'ASYM',
	    # 'val': [8.0, 7.0, 5.0, 3.0, 4.0, 2.0, 1.0, 6.0],
	    # 'verification': 7.0,
	    # 'width': 5}

		# returns None on error 

		contents = {} 

		this.logger.log("Reading HeRCM file {0}".format(filename))

		try:
			fileObject = open(filename, 'r')
		except FileNotFoundError: 
			this.logger.log("could not open file: file not found (31)", "error")
			return None
		except PermissionError: 
			this.logger.log("could not open file: permissions error (34)", 
							"error")
			return None 

		lines = fileObject.readlines() 
		fileObject.close() 

		# read in the header
		header = lines[0]
		lines.pop(0)
		splitHeader = header.split() 

		if len(splitHeader) != 6:
			this.logger.log("invalid header: too few fields (46)","error")
			return None

		if splitHeader[0] != 'HERCM':
			this.logger.log("could not read file, not a HeRCM file (50)", 
						    "error")
			return None 
		try:
			width = int(splitHeader[1])
			height = int(splitHeader[2])
			nzentries = int(splitHeader[3])
			verification = float(splitHeader[5])
		except ValueError:
			this.logger.log("could not read file, mangled header (57)", "error")
		symmetry = splitHeader[4]
		

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
		currentContents = None
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
				currentContents = None
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
					currentContents = []
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
				return None 
		
		if this.verify(contents): 
			return contents
		else: 
			this.logger.log("verification failed (155)", "error")
			return None 

	def generateVerificationSum(this,hercm):
		# returns the verification sum of hercm
		# hercm should be the same format as the return  of read()

		fields = ['val','col','row']
		sum = 0
		for field in fields:
			try:
				for value in hercm[field]:
					sum += value 
			except KeyError:
				this.logger.log("could not verify, missing field (157)","error")
				return None
			except TypeError:
				this.logger.log("could not verify, mangled field (159)","error")
				return None 

		return sum % float(hercm['nzentries'])
		
		

	def verify(this, hercm):
		# verifies the hercm provided 
		# hercm should be formatted the same way as the return value of read()

		# returns True of the hercm is valid
		# returns False if it is not 
		# returns None if an error is encountered 

		this.logger.log("verifying HeRCM...")


		

		verification = this.generateVerificationSum(hercm)
		if verification == None: 
			this.logger.log("could not generate verification sum (195)",'error')
			return None 

		try: 
			if verification == hercm['verification']:
				this.logger.log("verification passed")
				return True
			else:
				this.logger.log("verification failed, expected {0}, got {1}"
								.format(hercm['verification'], verification))
				return False 
		except ValueError:
			this.logger.log("could not verify, mangled field (165)", "error")
			return None 
		except KeyError:
			this.logger.log("could not verify, missing field (168)", "error")

	def write(this, hercm, filename):
		# hercm should be in the same format as the return value of read() 
		# fileame is the string path to the file to write
		# writes a hercm file with contents matching hercm to filename 

		# returns True on success, and None on failure 

		this.logger.log("writing file {0}".format(filename))

		try:
			fileObject = open(filename, 'w')
		except FileNotFoundError: 
			this.logger.log("could not open file: file not found (207)","error")
			return None
		except PermissionError: 
			this.logger.log("could not open file: permissions error (210)", 
							"error")
			return None 

		if not this.verify(hercm): 
			this.logger.log("verification failed (217)", "error")
			return None 


		header = 'HERCM '
		header = header + str(hercm['width']) + ' '
		header = header + str(hercm['height']) + ' '
		header = header + str(hercm['nzentries']) + ' '
		header = header + str(hercm['symmetry']) + ' '
		header = header + str(hercm['verification']) + '\n'

		this.logger.log("generated header: {0}".format(header))

		fileObject.write(header)

		fileObject.write('REMARKS LIST STRING\n')
		itemcounter = 0
		line = ''
		for item in hercm['remarks']:
			line = line + item + ' '
			itemcounter += 1
			if itemcounter == 9:
				fileObject.write(line+'\n')
				line = '' 
				itemcounter = 0
		fileObject.write(line+'\n')
		fileObject.write('ENDFIELD\n')

		fileObject.write('VAL LIST FLOAT\n')
		itemcounter = 0
		line = ''
		for item in hercm['val']:
			line = line + str(item) + ' '
			itemcounter += 1
			if itemcounter == 9:
				fileObject.write(line+'\n')
				line = '' 
				itemcounter = 0
		fileObject.write(line+'\n')
		fileObject.write('ENDFIELD\n')

		fileObject.write('ROW LIST INT\n')
		itemcounter = 0
		line = ''
		for item in hercm['row']:
			line = line + str(item) + ' '
			itemcounter += 1
			if itemcounter == 9:
				fileObject.write(line+'\n')
				line = '' 
				itemcounter = 0
		fileObject.write(line+'\n')
		fileObject.write('ENDFIELD\n')

		fileObject.write('COL LIST INT\n')
		itemcounter = 0
		line = ''
		for item in hercm['col']:
			line = line + str(item) + ' '
			itemcounter += 1
			if itemcounter == 9:
				fileObject.write(line+'\n')
				line = '' 
				itemcounter = 0
		fileObject.write(line+'\n')
		fileObject.write('ENDFIELD\n')

		fileObject.close() 
		return True 


class sparseConvert:
	def __init__(this, logger=None):
		# if a clogs.clogs instance is given as logger, it will be used for 
		# logging. Otherwise, a new clogs.clogs instance will be created 

		this.HSM = libhsm.hsm() 
		this.hercm = this.HSM.contents
		
		if logger == None:
			this.logger = clogs.clogs() 
		else:
			this.logger = logger 

		this.HERCMIO = hercmio(this.logger)

	def readMatrix(this, filename, format):
		# filename is the string path to the matrix file to open
		# format is the string 'hercm' or 'mtx' specifying matrix format 

		# reads the matrix into this.HSM for later processing 
		# converts non-hercm matrices to hercm internally 

		# returns None on failure, True on success 

		this.logger.log("reading matrix {0} which is format {1}"
					 	.format(filename, format))

		if format == 'hercm':
			matrix = this.HERCMIO.read(filename)
			if matrix == None:
				this.logger.log("could not read matrix, general failure (319)",
								"error")
				return None 
			this.logger.log("finished reading matrix")
			this.HSM.contents = matrix 
			return True 
		
		elif format == 'mtx':
			from scipy import io
			from scipy.sparse import csr_matrix 
			from numpy import array
	
			# reads in an MTX file and converts it to hercm 
	
			# returns STATUS_SUCCESS or STATUS_ERROR
	
			try:

				rawMatrix = scipy.sparse.coo_matrix(scipy.io.mmread(filename)) 
	
				this.hercm['val'] 			= rawMatrix.data.tolist()
				this.hercm['col'] 			= rawMatrix.col.tolist()
				this.hercm['row'] 			= rawMatrix.row.tolist()
				(matrixWidth, matrixHeight) = rawMatrix.shape
				this.hercm['height'] 		= int(matrixHeight)
				this.hercm['width'] 		= int(matrixWidth)
				this.hercm['symmetry'] 		= "ASYM"
				this.hercm['nzentries']     = len(this.hercm['val'])
				vs = this.HERCMIO.generateVerificationSum(this.hercm)
				this.hercm['verification']  = vs 
				this.hercm['remarks']		= []
				
				if 'symmetric' in io.mminfo(filename):
					this.hercm['symmetry'] = "SYM"
	
					list_to_delete = []
	
					"""
					# This code thanks to Steve Rubin
					# deletes duplicate values in lower triangle
					for i in range(0, len(matrix_numbers_list)):
						element_column = matrix_numbers_list[i][1]
						element_row = matrix_numbers_list[i][0]
						element_value = matrix_numbers_list[i][2]
						for j in range ((i+1), len(matrix_numbers_list)):
							if(matrix_numbers_list[j][1] == element_row and matrix_numbers_list[j][0] == element_column 
								and matrix_numbers_list[j][2] == element_value):
								list_to_delete.append(j)
								
						
					print ""
					#ERROR HERE: with indexes
					for i in range(0, len(list_to_delete)):
						print "deleting " + str(matrix_numbers_list[list_to_delete[i]]) + " as the value has a duplicate"
						del matrix_numbers_list[list_to_delete[i]]
						number_of_nnz_deleted += 1 
					
					"""
	
			except IOError: # make sure the file exists and is readable
				this.logger.log("could not open matrix file (375)", "error")
				return None
			return True

		else:
			this.logger.log("format must be hercm or mtx, cannot use format {0}"
							.format(format), "error")
			return None 


	def writeMatrix(this, filename, format):
		# writes this.HSM to the file 
		# filename is a string indicating path of file
		# format is a string indicating file format (mtx or hercm)
		# returns True on success, None on failure
		this.logger.log("writing matrix to file {0} in format {1}"
						.format(filename, format))
		if format == 'hercm':
			if not this.HERCMIO.write(this.hercm, filename):
				this.logger.log("could not write matrix, general failure" +
								" (395)","error")
				return None 
			else:
				this.logger.log("wrote matrix successfully") 
				return True 
		elif format == 'mtx':
			from scipy import io
			from scipy.sparse import csr_matrix 
			from numpy import array	
	
			try:
				scipy.io.mmwrite(filename, this.HSM.getInFormat('coo'))
			except Exception as e:
				this.logger.log("encountered exception while wiriting" +
								" matrix {0} (412)".format(str(e),'error'))
				return None
	
			return True 
		else:
			this.logger.log("format must be hercm or mtx, cannot use format {0}"
							.format(format), 'error')
			return None 


