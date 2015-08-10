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


	def makeAsymmetrical(this):
		# makes this matrix asymmetrical by duplicating any entries in the upper
		# triangle to the lower 

		# Note: this is a very expensive operation, with O(n) being 
		# height * width, and an entire second instance of HSM being created

		matrix = scipy.sparse.triu(this.getInFormat('coo'))
		matrixVal = matrix.data 
		matrixRow = matrix.row
		matrixCol = matrix.col 

		TEMP = hsm() 
		TEMP.contents['val'] = matrixVal.tolist()
		TEMP.contents['row'] = matrixRow.tolist()
		TEMP.contents['col'] = matrixCol.tolist()
		TEMP.contents['nzentries'] = matrix.nnz 
		TEMP.contents['height'] = this.contents['height']
		TEMP.contents['width'] = this.contents['width']
		TEMP.contents['symmetry'] = 'ASYM'


		for row in range(0,this.contents['height']):
			for col in range(0,this.contents['width']):
				val = TEMP.getValue(row, col) 
				if row != col:
					TEMP.setValue(col, row, val)

		this.contents = TEMP.contents 
		this.makeRowMajor()
		this.removeDuplicates()


	def makeSymmetrical(this):
		# make the matrix symmetrical by moving all entries to the upper 
		# triangle

		# note: this may create conflicting elements  

		for i in range(0,len(this.contents['val'])):
			# check if we are in the botton triange
			if this.contents['row'][i] > this.contents['col'][i]:
				# swap values 
				this.contents['row'][i], this.contents['col'][i] = \
				this.contents['col'][i], this.contents['val'][i]

		this.contents['symmetry'] = 'SYM' 
		this.makeRowMajor() 
		this.removeDuplicates()

	def checkForConflicts(this):
		# checks if this matrix has any conflicting values
		# returns true if the matrix has conflicting values
		# returns false otherwise 

		# note, this is a very expensive operation, O(n) = nnz^2, at worst

		for i in range(0, len(this.contents['val'])):
			val = this.contents['val'][i]
			row = this.contents['row'][i]
			col = this.contents['col'][i]
			for j in range(0, len(this.contents['val'])):
				innerVal = this.contents['val'][j]
				innerRow = this.contents['row'][j]
				innerCol = this.contents['col'][j]

				if innerVal == val and innerRow == row and innerCol == col:
					return True 

		return False 


	def setSymmetry(this, symmetry):
		# changes the symmetry of the matrix 
		# symmetry should be 'SYM' or 'ASYM'
		# returns True on success, None on failure 

		if symmetry not in ['SYM','ASYM']:
			return None 

		if this.contents['symmetry'] == None:
			this.contents['symmetry'] = symmetry
			return True 
		elif this.contents['symmetry'] == 'SYM': 
			# duplicate entries in upper triangle to lower triangle
			this.makeAsymmetrical()
			return True 
		elif this.contents['symmetry'] == 'ASYM':
			# move all entries to upper triangle 
			this.makeSymmetrical()
			if not this.checkForConflicts():
				return None 
			else:
				return True 
		return None 


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

	def setValue(this, newRow, newCol, newVal):
		# changes the value of row, col to val
		# all are integers 

		# returns None on error and True on success

		if newRow > this.contents['height']:
			return None 
		if newCol > this.contents['width']:
			return None 
		if newRow < 0:
			return None
		if newCol < 0:
			return None 

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

	def removeDuplicates(this): 
	 	# removes any duplicate entries 
	 	# if symmetrical, removes duplicates from lower triangle 

		listToDelete = []

		for i in range(0, len(this.contents['val'])):
			val = this.contents['val'][i]
			row = this.contents['row'][i]
			col = this.contents['col'][i]
			for j in range(i+1, len(this.contents['val'])):
				innerVal = this.contents['val'][j]
				innerRow = this.contents['row'][j]
				innerCol = this.contents['col'][j]

				if innerVal == val and innerRow == row and innerCol == col:
					listToDelete.append(j)
				else:
					print("{0} != {1}".format(val, innerVal))
					print("{0} != {1}".format(row, innerCol))
					print("{0} != {1}".format(col, innerRow))
				elif this.contents['symmetry'] == 'SYM':
					if innerVal == val and innerCol == row and innerRow == col:
						listToDelete.append(j)
					else:
						print("{0} != {1}".format(row, innerRow))
						print("{0} != {1}".format(col, innerCol))
						print("{0} != {1}".format(val, innerVal))


		print(listToDelete)
		for item in reversed(listToDelete):
			innerVal = this.contents['val'].pop(item)
			innerRow = this.contents['row'].pop(item)
			innerCol = this.contents['col'].pop(item)
		this.makeRowMajor()


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

		while not this.checkIfSorted(this.contents['row']):
			for i in range (1, len(this.contents['val'])):
				if this.contents['row'][i-1] > this.contents['row'][i]:
					# swap values to sort 
					#smallerValue = this.contents['row'][i]
					#largerValue = this.contents['row'][i-1]
					#this.contents['row'][i] = largerValue 
					#this.contents['row'][i-1] = smallerValue

					this.contents['row'][i], this.contents['row'][i-1] = \
					this.contents['row'][i-1], this.contents['row'][i]

					smallerValue = this.contents['col'][i]
					largerValue = this.contents['col'][i-1]
					this.contents['col'][i] = largerValue 
					this.contents['col'][i-1] = smallerValue

					smallerValue = this.contents['val'][i]
					largerValue = this.contents['val'][i-1]
					this.contents['val'][i] = largerValue 
					this.contents['val'][i-1] = smallerValue
		while not this.checkIfRowMajor():
			for i in range(1, len(this.contents['val'])):
				# check if the previous value of col is larger than the current
				# value AND the row value for both is identical 
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



