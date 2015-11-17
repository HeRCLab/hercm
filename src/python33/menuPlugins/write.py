import masterPlugin
import sys
sys.path.append("menuPlugins")
# it is better to use the existing extrapolateFormat method than copy paste it 
import load
import libHercmIO
import os

## write a matrix to a file
#
# Writes the working matrix to a file 

class writer(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "write"
        this.aliases = ["w"]
        this.commandInfo = {'requiredArguments': [[0, str, 'path']],
        'optionalArguments': [[1, str, 'format']],
        'argumentInfo': ['The file to write to', 'The format of said file'],
        'help': """Writes current matrix to specified file, in specified format
        note that the given path should include the desired file extension.
        if format is not given, it will be extrapolated from the filename"""}

    def execute(this, arguments, WORKINGMATRIX):
        filename = arguments[0]
        form = None
        if len(arguments) == 2:
            form = arguments[1]
        else:
            form = load.loader.extrapolateFormat(None, arguments[0])


        if form not in ['bxf', 'hercm', 'mat', 'mtx', 'valcol']:
            print("ERROR: file format {0} not supported".format(form))
    
        libHercmIO.writeMatrix(filename, form, WORKINGMATRIX)

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        if len(arguments) == 1:
            if load.loader.extrapolateFormat(None, arguments[0]) is None:
                print("ERROR: could not extrapolate format from filename")
                return False

        if os.path.exists(arguments[0]):
            print("WARNING: target file already exists, delete it? (y/n)")
            if (input().upper() in ["YES","Y"]):
                os.remove(arguments[0])
                return True
            else:
                return False

        return True