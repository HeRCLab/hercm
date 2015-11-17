import libHercMatrix
import scipy
import numpy
import scipy.io
from numpy.lib.recfunctions import append_fields
import traceback
import pprint
import os
import logging


class HercmioValidationError(Exception):
    pass


def read(filename):
    # reads in the HeRCM file specified by filename
    # returns it as an instance of libhsm.hsm

    HERCMATRIX = libHercMatrix.hercMatrix()
    contents = {}

    logging.info("Reading BXF file {0}".format(filename))

    try:
        fileObject = open(filename, 'r')
    except FileNotFoundError:
        logging.warning("(lsc-33) could not open file: file not found")
        raise FileNotFoundError("could not open file: {0} no such file"
                                .format(filename))
    except PermissionError:
        logging.warning("(lsc-37) could not open file: permissions error")
        raise PermissionError("could not open file: {0}, permission denied"
                              .format(filename))

    lines = fileObject.readlines()
    fileObject.close()

    # read in the header
    header = lines[0]
    lines.pop(0)
    splitHeader = header.split()

    if len(splitHeader) != 6:
        logging.warning("(lsc-50) invalid header: too few fields \n{0}"
            .format(header))
        raise HercmioValidationError("header contains too few fields")

    if (splitHeader[0] != 'HERCM') and (splitHeader[0] != 'BXF'):
        logging.warning("(lsc-55)could not read file, not a HeRCM file " +
                "or mangled header")
        raise HercmioValidationError("header does not contain HeRCM")
    try:
        width = int(splitHeader[1])
        height = int(splitHeader[2])
        nzentries = int(splitHeader[3])
        verification = float(splitHeader[5])
    except ValueError:
        logging.warning("(lsc-64) could not read file: mangled header")
        raise HercmioValidationError(
            "Could not extract values from header")

    symmetry = splitHeader[4]
    if symmetry not in ['SYM', 'ASYM']:
        raise HercmioValidationError("header contains invalid symmetry")

    logging.info("read header...")
    logging.info("width: {0}\nheight: {1}\nnzentries:{2}\nverification:{3}"
            .format(width, height, nzentries, verification))

    HERCMATRIX.width = width
    HERCMATRIX.height = height
    HERCMATRIX.nzentries = nzentries
    HERCMATRIX.symmetry = symmetry
    HERCMATRIX.verification = verification

    contents['width'] = width
    contents['height'] = height
    contents['nzentries'] = nzentries
    contents['symmetry'] = symmetry
    contents['verification'] = verification
    contents['val'] = []
    contents['col'] = []
    contents['row'] = []

    inField = False
    currentHeader = ''
    fieldname = ''
    ctype = ''
    vtype = ''
    currentContents = []
    for line in lines:
        if not inField:
            currentHeader = line.rstrip()
            splitHeader = currentHeader.split()
            fieldname = splitHeader[0]
            ctype = splitHeader[1]
            vtype = splitHeader[2]
            inField = True
        elif 'ENDFIELD' in line:
            inField = False
            contents[fieldname.lower()] = currentContents
            currentContents = []
            inField = False
        else:
            if ctype == 'SINGLE':
                if vtype == 'INT':
                    try:
                        currentContents = int(line)
                    except ValueError:
                        logging.warning("(lsc-117) could not read file, " +
                                "bad vtype")
                        return None
                elif vtype == 'FLOAT':
                    try:
                        currentContents = float(line)
                    except ValueError:
                        logging.warning("(lsc-124) could not read file, " +
                                " bad vtype")
                        return None
                else:
                    currentContents = line.rstrip()
            elif ctype == 'LIST':
                for value in line.split():

                    if vtype == 'INT':
                        try:
                            currentContents.append(int(value))
                        except ValueError:
                            logging.warning("(lsc-138) could not read " +
                                    "file, bad vtype")
                            return None
                    elif vtype == 'FLOAT':
                        try:
                            currentContents.append(float(value))
                        except ValueError:
                            logging.warning("(lsc-145) could not read " +
                                    str(value) + " bad vtype")
                            return None
                    else:
                        currentContents.append(value)
            else:
                logging.warning("(lsc-151) could not read file, bad ctype")
                return None

    for field in ['val', 'col', 'row', 'nzentries', 'width', 'height',
                  'symmetry', 'verification']:
        if field not in contents:
            logging.warning("""(lsc-157) read file, but needed field 
{0} missing""".format(field))
            raise HercmioValidationError("field {0} is missing from file"
                                         .format(field))

    for field in ['row', 'val', 'col']:
        if len(contents[field]) != HERCMATRIX.nzentries:
            logging.warning("""(lsc-162) length of {0} {1} does not 
match nzentries {2}""".format(field, len(contents[field]), HERCMATRIX.nzentries))

    for i in range(0, HERCMATRIX.nzentries):
        try:
            HERCMATRIX.addElement([contents['row'][i],
                            contents['col'][i],
                            contents['val'][i]])
        except IndexError:
            logging.warning("""(lsc-172) could not add index {0} of contents
 to HERCMATRIX instance. Nzentries is {1} and len val is {2}"""
                    .format(i, HERCMATRIX.nzentries,
                            len(contents['val'])), 'warning')

            raise IndexError("Unable to add index {0} to HERCMATRIX".format(i))

    if verify(contents):
        return HERCMATRIX
    else:
        logging.warning("(lsc-181) verification failed")
        return None


def generateVerificationSum(hercm):
    return 1


def verify(hercm):
    logging.warning("libBXF.verify is being updated, and dosen't actually do " + 
        "anything right now")
    return True 


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
        logging.warning("matrix validation failed. "+
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
