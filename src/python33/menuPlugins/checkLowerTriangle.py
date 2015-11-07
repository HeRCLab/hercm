import masterPlugin

## wrapper for libHerdMatrix.hercMatrix.checkLowerTriangle()


class checkLowerTriangle(masterPlugin.masterPlugin):

    def __init__(this):
        super().__init__()
        this.command = "checkLowerTriangle"
        this.aliases = ['check-tril']
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': 'Prints whether or not there are nonzero elements in the ' +
                    'lower triangle'}

    def execute(this, arguments, WORKINGMATRIX):
        print("This matrix contains no elements in the lower triangle: ",
            WORKINGMATRIX.checkLowerTriangle())
