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
		
		this.dtype = numpy.dtype([('row',numpy.int32),
								  ('col',numpy.int32),
								  ('val',numpy.float64)])
		this.elements   = None

		this.remarks 	  = []
		this.nzentries    = 0
		this.symmetry	  = 'ASYM'
		this.verification = None
		this.height 	  = 0
		this.width 		  = 0

	
	def getInFormat(this, form):
		# returns the matrix as a scipy.sparse type 
		# format is any string valid for scipy.sparse.coo_matrix.asformat
		# http://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.asformat.html#scipy.sparse.coo_matrix.asformat
		
		scipyMatrix = scipy.sparse.coo_matrix((this.elements['val'], 
											   (this.elements['row'], 
											   	this.elements['col'])),
											   shape = (this.height,
											   			this.width)
											   )

		return scipyMatrix.asformat(form)

	def addElement(this, element):
		# element can be any element supported by this.castElement() 

		try: 
			element = this.castElement(element)
			if this.elements == None:
				this.elements = numpy.array([element],dtype=this.dtype)
			else:
				this.elements = numpy.append(this.elements, element)
			this.nzentries = this.nzentries + 1
		except ValueError as e:
			raise ValueError("Could not cast element to valid format... ",str(e))


	def getElement(this, n ,form=list):
		# returns the nth element of this matrix, in the given form
		# if form is list, it is returned as a python list [row, col, val]
		# if form is numpy.void it is returned as a numpy.void with the 
		# dtype this.dtype 
		# if form is numpy.ndarray, it is returned as a numpy.ndarray with 
		# dtype this.dtype

		if n < 0 or n > this.nzentries:
			raise IndexError(n, "is out of bounds for array of size", 
							 this.nzentries)
		try:
			n = int(n) 
		except ValueError:
			raise ValueError("n is not an int or cannot be cast to an int")

		if form == list:
			retList = []
			retList.append(this.elements['row'][n])
			retList.append(this.elements['col'][n])
			retList.append(this.elements['val'][n])
			return retList
		elif form == numpy.void:
			return this.elements[n]
		elif form == numpy.ndarray:
			return np.array(this.elements[n])
		else:
			raise TypeError("form must be of type list or numpy.void")

	def castElement(this, element):
		# returns element as numpy.ndarray
		# element should be a list or numpy.void of the format 
		# [row, col, val]
		# elements of type numpy.ndarray whose dtype matches this.dtype
		# will be passed through
		# element of type numpy.ndarray whose dtype does not match will 
		# be converted  if possible 

		if type(element) == list:
			if len(element) != 3:
				raise ValueError("element must contain three indicies ")
			try:
				row = numpy.int32(element[0])
			except ValueError:
				raise ValueError("index 0 of list cannot be cast to int")
			try:
				col = numpy.int32(element[1])
			except ValueError:
				raise ValueError("index 1 of list cannot be cast to int")	
			try:
				val = numpy.float64(element[2])
			except ValueError:
				raise ValueError("index 2 of list cannot be cast to float")
			
			return numpy.array((row, col, val), dtype=this.dtype)
		elif type(element) == numpy.void:
			return numpy.array(element)
		elif type(element) == numpy.ndarray:
			if element.dtype == this.dtype:
				return element
			elif len(element) != 3:
				raise ValueError("element must contain three indicies")
			else:
				try:
					row = numpy.int32(element[0])
				except ValueError:
					raise ValueError("index 0 of list cannot be cast to int")
				try:
					col = numpy.int32(element[1])
				except ValueError:
					raise ValueError("index 1 of list cannot be cast to int")	
				try:
					val = numpy.float64(element[2])
				except ValueError:
					raise ValueError("index 2 of list cannot be cast to float")
				return numpy.array((row, col, val), dtype=this.dtype)
	
	

	def searchElement(this, element, rtol=1e-05, atol=1e-08):
		# returns a list of indices at which element occurs in 
		# the matrix. element is compared to this.elements with
		# numpy.isclose

		# element should be any supported by this.castElement() 


		# rtol and a tol are passed through to numpy.isclose, and are
		# used as described here: http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html
		# an element specified as a list, numpy.void, or numpy.ndarray 
		# will be matched using numpy.isclose 

		try: 
			element = this.castElement(element)
		except ValueError as e:
			raise ValueError("Could not cast element to valid format... ",str(e))

		instances = []

		for i in range(0, nzentries):
			if numpy.isclose(this.elements[i]['row'],
							 element['row'],
							 rtol, atol):
				if numpy.isclose(this.elements[i]['col'],
							 element['col'],
							 rtol, atol):
					if numpy.isclose(this.elements[i]['val'],
							 element['val'],
							 rtol, atol):
						instances.append(i)

		return instances


	def removeElement(this, n, rtol=0, atol=0):
		# if n can be cast to int, removes the nth element of the matrix
		# if n can be cast by this.castElement(), remove all instances
		# of that element, as found by this.searchElement() 

		# rtol and a tol are passed through to numpy.isclose, and are
		# used as described here: http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html
		# an element specified as a list, numpy.void, or numpy.ndarray 
		# will be matched using numpy.isclose 

		try:
			n = int(n)
			this.elements = numpy.delete(this.elements, n)
			this.nzentries = this.nzentries - 1
		except ValueError:
			try:
				n = this.castElement(n)
				instances = this.searchElement(n, rtol, atol)
				for i in instances:
					this.removeElement(i)
			except ValueError as e:
				raise ValueError("could not cast n to any valid format... ",
								 str(e))




	def getValue(this, row, col, rtol=1e-05, atol=1e-08):
		# returns the value stored at row, col  
		# if assumeRowMajor is true, uses an optimized search routine


		if row >= this.height:
			raise IndexError("row out of bounds") 
		if col >= this.width:
			raise IndexError("col out of bounds") 
		if row < 0:
			raise IndexError("row out of bounds") 
		if col < 0:
			raise IndexError("col out of bounds") 

		for i in range(0, this.nzentries):
			if numpy.isclose(this.elements[i]['row'],
							 row,
							 rtol, atol):
				if numpy.isclose(this.elements[i]['col'],
							 col,
							 rtol, atol):
					return this.elements[i]['val']


		return 0

	def setValue(this, newRow, newCol, newVal):
		# changes the value of row, col to val
		# all are integers 

		# assumeRowMajor is passed through to getValue

		if newRow >= this.height:
			raise IndexError("newRow out of bounds") 
		if newCol >= this.width:
			raise IndexError("newCol out of bounds") 
		if newRow < 0:
			raise IndexError("newRow out of bounds") 
		if newCol < 0:
			raise IndexError("newCol out of bounds")  

		if this.getValue(newRow, newCol) != 0:
			for i in range(0,this.nzentries):
				if this.elements['row'][i] == newRow:
					if this.elements['col'][i] == newCol:
						this.elements['val'][i] = newVal 
						if newVal == 0:
							this.removeZeros()
						return 
					

		# value does not exist yet, lets create it 
		newEntry = numpy.array((newRow, newCol, newVal),dtype=this.dtype)
		this.addElement(newEntry)
		this.nzentries = len(this.elements['val'])
		if newVal == 0:
			this.removeZeros()

	def removeZeros(this):
		# removes any instances of zero 

		if this.elements == None: 
			return 
		for i in reversed(range(0,this.nzentries)):
			if this.elements['val'][i] == 0:
				this.removeElement(i)
		this.nzentries = len(this.elements['val'])



	def makeRowMajor(this):
		# re orders this matrix such that it is row major 

		if this.elements == None:
			raise ValueError("cannot make nonexistent matrix row major")


		this.elements = numpy.sort(this.elements, order=["row", "col"])



