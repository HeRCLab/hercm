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
    # @param extrapolate if `True`, elements which would fall in the upper 
    # triangle of a sparse matrix will be transposed into the lower triangle. 
    # This is the default behavior. 
    # 
    # @exception ValueError element could not be cast by castElement()

    def addElement(this, element, extrapolate = True):
        # element can be any element supported by this.castElement()

        try:
            element = this.castElement(element)
            if (this.symmetry == 'SYM') and extrapolate:
                if element['row'] < element['col']:
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
    # @param extrapolate if extrapolate is `True`, and the matrix is symmetric, 
    # and row is less than col (the requested value is in the upper triangle), 
    # the return value will be extrapolated (eg. the return value will be the
    # actual value of the row, col in the matrix, not the value which is stored)
    # . This is accomplished by switching row and col before retrieving the 
    # value. This is the default behavior. If extrapolate is `False` the value 
    # actually stored will be returned (usually zero). 
    # 
    # @returns float with the value at the specified row, col
    
    def getValue(this, row, col, extrapolate = True):
        if (this.symmetry == 'SYM') and extrapolate:
            if row < col:
                # extrapolate for values in upper triangle
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
    # @param extrapolate if extrapolate is `True`, and the matrix is symmetric, 
    # and row is less than col (the requested element is in the upper triangle), 
    # the row and column will be switched so the element changed will be in the 
    # lower triangle. This is the default behavior. If extrapolate is `False` the value 
    # actually stored will be returned (usually zero). 
    # 
    # @exception IndexError newCol or newRow is out of bounds
    
    def setValue(this, newRow, newCol, newVal, extrapolate = True):

        if (this.symmetry == 'SYM') and extrapolate:
            if newRow < newCol:
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
    # instance, or something that can be cast to one. 
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

    ## check if there are elements in the lower triangle
    #
    # Checks if there are any elements stored in the lower triangle of the 
    # matrix. Kept for compatibility, as symmetric matrices are now stored
    # by their lower triangle. 
    # 
    # @returns True if there are no nonzero elements in the lower triangle
    # @returns False if there are nonzero elements in the lower triangle
    # 
    # **NOTE**: this has nothing to do with contents of the matrix. If you are
    # trying to find the symmetry of the matrix, please use checkSymmetry(). 

    def checkLowerTriangle(this):

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

    ## check if there are elements in the upper triangle
    #
    # Checks if there are any elements stored in the upper triangle of the 
    # matrix. Useful for verifying symmetric matrices are stored correctly. 
    # 
    # @returns True if there are no nonzero elements in the upper triangle
    # @returns False if there are nonzero elements in the upper triangle
    # 
    # **NOTE**: this has nothing to do with contents of the matrix. If you are
    # trying to find the symmetry of the matrix, please use checkSymmetry(). 

    def checkUpperTriangle(this):

        this.removeZeros()
        this.makeRowMajor()

        for i in range(0, this.nzentries):
            element = this.getElement(i)
            row = element[0]
            col = element[1]
            val = element[2]
            if row < col:
                if val != 0:
                    return False

        return True


    ## checks if the matrix is symmetric
    #
    # Checks if the matrix is symmetric. The matrix is considered symmetric
    # if one of the following conditions is met: 
    # 
    # 1. the checkUpperTriangle() returns `True` AND the symmetry attribute for
    # the matrix is equal to `"SYM"`
    # 2. there are no elements in the lower triangle such that their counterpart
    # in the upper triangle is not equal. In other words, the matrix is equal
    # to itself transposed
    # 
    # @returns True if either of the above conditions are met
    # @returns False otherwise
    # 
    # **NOTE**: this function checks if the matrix data is symmetric or not, 
    # regardless of how it is stored in COO format. If you want to verify the
    # matrix is correctly stored symmetrically, you should use 
    # checkLowerTriangle()

    def checkSymmetry(this):

        this.removeZeros()
        this.makeRowMajor()

        if this.checkUpperTriangle():
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

    ## makes this matrix symmetrical
    # 
    # Convert this matrix to symmetric. This both updates the matrix's
    # symmetry attribute, AND makes the data in the matrix symmetric. 
    # Several methods are available for accomplishing this task, which follow...
    # 
    # | value of `method` | effect |
    # |-----------------|--------|
    # | `truncate`      | All elements int he upper triangle discarded | 
    # | `add`           | The upper half of the triangle is transposed, and the result is added to the lower triangle |
    # | `smart`         | Elements of the upper triangle whose counterpart in the lower triangle is zero are moved to the lower triangle |
    # 
    # **NOTE**: the `smart` method is very performance naive, and is not very
    # fast. In most cases, it will not be useful and should probably be avoided
    # 
    # **NOTE**: the diagonal is never modified by any method
    # 
    # @throws ValueError `method` is not valid 

    def makeSymmetrical(this, method='truncate'):

        if method == 'truncate':
            lowerTriangle = scipy.sparse.tril(this.getInFormat('coo'))
            this.replaceContents(lowerTriangle)

        elif method == 'add':
            upperTriangle = scipy.sparse.triu(this.getInFormat('coo'), k=-1)

            this.makeSymmetrical(method='truncate')

            newMatrix = upperTriangle.transpose() + \
                this.getInFormat('coo')

            newMatrix = scipy.sparse.coo_matrix(newMatrix)

            this.replaceContents(newMatrix)

        elif method == 'smart':
            # this is horrifyingly slow O(n) = n^2 (n=nzentries)

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
            this.transpose() # this method still operates on the upper triangle
            this.makeSymmetrical('add')
            this.removeZeros()

        else:
            raise ValueError("method \"{0}\" is not valid, ".format(method) +
                    "expected one of: truncate, add, smart")
        this.symmetry = "SYM"
        this.removeZeros()

    ## convert the matrix to asymmetrical 
    # 
    # The inverse of makeSymmetrical(). Modifies matrix data such that it is 
    # asymmetrical. Like makeSymmetrical(), several methods are supported, which
    # follow...
    # 
    # | value of `method` | result |
    # |-------------------|--------|
    # | `truncate`        | The upper triangle is replaced with the lower triangle transposed |
    # | `add`             | The lower triangle is transposed and added to the upper triangle |
    # | `smart`           | Moves any elements in the lower triangle whose counterpart in the upper triangle is zero to the lower triangle |
    # 
    # **NOTE**: as with makeSymmetrical(), `smart` is very slow, and probably
    # not very useful. 
    # 
    # **NOTE**: the diagonal is never modified by any method
    # 
    # @throws ValueError `method` is not valid 

    def makeAsymmetrical(this, method='truncate'):

        if method == 'truncate':
            lowerTriangle = scipy.sparse.tril(this.getInFormat('coo'))
            this.replaceContents(lowerTriangle)
            lowerTriangle = scipy.sparse.tril(this.getInFormat('coo'), k=1)

            newMatrix = this.getInFormat('coo') + lowerTriangle.transpose()

            this.replaceContents(newMatrix)

        elif method == 'add':
            lowerTriangle = scipy.sparse.tril(this.getInFormat('coo'), k=1)
            lowerTriangle = lowerTriangle.transpose()

            newMatrix = this.getInFormat('coo') + lowerTriangle

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
            this.transpose() # smart still works on the upper triangle 

        else:
            raise ValueError("method \"{0}\" is not valid, ".format(method) +
                    "expected one of: truncate, add, smart")

        this.removeZeros()
        this.makeRowMajor()

    ## Make the matrix row major
    # 
    # Modifies the COO matrix data such that it is sorted as row major. This
    # does not affect matrix contents in any way. 

    def makeRowMajor(this):

        if this.elements is None:
            logging.warning("cannot make nonexistent matrix row major")
            return

        this.elements = numpy.sort(this.elements, order=["row", "col"])

    ## transpose the matrix 
    #
    # Perform a matrix transpose about the diagonal. 
    # 
    # @exception TypeError matrix is symmetric, and cannot be transposed
    # 
    # **NOTE**: you should never transpose a symmetric matrix. This 
    # functionality used to be permitted, but has been disabled because it broke
    # things. If you *really* want to transpose a symmetric matrix, use 
    # getInFormat() to get it as a scipy.sparse matrix, then use numpy's 
    # transpose function (you will probably still break everything, be careful).

    def transpose(this):
        
        if this.symmetry == "SYM":
            raise TypeError("Cannot transpose a symmetric matrix")

        for element in this.elements:
            originalRow = element[0]
            originalCol = element[1]
            element[0] = originalCol
            element[1] = originalRow
