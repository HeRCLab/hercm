import libHercMatrix
import scipy
import numpy
import scipy.io
from numpy.lib.recfunctions import append_fields
import traceback
import pprint
import os
import logging

## @package libBXF
#
# Provides IO for BXF format files


## read a BXF file
#
# @param filename absolute or relative path to the file to read
#
# @exception OSError file does not exist, permission error, or other IO error
# @exception ValueError file header is mangled, or one or more COO vectors
# is a different length than the others
# @exception TypeError one or more fields could not be typecast to required
# types
# 
# @return libHercMatrix.hercMatricx instance containing the matrix read from the
# file

def read(filename):
    # reads in the HeRCM file specified by filename
    # returns it as an instance of libhsm.hsm

    # matrix object we will return later
    HERCMATRIX = libHercMatrix.hercMatrix()

    # row, col, and val lists we will read the matrix data into later
    row = []
    col = []
    val = []

    logging.info("Reading BXF file {0}".format(filename))

    fileObject = open(filename, 'r')
    # this may raise OSError, which the caller should catch

    # Get a list of lines from the file. Might be a good point for future
    # optimization - lines could be processed one at a time
    lines = fileObject.readlines()
    fileObject.close()

    # read in the header
    header = lines[0]
    lines.pop(0)
    splitHeader = header.split()

    logging.info("read BXF header: " + header)

    # stuff we are going to read in from the header
    version = splitHeader[0]
    width = None
    height = None
    nzentries = None
    symmetry = None

    # version specific header parsing logic

    # deprecated HERCM (BXF 1.0) and BXF 2.0
    if version == "HERCM" or version == "BXF":
        if len(splitHeader) > 6:
            logging.warning("possibly mangled header - too many " +
                "fields for BXF 1.0 header. Attempting to read anyway...")
        elif len(splitHeader) < 6:
            logging.warning("possibly mangled header - too few fields for " +
                "BXF 1.0 header. Attempting to read anyway...")
        elif len(splitHeader) < 5:
            raise ValueError("Header has too few fields for any known BXF " +
                "version - unable to read header")

        # read fields from the header, see doc-extra/bxf-spec.md for more
        # details
        width = int(splitHeader[1])
        height = int(splitHeader[2])
        nzentries = int(splitHeader[3])
        symmetry = splitHeader[4].upper()

    elif version == "BXF21":
        if len(splitHeader) != 5:
            raise ValueError("Header has incorrect number of fields for BXF " +
                " 2.1")

        width=int(splitHeader[1])
        height=int(splitHeader[2])
        nzentries=int(spltiHeader[3])
        symmetry=splitHeader[4].upper()

    else:
        raise ValueError("Header did not contain  valid BXF version " +
            "identifier")

    # verify symmetry
    if symmetry not in ["SYM", "ASYM"]:
        logging.warning("Symmetry {0} is not valid, assuming asymmetric"
            .format(symmetry))
        symmetry = "ASYM"


    logging.info("finished reading header")

    HERCMATRIX.width = width
    HERCMATRIX.height = height
    HERCMATRIX.nzentries = nzentries
    HERCMATRIX.symmetry = symmetry

    inField = False
    currentHeader = ''
    fieldname = ''
    vtype = ''
    currentContents = []
    for line in lines:
        # we are starting a new field
        if not inField:
            currentHeader = line.rstrip()
            splitHeader = currentHeader.split()

            if version == "BXF21":
                fieldname = splitHeader[0]
                vtype = splitHeader[1]
            else:
                # if you review previous BXF specifications, field headers 
                # had three fields, the middle of which was either `LIST` or 
                # `SINGLE`. These can both be safely treated as lists, as BXF2.1
                # does
                # 
                fieldname = splitHeader[0]
                vtype = splitHeader[2]

            inField = True

        # this is the end of a field
        elif 'ENDFIELD' in line:

            # save the values we read from this field to lists for later use
            if fieldname.lower() == "val":
                val = currentContents
            elif fieldname.lower() == "row": 
                row = currentContents
            elif fieldname.lower() == "col":
                col = currentContents
            elif fieldname.lower() == "remarks":
                pass
            else:
                logging.warning("Ignoring field with unrecognized name: " 
                    + fieldname)

            # discard the contents of this field
            currentContents = []
            inField = False

        # we are currently reading data from a field 
        else:
            for value in line.split():
                # typecast this element according to the vtype
                # these may throw TypeError , which the caller should handle
                if vtype == 'INT':
                    currentContents.append(int(value))

                elif vtype == 'FLOAT':
                     currentContents.append(float(value))

                else:
                    currentContents.append(value)


    # do some basic validation
    if (len(row) != len(col)) or \
            (len(row) != len(val)) or \
            (len(val) != len(col)):
        raise ValueError("one or more vectors have non-matching lengths" +
            ", not a valid COO matrix")

    elif (len(val) != nzentries):
        # maybe this should throw an exception? 
        logging.warning("nzentries does not match number of nonzero entries " +
            "read from file - matrix may be mangled")

    else:
        logging.info("matrix seems sane, it is probably not corrupt")

    # copy matrix data into the matrix object
    for i in range(0, HERCMATRIX.nzentries):
        # this could probably be optimized by generating a scipy.sparse 
        # matrix then using hercMatrix.replaceContents()
        HERCMATRIX.addElement([row[i], col[i], val[i]])

    return HERCMATRIX

# TODO: remove this function
def generateVerificationSum(hercm):
    return 1

# TODO: remove this function
def verify(hercm):
    logging.warning("libBXF.verify is being updated, and dosen't actually do " +
        "anything right now")
    return True

# TODO: rewrite this to be BXF 2.1 complaint
def write(HERCMATRIX, filename, headerString="BXF  "):
    # HERCMATRIX should be an instance of libhsm.hsm
    # fileame is the string path to the file to write
    # writes a hercm file with contents matching hercm to filename

    # if you need to write a file with "HERCM" starting the header,
    # set headerString to "HERCM"

    logging.info("writing hercm file {0}".format(filename))

    try:
        fileObject = open(filename, 'w')
    except FileNotFoundError as e:
        logging.warning("(lsc-294) could not open file: file not found")
        raise FileNotFoundError("could not open file {0}... "
                                .format(filename), str(e))
    except PermissionError as e:
        logging.warning("(lsc-299) could not open file: permissions error")
        raise PermissionError("Could not open file {0}..."
                              .format(filename), str(e))

    if not verify(HERCMATRIX):
        logging.warning("matrix validation failed. " +
            "Got {0} expected {1}".format(generateVerificationSum(HERCMATRIX),
                HERCMATRIX.verification) + "You should verify the matrix was" +
                " written correctly.")

    header = headerString + ' '
    header = header + str(HERCMATRIX.width) + ' '
    header = header + str(HERCMATRIX.height) + ' '
    header = header + str(HERCMATRIX.nzentries) + ' '
    header = header + str(HERCMATRIX.symmetry) + ' '
    header = header + str(HERCMATRIX.verification) + '\n'

    logging.info("generated header: {0}".format(header))

    fileObject.write(header)

    logging.info("writing remarks")
    fileObject.write('REMARKS LIST STRING\n')
    itemcounter = 0
    line = ''
    for item in HERCMATRIX.remarks:
        logging.debug("writing item {0} in remarks".format(item))
        line = line + item + ' '
        itemcounter += 1
        if itemcounter == 9:
            fileObject.write(line + '\n')
            line = ''
            itemcounter = 0
    if itemcounter > 0:
        fileObject.write(line + '\n')
    fileObject.write('ENDFIELD\n')

    logging.info("writing val")
    fileObject.write('VAL LIST FLOAT\n')
    itemcounter = 0
    line = ''
    for item in HERCMATRIX.elements['val']:
        logging.debug("writing item {0} in val".format(str(item)))
        line = line + str(item) + ' '
        itemcounter += 1
        if itemcounter == 9:
            fileObject.write(line + '\n')
            line = ''
            itemcounter = 0
    if itemcounter > 0:
        fileObject.write(line + '\n')
    fileObject.write('ENDFIELD\n')

    logging.info("writing row")
    fileObject.write('ROW LIST INT\n')
    itemcounter = 0
    line = ''
    for item in HERCMATRIX.elements['row']:
        logging.debug("writing item {0} in row".format(str(item)))
        line = line + str(item) + ' '
        itemcounter += 1
        if itemcounter == 9:
            fileObject.write(line + '\n')
            line = ''
            itemcounter = 0
    if itemcounter > 0:
        fileObject.write(line + '\n')
    fileObject.write('ENDFIELD\n')

    logging.info("writing col")
    fileObject.write('COL LIST INT\n')
    itemcounter = 0
    line = ''
    for item in HERCMATRIX.elements['col']:
        logging.debug("writing item {0} in col".format(str(item)))
        line = line + str(item) + ' '
        itemcounter += 1
        if itemcounter == 9:
            fileObject.write(line + '\n')
            line = ''
            itemcounter = 0
    if itemcounter > 0:
        fileObject.write(line + '\n')
    fileObject.write('ENDFIELD\n')

    logging.info("finished writing, closing file")
    fileObject.close()
