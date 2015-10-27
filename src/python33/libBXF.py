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


class bxfio:
    # permits IO on HeRCM files

    def __init__(this):
        logging.debug("instantiated new instance of libBXF.bxfio")

    def read(this, filename):
        # reads in the HeRCM file specified by filename
        # returns it as an instance of libhsm.hsm

        HSM = libHercMatrix.hercMatrix()
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

        if splitHeader[0] != ('HERCM' or 'BXF  '):
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

        HSM.width = width
        HSM.height = height
        HSM.nzentries = nzentries
        HSM.symmetry = symmetry
        HSM.verification = verification

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
            if len(contents[field]) != HSM.nzentries:
                logging.warning("""(lsc-162) length of {0} {1} does not 
match nzentries {2}""".format(field, len(contents[field]), HSM.nzentries))

        for i in range(0, HSM.nzentries):
            try:
                HSM.addElement([contents['row'][i],
                                contents['col'][i],
                                contents['val'][i]])
            except IndexError:
                logging.warning("""(lsc-172) could not add index {0} of contents
 to HSM instance. Nzentries is {1} and len val is {2}"""
                        .format(i, HSM.nzentries,
                                len(contents['val'])), 'warning')

                raise IndexError("Unable to add index {0} to HSM".format(i))

        if this.verify(contents):
            return HSM
        else:
            logging.warning("(lsc-181) verification failed")
            return None

    def generateVerificationSum(this, hercm):
        # returns the verification sum of hercm
        # hercm should be in the format:

        # {'col': [4, 4, 3, 2, 1, 4, 2, 1],
        # 'height': 5,
        # 'nzentries': 8,
        # 'remarks': [],
        # 'row': [4, 3, 3, 4, 1, 1, 2, 4],
        # 'symmetry': 'ASYM',
        # 'val': [8.0, 7.0, 5.0, 3.0, 4.0, 2.0, 1.0, 6.0],
        # 'verification': 7.0,
        # 'width': 5}

        # hercm may also be an instance of libhsm.hsm

        if type(hercm) == dict:
            fields = ['val', 'col', 'row']
            sum = 0
            for field in fields:
                try:
                    for value in hercm[field]:
                        sum += value
                except KeyError as e:
                    logging.warning(
                        "(lsc-208) could not verify, missing field")
                    raise KeyError("missing field... ", str(e))
                except TypeError as e:
                    logging.warning(
                        "(lsc-213) could not verify, mangled field")
                    raise TypeError("one or more fields is of invalid type",
                                    str(e))

            logging.info("generated verification sum {0}"
                    .format(sum % float(len(hercm['val']))))

            return sum % float(len(hercm['val']))
        else:
            val = hercm.elements['val']
            row = hercm.elements['row']
            col = hercm.elements['col']

            return this.generateVerificationSum({'val': val,
                    'row': row,
                    'col': col})

    def verify(this, hercm):
        # verifies the hercm provided
        # hercm should be the same dict format as generateVerificationSum()
        # hercm may also be an instance of libhsm.hsm

        # returns True of the hercm is valid
        # returns False if it is not
        # returns None if an error is encountered

        if type(hercm) == dict:
            try:
                verification = this.generateVerificationSum(hercm)
            except KeyError as e:
                raise KeyError(
                    "failed to generate verification sum... ", str(e))
                return None
            except TypeError as e:
                raise TypeError("failed to generate verification sum... ",
                        str(e))
                return None

            try:
                if verification == hercm['verification']:
                    logging.info("verification passed")
                    return True
                else:
                    logging.warning("""(lsc-257) verification failed, expected
 {0}, got {1}""".format(hercm['verification'], verification))
                    return False
            except ValueError as e:
                logging.warning("(lsc-262) verification failed, mangled field")

                raise ValueError("Could not verify, mangled field...", str(e))
                return None
            except KeyError:
                logging.warning("(lsc-267) could not verify, missing field")

                raise KeyError("could not verify, missing field...", str(e))
                return None
        else:
            try:
                verification = this.generateVerificationSum(hercm)
            except KeyError as e:
                raise KeyError(
                    "failed to generate verification sum... ", str(e))
                return None
            except TypeError as e:
                raise TypeError(
                    "failed to generate verification sum... ", str(e))
                return None

            return hercm.verification == verification

    def write(this, HSM, filename, headerString="BXF  "):
        # HSM should be an instance of libhsm.hsm
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

        if not this.verify(HSM):
            logging.warning("(lsc-303) verification failed")
            raise HercmioValidationError("matrix did not pass validation")

        header = headerString + ' '
        header = header + str(HSM.width) + ' '
        header = header + str(HSM.height) + ' '
        header = header + str(HSM.nzentries) + ' '
        header = header + str(HSM.symmetry) + ' '
        header = header + str(HSM.verification) + '\n'

        logging.info("generated header: {0}".format(header))

        fileObject.write(header)

        logging.info("writing remarks")
        fileObject.write('REMARKS LIST STRING\n')
        itemcounter = 0
        line = ''
        for item in HSM.remarks:
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
        for item in HSM.elements['val']:
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
        for item in HSM.elements['row']:
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
        for item in HSM.elements['col']:
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
