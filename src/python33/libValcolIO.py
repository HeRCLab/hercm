import libHercMatrix
import scipy.sparse
import numpy

## @package libValcolIO
# Provides read/write support for the valcol formatted files
#


## read a valcol file
# Reads in the valcol file located at path
#
# @param path the absolute or relative path to the valcol file to read
#
# @returns libHerMatrix.hercMatrix instance containing the contents of the file

def read(path):
    # hercMatrix instance we will return later
    MATRIX = libHercMatrix.hercMatrix()
    # CSR matrix contents
    row_ptr = numpy.array([])  # row pointer
    col_idx = numpy.array([])  # column index
    val     = numpy.array([])  # values

    # read the file
    FILE = open(path, 'r')
    lines = FILE.readlines()
    FILE.close()

    # read in the header, split it, and save the contents
    header = lines[0].split()
    height = int(header[0])
    width = int(header[0])
    nzentries = int(header[1])

    lines.pop(0)  # get rid of the header
    for line in lines:
        if len(line.split()) == 2:
            # if the length is 2, we are in the column index + val section
            val = numpy.append(val, float(line.split()[0]))
            # col_idx is 1-indexed in valcol
            col_idx = numpy.append(col_idx, int(line.split()[1]) - 1)
        elif len(line.split()) == 1:
            # if line length is 1, we are in the row pointer section
            row_ptr = numpy.append(row_ptr, int(line))
        else:
            print("WARNING: malformed line for valcol file: {0}".format(line))


    # generate a scipy.sparse.csr_matrix instance of 
    # libHercMatrix.hercMatrix.replaceContents()
    CSRMATRIX = scipy.sparse.csr_matrix((val, col_idx, row_ptr), 
        shape=(height, width))

    # move data into the hercMatrix instance
    MATRIX.nzentries = nzentries
    MATRIX.height = height 
    MATRIX.width = width 
    MATRIX.replaceContents(CSRMATRIX) 

    # check if the matrix is symmetric 
    if MATRIX.checkLowerTriangle():
        print("Lower triangle is empty, assuming symmetric matrix...")
        MATRIX.symmetry = "SYM"

    return MATRIX 

## write a valcol file
#
# @param path string containing the absolute or relative path to write to
# @param MATRIX instance of libHercMatrix.hercMatrix() to be written
# 
def write(path, MATRIX):
    FILE = open(path, "w")
    CSRMATRIX = MATRIX.getInFormat("csr")
    val = CSRMATRIX.data
    col = CSRMATRIX.indices 
    row_ptr = CSRMATRIX.indptr 

    if MATRIX.height != MATRIX.width:
        raise TypeError("valcol does not support non-square matricies")

    FILE.write(str(MATRIX.height) + " " + str(MATRIX.nzentries) + "\n")
    for i in range(0, MATRIX.nzentries):
        FILE.write(str(val[i]) + " " + str(col[i] + 1) + "\n")

    for i in range(0, len(row_ptr) - 1):
        FILE.write(str(row_ptr[i]) + "\n")

    FILE.write(str(MATRIX.nzentries) + "\n")

    FILE.close()










