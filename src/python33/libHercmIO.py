# permits IO and conversion on various sparse matrix formats.
import libHercMatrix
import libBXF
import scipy
import numpy
import scipy.io
from numpy.lib.recfunctions import append_fields
import traceback
import pprint 
import os 
import logging 


class hercmIOConvertFormatError:
	pass

class hercmIO:
	def __init__(this):
		this.HSM = libHercMatrix.hercMatrix()  #TODO: change this name from HSM to something
		# more relevant 
		this.HERCMIO = libBXF.bxfio()


	def readMatrix(this, filename, form):
		# filename is the string path to the matrix file to open
		# format is the string 'hercm' or 'mtx' specifying matrix format 

		# reads the matrix into this.HSM for later processing 
		# converts non-hercm matrices to hercm internally 

		logging.info("reading matrix {0} in format {1}".format(filename, form))

		if form == ('hercm' or 'bxf'):
			matrix = None 
			try:
				matrix = this.HERCMIO.read(filename)
			except Exception as e:
				print("ERROR: could not read matrix")
				print("stack trace...")
				print(traceback.format_exc())

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

				this.HSM.elements = append_fields(row, 
					'col', 
					col, 
					usemask = False, 
					dtypes=[numpy.int32])

				this.HSM.elements = append_fields(this.HSM.elements, 
					'val', 
					val, 
					usemask = False, 
					dtypes=[numpy.float64])

				
				this.HSM.nzentries = len(this.HSM.elements['val'])

					
			except IOError as e: # make sure the file exists and is readable
				logging.warning("(lsc-480) could not open matrix file")
				raise IOError("could not open matrix file for writing...",
							  str(e))
			

		elif form == 'mat': # matlab matrices 
			from scipy import io
			from scipy import sparse 
			from numpy import array 

			try:
			
				rawMatrix = scipy.sparse.coo_matrix(
					scipy.io.loadmat(filename)['matrix'])
				
				

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

				this.HSM.elements = append_fields(row, 
					'col', 
					col, 
					usemask = False, 
					dtypes=[numpy.int32])

				this.HSM.elements = append_fields(this.HSM.elements, 
					'val', val, usemask = False, dtypes=[numpy.float64])

				
				this.HSM.nzentries = len(this.HSM.elements['val'])

				if this.HSM.checkSymmetry():
					this.HSM.symmetry = 'SYM'

				
			
		
			except IOError as e: # make sure the file exists and is readable
				logging.warning("(lsc-536)could not open matrix file")
				raise IOError("could not open matrix file for writing...",
							  str(e))



		else:
			this.logger.log("format must be hercm or mtx, cannot use format {0}"
							.format(form), "error")
			logging.warning("(lsc-545) format {0} is not valid".format(form))
			
		logging.info("converting matrix to row-major")
		this.HSM.makeRowMajor()

		if this.HSM.symmetry == 'SYM':
			logging.info("matrix is symmetric, truncating lowe rtriangle") 
			this.HSM.makeSymmetrical('truncate') 


	def writeMatrix(this, filename, form):
		# writes this.HSM to the file 
		# filename is a string indicating path of file
		# format is a string indicating file format (mtx or hercm)
		# returns True on success, None on failure

		logging.info("writing matrix {0} in format {1}..."
			.format(filename, form))

		if os.path.isfile(filename):
			logging.warning("(lsc-566) file exists, cannot write")
			raise FileExistsError("could not write to file {0}".format(filename)
				+ " file already exists!")

		if this.HSM.symmetry == 'SYM':
			logging.info("matrix is symmetric, truncating lower triangle")
			this.HSM.makeSymmetrical('truncate')



		logging.info("making matrix row major...")
		this.HSM.makeRowMajor()

		if form == 'hercm':
			try:
				this.HERCMIO.write(this.HSM, filename, "HERCM")
			except HercmioValidationError:
				print("ERROR: matrix did not pass validation!")
				print("Matrix will not be written to file")

		if form == 'bxf':
			try:
				this.HERCMIO.write(this.HSM, filename)
			except HercmioValidationError:
				print("ERROR: matrix did not pass validation!")
				print("Matrix will not be written to file")
			
		elif form == 'mtx':
			try:
				scipy.io.mmwrite(filename, this.HSM.getInFormat('coo'))
			except ValueError as e: 
				logging.warning("""(lsc-589) encountered ValueError exception 
while writing file. Exception: {0}. You probably have out of bounds indices 
in row or col""".format(e))
			except Exception as e:
				logging.warning("""(lsc-593) encountered general error while
 writing: {0}""".format(str(e)))

				raise IOError("encountered exception while writing matrix")
	
			# fix header of mtx file 
			if this.HSM.symmetry == 'SYM':
				logging.info("format is mtx and matrix is symmetric, fixing" +
					" header...")
				with open(filename) as inputFile:
					lines = inputFile.readlines() 
				lines[0]="%%MatrixMarket matrix coordinate pattern symmetric\n"

				with open(filename,'w') as outputFile:
					for line in lines:
						outputFile.write(line) 

		elif form == 'mat': # matlab matrix file 
			from scipy import io
			from scipy import sparse 
			from numpy import array 

			scipy.io.savemat(filename, {'matrix':this.HSM.getInFormat('coo')})


		else:
			logging.warning("(lsc-621) format {0} is not valid".format(form))
			raise SparseConvertFormatError("{0} is not a valid format"
											.format(form))




