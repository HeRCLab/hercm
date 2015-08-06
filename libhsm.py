# lib HeRC Sparse Matrix 
# library for storing csr matricies in hercm format, and for interacting with 
# said matricies 

class hsm: 
	# hercm matrix class 
	# stores hercm matricies and permits access by various methods 
	def __init__(this):
		from scipy.sparse import csr_matrix 
		# hercm matrix attributes 
		
		# this serves as the internal representation 
		this.contents = {'val'		 :None,
						 'row_ptr'   :None,
						 'colind'	 :None,
						 'nzentries' :None,
						 'height'	 :None,
						 'width'	 :None,
						 'symmetry'  :None}

	def getScipyCSR(this):
		# returns scipy.sparse.csr_matrix of contents
		from numpy import asarray 
		val 	= asarray(this.contents['val'])
		row_ptr = asarray(this.contents['row_ptr'])
		colind  = asarray(this.contents['colind'])
		width   = this.contents['width']
		height  = this.contents['height']

		from scipy.sparse import csr_matrix 
		return csr_matrix((val,
					       colind,
						   row_ptr),
						   shape = (width, height))
	def getValue(this, row, col):
		# returns the value stored at row, col 
		# returns None if the value cannot be found 

		if row > this.contents['height']:
			return None 
		if col > this.contents['width']:
			return None 
		if row < 0:
			return None
		if col < 0:
			return None 

		# index in val of the first value of the desired row 
		rowStartIndex = this.contents['row_ptr'][row]

		# index in val of the last value of the desired row
		rowEndIndex   = this.contents['row_ptr'][row+1] -1 

		for index in range(rowStartIndex, rowEndIndex):
			if this.contents['colind'][index] == col:
				return this.contents['val'][index]

		return 0