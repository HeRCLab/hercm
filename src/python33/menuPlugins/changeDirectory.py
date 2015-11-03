import masterPlugin
import MatrixUtils
import os

## Wrapper for MatrixUtils.changeDirectory()

class changeDirectory(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "changeDirectory"
        this.aliases = ["cd", "chdir"]
        this.commandInfo = {'requiredArguments': [[0, str, 'path']],
            'optionalArguments': None,
            'argumentInfo': ['new working directory'],
            'help': 'Changes the current working directory to path'}

    def execute(this, arguments, WORKINGMATRIX):
        MatrixUtils.changeDirectory(arguments[0])

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        if not os.path.exists(arguments[0]):
            print("ERROR: target directory does not exist")
            return False

        if not os.path.isdir(arguments[0]):
            print("ERROR: target path is not a directory")
            return False

        return True 