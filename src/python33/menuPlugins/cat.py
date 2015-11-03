import masterPlugin
import MatrixUtils
import os

## wrapper for MatrixUtils.cat()

class cat(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "cat"
        this.aliases = None
        this.commandInfo = {'requiredArguments': [[0, str, 'path']],
            'optionalArguments': None,
            'argumentInfo': ['The file to print all lines from'],
            'help': 'Prints all lines from the file'}

    def execute(this, arguments, WORKINGMATRIX):
        MatrixUtils.cat(arguments[0])

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        if not os.path.exists(arguments[0]):
            print("ERROR: target file does not exist")
            return False

        return True 