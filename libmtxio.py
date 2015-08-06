# wrapper for scipy mtx io functions
# can convert between mtx and hercm
import libhsm 



class mtxio:
	STATUS_ERROR = "MTXIO_STATUS_ERROR"
	STATUS_SUCCESS = "MTXIO_STATUS_SUCCESS"

	def __init__(this):
		this.HSM = libhsm.hsm()
		this.hercm = this.HSM.contents 
	
	def readMtx(this, filename):
		from scipy import io
		from scipy.sparse import csr_matrix 
		from numpy import array

		# reads in an MTX file and converts it to hercm 

		# returns STATUS_SUCCESS or STATUS_ERROR

		try:
			rawMatrix = csr_matrix(io.mmread(filename)) 

			this.hercm['val'] 			= rawMatrix.data.tolist()
			this.hercm['colind'] 		= rawMatrix.indices.tolist()
			this.hercm['row_ptr'] 		= rawMatrix.indptr.tolist()
			(matrixWidth, matrixHeight) = rawMatrix.shape
			this.hercm['height'] 		= int(matrixHeight)
			this.hercm['width'] 		= int(matrixWidth)
			this.hercm['symmetry'] 		= "ASYM"
			this.hercm['nzentries']     = len(this.hercm['val'])
			
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
				
				
							return this.STATUS_SUCCESS
				"""

		except IOError: # make sure the file exists and is readable
			return this.STATUS_ERROR
		return this.STATUS_SUCCESS

	def writeHercm(this, filename, hercm=None):
		# writes the hercm file contents in hercm to the hercm file filename
		# if hercm is not given, this.hercm is used instead 

		# returns STATUS_SUCCESS or STATUS_ERROR

		with open(filename,'w') as fileObject:
			if hercm == None:
				hercm = this.hercm 
			val 		 = this.hercm['val']
			colind 		 = this.hercm['colind']
			row_ptr 	 = this.hercm['row_ptr']
			matrixWidth  = this.hercm['width']
			matrixHeight = this.hercm['height']
			symmetry 	 = this.hercm['symmetry']
	
			fileObject.write("HERCM FILE ") # start the header 
			fileObject.write("CSR ")
			fileObject.write(str(matrixWidth)+" ")
			fileObject.write(str(matrixHeight)+" ")
			fileObject.write(str(len(val)))
			fileObject.write(" "+symmetry+"\n") # end of the header 
			fileObject.write("ROWPTRLENGTH\n")
			fileObject.write(str(len(row_ptr))+"\n")
			fileObject.write("VAL\n")
			for entry in val:
				fileObject.write(str(entry)+" ")
			fileObject.write("\n")
			fileObject.write("ROWPTR\n")
			for entry in row_ptr:
				fileObject.write(str(entry)+" ")
			fileObject.write("\n")
			fileObject.write("COLIND\n")
			for entry in colind:
				fileObject.write(str(entry)+" ")
			fileObject.write("\n")
			fileObject.write("END")
			return this.STATUS_SUCCESS
		return STATUS_ERROR

	def readHercm(this, filename):
		# reads in a hercm to this.hercm, then returns this.hercm 

		# returns STATUS_SUCCESS or STATUS_ERROR

		prevLine = ''
		with open(filename,'r') as fileObject:
			for line in fileObject: 
				line = line.rstrip()
				splitLine = line.split()
				if 'HERCM FILE' in line:					
					try:
						this.hercm['width'] 	= int(splitLine[3])
						this.hercm['height'] 	= int(splitLine[4]) 
						this.hercm['nzentries'] = int(splitLine[5])
						this.hercm['symmetry']  = splitLine[6]
					except IndexError:
						return this.STATUS_ERROR
				if prevLine == 'VAL':
					this.hercm['val'] = [float(x) for x in splitLine]
				if prevLine == 'ROWPTR':
					this.hercm['row_ptr'] = [int(x) for x in splitLine]
				if prevLine == 'COLIND':
					this.hercm['colind'] = [int(x) for x in splitLine]

				prevLine = line


		return this.STATUS_SUCCESS

	def writeMtx(this, filename, hercm=None):
		from scipy import io
		from scipy.sparse import csr_matrix 
		from numpy import array

		# writes hercm to mtx file 
		# if hercm is not supplied, uses this.hercm instead

		# returns STATUS_SUCCESS or STATUS_ERROR

		if hercm == None:
			hercm = this.hercm

		hercm['val'] = array(hercm['val'])
		hercm['colind'] = array(hercm['colind'])
		hercm['row_ptr'] = array(hercm['row_ptr'])

		csrMatrix = csr_matrix((this.hercm['val'],
								this.hercm['colind'],
								this.hercm['row_ptr']),
								shape = (this.hercm['width'], 
										 this.hercm['height']))


		try:
			io.mmwrite(filename, csrMatrix)
		except Exception:
			return this.STATUS_ERROR

		return this.STATUS_SUCCESS

	def getHercm(this):
		# returns this.hercm 
		return this.hercm 