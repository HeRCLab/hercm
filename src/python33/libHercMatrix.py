# lib HeRC Sparse Matrix
# library for storing csr matricies in hercm format, and for interacting with
# said matricies

import numpy
import scipy
import logging

## @package libHercMatrix

## Class for storing and manipulating sparse matrices
#
# Store matrices in COO format via custom numpy dtype. Provides functions for
# numpy/scipy interoperability, and basic matrix manipulation. Does NOT do any
# file IO. 
# 
# Keep in mind that while reading here, an element typically refers to a a list
# or numpy array that contains a row, col, val triplet in that order.
# 
# Unless otherwise noted, everything here is always zero indexed. 

class hercMatrix:
    

    ## Fairly basic constructor. Nothing special here. 

    def __init__(this):
        from scipy.sparse import csr_matrix
        # hercm matrix attributes

        this.dtype = numpy.dtype([('row', numpy.int32),
                                  ('col', numpy.int32),
                                  ('val', numpy.float64)])
        this.elements = None

        this.remarks = []
        this.nzentries = 0
        this.symmetry = 'ASYM'
        this.verification = None
        this.height = 0
        this.width = 0

    ## Return this matrix as a scipy.sparse matrix
    # 
    # Returns the matrix stored in this class instance as an instance of 
    # scipy.sparse. 
    # 
    # @param form A string indicating the format. Should be any string supported
    # by [scipy.sparse.coo_matrix.asformat()](http://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.asformat.html#scipy.sparse.coo_matrix.asformat)
    # as this is basically a wrapper for that function. 
    # 
    # @returns scipy.sparse.XXX_matrix instance 

    def getInFormat(this, form):

        scipyMatrix = None
        try:
            scipyMatrix = scipy.sparse.coo_matrix((this.elements['val'],
                                               (this.elements['row'],
                                                this.elements['col'])),
                shape=(this.height,
                       this.width)
            )
        except TypeError:  # matrix has not been initialized yet
            this.addElement([0, 0, 0])
            this.height = 1
            this.width = 1
            scipyMatrix = this.getInFormat(form)

        return scipyMatrix.asformat(form)

    ## Add a new COO element 
    #
    # Appends a new COO element to the matrix. 
    # 
    # @param element anything supported by 
    # libHercMatrix.hercMatrix.castElement()
    # 
    # @exception ValueError element could not be cast by castElement()

    def addElement(this, element):
        # element can be any element supported by this.castElement()

        try:
            element = this.castElement(element)
            if this.symmetry == 'SYM':
                if element['row'] > element['col']:
                    # put element in the top triangle, this matrix is
                    # symmetric!
                    temp = numpy.array(this.dtype)
                    temp = element
                    element['row'] = temp['col']
                    element['col'] = temp['row']

            if this.elements is None:
                this.elements = numpy.array([element], dtype=this.dtype)
            else:
                this.elements = numpy.append(this.elements, element)
            this.nzentries = this.nzentries + 1
        except ValueError as e:
            raise ValueError(
                "Could not cast element to valid format... ", str(e))

    ## Get a COO element from this matrix
    #
    # Returns an array in the order `[row, col, val]`. Numpy return types will
    # have the dtype libHercMatrix.hercMatrix.dtype
    #
    # @param n integer indicating the index of the element
    # @param form python class list, numpy.void, or numpy.ndarray
    # 
    # @exception IndexError n is out of bounds for this matrix 
    # @exception ValueError n is not and integer, and cannot be cast as such
    # @exception TypeError form is not a list, numpy.void, or numpy.ndarray
    # 
    # **NOTE**: form should not be a class instance, but the class itself. 
    # for example, you might call this function as getElement(5, list)
    # 
    # 

    def getElement(this, n, form=list):

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

    ## Cast a COO matrix element 
    #
    # Typecasts a COO matrix element of the format [row, col, val] such that it
    # matches libHercMatrix.hercMatrix.dtype 
    # 
    # @param element list, numpy.void, or numpy.ndarray
    # 
    # @returns numpy.ndarray
    # 
    # @exception ValueError one or more indicies of element cannot be converted 
    # to a required type, or element has the wrong number of indicies
    # 

    def castElement(this, element):

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

    ## Search the matrix for an element
    # 
    # Searches the matrix for an element that is a close match for the one 
    # provided. 
    # 
    # @param element anything supported by castElement()
    # @param rtol passed through to [numpy.isclose](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html)
    # @param atol see above
    # 
    # @returns list of indicies at which the element occurs 

    def searchElement(this, element, rtol=1e-05, atol=1e-08):
        try:
            element = this.castElement(element)
        except ValueError as e:
            raise ValueError(
                "Could not cast element to valid format... ", str(e))

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

    ## Remove an element from the matrix
    #
    # Removes either the nth element of the matrix, or the element matching
    # n (if n can be cast by castElement()). If n is not an int, ALL elements 
    # matching it are removed (this is why rtol and atol are zero by default).
    # 
    # @param n int or any supported by castElement()
    # @param rtol passed through to [numpy.isclose](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html)
    # @param atol see above
    # 
    # **NOTE**: atol and rtol are only used if n is not an int 

    def removeElement(this, n, rtol=0, atol=0):

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


    ## returns the value of an element by coordinates
    # 
    # Returns the value stored at a particular row, column pair in the matrix. 
    # 
    # @param row int indicating row number of the element
    # @param col int indicating the column number of the element
    # 
    # @todo why are atol and rtol here - row and col are ints? They should 
    # probably be removed. 
    # 
    # @returns float with the value at the specified row, col
    
    def getValue(this, row, col, rtol=1e-05, atol=1e-08):
        if this.symmetry == 'SYM':
            if row > col:
                # extrapolate for values in lower triangle
                tempRow = row
                tempCol = col
                row = tempCol
                col = tempRow

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

    ## Change the value by coordinates
    # 
    # Changes the value at the specified coordinates, truncating the current
    # value if there is one. 
    # 
    # @param newRow int indicating the row of the value to set
    # @param newCol int indicating the column of the value to set
    # @param newVal float containing the value to set
    # 
    # @exception IndexError newCol or newRow is out of bounds
    
    def setValue(this, newRow, newCol, newVal):

        if this.symmetry == 'SYM':
            if newRow > newCol:
                this.setValue(newCol, newRow, newVal)
                return

        if newRow >= this.height:
            raise IndexError("newRow out of bounds")
        if newCol >= this.width:
            raise IndexError("newCol out of bounds")
        if newRow < 0:
            raise IndexError("newRow out of bounds")
        if newCol < 0:
            raise IndexError("newCol out of bounds")

        if this.symmetry == 'SYM':
            if newRow > newCol:
                # put value in the correct triangle
                tempRow = newRow
                tempCol = newCol
                newRow = tempCol
                newCol = tempRow

        if this.getValue(newRow, newCol) != 0:
            for i in range(0, this.nzentries):
                if this.elements['row'][i] == newRow:
                    if this.elements['col'][i] == newCol:
                        this.elements['val'][i] = newVal
                        if newVal == 0:
                            this.removeZeros()
                        return

        # value does not exist yet, lets create it
        newEntry = numpy.array((newRow, newCol, newVal), dtype=this.dtype)
        this.addElement(newEntry)
        this.nzentries = len(this.elements['val'])
        if newVal == 0:
            this.removeZeros()

    ## Remove all zero elements from the matrix
    #
    # This does not affect the actual contents of the matrix, only it's 
    # representation in COO format. Removes any COO elements where val is
    # exactly zero. 

    def removeZeros(this):

        matrix = this.getInFormat('csr')
        matrix.eliminate_zeros()
        this.replaceContents(matrix)
        this.nzentries = len(this.elements['val'])

    ## replace matrix contents with a scipy sparse matrix
    #
    # Overwrites this matrix with the contents of a scipy.sparse.XXX_matrix 
    # instance 
    # 
    # @param newContents anything which can be cast by scipy.sparse.coo_matrix

    def replaceContents(this, newContents):
        try:
            newContents = scipy.sparse.coo_matrix(newContents)
        except ValueError:
            try: 
                newContents = newContents.tocoo()
            except Exception:
                raise TypeError("Could not replace contents of matrix with " + 
                   "object of type {0}".format(type(newContents)))

        try:
            this.elements.resize(len(newContents.data))
        except AttributeError:
            # elements is None because it has not been initialized 
            this.elements = numpy.array([[],[],[]],dtype=this.dtype)
            this.elements.resize(len(newContents.data))

        this.elements['row'] = newContents.row.astype(numpy.int32)
        this.elements['col'] = newContents.col.astype(numpy.int32)
        this.elements['val'] = newContents.data.astype(numpy.float64)
        this.nzentries = len(this.elements['val'])

    def checkLowerTriangle(this):
        # returns true if this matrix contains no elements in the lower triangle
        # returns false otherwise

        this.removeZeros()
        this.makeRowMajor()

        for i in range(0, this.nzentries):
            element = this.getElement(i)
            row = element[0]
            col = element[1]
            val = element[2]
            if row > col:
                if val != 0:
                    return False

        return True

    def checkSymmetry(this):
        # checks if the lower triangle is empty and symmetry attribute is SYM,
        # OR if there are no elements in the lower triangle which do not match
        # the corresponding elements int he upper triangle.

        this.removeZeros()
        this.makeRowMajor()

        if this.checkLowerTriangle():
            if this.symmetry == 'SYM':
                return True

        for i in range(0, this.nzentries):
            element = this.getElement(i)
            row = element[0]
            col = element[1]
            val = element[2]
            if row > col:
                if val != this.getValue(col, row):
                    return False

        return True

    def makeSymmetrical(this, method='truncate'):
        # makes this matrix symmetrical
        # if method is 'truncate', this will be done by discarding the
        # bottom triangle, regardless of contents

        # if method is 'add', this will be done by adding all elements
        # from the bottom triangle to the corresponding element in the
        # top triangle, ignoring the diagonal

        # if method is 'smart', this will be done by adding all elements
        # from the bottom triangle to the top triangle ONLY if the corresponding
        # element in the top triangle is zero, and otherwise discarding elements
        # from the bottom triangle. This is the slowest method

        # truncate should work for any 'true' symmetric matrix, where numpy
        # has silently duplicate elements from the bottom triangle to the top
        # thus, it is the default

        # the other methods are useful for turning asymmetrical matrices
        # symmetric

        if method == 'truncate':
            upperTriangle = scipy.sparse.triu(this.getInFormat('coo'))
            this.replaceContents(upperTriangle)

        elif method == 'add':
            lowerTriangle = scipy.sparse.tril(this.getInFormat('coo'), k=-1)

            this.makeSymmetrical(method='truncate')

            newMatrix = lowerTriangle.transpose() + \
                this.getInFormat('coo')

            newMatrix = scipy.sparse.coo_matrix(newMatrix)

            this.replaceContents(newMatrix)

        elif method == 'smart':
            # this is horrifyingly show O(n) = n^2 (n=nzentries)

            this.removeZeros()
            upperTriangle = scipy.sparse.triu(this.getInFormat('coo'))
            lowerTriangle = scipy.sparse.tril(this.getInFormat('coo'), k=-1)

            # remove conflicting entries
            for row, col in zip(upperTriangle.row, upperTriangle.col):
                lcounter = 0  # counter in lower triangle
                for lrow, lcol in zip(lowerTriangle.row, lowerTriangle.col):
                    # lrow and lcol refer to the lower column and lower row
                    # of the lower triangle coo matrix
                    if lcol == row:
                        if lrow == col:
                            lowerTriangle.data[lcounter] = 0
                    lcounter = lcounter + 1
            newMatrix = upperTriangle + lowerTriangle

            this.replaceContents(newMatrix)

            this.makeSymmetrical('add')

            this.removeZeros()

        else:
            raise ValueError("method \"{0}\" is not valid, ".format(method) +
                    "expected one of: truncate, add, smart")

        this.removeZeros()

    def makeAsymmetrical(this, method='truncate'):
        # if method is truncate
        # reflects everything above the diagonal into the lower triangle,
        # ignoring the diagonal
        # any values in the lower triangle will be lost

        # if method is add
        # adds everything in the upper triangle to the lower triangle, ignoring
        # the diagonal

        # if method is smart
        # copies each element of the upper triangle into the lower, only if
        # the element in the lower triangle is zero

        if method == 'truncate':
            upperTriangle = scipy.sparse.triu(this.getInFormat('coo'))
            this.replaceContents(upperTriangle)
            upperTriangle = scipy.sparse.triu(this.getInFormat('coo'), k=1)

            newMatrix = this.getInFormat('coo') + upperTriangle.transpose()

            this.replaceContents(newMatrix)
        elif method == 'add':
            upperTriangle = scipy.sparse.triu(this.getInFormat('coo'), k=1)
            upperTriangle = upperTriangle.transpose()

            newMatrix = this.getInFormat('coo') + upperTriangle

            this.replaceContents(newMatrix)

        elif method == 'smart':
            upperTriangle = scipy.sparse.triu(this.getInFormat('coo'), k=1)
            uppertriangle = upperTriangle.transpose()
            lowerTriangle = scipy.sparse.tril(this.getInFormat('coo'), k=-1)
            for i in range(0, upperTriangle.nnz):
                for j in range(0, lowerTriangle.nnz):
                    # remember upperTriangle has already been transposed
                    if upperTriangle.row[i] == lowerTriangle.row[j]:
                        if upperTriangle.col[i] == lowerTriangle.col[j]:
                            if lowerTriangle.data[j] != 0:
                                upperTriangle.data[i] = 0

            # lower triangle is not modified, just use the one that is live
            newMatrix = this.getInFormat('coo') + upperTriangle
            this.replaceContents(newMatrix)

        else:
            raise ValueError("method \"{0}\" is not valid, ".format(method) +
                    "expected one of: truncate, add, smart")

        this.removeZeros()

    def makeRowMajor(this):
        # re orders this matrix such that it is row major

        if this.elements is None:
            logging.warning("cannot make nonexistent matrix row major")
            return

        this.elements = numpy.sort(this.elements, order=["row", "col"])

    def transpose(this):
        # perform matrix transpose, switching the top and bottom triangles about
        # the diagonal
        
        logging.warning("transposing symmetric matrix, this will probably " +
            "truncate everything not on the diagonal")

        for element in this.elements:
            originalRow = element[0]
            originalCol = element[1]
            element[0] = originalCol
            element[1] = originalRow
