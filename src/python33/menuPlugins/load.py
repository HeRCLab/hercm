import masterPlugin
import os
import libHercmIO

## load command plugin
#
# Based on arguments, loads a matrix from a file into WORKINGMATRIX, then 
# then returns it as a libHercMatrix.hercMatrix instance 

class loader(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "load"
        this.aliases = ["l"]
        this.commandInfo = {'requiredArguments': [[0, str, 'path']],
            'optionalArguments': [[1, str, 'format']],
            'argumentInfo': ['The file to load', 'The format of said file'],
            'help': """Reads in the file for viewing and manipulation. If format
                is not provided, it will be extrapolated from the filename"""}

    def execute(this, arguments):
        filename = arguments[0]
        form = None
        if len(arguments) == 2:
            form = arguments[1]
        else:
            form = this.extrapolateFormat(arguments[0])
    
        HERCMATRIX = libHercmIO.readMatrix(filename, form, True)
        return HERCMATRIX

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        if len(arguments) == 1:
            if this.extrapolateFormat(arguments[0]) is None:
                print("ERROR: could not extrapolate format from filename")
                return False

        if not os.path.exists(arguments[0]):
            print("ERROR: target file does not exist!")
            return False

        if not os.path.isfile(arguments[0]):
            print("ERROR: target is a directory, not a file")
            return False


        return True

    ## attempt to extrapolate format from filename
    # returns the format if it can be extrapolated, or None if it cannot
    def extrapolateFormat(this, filename):
        if filename[-3:] == "bxf":
            return 'bxf'
        if filename[-3:] == 'mat':
            return 'mat'
        if filename[-3:] == 'mtx':
            return 'mtx'
        if filename[-3:] == 'hercm':
            return 'hercm'

        return None
