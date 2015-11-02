import masterPlugin

## Wrapper for libHercMatrix.hercMatrix.checkSymmetry()

class checkSymmetry(masterPlugin.masterPlugin):
    def __init__(this):
        super().__init__()
        this.command = "check-symmetry"
        this.aliases = ["checksym"]
        this.commandInfo = {'requiredArguments': None,
            'optionalArguments': None,
            'argumentInfo': None,
            'help': """Checks the symmetry attribute of the matrix, and whether 
                    or not the data in the matrix is actually symmetrical"""}

    def execute(this, arguments, WORKINGMATRIX):
        print("Symmetry attribute is:", WORKINGMATRIX.symmetry)
        print("Matrix is actually symmetric:", WORKINGMATRIX.checkSymmetry())
