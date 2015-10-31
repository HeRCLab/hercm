import masterPlugin
import MatrixUtils

## Wrapper for MatrixUtils.printRaw()

class raw(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "raw"
        this.aliases = ["coo","coodisplay"]
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': 'display the raw COO format data for the matrix'}

    def execute(this, arguments, WORKINGMATRIX):
        MatrixUtils.printRaw(WORKINGMATRIX)

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True