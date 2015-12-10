import masterPlugin

## wrapper for libHercMatrix.hercMatrix.checkLUpperTriangle()


class checkUpperTriangle(masterPlugin.masterPlugin):

    def __init__(this):
        super().__init__()
        this.command = "checkUpperTriangle"
        this.aliases = ['check-triu']
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': 'Prints whether or not there are nonzero elements in the ' +
                    'lower triangle'}

    def execute(this, arguments, WORKINGMATRIX):
        print("This matrix contains no elements in the upper triangle: ",
            WORKINGMATRIX.checkUpperTriangle())
