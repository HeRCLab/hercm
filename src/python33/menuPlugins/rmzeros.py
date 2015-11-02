import masterPlugin

## Wrapper for libHercMatrix.hercMatrix.removeZeros()


class rmzeros(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "rmzeros"
        this.aliases = None
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': """Removes zero elements from the matrix (only affects COO
                    data not the contents of the matrix)"""}

    def execute(this, arguments, WORKINGMATRIX):
        print("Removing zeros from matrix...")
        WORKINGMATRIX.removeZeros()
        print("done")


    def validate(this, arguments, WORKINGMATRIX):
        if not super().validate(arguments, WORKINGMATRIX):
            return False

        return True