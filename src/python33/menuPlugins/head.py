import masterPlugin
import MatrixUtils
import os

## Wrapper fro MatrixUtils.head()

class head(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "head"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, str, 'path']],
            'optionalArguments': [[0, int, 'lines']],
            'argumentInfo': ['the path to the file to get the head of',
                    'the number of lines to print from the file'],
            'help': 'Prints the first lines (10 by default) lines of the file'}

    def execute(this, arguments, WORKINGMATRIX):
        path = arguments[0]
        numlines = 10
        if len(arguments) == 2:
            numlines = arguments[1]

        MatrixUtils.head(path, numlines)


    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        if not os.path.exists(arguments[0]):
            print("ERROR: target file does not exist")
            return False

        return True 