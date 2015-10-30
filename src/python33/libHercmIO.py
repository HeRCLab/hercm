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


""" @package libHercmIO
# Introduction 
"""


def readMatrix(filename, form, showProgress=False):
    # filename is the string path to the matrix file to open
    # format is the string 'hercm' or 'mtx' specifying matrix format

    # reads the matrix into HERCMATRIX for later processing
    # converts non-hercm matrices to hercm internally

    # returns as hecMatrix instance

    HERCMATRIX = libHercMatrix.hercMatrix()

    logging.info("reading matrix {0} in format {1}".format(filename, form))

    if (form == 'hercm') or (form =='bxf'):
        if showProgress:
            print("format is bxf, reading matrix using HERCMIO...")
        matrix = None
        try:
            matrix = libBXF.read(filename)
        except Exception as e:
            print("ERROR: could not read matrix")
            print("stack trace...")
            print(traceback.format_exc())

        HERCMATRIX = matrix
        HERCMATRIX.nzentries = len(HERCMATRIX.elements['val'])

        if showProgress:
            print("finished reading matrix.")

    elif form == 'mtx':
        from scipy import io
        from scipy.sparse import csr_matrix
        from numpy import array

        # reads in an MTX file and converts it to hercm

        try:
            if showProgress:
                print("reading data from file...")

            rawMatrix = scipy.sparse.coo_matrix(scipy.io.mmread(filename))

            if 'symmetric' in io.mminfo(filename):
                HERCMATRIX.symmetry = "SYM"
            else:
                HERCMATRIX.symmetry = "ASYM"

            hercm = {}  # needed to generate verification

            if showProgress:
                print("generating header data..")
            hercm['val'] = rawMatrix.data
            hercm['col'] = rawMatrix.col.tolist()
            hercm['row'] = rawMatrix.row.tolist()
            (matrixWidth, matrixHeight) = rawMatrix.shape
            HERCMATRIX.height = int(matrixHeight)
            HERCMATRIX.width = int(matrixWidth)
            vs = libBXF.generateVerificationSum(hercm)
            HERCMATRIX.verification = vs
            HERCMATRIX.remarks = []

            # I'm not sure why  has to be hard...
            # http://stackoverflow.com/questions/26018781/numpy-is-it-possible-to-preserve-the-dtype-of-columns-when-using-column-stack

            if showProgress:
                print("preparing matrix data...")
            val = numpy.asarray(hercm['val'], dtype='float64')
            col = numpy.asarray(hercm['col'], dtype='int32')
            row = numpy.asarray(hercm['row'], dtype='int32')

            val = numpy.rec.array(val, dtype=[(('val'), numpy.float64)])
            col = numpy.rec.array(col, dtype=[(('col'), numpy.int32)])
            row = numpy.rec.array(row, dtype=[(('row'), numpy.int32)])

            HERCMATRIX.elements = append_fields(row,
                    'col',
                    col,
                    usemask=False,
                    dtypes=[numpy.int32])

            HERCMATRIX.elements = append_fields(HERCMATRIX.elements,
                    'val',
                    val,
                    usemask=False,
                    dtypes=[numpy.float64])

            HERCMATRIX.nzentries = len(HERCMATRIX.elements['val'])

            if showProgress:
                print("finished reading matrix")

        except IOError as e:  # make sure the file exists and is readable
            logging.warning("(lsc-480) could not open matrix file")
            raise IOError("could not open matrix file for writing...",
                          str(e))

    elif form == 'mat':  # matlab matrices
        from scipy import io
        from scipy import sparse
        from numpy import array

        try:

            rawMatrix = scipy.sparse.coo_matrix(
                scipy.io.loadmat(filename)['matrix'])

            hercm = {}  # needed to generate verification

            hercm['val'] = rawMatrix.data
            hercm['col'] = rawMatrix.col.tolist()
            hercm['row'] = rawMatrix.row.tolist()
            (matrixWidth, matrixHeight) = rawMatrix.shape
            HERCMATRIX.height = int(matrixHeight)
            HERCMATRIX.width = int(matrixWidth)
            vs = libBXF.generateVerificationSum(hercm)
            HERCMATRIX.verification = vs
            HERCMATRIX.remarks = []

            # I'm not sure why  has to be hard...
            # http://stackoverflow.com/questions/26018781/numpy-is-it-possible-to-preserve-the-dtype-of-columns-when-using-column-stack

            val = numpy.asarray(hercm['val'], dtype='float64')
            col = numpy.asarray(hercm['col'], dtype='int32')
            row = numpy.asarray(hercm['row'], dtype='int32')

            val = numpy.rec.array(val, dtype=[(('val'), numpy.float64)])
            col = numpy.rec.array(col, dtype=[(('col'), numpy.int32)])
            row = numpy.rec.array(row, dtype=[(('row'), numpy.int32)])

            HERCMATRIX.elements = append_fields(row,
                    'col',
                    col,
                    usemask=False,
                    dtypes=[numpy.int32])

            HERCMATRIX.elements = append_fields(HERCMATRIX.elements,
                    'val', val, usemask=False, dtypes=[numpy.float64])

            HERCMATRIX.nzentries = len(HERCMATRIX.elements['val'])

            if HERCMATRIX.checkSymmetry():
                HERCMATRIX.symmetry = 'SYM'

        except IOError as e:  # make sure the file exists and is readable
            logging.warning("(lsc-536)could not open matrix file")
            raise IOError("could not open matrix file for writing...",
                          str(e))

    else:
        logging.warning("(lsc-545) format {0} is not valid".format(form))

    if showProgress:
        print("converting matrix to row-major...")
    logging.info("converting matrix to row-major")
    HERCMATRIX.makeRowMajor()

    if showProgress:
        print("matrix is now row major")

    if HERCMATRIX.symmetry == 'SYM':
        logging.info("matrix is symmetric, truncating lower triangle")
        if showProgress:
            print("matrix is symmetric, truncating lower triangle...")
        HERCMATRIX.makeSymmetrical('truncate', showProgress)
        if showProgress:
            print("lower triangle truncated")

    return HERCMATRIX


def writeMatrix(filename, form, HERCMATRIX):
    # writes HERCMATRIX to the file
    # filename is a string indicating path of file
    # format is a string indicating file format (mtx or hercm)
    # returns True on success, None on failure

    logging.info("writing matrix {0} in format {1}..."
            .format(filename, form))

    if os.path.isfile(filename):
        logging.warning("(lsc-566) file exists, cannot write")
        raise FileExistsError("could not write to file {0}".format(filename)
                + " file already exists!")

    if HERCMATRIX.symmetry == 'SYM':
        logging.info("matrix is symmetric, truncating lower triangle")
        HERCMATRIX.makeSymmetrical('truncate')

    logging.info("making matrix row major...")
    HERCMATRIX.makeRowMajor()

    if form == 'hercm':
        # TODO: these will probably need a try/except block at some point 
        
        libBXF.write(HERCMATRIX, filename, "HERCM")

    if form == 'bxf':
            
            libBXF.write(HERCMATRIX, filename)

    elif form == 'mtx':
        try:
            scipy.io.mmwrite(filename, HERCMATRIX.getInFormat('coo'))
        except ValueError as e:
            logging.warning("""(lsc-589) encountered ValueError exception 
while writing file. Exception: {0}. You probably have out of bounds indices 
in row or col""".format(e))
        except Exception as e:
                logging.warning("""(lsc-593) encountered general error while
 writing: {0}""".format(str(e)))


        # fix header of mtx file
        if HERCMATRIX.symmetry == 'SYM':
            logging.info("format is mtx and matrix is symmetric, fixing" +
                    " header...")
            with open(filename) as inputFile:
                lines = inputFile.readlines()
            lines[0] = "%%MatrixMarket matrix coordinate pattern symmetric\n"

            with open(filename, 'w') as outputFile:
                for line in lines:
                    outputFile.write(line)

    elif form == 'mat':  # matlab matrix file
        from scipy import io
        from scipy import sparse
        from numpy import array

        scipy.io.savemat(filename, {'matrix': HERCMATRIX.getInFormat('coo')})

    else:
        logging.warning("(lsc-621) format {0} is not valid".format(form))
        raise TypeError("{0} is not a valid format"
                        .format(form))
