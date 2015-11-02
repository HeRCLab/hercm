import masterPlugin

## wrapper for libHercMatrix.hercMatrix.makeRowMajor()

class rowMajor(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "row-major"
        this.aliases = None
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': """Makes the matrix row-major (only affects COO data, not
                    the contents of the matrix)"""}

    def execute(this, arguments, WORKINGMATRIX):
        print("Making the matrix row-major...")
        WORKINGMATRIX.makeRowMajor()
        print("done")

    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False
        return True