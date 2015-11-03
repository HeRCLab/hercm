import masterPlugin
import MatrixUtils

##  Wrapper for MatrixUtils.printWorkingDirectory()


class printWorkingDirectory(masterPlugin.masterPlugin):

    def __init__(this):
        super().__init__()
        this.command = "printWorkingDirectory"
        this.aliases = ["pwd"]
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': 'Prints the current working directory'}

    def execute(this, arguments, WORKINGMATRIX):
        MatrixUtils.printWorkingDirectory()
