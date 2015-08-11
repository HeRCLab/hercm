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
						 'remarks'	 :None,
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

	def getValcol(this):
		# returns a numpy matrix, where each element is in the format 
		# (row, col, val)

		valcolType = numpy.dtype([('row',int),('col',int),('val',float)]])
		valcol = numpy.array(dtype=valcolType)

		for i in range(0,i):
			valcol



	def getValue(this, row, col, assumeRowMajor=False):
		# returns the value stored at row, col 
		# returns None if the value cannot be found 
		# if assumeRowMajor is true, uses an optimized search routine


		if row > this.contents['height']:
			return None 
		if col > this.contents['width']:
			return None 
		if row < 0:
			return None
		if col < 0:
			return None 

		if not assumeRowMajor:
			for i in range(0, this.contents['nzentries']):
				if this.contents['row'][i] == row:
					if this.contents['col'][i] == col:
						return this.contents['val'][i]
		else:
			for i in range(0, this.contents['nzentries']):
				if this.contents['row'][i] < row:
					pass 
				elif this.contents['row'][i] > row:
					return 0 
				elif this.contents['col'][i] > col and \
				this.contents['row'] == row:
					return 0
				elif this.contents['col'][i] == col and \
				this.contents['row'] == row:
					return this.contents['val'][i]

		


		return 0

	def setValue(this, newRow, newCol, newVal, assumeRowMajor=False):
		# changes the value of row, col to val
		# all are integers 

		# returns None on error and True on success

		# assumeRowMajor is passed through to getValue

		if newRow > this.contents['height']:
			return None 
		if newCol > this.contents['width']:
			return None 
		if newRow < 0:
			return None
		if newCol < 0:
			return None 

		if this.getValue(newRow, newCol, assumeRowMajor) != 0:
			for i in range(0,this.contents['nzentries']):
				if this.contents['row'][i] == newRow:
					if this.contents['col'][i] == newCol:
						this.contents['val'][i] = newVal 
						if newVal == 0:
							this.removeZeros()
						return True

		# value does not exist yet, lets create it 
		this.contents['row'].append(newRow)
		this.contents['col'].append(newCol) 
		this.contents['val'].append(newVal)
		this.contents['nzentries'] = len(this.contents['val'])
		if newVal == 0:
			this.removeZeros()
		return True

	def removeZeros(this):
		# removes any instances of zero 

		for i in reversed(range(0,this.contents['nzentries'])):
			if this.contents['val'][i] == 0:
				this.contents['val'].pop(i)
				this.contents['col'].pop(i)
				this.contents['row'].pop(i)
		this.contents['nzentries'] = len(this.contents['val'])



	def checkIfSorted(this, listToCheck):
		# checks if listToCheck is sorted, returns true is so, false if not
		for i in range(1,len(listToCheck)):
			if listToCheck[i-1] > listToCheck[i]:
				return False
		return True 

	def checkIfRowMajor(this):
		# returns true if this matrix is in row major format
		# returns false otherwise 
		
		if not this.checkIfSorted(this.contents['row']):
			return False
		for i in range(1,len(this.contents['row'])):
			if this.contents['col'][i-1] > this.contents['col'][i]:
				if this.contents['row'][i-1] == this.contents['row'][i]:
					return False 

		return True 

	def makeRowMajor(this):
		# re orders this matrix such that it is row major 

		import sys 

		lengthNotSorted = len(this.contents['val'])

		while not this.checkIfSorted(this.contents['row']):
			print("\nElements are not sorted, initiating pass...")
			for i in range (1, len(this.contents['val'])):
				if i % 10000 == 0:
					percentComplete = round(100 * (i/len(this.contents['val'])),1)
					print("\r[{0}] % complete".format(percentComplete),end="")
					
				if this.contents['row'][i-1] > this.contents['row'][i]:
					# swap values to sort 

					this.contents['row'][i], this.contents['row'][i-1] = \
					this.contents['row'][i-1], this.contents['row'][i]

					this.contents['col'][i], this.contents['col'][i-1] = \
					this.contents['col'][i-1], this.contents['col'][i]

					this.contents['val'][i], this.contents['val'][i-1] = \
					this.contents['val'][i-1], this.contents['val'][i]


		while not this.checkIfRowMajor():
			print("Matrix is not row major, initiating pass...")
			for i in range(1, len(this.contents['val'])):
				# check if the previous value of col is larger than the current
				# value AND the row value for both is identical 

				if i % 1000 == 0:
					sys.stdout.write("\r[{0}] % ccomplete"
								 .format(100 * (i/len(this.contents['val']))))
					sys.stdout.flush()

				if this.contents['col'][i-1] > this.contents['col'][i]:
					if this.contents['row'][i-1] == this.contents['row'][i]:
						# swap values to sort 
						smallerValue = this.contents['row'][i]
						largerValue = this.contents['row'][i-1]
						this.contents['row'][i] = largerValue 
						this.contents['row'][i-1] = smallerValue
	
						smallerValue = this.contents['col'][i]
						largerValue = this.contents['col'][i-1]
						this.contents['col'][i] = largerValue 
						this.contents['col'][i-1] = smallerValue
	
						smallerValue = this.contents['val'][i]
						largerValue = this.contents['val'][i-1]
						this.contents['val'][i] = largerValue 
						this.contents['val'][i-1] = smallerValue



