# lib HeRC Sparse Matrix 
# library for storing csr matricies in hercm format, and for interacting with 
# said matricies 

import numpy 
import scipy

class hsm: 
	# hercm matrix class 
	# stores hercm matricies and permits access by various methods 
	def __init__(this):
		from scipy.sparse import csr_matrix 
		# hercm matrix attributes 
		
		# this serves as the internal representation 
		this.contents = {'val'		 :None,
						 'row'   	 :None,
						 'col'	 	 :None,
						 'nzentries' :None,
						 'height'	 :None,
						 'width'	 :None,
						 'symmetry'  :None}

	
	def getInFormat(this, format):
		# returns the matrix as a scipy.sparse type 
		# format is any string valid for scipy.sparse.coo_matrix.asformat
		# http://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.asformat.html#scipy.sparse.coo_matrix.asformat
		
		scipyMatrix = scipy.sparse.coo_matrix((this.contents['val'], 
											   (this.contents['row'], 
											   	this.contents['col'])),
											   shape = (this.contents['height'],
											   			this.contents['width'])
											   )

		return scipyMatrix.asformat(format)



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

		for i in range(0, this.contents['nzentries']):
			if this.contents['row'][i] == row:
				if this.contents['col'][i] == col:
					return this.contents['val'][i]

		return 0