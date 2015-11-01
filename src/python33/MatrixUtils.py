import readline
import libHercMatrix
import libHercmIO
import matplotlib
import matplotlib.pyplot
import logging
import os
import textwrap
import pprint
import libBXF

## @package MatrixUtils provides matrix utilities 
#
# Tools that may be useful elsewhere, but are predominately intended for use 
# with BXFExplorer commands. 

## Print an overview of the matrix to the console. 
# Prints either the entire matrix, or an overview of the matrix if it is too 
# large. 
# 
# @param[in] HERCMATRIX the instance of libHercMatrix.hercMatrix to display
# @param[in] maxHeight no more than `maxHeight` rows will be printed, default
# is 10. 
# @param[in] maxWidth no more than `maxWidth` columns will be printed, default 
# is 10. 
# 
# @returns `None`
# 
# # Examples
# 
# 5x5 matrix containing only 2s 
# ```
# > display
#        2         2         2         2         2
#        2         2         2         2         2
#        2         2         2         2         2
#        2         2         2         2         2
#        2         2         2         2         2
# ```
# 
# bcsstk01
# ```
# > display
# 2.83e+06         0         0         0     1e+06  ...         0         0         0         0         0
#        0  1.64e+06         0    -2e+06         0  ...         0         0         0         0         0
#        0         0  1.72e+06 -2.08e+06 -2.78e+06  ...         0         0         0         0         0
#        0    -2e+06 -2.08e+06     1e+09         0  ...         0         0         0         0         0
#    1e+06         0 -2.78e+06         0  1.07e+09  ...         0         0         0         0         0
#
#        0         0         0         0         0  ...   3.5e+06  5.18e+05  -4.8e+06         0         0
#        0         0         0         0         0  ...  5.18e+05  4.58e+06  1.35e+05         0         0
#        0         0         0         0         0  ...  -4.8e+06  1.35e+05  2.47e+09         0         0
#        0         0         0         0         0  ...         0         0         0  9.62e+08  -1.1e+08
#        0         0         0         0         0  ...         0         0         0  -1.1e+08  5.31e+08
#``` 

def displayMatrix(HERCMATRIX, maxHeight=10, maxWidth=10):

    if maxHeight % 2 != 0:
        raise ValueError("maxHeight must be an even number")
    if maxWidth % 2 != 0:
        raise ValueError("maxWidth must be an even number")

    row = 0
    while row < HERCMATRIX.height:
        if row == (maxWidth / 2):
            row = HERCMATRIX.height - (maxHeight / 2)
            print("\n", end="")
        col = 0
        while col < HERCMATRIX.width:
            if col == (maxWidth / 2):
                col = HERCMATRIX.width - (maxWidth / 2)
                print(" ... ", end="")
            try:
                print('{:9.3g} '
                      .format(round(HERCMATRIX.getValue(row, col), 3)), end="")
            except IndexError:
                print('   EE   ', end="")
            col += 1
        print("")
        row += 1


## Print the matrix converted to CSR format
# Prints the contents of the matrix, converted to CSR format. Prompts the user 
# if the matrix contains more than 25 elements ***TODO**: it should prompt the 
# user only of more than 25 elements would be displayed). Automatically 
# the row of any given element for convenience, and prints elements of the 
# row_ptr array at the indexes which they refer to. 
# 
# @params[in] HERCMATRIX an instance of libHercMatrix.hercMatrix to view
# @params[in] firstRow the first row of the matrix to display (note, this 
# refers to the first row of the matrix, not the index of the element). Default
# is 10. 
# @params[in] lastRow the last row of the matrix to display. Default is `None` 
# (if `lastRow` is `None`, it is interpreted as the end of the matrix). 
# 
# @returns `None`
# 
# # Examples
# printing the 1st through the 5th rows of bcspwr01
# ```
# > csrdisplay 1 5
# WARNING: matrix contains more than 25 entries,
# are you sure you wish to proceed?
# (yes/no)> yes
# index  value      column  row_ptr row
#    8  1.6e+06       1       8       1
#    9   -2e+06       3               1
#   10  5.6e+06       5               1
#   11 -6.7e+03       7               1
#   12   -2e+06       9               1
#   13 -3.1e+04      19               1
#   14  5.6e+06      23               1
#   15 -1.6e+06      25               1
#   16  1.7e+06       2      16       2
#   17 -2.1e+06       3               2
#   18 -2.8e+06       4               2
#   19 -1.7e+06       8               2
#   20 -1.5e+04      20               2
#   21 -2.8e+06      22               2
#   22 -2.9e+04      26               2
#   23 -2.1e+06      27               2
#   24    1e+09       3      24       3
#   25    2e+06       7               3
#   26    4e+08       9               3
#   27 -3.3e+06      21               3
#   28  2.1e+06      26               3
#   29    1e+08      27               3
#   30  1.1e+09       4      30       4
#   31   -1e+06       6               4
#   32    2e+08      10               4
#   33  2.8e+06      20               4
#   34  3.3e+08      22               4
#   35 -8.3e+05      28               4
#   36  1.5e+09       5      36       5
#   37   -2e+06      11               5
#   38 -5.6e+06      19               5
#   39  6.7e+08      23               5
#   40 -2.1e+06      24               5
#   41    1e+08      29               5
# ```

def printCSR(HERCMATRIX, firstRow=0, lastRow=None):
    # display the raw CSR matrix
    if lastRow == None:
        lastRow = HERCMATRIX.nzentries - 1

    pp = pprint.PrettyPrinter()
    if HERCMATRIX.nzentries > 25:
        print("WARNING: matrix contains more than 25 entries, ")
        print("are you sure you wish to proceed?")
        if input('(yes/no)> ').upper() != "YES":
            return

    matrix = HERCMATRIX.getInFormat('csr')

    print('{:6} {:10} {:7} {:7} {:7}'
          .format('index', 'value', 'column', 'row_ptr', 'row'))
    ptrCount = 0
    currentRow = 0
    for index in range(0, HERCMATRIX.nzentries - 1):
        if matrix.indptr[ptrCount] == index:
            currentRow = ptrCount
            if currentRow >= firstRow:
                if currentRow <= lastRow:
                    print('{:5} {:8.2g} {:7} {:7} {:7}'
                          .format(index, matrix.data[index],
                            matrix.indices[index],
                            matrix.indptr[ptrCount], currentRow))
            ptrCount += 1
        else:
            try:
                if currentRow >= firstRow:
                    if currentRow <= lastRow:
                        print('{:5} {:8.2g} {:7} {:7} {:7}'
                              .format(index, matrix.data[index],
                                matrix.indices[index],
                                ' ', currentRow))
            except IndexError:
                # for some reason, matrix.data seems way too short

                print("IndexError! {0} out of bounds".format(index))


## Prints the matrix as it is represented in libHercMatrix.hercMatrix
#
# Prints the matrix in COO format, as an exact representation of the given 
# instance of libHercMatrix.hercMatrix's internal storage of the matrix. 
# 
# @param[in] HERCMATRIX the instance of libHercMatrix.hercMatrix to display
# 
# @returns `None`
# 
# # Examples
# output for a 4x4 matrix of 7s 
# ```
# > raw
# - raw matrix contents -
# row    col    val
#     0      0    7.0
#     0      0    7.0
#     0      1    7.0
#     0      2    7.0
#     0      3    7.0
#     1      0    7.0
#     1      1    7.0
#     1      2    7.0
#     1      3    7.0
#     2      0    7.0
#     2      1    7.0
#     2      2    7.0
#     2      3    7.0
#     3      0    7.0
#     3      1    7.0
#     3      2    7.0
#     3      3    7.0
# ```

def printRaw(HERCMATRIX):
    # display the matrix as raw COO data
    print("- raw matrix contents -")
    print("{0:6} {1:6} {2:6}".format("row", "col", "val"))
    for i in range(0, HERCMATRIX.nzentries):
        element = HERCMATRIX.getElement(i)
        row = element[0]
        col = element[1]
        val = element[2]
        print("{0:6} {1:6} {2:6}".format(row, col, val))


## Prints a rectangular selection of values
# Prints a rectangle of values, bounded by col1, row1 and col2, row2 from
# HERCMATRIX
# 
# @param[in] row1 int specifying row of upper left bound
# @param[in] row2 int specifying row of bottom right bound
# @param[in] col1 int specifying col of upper left bound
# @param[in] col2 int specifying col of bottom right bound
# @param[in] HERCMATRIX instance of libHercMatrix.hercMatrix to print values 
# from
# 
# @returns None
# 
# @throws IndexError if any value is out of bounds
# @throws ValueError if `row1` > `row2` or `col1` > `col2`

def printRange(row1, row2, col1, col2, HERCMATRIX):
    # prints a rectangular range of values in HERCMATRIX, with row1, col1 as
    # the top left corner, and row2, col2 in the bottom right


    if row1 < 0:
        raise IndexError("row1 may not be less than zero")
    if row1 > HERCMATRIX.height:
        raise IndexError("row1 is out of bounds")
    if row2 < 0:
        raise IndexError("row2 may not be less than zero")
    if row2 > HERCMATRIX.height:
        raise IndexError("row2 is out of bounds")
    if col1 < 0:
        raise IndexError("col1 may not be less than zero")
    if col1 > HERCMATRIX.width:
        raise IndexError("col1 is out of bounds")
    if col2 < 0:
        raise IndexError("col2 may not be less than zero")
    if col2 > HERCMATRIX.width:
        raise IndexError("col2 is out of bounds")

    if row1 > row2:
        raise ValueError("row1 larger than row2")
    if col1 > col2:
        raise ValueError("col1 larger than col2")

    TMPMATRIX = libHercMatrix.hercMatrix()
    TMPMATRIX.height = abs(row2 - row1) 
    TMPMATRIX.width  = abs(col2 - col1) 

    width = HERCMATRIX.width 
    height = HERCMATRIX.height

    for element in HERCMATRIX.elements:
        row = element[0]
        col = element[1]
        val = element[2]

        if (row >= row1) and (row < row2):
            if (col >= col1) and (col < col2):
                try:
                    TMPMATRIX.setValue(row - row1,
                        col - col1,
                        val)
                except IndexError as e:
                    logging.warning("encountered error {0}".format(e))
                    logging.warning("writing to row {0} col {1} of "
                        .format(row - row1, col - col1))
                    logging.warning("row {0} col {1}"
                        .format(TMPMATRIX.height, TMPMATRIX.width))


    TMPMATRIX.makeRowMajor()
    displayMatrix(TMPMATRIX)


def touch(col, row, val, HERCMATRIX):
    # sets the value at row, col to val

    try:
        oldValue = HERCMATRIX.getValue(row, col)
    except IndexError:
        print("ERROR: row {0}, col {1} is out of bounds".format(row, col))
        return
    HERCMATRIX.setValue(row, col, val)
    print("updated value of col {1}, row {0} to {2} from {3}"
          .format(row, col, HERCMATRIX.getValue(row, col), oldValue))

    if oldValue == 0 and val != 0:
        print("WARNING: you have added a new non zero entry, COO vectors")
        print("may not be in row-major form!")


def paint(row1, row2, col1, col2, val, HERCMATRIX):
    # paints a rectangular region of HERCMATRIX with val, with the top left
    # corner as row1, col1, and the bottom right as row2, col2

    width = HERCMATRIX.width
    height = HERCMATRIX.height
    for row in range(0, height):
        for col in range(0, width):
            if col >= col1 and col <= col2:
                if row >= row1 and row <= row2:
                    HERCMATRIX.setValue(row, col, val)


def paintDiagonal(begin, end, spread, val, HERCMATRIX, offset=0):
    # paints a diagonal, starting at column begin, ending at column end with
    # the value val, spread indices to either side of the diagonal.
    # optionally offsets by offset columns to the left or right

    for i in range(begin, end):
        for j in range(0, spread):
            try:
                col = offset + i + j  # right side
                HERCMATRIX.setValue(i, col, val)
                col = offset + i - j  # left side
                HERCMATRIX.setValue(i, col, val)
            except IndexError:
                pass  # out of bounds


def setDims(height, width, HERCMATRIX):
    # sets the dimensions of HERCMATRIX to width x height

        # remove out of bounds entries
    for i in reversed(range(0, HERCMATRIX.nzentries)):
        if HERCMATRIX.elements['row'][i] >= height:
            HERCMATRIX.setValue(HERCMATRIX.elements['row'][i],
                                HERCMATRIX.elements['col'][i], 0)
        elif HERCMATRIX.elements['col'][i] >= width:
            HERCMATRIX.setValue(HERCMATRIX.elements['row'][i],
                                HERCMATRIX.elements['col'][i], 0)

    HERCMATRIX.height = height
    HERCMATRIX.width = width
    HERCMATRIX.removeZeros()


def setSymmetry(newSymmetry, HERCMATRIX, method="truncate"):
    # wrapper for libHercMatrix.hercMatrix.makeSymmetrical/makeAsymmetrical

    if method not in ['truncate', 'add', 'smart']:
        raise KeyError("method {0} is not valid".format(method))

    validOptions = ['sym', 'asym', 'asymmetric', 'symmetric',
    'symmetrical', 'asymmetrical']

    newSymmetry = newSymmetry.lower()

    if newSymmetry not in validOptions:
        print("{0} is not a valid symmetry".format(newSymmetry))
        return

    if newSymmetry in ['sym', 'symmetric', 'symmetrical']:
        symmetry = 'SYM'
    else:
        symmetry = 'ASYM'

    if symmetry != HERCMATRIX.symmetry:
        if symmetry == 'SYM':
            HERCMATRIX.makeSymmetrical(method)
        elif symmetry == 'ASYM':
            HERCMATRIX.makeAsymmetrical(method)

    HERCMATRIX.symmetry = symmetry
    HERCMATRIX.makeRowMajor()
    HERCMATRIX.removeZeros()


def initilize(height, width, HERCMATRIX, val=0):
    # initializes a blank matrix height x width in size in the HERCMATRIX
    # instance

    # optionally sets all elements in the matrix equal to val

    setDims(0, 0, HERCMATRIX)
    setDims(height, width, HERCMATRIX)

    for i in range(0, height):  # this is faster than using paint
        for j in range(0, width):
            HERCMATRIX.setValue(i, j, val)
    if HERCMATRIX.elements is None:
        HERCMATRIX.nzentries = 0
    else:
        HERCMATRIX.nzentries = len(HERCMATRIX.elements['val'])
    HERCMATRIX.symmetry = 'ASYM'
    HERCMATRIX.remarks = []


def generateVerification(HERCMATRIX):
    # updates verification sum of matrix
    try:
        newSum = libBXF.generateVerificationSum(HERCMATRIX)
    except TypeError:
        print("ERROR: could not generate verification sum of empty matrix")
    HERCMATRIX.verification = newSum


def plot(HERCMATRIX):
    # plots the matrix with matplotlib
    matrix = HERCMATRIX.getInFormat('coo')

    matplotlib.pyplot.spy(matrix)
    matplotlib.pyplot.show()


def printSymmetry(HERCMATRIX):
    print("Symmetry attribute is:", HERCMATRIX.symmetry)
    print("Matrix is actually symmetric:", HERCMATRIX.checkSymmetry())


def printDirectoryListing(directory=None):
    # prints a directory listing of directory, of cwd if directory=None
    if directory is None:
        if os.path.exists(directory):
            pass
        elif os.path.exists(os.path.join(os.getcwd(), directory)):
            directory = os.path.join(os.getcwd(), directory)
        else:
            print("ERROR: could not get directory listing")
            print(directory, " is not a valid path")
            print(os.path.join(os.getcwd(), directory),
                  " is not a valid path")
            directory = os.getcwd()
    else:
        directory = os.getcwd()

    print("Directory listing for: ", directory)
    for item in os.listdir(directory):
        print(item)


def printWorkingDirectory():
    # prints the CWD

    print(os.getcwd())


def head(path, numlines=10):
    # prints the first numlines of file at path
    print("First {0} lines of file {1}".format(numlines, path))
    f = open(path)
    for line in f.readlines()[0:numlines]:
        print(line, end='')


def cat(path):
    # prints all lines in file at path

    print("Contents of file {0}".format(path))
    f = open(path)
    for line in f.readlines():
        print(line, end='')


def changeDirectory(newDir):
    # changes cwd to newDir
    if not os.path.exists(newDir):
        print("ERROR: cannot cd to nonexistent path")
        return
    if os.path.isfile(newDir):
        print("ERROR: {0} is not a directory".format(arguments[0]))
        return
    os.chdir(newDir)


def convert(source, destination, sourceFormat, destinationFormat):
    # converts the matrix at source in sourceFormat to destinationFormat
    # then writes out at destination

    if not os.path.exists(source):
        print("ERROR: load from nonexistent path")
        return
    if not os.path.isfile(source):
        print("ERROR: {0} is not a file".format(source))
        return
    HERCMATRIX = libHercMatrix.hercMatrix()

    HERCMATRIX = load(source, sourceFormat)
    generateVerification(HERCMATRIX)
    write(destination, destinationFormat, HERCMATRIX)
