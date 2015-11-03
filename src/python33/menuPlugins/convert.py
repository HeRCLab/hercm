import masterPlugin
import MatrixUtils
import os

## Wrapper for MatrixUtils.convert()

class convert(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "convert"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, str, 'source'],
            [1, str, 'source format'],
            [2, str, 'destination'],
            [3, str, 'destination format']],
        'optionalArguments': None,
        'argumentInfo': ['The path to the source file',
                    'the file format of the source file',
                    'the path to the destination file',
                    'the format of the destination file'],
        'help': """Reads the source file in the specified format, then writes it
                'back out at the specified destination in the destination 
                format"""}

    def execute(this, arguments, WORKINGMATRIX):
        source = arguments[0] 
        destination = arguments[2]
        sourceFormat = arguments[1]
        destinationFormat = arguments[3]


        MatrixUtils.convert(source, 
            destination, 
            sourceFormat, 
            destinationFormat)

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        if not os.path.exists(arguments[0]):
            print("ERROR: source file does not exist")
            return False

        if not os.path.isfile(arguments[0]):
            print("ERROR: source is not a file")
            return False

        return True